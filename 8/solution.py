#!/usr/bin/env python3

from copy import deepcopy
import re
import click

INSTRUCTION_SET = re.compile(r"^(acc|jmp|nop) ((\+|-)\d+)$")

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    lines = [line.strip() for line in input_file.readlines()]
    instructions = [parse_instruction(line) for line in lines]
    accumulator, _ = run_until_loop(instructions)
    print("Accumulator before looping: {}".format(accumulator))
    accumulator, modified_instruction = find_non_looping_run(instructions)
    print("Accumulator for non-looping: {}".format(accumulator))
    print("Modified instruction: {}".format(modified_instruction))

def parse_instruction(line):
    match = INSTRUCTION_SET.match(line)
    if not match:
        raise ValueError("Unexpected input: {}".format(line))
    operation, argument, _ = match.groups()
    return (operation, int(argument))

def run_until_loop(instructions):
    ip = 0
    accumulator = 0
    visited_instructions = set()
    while ip < len(instructions) and ip not in visited_instructions:
        visited_instructions.add(ip)
        operation, argument = instructions[ip]
        if operation == "acc":
            accumulator += argument
            ip += 1
        elif operation == "jmp":
            ip += argument
        elif operation == "nop":
            ip +=1
        else:
            raise ValueError("Unknown instruction: {} {}".format(operation, argument))
    return (accumulator, ip == len(instructions))

def find_non_looping_run(instructions):
    for i in reversed(range(len(instructions))):
        operation, argument = instructions[i]
        if operation not in ["jmp", "nop"]:
            continue
        mutaded_instructions = deepcopy(instructions)
        if operation == "jmp":
            mutaded_instructions[i] = ("nop", argument)
        elif operation == "nop":
            mutaded_instructions[i] = ("jmp", argument)
        accumulator, clean_exit = run_until_loop(mutaded_instructions)
        if clean_exit:
            return (accumulator, i)
    raise ValueError("Could not find any mutation that solved the pussel")

if __name__ == '__main__':
    main()
