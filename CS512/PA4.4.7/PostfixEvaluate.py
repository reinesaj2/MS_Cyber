#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 14:38:12 2023

@author: abrahamreines
"""

from PostfixTranslate import PostfixTranslate
from SimpleStack import Stack
from OrderedRecordArray import OrderedRecordArray

def precedence(operator):
    """Get the precedence level of an operator."""
    operators = ["|", "&", "+-", "*/%", "^", "()", "="]
    for p, ops in enumerate(operators):
        if operator in ops:
            return p + 1

def PostfixEvaluate(formula):
    """
    Evaluate a given infix formula by first converting it to postfix notation.
    This function also handles variable assignments and references.
    """
    translator = PostfixTranslate()
    postfix = translator.translate(formula).split()
    s = Stack(100)
    variables = OrderedRecordArray(100)

    for token in postfix:
        prec = precedence(token)

        if prec:
            if token == '=':
                if s.is_empty():
                    raise ValueError("Not enough operands for assignment operator.")
                
                value = s.pop()
                
                if s.is_empty() or not isinstance(s.peek(), str):
                    raise ValueError("Invalid left-hand side for assignment.")
                
                var_name = s.pop()
                variables.insert((var_name, value))
                s.push(value)

            else:
                if isinstance(left, str):
                    left_value = variables.search(left)
                    if left_value is None:
                        raise ValueError(f"Variable {left} is not set.")
                    left = left_value[1]
                
                if isinstance(right, str):
                    right_value = variables.search(right)
                    if right_value is None:
                        raise ValueError(f"Variable {right} is not set.")
                    right = right_value[1]
                
                result = eval(f"{left} {token} {right}")
                s.push(result)
        else:
            s.push(token if token.isalpha() else int(token))

        print(f'After processing {token}, stack holds: {s}')


    final_result = s.pop()
    print(f"Final result = {final_result}")

if __name__ == '__main__':
    infix_expr = input("Infix expression to evaluate: ")
    print(f"The postfix representation of {infix_expr} is {PostfixTranslate().translate(infix_expr)}")
    PostfixEvaluate(infix_expr)
