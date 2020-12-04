#!/usr/bin/env python3

import re
import click

REQUIRED_FIELDS = {
        "byr": re.compile(r"^\d{4}$"),
        "iyr": re.compile(r"^\d{4}$"),
        "eyr": re.compile(r"^\d{4}$"),
        "hgt": re.compile(r"^(\d+)(cm|in)$"),
        "hcl": re.compile(r"^#[a-f0-9]{6}$"),
        "ecl": re.compile(r"^(amb|blu|brn|gry|grn|hzl|oth)$"),
        "pid": re.compile(r"^[0-9]{9}$"),
        "cid": re.compile(r"")
        }

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    lines = [line.strip() for line in input_file.readlines()]
    passports = construct_passports(lines)
    print("Number of passports: {}".format(len(passports)))
    valid_passports1 = [passport for passport in passports if validate1(passport)]
    print("Valid passports 1: {}".format(len(valid_passports1)))
    valid_passports2 = [passport for passport in passports if validate2(passport)]
    print("Valid passports 2: {}".format(len(valid_passports2)))

def construct_passports(lines):
    passports = list()
    current_passport_lines = list()
    for line in lines:
        if line != "":
            current_passport_lines.append(line)
        else:
            passport = parse_passport(" ".join(current_passport_lines))
            passports.append(passport)
            current_passport_lines = list()
    passport = parse_passport(" ".join(current_passport_lines))
    passports.append(passport)
    return passports

def parse_passport(passport_line):
    passport = dict()
    for attribute in passport_line.split(" "):
        key, value = attribute.split(":")
        passport[key] = value
    return passport

def validate1(passport):
    for key in REQUIRED_FIELDS:
        if key not in passport and key != "cid":
            return False
    return True

def validate2(passport):
    for key, pattern in REQUIRED_FIELDS.items():
        if key not in passport and key != "cid":
            return False
        if key == "cid":
            continue
        value = passport[key]
        pattern_match = pattern.match(value)
        if not pattern_match:
            return False
        if key == "byr" and not 1920 <= int(value) <= 2002:
            return False
        if key == "iyr" and not 2010 <= int(value) <= 2020:
            return False
        if key == "eyr" and not 2020 <= int(value) <= 2030:
            return False
        if key == "hgt" and not valid_height(*pattern_match.groups()):
            return False
    return True

def valid_height(measurement, unit):
    if unit == "cm":
        return 150 <= int(measurement) <= 193
    if unit == "in":
        return 59 <= int(measurement) <= 76
    return False

if __name__ == '__main__':
    main()
