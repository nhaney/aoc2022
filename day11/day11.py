import enum
import os
from dataclasses import dataclass
from functools import reduce
from itertools import accumulate
from typing import List, Tuple, Self


class OperationType(enum.Enum):
    ADDITION = 1
    MULTIPLICATION = 2


@dataclass
class Monkey:
    id: int
    inventory: List[int]
    operation: OperationType
    operand: str
    test_divisor: int
    throw_if_true: int
    throw_if_false: int


@dataclass
class Monkey:
    id: int
    inventory: List[int]
    operation: OperationType
    operand: str
    test_divisor: int
    throw_if_divisible: int
    throw_if_not_divisible: int

    def clear_inventory(self) -> Self:
        """returns a copy of this monkey with no inventory"""
        return Monkey(
            self.id,
            [],
            self.operation,
            self.operand,
            self.test_divisor,
            self.throw_if_divisible,
            self.throw_if_not_divisible
        )


@dataclass
class Throw:
    to: int
    amount: int


def parse_monkey(monkey_lines: List[str]) -> Monkey:
    monkey_id = int(monkey_lines[0][monkey_lines[0].index(":") - 1])
    starting_items = list(map(int, monkey_lines[1].strip().split(": ")[1].split(", ")))
    operation_type = OperationType.ADDITION if "+" in monkey_lines[2] else OperationType.MULTIPLICATION
    operand = monkey_lines[2].split()[-1]
    test_divisor = int(monkey_lines[3].split()[-1])
    throw_if_true = int(monkey_lines[4].split()[-1])
    throw_if_false = int(monkey_lines[5].split()[-1])
    return Monkey(monkey_id, starting_items, operation_type, operand, test_divisor, throw_if_true, throw_if_false)


def apply_worry_operation(item: int, monkey: Monkey) -> int:
    operand = item if monkey.operand == "old" else int(monkey.operand)

    match monkey.operation:
        case OperationType.ADDITION:
            return item + operand
        case OperationType.MULTIPLICATION:
            return item * operand
        case _: 
            raise ValueError(f"Invalid operation type {monkey.operation}")


def process_item(item: int, monkey: Monkey) -> Throw:
    worry_level_after_inspection = apply_worry_operation(item, monkey)
    worry_level_before_throw = worry_level_after_inspection // 3

    if worry_level_before_throw % monkey.test_divisor == 0:
        return Throw(monkey.throw_if_divisible, worry_level_before_throw)
    else:
        return Throw(monkey.throw_if_not_divisible, worry_level_before_throw)


def process_monkey(current_throws: List[Throw], monkey: Monkey) -> List[Throw]:
    breakpoint()
    throws_to_this_monkey = [throw for throw in current_throws if throw.to == monkey.id]
    throws_to_other_monkeys = [throw for throw in current_throws if throw.to != monkey.id]
    throws = throws_to_other_monkeys + [process_item(item, monkey) for item in monkey.inventory + [throw.amount for throw in throws_to_this_monkey]]
    return throws


def process_round(monkeys: List[Monkey]) -> List[Monkey]:
    breakpoint()
    monkey_throws_left = reduce(process_monkey, monkeys, [])
    breakpoint()
    

with open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as f:
    text = f.read()

monkey_sections = text.split("\n\n")
monkeys = [parse_monkey(monkey_lines.split("\n")) for monkey_lines in monkey_sections]

process_round(monkeys)

