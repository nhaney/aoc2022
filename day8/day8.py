import os
import sys
from dataclasses import dataclass
from functools import partial, reduce
from itertools import product
from typing import List, Set, Tuple

"""
We need to count all trees on the outside edges.

We need to find the max height tree in each row and column. A tree that is visible is defined as
it is taller than all previous trees in the current row/column.

We can just have a function that calculates which trees are visible for the following rows/columns:

* all rows
* all rows reversed
* all columns
* all columns reversed

Once we have this, we just need to make sure that we don't count the same tree twice when it is visible
from multiple locations. To do this, we can pass in a "secondary index" that represents either the x
axis when scanning a row or the y axis when scanning a column. The function that counts trees will
return a set of coordinates that can then be merged with the currently selected set of coordinates.
"""


def tree_counter(grid: List[List[int]]) -> int:
    @dataclass(frozen=True)
    class _TreeScanResult:
        visible_trees: List[bool]
        max_tree: int

        @classmethod
        def default(cls, size: int):
            return _TreeScanResult([False] * size, -sys.maxsize)

    def _scan_trees(cur_result: _TreeScanResult, i: int, val: int) -> _TreeScanResult:
        visible_trees = cur_result.visible_trees[:]

        is_new_max = val > cur_result.max_tree

        if is_new_max:
            visible_trees[i] = True

        return _TreeScanResult(
            visible_trees, val if is_new_max else cur_result.max_tree
        )

    def _get_visible_trees_in_row(
        i: int, row: List[int], reversed: bool
    ) -> Set[Tuple[int, int]]:
        n = len(row)
        trees_in_order = row if not reversed else row[::-1]
        scan_result = reduce(
            lambda accum, index_and_val: _scan_trees(
                accum, index_and_val[0], index_and_val[1]
            ),
            enumerate(trees_in_order),
            _TreeScanResult.default(n),
        )

        return set(
            (
                (i, k if not reversed else (n - 1) - k)
                for k, is_visible in enumerate(scan_result.visible_trees)
                if is_visible
            )
        )

    def _get_visible_trees_in_col(
        j: int, col: List[int], reversed: bool
    ) -> Set[Tuple[int, int]]:
        n = len(col)
        trees_in_order = col if not reversed else col[::-1]
        scan_result = reduce(
            lambda accum, index_and_val: _scan_trees(
                accum, index_and_val[0], index_and_val[1]
            ),
            enumerate(trees_in_order),
            _TreeScanResult.default(n),
        )

        return set(
            (
                (k if not reversed else (n - 1) - k, j)
                for k, is_visible in enumerate(scan_result.visible_trees)
                if is_visible
            )
        )

    trees_visible_from_left = reduce(
        lambda accum, i_and_row: accum
        | _get_visible_trees_in_row(i_and_row[0], i_and_row[1], reversed=False),
        enumerate(grid),
        set(),
    )

    trees_visible_from_right = reduce(
        lambda accum, i_and_row: accum
        | _get_visible_trees_in_row(i_and_row[0], i_and_row[1], reversed=True),
        enumerate(grid),
        set(),
    )

    trees_visible_from_top = reduce(
        lambda accum, j_and_col: accum
        | _get_visible_trees_in_col(j_and_col[0], j_and_col[1], reversed=False),
        enumerate(zip(*grid)),
        set(),
    )

    trees_visible_from_bottom = reduce(
        lambda accum, j_and_col: accum
        | _get_visible_trees_in_col(j_and_col[0], j_and_col[1], reversed=True),
        enumerate(zip(*grid)),
        set(),
    )

    return len(
        trees_visible_from_left
        | trees_visible_from_right
        | trees_visible_from_top
        | trees_visible_from_bottom
    )


def distance_to_gte_or_end(
    iter, val: int, have_encountered_larger_value: bool = False
) -> int:
    """
    Calculates how many iterations occur before the end of the iterator or until a greater than or equal
    to the value passed in is encountered.
    """
    if have_encountered_larger_value:
        return 0

    did_encounter_larger_value = False
    try:
        next_value = next(iter)
        if next_value >= val:
            did_encounter_larger_value = True
    except StopIteration:
        return 0

    return 1 + distance_to_gte_or_end(iter, val, did_encounter_larger_value)


def calculate_scenic_score(i: int, j: int, grid: List[List[int]]) -> int:
    val = grid[i][j]
    m, n = len(grid), len(grid[0])

    score_to_right = (
        distance_to_gte_or_end(iter(grid[i][j + 1 :]), val) if i != m - 1 else 0
    )
    score_to_left = (
        distance_to_gte_or_end(iter(grid[i][j - 1 :: -1]), val) if i != 0 else 0
    )
    score_to_bottom = (
        distance_to_gte_or_end(iter(list(zip(*grid))[j][i + 1 :]), val)
        if j != n - 1
        else 0
    )
    score_to_top = (
        distance_to_gte_or_end(iter(list(zip(*grid))[j][i - 1 :: -1]), val)
        if j != 0
        else 0
    )

    result = score_to_right * score_to_left * score_to_top * score_to_bottom
    return result


with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
    text = f.read()

lines = text.split("\n")

grid = [[int(c) for c in line] for line in lines]

result1 = tree_counter(grid)
print(result1)

result2 = max(
    [
        calculate_scenic_score(i, j, grid)
        for i in range(len(grid))
        for j in range(len(grid[0]))
    ]
)
print(result2)
