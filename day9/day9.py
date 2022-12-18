import enum
import os
from dataclasses import dataclass
from functools import reduce
from itertools import accumulate
from typing import List, Tuple, Self


class Direction(enum.Enum):
    U = 1
    D = 2
    L = 3
    R = 4


@dataclass
class MoveCommand:
    dir: Direction
    steps: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        dir_s, steps_s = s.split()
        return MoveCommand(Direction[dir_s], int(steps_s))


@dataclass
class RopePosition:
    knot_positions: List[Tuple[int, int]]


def move_head_in_direction(head_pos: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
    """Given a move command, moves the head rope position."""
    cur_x, cur_y = head_pos

    match direction:
        case Direction.U:
            return cur_x, cur_y + 1
        case Direction.D:
            return cur_x, cur_y - 1
        case Direction.R:
            return cur_x + 1, cur_y
        case Direction.L:
            return cur_x - 1, cur_y
        case _:
            raise ValueError("Invalid direction")


def move_knot_behind_other(pos_to_follow: Tuple[int, int], cur_pos: Tuple[int, int]) -> Tuple[int, int]:
    """Given the new position of the head of the rope, moves the tail so that it "follows" it."""
    tail_x, tail_y = cur_pos
    head_x, head_y = pos_to_follow
    dx, dy = head_x - tail_x, head_y - tail_y

    def _are_positions_touching(x1, y1, x2, y2) -> bool:
        """Returns true if the positions are overlapping or only one space apart."""
        # overlapping
        if x1 == x2 and y1 == y2:
            return True
        
        # one space to the left or right
        if abs(x1 - x2) == 1 and y1 == y2:
            return True

        # one space up or down
        if x1 == x2 and abs(y1 - y2) == 1:
            return True
        
        # diagonally touching
        if abs(x1 - x2) == 1 and abs(y1 - y2) == 1:
            return True
        
        return False
 
    # if the positions are touching, no movement necessary
    if _are_positions_touching(tail_x, tail_y, head_x, head_y):
        return tail_x, tail_y 
    
    # if we are doing a non-diagonal move, move one space either up or down
    if dx == 0 or dy == 0:
        if dx:
            assert abs(dx) == 2
            return tail_x + (dx // abs(dx)), tail_y
        else:
            assert abs(dy) == 2
            return tail_x, tail_y + (dy // abs(dy))
        
    # if we are moving diagonally, we have to move diagonally one place the direction of the head
    return tail_x + (dx // abs(dx)), tail_y + (dy // abs(dy))


def simulate_one_step_in_direction(rope_pos: RopePosition, dir: Direction) -> RopePosition:
    new_head_pos = move_head_in_direction(rope_pos.knot_positions[0], dir)
    positions = list(accumulate(rope_pos.knot_positions[1:], move_knot_behind_other, initial=new_head_pos))
    return RopePosition(positions)


def simulate_rope_movement(movement_history: List[RopePosition], command: MoveCommand) -> List[RopePosition]:
    """Applies a movement command to the rope and returns all of the positions of the ropes given the movements."""
    last_pos = movement_history[-1]
    new_movements = list(accumulate([command.dir] * command.steps, simulate_one_step_in_direction, initial=last_pos))
    return movement_history[:-1] + new_movements


def parse_move_commands(lines: List[str]) -> List[MoveCommand]:
    return [MoveCommand.from_str(line) for line in lines]


with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
    text = f.read()

lines = text.split("\n")
move_commands = parse_move_commands(lines)

# part 1
positions = reduce(simulate_rope_movement, move_commands, [RopePosition([(0, 0), (0, 0)])])

unique_tail_positions = set([position.knot_positions[-1] for position in positions])
result1 = len(unique_tail_positions)
print(result1)

# part 2
positions = reduce(simulate_rope_movement, move_commands, [RopePosition([(0, 0) for _ in range(10)])])

unique_tail_positions = set([position.knot_positions[-1] for position in positions])
result2 = len(unique_tail_positions)
print(result2)