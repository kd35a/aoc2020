#!/usr/bin/env python3

import re
import click

LINE_PATTERN = re.compile(r"^(\d+)-(\d+) ([a-z]): (\w+)$")

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    lines = [line.strip() for line in input_file.readlines()]
    print("Sled rental valid passwords: {}".format(
        sum([sled_rental_validation(line) for line in lines])))
    print("Toboggan Corporate valid passwords: {}".format(
        sum([toboggan_validation(line) for line in lines])))

def sled_rental_validation(line):
    min_occurances, max_occurances, character, password = LINE_PATTERN.match(line).groups()
    character_occurances = password.count(character)
    return int(min_occurances) <= character_occurances <= int(max_occurances)

def toboggan_validation(line):
    first_index, second_index, character, password = LINE_PATTERN.match(line).groups()
    first_character_matches = password[int(first_index) - 1] == character
    second_character_matches = password[int(second_index) - 1] == character
    return first_character_matches != second_character_matches

if __name__ == '__main__':
    main()
