#!/usr/bin/env python3

from copy import deepcopy
import click

FLOOR = "."
EMPTY = "L"
OCCUPIED = "#"

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    layout = [list(line.strip()) for line in input_file.readlines()]
    result = cycle_til_stable(deepcopy(layout), count_neighbours1, 4)
    print("Occupied seats when stable: {}".format(result))
    result2 = cycle_til_stable(layout, count_visible_neighbours, 5)
    print("Occupied seats when stable 2: {}".format(result2))

def cycle_til_stable(layout, count_neighbours, occ_max):
    will_change = set("dummy")
    while will_change:
        will_change = set()
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                if layout[i][j] == FLOOR:
                    continue
                neighbours = count_neighbours(layout, i, j)
                if layout[i][j] == EMPTY and neighbours == 0:
                    will_change.add((i, j))
                elif layout[i][j] == OCCUPIED and neighbours >= occ_max:
                    will_change.add((i, j))

        for i, j in will_change:
            if layout[i][j] == EMPTY:
                layout[i][j] = OCCUPIED
            elif layout[i][j] == OCCUPIED:
                layout[i][j] = EMPTY

    return [brick for line in layout for brick in line].count(OCCUPIED)

def count_neighbours1(layout, i, j):
    i_min = max(i-1, 0)
    j_min = max(j-1, 0)
    list_of_grid = [brick for line in layout[i_min:i+2] for brick in line[j_min:j+2]]
    count = list_of_grid.count(OCCUPIED)
    if layout[i][j] == OCCUPIED:
        return count - 1
    return count

DIRECTIONS = [
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1)
        ]

def count_visible_neighbours(layout, i, j):
    return sum([has_visible(layout, i, j, dx, dy) for dx, dy in DIRECTIONS])

def has_visible(layout, x, y, dx, dy):
    x += dx
    y += dy
    while 0 <= x < len(layout) and 0 <= y < len(layout[0]):
        if layout[x][y] == OCCUPIED:
            return 1
        if layout[x][y] == EMPTY:
            return 0
        x += dx
        y += dy
    return 0


if __name__ == '__main__':
    main()
