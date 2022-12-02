import enum
import os
from typing import Tuple


class Choice(enum.Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(enum.Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


def play(they_played: Choice, you_played: Choice) -> Result:
    match they_played:
        case Choice.ROCK:
            match you_played:
                case Choice.ROCK:
                    return Result.DRAW
                case Choice.PAPER:
                    return Result.WIN
                case Choice.SCISSORS:
                    return Result.LOSE
        case Choice.PAPER:
            match you_played:
                case Choice.ROCK:
                    return Result.LOSE
                case Choice.PAPER:
                    return Result.DRAW
                case Choice.SCISSORS:
                    return Result.WIN
        case Choice.SCISSORS:
            match you_played:
                case Choice.ROCK:
                    return Result.WIN
                case Choice.PAPER:
                    return Result.LOSE
                case Choice.SCISSORS:
                    return Result.DRAW


def calculate_your_score(they_played: Choice, you_played: Choice) -> int:
    return you_played.value + play(they_played, you_played).value


def parse_line_1(line: str) -> Tuple[Choice, Choice]:
    they_played_mapping = {
        "A": Choice.ROCK,
        "B": Choice.PAPER,
        "C": Choice.SCISSORS,
    }

    you_played_mapping = {
        "X": Choice.ROCK,
        "Y": Choice.PAPER,
        "Z": Choice.SCISSORS,
    }

    split_line = line.split()
    assert len(split_line) == 2

    they_played_str, you_played_str = split_line
    return they_played_mapping[they_played_str], you_played_mapping[you_played_str]


def parse_line_2(line: str) -> Tuple[Choice, Choice]:
    they_played_mapping = {"A": Choice.ROCK, "B": Choice.PAPER, "C": Choice.SCISSORS}

    split_line = line.split()
    assert len(split_line) == 2

    they_played_str, you_played_str = split_line

    they_played = they_played_mapping[they_played_str]

    match you_played_str:
        case "X":
            match they_played:
                case Choice.ROCK:
                    you_played = Choice.SCISSORS
                case Choice.PAPER:
                    you_played = Choice.ROCK
                case Choice.SCISSORS:
                    you_played = Choice.PAPER
        case "Y":
            you_played = they_played
        case "Z":
            match they_played:
                case Choice.ROCK:
                    you_played = Choice.PAPER
                case Choice.PAPER:
                    you_played = Choice.SCISSORS
                case Choice.SCISSORS:
                    you_played = Choice.ROCK

    return they_played, you_played


with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
    text = f.read()

lines = text.split("\n")

# part 1
rounds = map(parse_line_1, lines)
part1_result = sum(map(lambda x: calculate_your_score(*x), rounds))
print(part1_result)

# part 2
rounds = map(parse_line_2, lines)
part2_result = sum(map(lambda x: calculate_your_score(*x), rounds))
print(part2_result)
