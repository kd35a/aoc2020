#!/usr/bin/env python3

from itertools import product
from copy import deepcopy
import re
import click

INSTRUCTION_PATTERN = re.compile(r"^(mask|(mem\[(\d+)\])) = ([X01]{36}|\d+)$")

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    instructions = [parse_inst(line.strip()) for line in input_file.readlines()]
    sum_of_values = run_program(instructions)
    print("Sum of values: {}".format(sum_of_values))
    sum_of_values2 = run_program2(instructions)
    print("Sum of values, part 2: {}".format(sum_of_values2))

def parse_inst(line):
    groups = INSTRUCTION_PATTERN.match(line).groups()
    if groups[0] == "mask":
        return (groups[0], groups[3])
    return (int(groups[2]), int(groups[3]))

def run_program(instructions):
    mask = "X"*36
    values = {}
    for instruction in instructions:
        if instruction[0] == "mask":
            mask = instruction[1]
        else:
            values[instruction[0]] = apply_mask(instruction[1], mask)
    return sum(values.values())

def apply_mask(value, mask):
    zeroing_binary = [m if m == '0' else '1' for m in mask]
    zeroing = int("".join(zeroing_binary), 2)
    oneing_binary = [m if m == '1' else '0' for m in mask]
    oneing = int("".join(oneing_binary), 2)
    return (value & zeroing) | oneing

def run_program2(instructions):
    mask = "X"*36
    values = {}
    for instruction in instructions:
        if instruction[0] == "mask":
            mask = instruction[1]
        else:
            addresses = apply_mask2(instruction[0], mask)
            for address in addresses:
                values[address] = instruction[1]
    return sum(values.values())

def apply_mask2(address, mask):
    address_binary = "{:0>36b}".format(address)
    base_address = ""
    for a, m in zip(address_binary, mask):
        if m == '0':
            base_address += a
        else:
            base_address += m
    num_addresses = 2**base_address.count("X")
    addresses = [None]*num_addresses
    for i in range(num_addresses):
        addresses[i] = deepcopy([ba for ba in base_address])
    x_count = base_address.count("X")
    fillings = list(product("01", repeat=x_count))
    for adrindex, fills in enumerate(fillings):
        j = 0
        for i in [index for index, a in enumerate(base_address) if a == 'X']:
            addresses[adrindex][i] = fills[j]
            j += 1
    return [int("".join(a), 2) for a in addresses]

if __name__ == '__main__':
    main()
