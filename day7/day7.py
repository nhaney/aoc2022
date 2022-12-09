import os
import enum
from dataclasses import dataclass
from itertools import chain
from typing import Iterator, Iterable, List, Self


@dataclass
class DirectoryNode:
    name: str
    total_size: int
    children: List[Self]

    def get_all_dirs_under_node(self) -> Iterable[Self]:
        yield from chain(*[child.get_all_dirs_under_node() for child in self.children])
        yield self
    
    def get_all_dirs_under_node_with_size_less_than(self, size_limit: int) -> Iterable[Self]:
        return [node for node in self.get_all_dirs_under_node() if node.total_size <= size_limit]
    
    def find_smallest_directory_larger_than(self, min_size: int) -> Self:
        return min([node for node in self.get_all_dirs_under_node() if node.total_size >= min_size], key=lambda x: x.total_size)


def parse_command_output(cmd_lines: List[str]) -> DirectoryNode:
    """parses the command output and returns the root directory node in the file system."""
    class LineType(enum.Enum):
        """The three type of lines we expect to see in the output."""
        CD = 1
        CD_UP = 2
        LS = 3
        LS_OUTPUT_DIR = 4
        LS_OUTPUT_FILE = 5

        @classmethod
        def parse_from_line(cls, line: str) -> Self:
            line_parts = line.split()

            if line.startswith("$"):
                assert len(line_parts) >= 2
                cmd = line_parts[1]

                assert cmd in ("cd", "ls")

                if cmd == "cd":
                    return LineType.CD if ".." not in line else LineType.CD_UP
                
                return LineType.LS
            else:
                # we are parsing LS output
                assert len(line_parts) == 2
                output_start, _ = line.split()

                if output_start == "dir":
                    return LineType.LS_OUTPUT_DIR
                elif output_start.isdigit():
                    return LineType.LS_OUTPUT_FILE
                
                raise ValueError(f"could not parse LS output {line=}")

    def create_dir_helper(name: str, line_iter: Iterator[str]) -> DirectoryNode:
        """Called after a LineType.CD is encountered with a directory name."""
        assert LineType.parse_from_line(next(line_iter)) == LineType.LS, "Expect an ls after entering a directory"

        child_dirs = []
        expected_dirs = []
        total_size = 0

        for line in line_iter:
            line_type = LineType.parse_from_line(line)

            match line_type:
                case LineType.LS_OUTPUT_DIR:
                    _, dir_name = line.split()
                    expected_dirs.append(dir_name)
                case LineType.LS_OUTPUT_FILE:
                    size, _ = line.split()
                    total_size += int(size)
                case LineType.CD:
                    _, _, cd_target = line.split()
                    child_dir = create_dir_helper(cd_target, line_iter)
                    total_size += child_dir.total_size
                    child_dirs.append(child_dir)
                case LineType.CD_UP:
                    break
                case _:
                    raise ValueError(f"Encountered unexpected line type while trying to create directory {name}. {line=}")

        # make sure that we visited all expected directories
        assert all([child_dir.name in expected_dirs for child_dir in child_dirs]), "Did not visit all expected dirs."
        return DirectoryNode(name, total_size, child_dirs)
    
    lines_iter = iter(cmd_lines)
    first_line = next(lines_iter)
    _, _, cd_target = first_line.split()

    assert LineType.parse_from_line(first_line) == LineType.CD and cd_target == "/", "command lines should start with a cd command on root (/)"
    return create_dir_helper(cd_target, lines_iter)


with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
    text = f.read()

lines = text.split("\n")

root_directory_node = parse_command_output(lines)

# part1
nodes_with_size_less_than_max = root_directory_node.get_all_dirs_under_node_with_size_less_than(100000)
result1 = sum([node.total_size for node in nodes_with_size_less_than_max])
print(result1)

# part2
total_space = 70000000
required_space = 30000000
unused_space = total_space - root_directory_node.total_size
space_still_needed = required_space - unused_space

assert space_still_needed >= 0

min_node_to_delete = root_directory_node.find_smallest_directory_larger_than(space_still_needed)
result2 = min_node_to_delete.total_size
print(result2)
