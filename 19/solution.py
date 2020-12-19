#!/usr/bin/env python3

import json
import re
from functools import lru_cache
import click

RULE_PATTERN = re.compile(r"^(\d+): (\"([a-z])\"|.*)$")

all_rules = {}
char_rules = list()

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    raw_rules, messages = input_file.read().split("\n\n")
    parse_rules(raw_rules)
    # Remove following changes for part 1
    all_rules["8_0"] = ["42"]
    all_rules["8_1"] = ["42", "8"]
    all_rules["11_0"] = ["42", "31"]
    all_rules["11_1"] = ["42", "11", "31"]
    valid_messages = [m.strip() for m in messages.split("\n") if is_valid(m.strip(), "0")]
    print("Number of valid messages: {}".format(len(valid_messages)))

def parse_rules(raw_rules):
    for line in raw_rules.split("\n"):
        rule_id, complete_rule, char = RULE_PATTERN.match(line.strip()).groups()
        if char:
            all_rules[rule_id] = char
            char_rules.append(rule_id)
        else:
            for index, part in enumerate(complete_rule.split(" | ")):
                sub_rule = part.split(" ")
                all_rules["{}_{}".format(rule_id, index)] = sub_rule

@lru_cache(None)
def is_valid(message, from_rule):
    for rule in get_rules(from_rule):
        if isinstance(all_rules[rule], str):
            return all_rules[rule] == message
        sub_rules = all_rules[rule]
        if len(sub_rules) == 1:
            if is_valid(message, sub_rules[0]):
                return True
        elif len(sub_rules) == 2:
            b, c = sub_rules
            for p in range(1,len(message)):
                if is_valid(message[:p], b) and is_valid(message[p:], c):
                    return True
        elif len(sub_rules) == 3:
            b, c, d = sub_rules
            for p in range(1, len(message)-1):
                for s in range(p+1, len(message)):
                    if is_valid(message[:p], b) and is_valid(message[p:s], c) and is_valid(message[s:], d):
                        return True
        else:
            raise ValueError("Not yet implemented")

    return False


def get_rules(prefix):
    return [rule for rule in all_rules if rule.split("_")[0] == prefix]

if __name__ == '__main__':
    main()
