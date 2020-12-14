#!/usr/bin/env python3

import click

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    lines = [line.strip() for line in input_file.readlines()]
    start_time = int(lines[0])
    bus_ids = [int(bus_id) for bus_id in lines[1].split(",") if bus_id != "x"]
    first_bus_id, wait_time = part_one(start_time, bus_ids)
    print("Part one: {}".format(first_bus_id*wait_time))
    t = part_two(lines[1])
    print("Subsequent start t: {}".format(t))

def part_one(start_time, bus_ids):
    bus_ids_wait_times = [(bus_id, bus_id-(start_time%bus_id)) for bus_id in bus_ids]
    return min(bus_ids_wait_times, key=lambda x: x[1])

def part_two(line):
    bus_ids_with_t_offset = [(int(bus_id), offset) for (offset, bus_id) in enumerate(line.split(",")) if bus_id != "x"]

    a_one, o_one = bus_ids_with_t_offset[0]
    t = 0
    t_step = a_one
    for i in range(1, len(bus_ids_with_t_offset)):
        a_two, o_two = bus_ids_with_t_offset[i]
        while True:
            t += t_step
            if (t+o_one)%a_one == 0 and (t+o_two)%a_two == 0:
                t_step = t_step*a_two
                break

    return t

if __name__ == '__main__':
    main()
