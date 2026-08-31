#!/usr/bin/env python3
"""Multiply two CSV matrices and write the result as CSV."""

import csv
import sys
from pathlib import Path


def read_matrix(path: Path) -> list[list[float]]:
    with path.open(newline="", encoding="utf-8") as matrix_file:
        matrix = [[float(value) for value in row] for row in csv.reader(matrix_file)]

    if not matrix or not matrix[0]:
        raise ValueError(f"Matrix is empty: {path}")
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError(f"Matrix has rows with different lengths: {path}")
    return matrix


def multiply(
    matrix_a: list[list[float]],
    matrix_b: list[list[float]],
) -> list[list[float]]:
    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError(
            "Incompatible matrix dimensions: "
            f"{len(matrix_a)}x{len(matrix_a[0])} and "
            f"{len(matrix_b)}x{len(matrix_b[0])}"
        )

    columns_b = list(zip(*matrix_b))
    return [
        [sum(a * b for a, b in zip(row_a, column_b)) for column_b in columns_b]
        for row_a in matrix_a
    ]


def write_matrix(path: Path, matrix: list[list[float]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerows([[f"{value:g}" for value in row] for row in matrix])


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(
            "Usage: python multiply_csv.py MATRIX_A.csv MATRIX_B.csv RESULT.csv"
        )

    input_a, input_b, output = map(Path, sys.argv[1:])
    matrix_a = read_matrix(input_a)
    matrix_b = read_matrix(input_b)
    result = multiply(matrix_a, matrix_b)
    write_matrix(output, result)
    print(
        f"multiplied {len(matrix_a)}x{len(matrix_a[0])} by "
        f"{len(matrix_b)}x{len(matrix_b[0])}"
    )


if __name__ == "__main__":
    main()
