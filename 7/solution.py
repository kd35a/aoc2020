#!/usr/bin/env python3

import json
import re
import click

RULE_PATTERN = re.compile(r"^(\w+ \w+) bags contain (no other bags|.*).$")
CAN_CONTAIN_PATTERN = re.compile(r"^(\d+) (\w+ \w+) bags?$")
NO_OTHER_BAGS = "no other bags"

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    rule_lines = [line.strip() for line in input_file.readlines()]
    rules = dict()
    for rule_line in rule_lines:
        rules.update(parse_rule_line(rule_line))
    print(count_valid_rules(rules))
    print(count_containg_bags(rules, "shiny gold"))

def parse_rule_line(rule_line):
    match = RULE_PATTERN.match(rule_line)
    if not match:
        raise ValueError("Rule line is strange: {}".format(rule_line))
    bag_color = match.group(1)
    bag_can_contain = dict()

    if match.group(2) != NO_OTHER_BAGS:
        can_contain_matches = [CAN_CONTAIN_PATTERN.match(c) for c in match.group(2).split(", ")]
        for m in can_contain_matches:
            count, color = m.groups()
            bag_can_contain[color] = int(count)

    return {bag_color: bag_can_contain}

def count_valid_rules(rules):
    wanted = "shiny gold"
    direct = [bag_color for bag_color in rules if wanted in rules[bag_color]]
    direct_and_indirect = direct
    while True:
        indirect = list()
        for bag_color in direct_and_indirect:
            indirect.extend([ind for ind in rules if bag_color in rules[ind] and ind not in direct_and_indirect])
        if not indirect:
            break
        direct_and_indirect.extend(set(indirect))
    return len(direct_and_indirect)

def count_containg_bags(rules, wanted):
    total_count = 0
    for bag, count in rules[wanted].items():
        total_count += count + count*count_containg_bags(rules, bag)
    return total_count

if __name__ == '__main__':
    main()
