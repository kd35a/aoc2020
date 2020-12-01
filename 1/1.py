#!/usr/bin/env python3

from itertools import combinations
from functools import reduce
import operator
import click

@click.command()
@click.argument('input_file', type=click.File())
@click.argument('combination_length', default=2, type=click.INT)
def main(input_file, combination_length):
    numbers = [int(line.strip()) for line in input_file.readlines()]
    for combination in combinations(numbers, combination_length):
        if sum(combination) == 2020:
            print("{} = {}".format(str(combination), reduce(operator.mul, combination)))
            return

if __name__ == '__main__':
    main()
