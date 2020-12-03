#!/usr/bin/env python3

from functools import reduce
import operator
import click

X_INDEX = 1
Y_INDEX = 0

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    lines = [line.strip() for line in input_file.readlines()]
    tree_map = [[is_tree(coord) for coord in line] for line in lines]
    slopes = [
            (1, 1),
            (1, 3),
            (1, 5),
            (1, 7),
            (2, 1)
            ]
    slope_encounters = list()
    for slope in slopes:
        encounters = count_trees_on_slope(tree_map, slope)
        slope_encounters.append(encounters)
        print("Encountered {} trees on slope {}".format( encounters, slope))
    print("Solution: {}".format(reduce(operator.mul, slope_encounters)))

def count_trees_on_slope(tree_map, slope):
    line_length = len(tree_map[0])
    current_coord = [0, 0]
    tree_encounters = 0
    while current_coord[Y_INDEX] < len(tree_map):
        y_coord, x_coord = current_coord
        if tree_map[y_coord][x_coord % line_length]:
            tree_encounters += 1
        current_coord[X_INDEX] += slope[X_INDEX]
        current_coord[Y_INDEX] += slope[Y_INDEX]
    return tree_encounters

def is_tree(coord):
    if coord == '.':
        return False
    if coord == '#':
        return True
    raise ValueError("Unknown coordinate value: {}".format(coord))

if __name__ == '__main__':
    main()
