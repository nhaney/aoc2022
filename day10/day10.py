import enum
import os
from dataclasses import dataclass
from functools import reduce
from typing import List, Self, Optional


class InstructionType(enum.Enum):
    NOOP = 0
    ADDX = 1


@dataclass
class Instruction:
    i_type: InstructionType
    data: int
    cycles_to_complete: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        parts = s.split()

        if len(parts) == 1:
            instruction = parts[0]
            assert instruction == "noop"
            return Instruction(InstructionType.NOOP, 0, 1)

        assert len(parts) == 2
        instruction, data = parts

        assert instruction == "addx"
        return Instruction(InstructionType.ADDX, int(data), 2)


@dataclass
class CpuState:
    """Represents the state of the CPU."""

    x_reg: int


@dataclass
class CpuCycleState:
    cycle: int
    instruction_processed: Optional[Instruction]
    state_during: CpuState
    state_after: CpuState


def apply_instruction_to_states(
    cycle_states: List[CpuCycleState], instruction: Instruction
) -> List[CpuCycleState]:
    last_state = cycle_states[-1]

    cur_cycle = last_state.cycle + 1
    cur_x_reg = last_state.state_after.x_reg

    match instruction.i_type:
        case InstructionType.NOOP:
            # progress cycle counter by 1
            new_states = [
                CpuCycleState(
                    cur_cycle, instruction, CpuState(cur_x_reg), CpuState(cur_x_reg)
                )
            ]
        case InstructionType.ADDX:
            new_states = [
                # cycle where this begins execution, value stays the same during the cycle
                CpuCycleState(
                    cur_cycle, instruction, CpuState(cur_x_reg), CpuState(cur_x_reg)
                ),
                # cycle where this is applied, during the cycle it is still the old value.
                CpuCycleState(
                    cur_cycle + 1,
                    None,
                    CpuState(cur_x_reg),
                    CpuState(cur_x_reg + instruction.data),
                ),
            ]

    return cycle_states + new_states


with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
    text = f.read()

lines = text.split("\n")
instructions = [Instruction.from_str(line) for line in lines]
initial_cpu_states = [CpuCycleState(0, None, CpuState(1), CpuState(1))]

cycle_history = reduce(apply_instruction_to_states, instructions, initial_cpu_states)

# part 1
signal_strength_cycles = {20, 60, 100, 140, 180, 220}

signal_strengths = [
    cycle_state.cycle * cycle_state.state_during.x_reg
    for cycle_state in cycle_history
    if cycle_state.cycle in signal_strength_cycles
]

result1 = sum(signal_strengths)
print(result1)

# part 2
def get_pixel_state_during_each_cycle(cycle_history: List[CpuCycleState]) -> List[bool]:
    """Returns a list of pixel states during each cycle. True means lit, False means unlit."""

    def _should_light_during_cycle(cycle_state: CpuCycleState):
        draw_pos = (cycle_state.cycle - 1) % 40
        x_reg = cycle_state.state_during.x_reg
        return draw_pos == x_reg - 1 or draw_pos == x_reg or draw_pos == x_reg + 1

    return [_should_light_during_cycle(cycle_state) for cycle_state in cycle_history]


def chunker(iterable, chunk_size):
    n = len(iterable)
    return [iterable[i : i + chunk_size] for i in range(0, n, chunk_size)]


pixel_states_for_each_cycle = get_pixel_state_during_each_cycle(cycle_history[1:])
output_chars = [
    "#" if pixel_is_lit else "." for pixel_is_lit in pixel_states_for_each_cycle
]
output_chars = "".join(output_chars)
output_lines = chunker(output_chars, 40)
result2 = "\n".join(output_lines)
print(result2)
