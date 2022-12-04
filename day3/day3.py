import os
from functools import reduce


def find_common_character(*strs) -> str:
    sets = map(set, strs)
    common_chars = reduce(lambda x, y: x & y, sets)

    assert len(common_chars) == 1
    return list(common_chars)[0]


def find_common_character_in_both_halves(line: str) -> str:
    assert len(line) % 2 == 0

    half_length = len(line) // 2
    return find_common_character(line[:half_length], line[half_length:])


def find_character_priority(c: str) -> int:
    assert len(c) == 1

    is_upper = c.isupper()

    value = ord(c) - ord("A" if is_upper else "a") + 1

    if is_upper:
        value += 26

    return value

def chunker(iterable, chunk_size):
    n = len(iterable)
    return [iterable[i:i + group_size] for i in range(0, n, chunk_size)]


with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
    text = f.read()

lines = text.split("\n")

# part 1
common_characters = map(find_common_character_in_both_halves, lines)
priorities = map(find_character_priority, common_characters)
result1 = sum(priorities)
print(result1)

# part 2
group_size = 3
assert len(lines) % group_size == 0
n = len(lines)
groups = chunker(lines, group_size)
common_characters = [find_common_character(*group) for group in groups]
result2 = sum(map(find_character_priority, common_characters))
print(result2)
