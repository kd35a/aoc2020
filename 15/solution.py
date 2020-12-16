#!/usr/bin/env python3

import click

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    line = input_file.read()
    starting_numbers = [int(num) for num in line.split(",")]
    last_spoken_number = play_game(starting_numbers, 2020)
    print("Last spoken number: {}".format(last_spoken_number))
    last_spoken_number2 = play_game(starting_numbers, 30000000)
    print("Last spoken number 2: {}".format(last_spoken_number2))

def play_game(starting_numbers, num_spoken_numbers):
    spoken_numbers = {number: [index] for index, number in enumerate(starting_numbers)}
    last_spoken = starting_numbers[-1]
    for i in range(len(starting_numbers), num_spoken_numbers):
        indexes = spoken_numbers[last_spoken]
        if not indexes or len(indexes) <= 1:
            last_spoken = 0
        else:
            a, b = indexes[-2:]
            last_spoken = b - a
        if last_spoken not in spoken_numbers:
            spoken_numbers[last_spoken] = [i]
        else:
            spoken_numbers[last_spoken].append(i)

    return last_spoken

if __name__ == '__main__':
    main()
