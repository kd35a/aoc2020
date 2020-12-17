#!/usr/bin/env python3

import click

STATE_ACTIVE = "#"
STATE_INACTIVE = "."

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    pocket = parse_input(input_file.read())
    active_cubes = run_cycles(pocket)
    print("Active cubes: {}".format(active_cubes))

def run_cycles(pocket):
    z_min, z_max = min(pocket), max(pocket)
    x_min, x_max = min(pocket[z_min]), max(pocket[z_min])
    y_min, y_max = min(pocket[z_min][x_min]), max(pocket[z_min][x_min])
    w_min, w_max = 0, 0
    for _ in range(6):
        state_changes = {}
        for z in range(z_min-1, z_max+2):
            for x in range(x_min-1, x_max+2):
                for y in range(y_min-1, y_max+2):
                    for w in range(w_min-1, w_max+2):
                        neighbours = count_neighbours(pocket, z, x, y, w)
                        this_active = is_active(pocket, z, x, y, w)
                        if this_active and neighbours != 2 and neighbours != 3:
                            state_changes[(z, x, y, w)] = STATE_INACTIVE
                        elif not this_active and neighbours == 3:
                            state_changes[(z, x, y, w)] = STATE_ACTIVE
        for (z, x, y, w) in state_changes:
            z_min = min(z, z_min)
            z_max = max(z, z_max)
            x_min = min(x, x_min)
            x_max = max(x, x_max)
            y_min = min(y, y_min)
            y_max = max(y, y_max)
            w_min = min(w, w_min)
            w_max = max(w, w_max)
            new_state = state_changes[(z, x, y, w)]
            if z not in pocket:
                pocket[z] = {x: {y: {w: new_state}}}
            elif x not in pocket[z]:
                pocket[z][x] = {y: {w: new_state}}
            elif y not in pocket[z][x]:
                pocket[z][x][y] = {w: new_state}
            else:
                pocket[z][x][y][w] = new_state

    active_cubes = 0
    for z in range(z_min, z_max+1):
        for x in range(x_min, x_max+1):
            for y in range(y_min, y_max+1):
                for w in range(w_min, w_max+1):
                    if is_active(pocket, z, x, y, w):
                        active_cubes += 1
    return active_cubes

def is_active(pocket, z, x, y, w):
    if z not in pocket:
        return False
    if x not in pocket[z]:
        return False
    if y not in pocket[z][x]:
        return False
    if w not in pocket[z][x][y]:
        return False
    return pocket[z][x][y][w] == STATE_ACTIVE

def count_neighbours(pocket, z, x, y, w):
    active_neighbours = 0
    for zi in range(z-1, z+2):
        for xi in range(x-1, x+2):
            for yi in range(y-1, y+2):
                for wi in range(w-1, w+2):
                    if (zi, xi, yi, wi) == (z, x, y, w):
                        continue
                    if is_active(pocket, zi, xi, yi, wi):
                        active_neighbours += 1
    return active_neighbours

def parse_input(input_data):
    pocket_plane = {}
    for i, line in enumerate(input_data.split("\n")):
        pocket_line = {}
        for j, state in enumerate(list(line)):
            pocket_line[j] = {0: state}
        pocket_plane[i] = pocket_line
    return {0: pocket_plane}

if __name__ == '__main__':
    main()
