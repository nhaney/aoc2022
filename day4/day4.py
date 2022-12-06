import os
from dataclasses import dataclass
from typing import Tuple


@dataclass
class ElfAssignment:
    start: int
    end: int

    @classmethod
    def from_str(cls, s: str) -> "ElfAssignment":
        """Parses a string in the following format: 2-4"""
        start_end_strs = s.split("-")

        assert len(start_end_strs) == 2
        start_str, end_str = start_end_strs

        assert start_str.isdigit() and end_str.isdigit()
        start, end = int(start_str), int(end_str)
        assert start <= end

        return cls(start, end)

    def contains(self, other: "ElfAssignment") -> bool:
        """Returns true if this assignment contains the assignment passed in."""
        return other.start >= self.start and other.end <= self.end

    def overlaps(self, other: "ElfAssignment") -> bool:
        """Returns true if this assignment overlaps with the other passed in."""
        return self.start <= other.end and other.start <= self.end


def parse_assignment(line: str) -> Tuple[ElfAssignment, ElfAssignment]:
    assignment_strs = line.split(",")
    assert len(assignment_strs) == 2
    return ElfAssignment.from_str(assignment_strs[0]), ElfAssignment.from_str(
        assignment_strs[1]
    )


with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
    text = f.read()

lines = text.split("\n")

# part 1
assignments = [parse_assignment(line) for line in lines]
pairs_with_containment = [a1.contains(a2) or a2.contains(a1) for a1, a2 in assignments]
result1 = sum(pairs_with_containment)
print(result1)

# part 2
pairs_that_overlap = [a1.overlaps(a2) for a1, a2 in assignments]
result2 = sum(pairs_that_overlap)
print(result2)
