#!/usr/bin/env python3

from itertools import combinations
import click

@click.command()
@click.argument('input_file', type=click.File())
@click.argument('preamble_length', type=click.INT)
def main(input_file, preamble_length):
    numbers = [int(line.strip()) for line in input_file.readlines()]
    breaking_number, breaking_index = find_breaking_number(numbers, preamble_length)
    print("Breaking number: {}".format(breaking_number))
    set_min, set_max = find_span(numbers, breaking_number, breaking_index)
    print("Sum of min+max in span: {}".format(set_min+set_max))

def find_breaking_number(numbers, preamble_length):
    breaking_number = -1
    breaking_index = -1
    for i in range(len(numbers) - preamble_length):
        current_index = i + preamble_length
        current_number = numbers[current_index]
        is_valid = False
        for a, b in combinations(numbers[i:current_index], 2):
            if a + b == current_number:
                is_valid = True
        if not is_valid:
            breaking_number = current_number
            breaking_index = current_index
            break
    return (breaking_number, breaking_index)

def find_span(numbers, breaking_number, breaking_index):
    bottom_half = numbers[0:breaking_index]
    top_half = numbers[breaking_index+1:]
    result = None
    i = 0
    for half in [bottom_half, top_half]:
        print("Testing half {}".format(i))
        i += 1
        span = find_span_sum(half, breaking_number)
        print(str(span))
        if span:
            result = span
            break
    if not result:
        raise ValueError("Couldn't find a span")
    return result

def find_span_sum(numbers, expected_sum):
    if sum(numbers) == expected_sum:
        return (min(numbers), max(numbers))
    sets = set()
    sets.add((1, len(numbers)))
    sets.add((0, len(numbers)-1))
    while sets:
        bottom, top = sets.pop()
        current_set = numbers[bottom:top]
        sum_of_current_set = sum(current_set)
        if sum_of_current_set == expected_sum:
            return (min(current_set), max(current_set))
        if sum_of_current_set < expected_sum:
            continue
        if top - bottom > 3:
            sets.add((bottom+1, top))
            sets.add((bottom, top-1))
    return None

if __name__ == '__main__':
    main()
