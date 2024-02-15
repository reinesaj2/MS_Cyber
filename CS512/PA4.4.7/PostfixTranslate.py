#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 14:24:32 2023

@author: abrahamreines
"""

from SimpleStack import Stack

class PostfixTranslate:
    """
    Translate infix expressions to postfix notation.
    """
    def __init__(self):
        self.operators = ["|", "&", "+-", "*/%", "^", "()", "="]
        
    def precedence(self, operator):
        """Get the precedence of an operator."""
        for p, ops in enumerate(self.operators):
            if operator in ops:
                return p + 1
    
    def nextToken(self, s):
        """Extract the next token from the input string."""
        token = ""
        s = s.strip()
        if len(s) > 0:
            if self.precedence(s[0]):
                token = s[0]
                s = s[1:]
            else:
                while len(s) > 0 and not self.precedence(s[0]):
                    token += s[0]
                    s = s[1:]
        return token, s
    
    def translate(self, formula):
        """Translate an infix formula into postfix notation."""
        postfix = []
        s = Stack(100)
        token, formula = self.nextToken(formula)
        
        while token:
            prec = self.precedence(token)
            if prec:
                while not s.is_empty() and self.precedence(s.peek()) >= prec:
                    postfix.append(s.pop())
                s.push(token)
            else:
                postfix.append(token)
            token, formula = self.nextToken(formula)
        
        while not s.is_empty():
            postfix.append(s.pop())
        
        return ' '.join(postfix)
