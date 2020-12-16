#!/usr/bin/env python3

import re
from functools import reduce
import operator
import click

FIELD_RULE_PATTERN = re.compile(r"^([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)$")

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    input_data = input_file.read()
    sections = input_data.split("\n\n")
    field_rules = parse_field_rules(sections[0])
    my_ticket = parse_tickets(sections[1])[0]
    nearby_tickets = parse_tickets(sections[2])
    part_one, valid_tickets = solve_part_one(field_rules, nearby_tickets)
    print("Part one: {}".format(part_one))
    field_mappings = identify_fields(field_rules, valid_tickets)
    part_two = solve_part_two(my_ticket, field_mappings)
    print("Part two: {}".format(part_two))

def solve_part_one(field_rules, nearby_tickets):
    invalid_fields = list()
    valid_tickets = list()
    for ticket in nearby_tickets:
        is_valid = True
        for field in ticket:
            if not follows_rules(field_rules, field):
                is_valid = False
                invalid_fields.append(field)
        if is_valid:
            valid_tickets.append(ticket)
    return (sum(invalid_fields), valid_tickets)

def solve_part_two(ticket, field_mappings):
    departure_values = list()
    for field in field_mappings:
        if field.startswith("departure"):
            departure_values.append(ticket[field_mappings[field][0]])

    return reduce(operator.mul, departure_values)

def follows_rules(field_rules, field):
    for rule in field_rules.values():
        if follows_rule(rule, field):
            return True
    return False

def follows_rule(rule, field):
    first_range, second_range = rule
    return field in first_range or field in second_range

def identify_fields(field_rules, tickets):
    field_mappings = {field: list(range(len(field_rules))) for field in field_rules}
    for ticket in tickets:
        for field, rule in field_rules.items():
            for index, field_value in enumerate(ticket):
                if index in field_mappings[field] and not follows_rule(rule, field_value):
                    field_mappings[field].remove(index)
    fields_with_mapping_lengts = [(field, len(field_mappings[field])) for field in field_mappings]
    fields_with_mapping_lengts.sort(key=lambda x: x[1])
    for field, _ in fields_with_mapping_lengts:
        for field_mapping in field_mappings[field]:
            for other_field in field_mappings:
                if field != other_field and field_mapping in field_mappings[other_field]:
                    field_mappings[other_field].remove(field_mapping)
    return field_mappings

def parse_field_rules(lines):
    fields = {}
    for line in lines.split("\n"):
        match = FIELD_RULE_PATTERN.match(line)
        if not match:
            raise ValueError("Could not parse: {}".format(line))
        field, amin, amax, bmin, bmax = match.groups()
        fields[field] = (list(range(int(amin), int(amax)+1)), list(range(int(bmin), int(bmax)+1)))
    return fields

def parse_tickets(lines):
    tickets = list()
    for line in lines.strip().split("\n")[1:]:
        ticket = [int(v) for v in line.split(",")]
        tickets.append(ticket)
    return tickets

if __name__ == '__main__':
    main()
