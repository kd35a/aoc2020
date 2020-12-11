#!/usr/bin/env python3

from collections import Counter
from math import comb
import click

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    adapter_outputs = sorted([int(line.strip()) for line in input_file.readlines()])
    jolt_jumps = calculate_jumps(adapter_outputs)
    jolt_jump_counts = Counter(jolt_jumps)
    print("Answer: {}".format(jolt_jump_counts[1]*jolt_jump_counts[3]))
    num_arrangements = calc_arrangements(adapter_outputs)
    print("Number of arrangements: {}".format(num_arrangements))

def calculate_jumps(adapter_outputs):
    device_jolts = max(adapter_outputs) + 3
    adapter_outputs.append(device_jolts)
    current_jolt = 0
    jolt_jumps = list()
    for adapter_output in adapter_outputs:
        jolt_jump = adapter_output - current_jolt
        if jolt_jump > 3 or jolt_jump < 1:
            raise ValueError("Unexpected jolt jump: {}".format(jolt_jump))
        current_jolt = adapter_output
        jolt_jumps.append(jolt_jump)
    return jolt_jumps

def is_valid(adapter_outputs):
    for i in range(len(adapter_outputs) - 1):
        a, b = adapter_outputs[i:i+2]
        if b - a > 3 or b - a < 1:
            return False
    return True

def calc_arrangements(adapter_outputs):
    adapter_outputs.insert(0, 0) # inserting socket, device is already there since calculate_jumps
    reachables = [1] + ([0]*(len(adapter_outputs)-1))
    for i in range(len(adapter_outputs)-3):
        a_count = reachables[i]
        a, b, c, d = adapter_outputs[i:i+4]
        if b - a <= 3:
            reachables[i+1] += a_count
        if c - a <= 3:
            reachables[i+2] += a_count
        if d - a <= 3:
            reachables[i+3] += a_count

    a_count = reachables[-3]
    a, b, c = adapter_outputs[-3:]
    if b - a <= 3:
        reachables[-2] += a_count
    if c - a <= 3:
        reachables[-1] += a_count

    a_count = reachables[-2]
    a, b = adapter_outputs[-2:]
    if b - a <= 3:
        reachables[-1] += a_count

    return reachables[-1]

if __name__ == '__main__':
    main()
