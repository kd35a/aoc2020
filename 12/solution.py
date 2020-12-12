#!/usr/bin/env python3

from math import sqrt, atan2, cos, radians, sin
import re
import click

INSTRUCTION_PATTERN = re.compile(r"^([NSEWLRF])(\d+)$")

NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"
TURN_LEFT = "L"
TURN_RIGHT = "R"
FORWARD = "F"

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    instructions = [parse_instr(line.strip()) for line in input_file.readlines()]
    part1_manhattan_distance = calc_manhattan_distance1(instructions)
    print("Manhattan distance part 1: {}".format(part1_manhattan_distance))
    part2_manhattan_distance = calc_manhattan_distance2(instructions)
    print("Manhattan distance part 2: {}".format(part2_manhattan_distance))

def parse_instr(line):
    match = INSTRUCTION_PATTERN.match(line)
    if not match:
        raise ValueError("Unexpected line: {}".format(line))
    action, value = match.groups()
    return (action, int(value))

def calc_manhattan_distance1(instructions):
    heading = 90
    position = [0, 0]
    for instruction in instructions:
        action, value = instruction
        new_heading, dlong, dlat = calc_movement1(heading, action, value)
        heading = new_heading
        position[0] += dlong
        position[1] += dlat
    return abs(position[0]) + abs(position[1])

def calc_movement1(heading, action, value):
    if action == NORTH:
        return (heading, 0, value)
    if action == SOUTH:
        return (heading, 0, -value)
    if action == EAST:
        return (heading, value, 0)
    if action == WEST:
        return (heading, -value, 0)
    if action == TURN_LEFT:
        return (heading - value, 0, 0)
    if action == TURN_RIGHT:
        return (heading + value, 0, 0)
    if action == FORWARD:
        rad = radians(heading)
        dlong = round(value*sin(rad))
        dlat = round(value*cos(rad))
        return (heading, dlong, dlat)

def calc_manhattan_distance2(instructions):
    position = [0, 0]
    waypoint_position = [10, 1]
    for instruction in instructions:
        action, value = instruction
        new_position, new_waypoint_position = calc_movement2(position, waypoint_position, action, value)
        position = new_position
        waypoint_position = new_waypoint_position
    return abs(position[0]) + abs(position[1])

def calc_movement2(position, waypoint_position, action, value):
    if action == NORTH:
        new_waypoint_position = [value + delta for (value, delta) in zip(waypoint_position, [0, value])]
        return (position, new_waypoint_position)
    if action == SOUTH:
        new_waypoint_position = [value + delta for (value, delta) in zip(waypoint_position, [0, -value])]
        return (position, new_waypoint_position)
    if action == EAST:
        new_waypoint_position = [value + delta for (value, delta) in zip(waypoint_position, [value, 0])]
        return (position, new_waypoint_position)
    if action == WEST:
        new_waypoint_position = [value + delta for (value, delta) in zip(waypoint_position, [-value, 0])]
        return (position, new_waypoint_position)
    if action == TURN_LEFT:
        new_waypoint_position = rotate(waypoint_position, value)
        return (position, new_waypoint_position)
    if action == TURN_RIGHT:
        new_waypoint_position = rotate(waypoint_position, -value)
        return (position, new_waypoint_position)
    if action == FORWARD:
        new_position = [
                position[0] + value*waypoint_position[0],
                position[1] + value*waypoint_position[1]
                ]
        return (new_position, waypoint_position)

def rotate(position, deg):
    theta = atan2(position[1], position[0])
    r = sqrt(position[0]**2 + position[1]**2)
    new_theta = theta + radians(deg)
    new_long = round(r*cos(new_theta))
    new_lat = round(r*sin(new_theta))
    return [new_long, new_lat]

if __name__ == '__main__':
    main()
