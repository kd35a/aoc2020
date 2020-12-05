#!/usr/bin/env python3

from math import floor, ceil
import re
import click

BIN_PATH = re.compile(r"^([FB]{7})([LR]{3})$")

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    seat_ids = list()
    for line in input_file.readlines():
        row_path, column_path = BIN_PATH.match(line.strip()).groups()
        row_num = bin_search_row(row_path)
        column_num = bin_search_column(column_path)
        seat_num = row_num*8 + column_num
        seat_ids.append(seat_num)
    print("Max seat ID: {}".format(max(seat_ids)))
    print("Empty seat: {}".format(find_missing_seat(seat_ids)))

def bin_search_row(bin_path):
    min_row = 0
    max_row = 127
    for path in bin_path:
        if path == 'F':
            max_row -= floor((max_row - min_row)/2)
        if path == 'B':
            min_row += ceil((max_row - min_row)/2)
    return min_row

def bin_search_column(bin_path):
    min_column = 0
    max_column = 7
    for path in bin_path:
        if path == 'L':
            max_column -= floor((max_column - min_column)/2)
        if path == 'R':
            min_column += ceil((max_column - min_column)/2)
    return min_column

def find_missing_seat(seat_ids):
    sorted_ids = sorted(seat_ids)
    candidates = list()
    for i in range(len(sorted_ids) - 1):
        a = sorted_ids[i]
        b = sorted_ids[i+1]
        if b == a + 2:
            candidates.append(a+1)
    assert len(candidates) == 1
    return candidates[0]

if __name__ == '__main__':
    main()
