import os
from dataclasses import dataclass
from itertools import accumulate
from typing import Dict, Iterator, Self


@dataclass
class DistinctWindow:
    distinct_chars: Dict[str, int]
    min_index: int
    max_index: int

    @classmethod
    def init_from_iter(cls, it: Iterator[str]) -> Self:
        first_char = next(it)
        assert len(first_char) == 1
        return cls({first_char: 0}, 0, 0)

    @property
    def window_length(self) -> int:
        return (self.max_index - self.min_index) + 1


def update_window(cur: DistinctWindow, next_char: str) -> DistinctWindow:
    assert len(next_char) == 1
    repeat_index = cur.distinct_chars.get(next_char, -1)
    new_distinct_chars = {
        c: i for c, i in cur.distinct_chars.items() if i > repeat_index
    }

    this_index = cur.max_index + 1
    new_distinct_chars[next_char] = this_index
    new_min_index = repeat_index + 1 if repeat_index != -1 else cur.min_index

    return DistinctWindow(new_distinct_chars, new_min_index, this_index)


def find_first_index_after_distinct_char_marker(
    stream: Iterator[str], marker_length: int
) -> int:
    windows = accumulate(
        stream, update_window, initial=DistinctWindow.init_from_iter(stream)
    )
    return (
        next(filter(lambda x: x.window_length >= marker_length, windows)).max_index + 1
    )


with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
    text = f.read()


# part 1
print(find_first_index_after_distinct_char_marker(iter(text), 4))

# part 2
print(find_first_index_after_distinct_char_marker(iter(text), 14))
