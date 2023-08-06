# Copyright © 2019 Ben Simms and Ben Mintz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import importlib.util
import collections
import sys
from typing import Any, Collection, List, Tuple

from cffi import FFI

ffi = FFI()
ffi.cdef("""
struct Searcher {
    char private[0];
};

struct SearchElement {
  const char *key;
  const void *val;
};

struct ExtendedResultElement {
  const void *value;
  size_t start, end;
};

struct SearchResult {
    void *const *const values;
    size_t length;
};

struct ExtendedSearchResult {
  struct ExtendedResultElement *const values;
  size_t length;
};

struct Searcher *new_searcher(struct SearchElement *search_strings, size_t num_strings);
struct SearchResult search_searcher(const struct Searcher *searcher, const char* haystack);
struct ExtendedSearchResult search_searcher_extended(const struct Searcher *searcher, const char* haystack);
size_t searcher_size(const struct Searcher *searcher);
void deallocate_result(struct SearchResult result);
void deallocate_extended_result(struct ExtendedSearchResult result);
void deallocate_searcher(struct Searcher *result);
""")

C = ffi.dlopen(importlib.util.find_spec("_lacbd").loader.get_filename())

MatchResult = collections.namedtuple('MatchResult', 'value start end')

class Searcher:
    def __init__(self, elements: Collection[Tuple[str, Any]]):
        # keys down't have to stay alive since the searcher makes a copy of them
        keys = [ffi.new("char[]", k.lower().encode("utf8")) for k, _ in elements]

        # make sure values are kept alive
        self.__values = [ffi.new_handle(v) for _, v in elements]

        elements = ffi.new("struct SearchElement[]", len(elements))

        for idx, (key, val) in enumerate(zip(keys, self.__values)):
            elements[idx].key = key
            elements[idx].val = val

        self.__searcher = ffi.gc(
            C.new_searcher(elements, len(elements)), C.deallocate_searcher
        )

    def search(self, haystack: str) -> List[str]:
        haystack = ffi.new("char[]", haystack.lower().encode("utf8"))
        results = ffi.gc(
            C.search_searcher(self.__searcher, haystack), C.deallocate_result
        )
        return [ffi.from_handle(results.values[i]) for i in range(results.length)]

    def search_extended(self, haystack: str) -> List[Tuple[str, int, int]]:
        haystack = ffi.new("char[]", haystack.lower().encode("utf8"))
        results = ffi.gc(
            C.search_searcher_extended(self.__searcher, haystack),
            C.deallocate_extended_result,
        )

        def extract(v):
            return MatchResult(ffi.from_handle(v.value), v.start, v.end)

        return [extract(results.values[i]) for i in range(results.length)]

    def __sizeof__(self):
        return (
            super().__sizeof__()
            + C.searcher_size(self.__searcher)
            + sum(
                sys.getsizeof(i) + sys.getsizeof(ffi.from_handle(i))
                for i in self.__values
            )
        )

    def __len__(self):
        return len(self.__values)

    def __class_getitem__(cls, item):
        return f"{cls.__name__}[{item!r}]"
