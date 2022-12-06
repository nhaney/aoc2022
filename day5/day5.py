import os
import re
from dataclasses import dataclass
from functools import partial, reduce
from typing import List, Optional, Self


@dataclass
class MoveCommand:
    amount: int
    from_stack: int
    to_stack: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        m = re.match(r"move (\d+) from (\d+) to (\d+)", s)

        assert m is not None

        return cls(
            amount=int(m.group(1)),
            from_stack=int(m.group(2)),
            to_stack=int(m.group(3)),
        )


def parse_stacks_initial_state(stacks_lines: List[str]) -> List[List[str]]:
    """Parses lines that represent the various stacks in their initial state."""

    def _parse_crate_str(crate_str: str) -> Optional[str]:
        """parses a crate of the from '[Q] ' to 'Q'"""
        n = len(crate_str.strip())
        if not n:
            # this means there was nothing on the stack
            return None

        assert len(crate_str.strip()) == 3
        return crate_str.strip()[1]

    def _parse_crate_stack_line(line: str) -> List[Optional[str]]:
        # how many characters each "crate" in the line takes up in the input file
        crate_width = 4
        return [
            _parse_crate_str(line[i : i + crate_width])
            for i in range(0, len(line), crate_width)
        ]

    def _add_layer_to_state(
        stack_state: List[List[str]], layer: List[Optional[str]]
    ) -> List[List[str]]:
        return [
            stack_state[i] + ([crate] if crate is not None else [])
            for i, crate in enumerate(layer)
        ]

    layers = [_parse_crate_stack_line(line) for line in reversed(stacks_lines)]
    empty_stack_state = [[] for _ in range(len(layers[0]))]

    return reduce(_add_layer_to_state, layers, empty_stack_state)


def apply_move_to_stacks(
    stacks: List[List[str]], command: MoveCommand, is_9001: bool = False
) -> List[List[str]]:
    """Returns a new version of the `stacks` based on the move command passed in."""
    from_i, to_i = command.from_stack - 1, command.to_stack - 1
    start_stack, end_stack = stacks[from_i][:], stacks[to_i][:]

    assert (
        len(start_stack) >= command.amount
    ), f"Can not pop {command.amount} from {start_stack}.\n{command}\n{stacks=}"

    start_stack, to_add = (
        start_stack[: len(start_stack) - command.amount],
        start_stack[len(start_stack) - command.amount :],
    )

    if not is_9001:
        to_add = to_add[::-1]

    end_stack += to_add

    result = [
        start_stack if i == from_i else end_stack if i == to_i else stack
        for i, stack in enumerate(stacks)
    ]

    return result


with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
    text = f.read()

lines = text.split("\n")

init_lines = [line for line in lines if line.startswith("[")]
initial_stacks_state = parse_stacks_initial_state(init_lines)

move_lines = [line for line in lines if line.startswith("move")]
move_commands = [MoveCommand.from_str(line) for line in move_lines]

# part 1
final_stacks_state = reduce(apply_move_to_stacks, move_commands, initial_stacks_state)
result1 = "".join([stack[-1] for stack in final_stacks_state])
print(result1)

# part 2
apply_move_with_9001 = partial(apply_move_to_stacks, is_9001=True)
final_stacks_state = reduce(apply_move_with_9001, move_commands, initial_stacks_state)
result2 = "".join([stack[-1] for stack in final_stacks_state])
print(result2)
