#!/usr/bin/env python3

import re
import click


@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    input_content = input_file.read()
    groups = [group for group in input_content.split("\n\n")]
    groups_uniq_count = [len(set(group_answers.replace("\n", ""))) for group_answers in groups]
    print("Sum of unique answers by group: {}".format(sum(groups_uniq_count)))
    group_common_count = [count_common_answers(group.strip()) for group in groups]
    print("Sum of common answers by group: {}".format(sum(group_common_count)))

def count_common_answers(group):
    complete_set = set(group.replace("\n", ""))
    individuals = group.split("\n")
    common_set = list()
    for answer in complete_set:
        if all(answer in individual for individual in individuals):
            common_set.append(answer)
    return len(common_set)

if __name__ == '__main__':
    main()
