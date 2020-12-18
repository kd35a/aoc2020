#!/usr/bin/env python3

from functools import reduce
from operator import mul
import click

STATE_NUM = "NUM"
STATE_OPT = "OPERATOR"

@click.command()
@click.argument('input_file', type=click.File())
def main(input_file):
    lines = [line.strip() for line in input_file.readlines()]
    result = sum([calculate(line, calculate_expression) for line in lines])
    print("Sum of all calculations: {}".format(result))
    result2 = sum([calculate(line, calculate_expression2) for line in lines])
    print("Sum of all calculations 2: {}".format(result2))

def calculate(expression, calculator_function):
    expression_boundaries = find_sub_expressions(expression)
    while expression_boundaries:
        ((start, stop), _) = expression_boundaries
        expr = expression[start+1:stop]
        value = calculator_function(expr)
        expression = expression[:start] + str(value) + expression[stop+1:]
        expression_boundaries = find_sub_expressions(expression)
    return calculator_function(expression)

def calculate_expression(exp):
    state = STATE_OPT
    parts = exp.split(" ")
    if len(parts) == 1:
        return int(parts[0])
    result = int(parts[0])
    operator = ""
    for part in parts[1:]:
        if state == STATE_OPT:
            operator = part
            state = STATE_NUM
        elif state == STATE_NUM:
            value = int(part)
            if operator == "*":
                result *= value
            elif operator == "+":
                result += value
            state = STATE_OPT
    return result

def calculate_expression2(exp):
    state = STATE_OPT
    parts = exp.split(" ")
    if len(parts) == 1:
        return int(parts[0])
    operator = ""
    rpn_stack = [int(parts[0])]
    for part in parts[1:]:
        if state == STATE_OPT:
            operator = part
            state = STATE_NUM
        elif state == STATE_NUM:
            value = int(part)
            if operator == "*":
                rpn_stack.append(value)
            elif operator == "+":
                prev_value = rpn_stack.pop()
                result = value + prev_value
                rpn_stack.append(result)
            state = STATE_OPT
    return reduce(mul, rpn_stack)

def find_sub_expressions(expression):
    parenthesises = list()
    expression_boundaries = list()
    for i, c in enumerate(expression):
        if c == "(":
            parenthesises.append(i)
        if c == ")":
            depth = len(parenthesises)
            expression_boundaries.append(((parenthesises.pop(), i), depth))
    expression_boundaries.sort(key=lambda x: x[1], reverse=True)
    if expression_boundaries:
        return expression_boundaries[0]
    return None

if __name__ == '__main__':
    main()
