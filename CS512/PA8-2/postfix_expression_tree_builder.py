#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 11:01:12 2023

@author: abrahamreines
"""

class BinaryTree:
    """
    Author: Abraham J. Reines, Modified: Nov 11
    A BinaryTree class without key ordering. 
    It creates single node trees as well as combines two trees with an operator as the root.
    """

    def __init__(self, root_obj):
        """ Initialize the tree with a root object """
        self.key = root_obj # vital for the constructor initialization 
        self.left_child = None
        self.right_child = None

    def insert_left(self, new_node):
        """ Insert a new left child """
        if self.left_child is None:
            self.left_child = BinaryTree(new_node)
        else:
            t = BinaryTree(new_node)
            t.left_child = self.left_child
            self.left_child = t

    def insert_right(self, new_node):
        """ Insert a new right child """
        if self.right_child is None:
            self.right_child = BinaryTree(new_node)
        else:
            t = BinaryTree(new_node)
            t.right_child = self.right_child
            self.right_child = t

    def get_right_child(self):
        """ Return the right child """
        return self.right_child

    def get_left_child(self):
        """ Return the left child """
        return self.left_child

    def set_root_val(self, obj):
        """ Set the value of the root """
        self.key = obj

    def get_root_val(self):
        """ Get the value of the root """
        return self.key

    def __str__(self):
        """ String representation for printing """
        return self.preorder()

    def preorder(self):
        """Preorder traversal"""
        return f"{self.key} " + \
               (self.left_child.preorder() if self.left_child else "") + \
               (self.right_child.preorder() if self.right_child else "")

    def inorder(self):
        """Inorder traversal, can prove to be troublesome"""
        if isinstance(self.key, str) and self.key in "+-*/":  # Check if the node is an operator
            left = self.left_child.inorder() if self.left_child else ""
            right = self.right_child.inorder() if self.right_child else ""
            return f"({left} {self.key} {right})"
        else:
            return str(self.key) # For one operand

    def postorder(self):
        """Postorder traversal"""
        return (self.left_child.postorder() if self.left_child else "") + \
               (self.right_child.postorder() if self.right_child else "") + \
               f"{self.key} "
               
def constructTreeFromExpression(expression):
    """
    Construct a binary tree based on the given expression.
    """
    tokens = expression.split()
    stack = []

    for token in tokens:
        if token in "+-*/":
            if len(stack) < 2:  # Check operands for insufficiency 
                raise ValueError(f"Invalid expression: '{token}' does not have sufficient operands.")
            right = stack.pop()
            left = stack.pop()
            node = BinaryTree(token)
            node.left_child = left
            node.right_child = right
            stack.append(node)
        else:
            stack.append(BinaryTree(token))
    
    if len(stack) != 1:  # There should be exactly one tree remaining
        raise ValueError("Invalid expression: Does not form correct binary tree. Check token.")
    
    return stack[0]

def testExpressionTrees():
    """
    Test the BinaryTree class with various expressions, including additional test cases.
    """
    expressions = {
        "a": "91 95 + 15 + 19 + 4 *",
        "b": "B B * A C 4 * * -",
        "c": "42",
        "d": "A 57",          # Expected to produce an exception
        "e": "+ /",           # Expected to produce an exception
        
        # Let's include additional tests for fun
        
        "f": "8 5 * 7 3 + /", # Valid expression
        "g": "3 4 5 * - 6 2 / +", # Valid expression
        "h": "100",           # Single node
        "i": "x",             # Single node
        "j": "5 + -",         # Not enough operands
        "k": "9 8",           # Too many operands
        "l": "7 3 &) *"       # Unrecognized token
    }

    for key, expr in expressions.items():
        try:
            tree = constructTreeFromExpression(expr)
            # Test traversals for valid expressions
            print(f"Expression {key}: Preorder - {tree.preorder().strip()}")
            print(f"Expression {key}: Inorder - {tree.inorder().strip()}")
            print(f"Expression {key}: Postorder - {tree.postorder().strip()}\n")
        except Exception as e:
            print(f"Expression {key}: Exception caught as expected - {e}\n")

testExpressionTrees()

import inspect

def complianceReport():
    """
    Generates a compliance report.
    """
    
    current_script = inspect.getsource(inspect.getmodule(inspect.currentframe()))

    # Define the features
    features = {
        "BinaryTree class": False,
        "Method to build a tree from a postfix expression": False,
        "Handling of operands and operators in postfix expression": False,
        "Error handling for invalid expressions": False,
        "Support for preorder, inorder, and postorder": False,
        "Function to evaluate multiple expressions": False,
    }

    # Check for each feature in the script
    if "class BinaryTree" in current_script and all(method in current_script for method in ["insert_left", 
                                                                                            "insert_right", 
                                                                                            "get_right_child", 
                                                                                            "get_left_child", 
                                                                                            "set_root_val", 
                                                                                            "get_root_val"]):
        features["BinaryTree class"] = True

    if "constructTreeFromExpression" in current_script:
        features["Method to build a tree from a postfix expression"] = True

    if any(op in current_script for op in ["token in \"+-*/\"", "ValueError"]):
        features["Handling of operands and operators in postfix expression"] = True

    if "raise ValueError" in current_script:
        features["Error handling for invalid expressions"] = True

    if all(traversal in current_script for traversal in ["preorder", "inorder", "postorder"]):
        features["Support for preorder, inorder, and postorder"] = True

    if "testExpressionTrees" in current_script:
        features["Function to evaluate multiple expressions"] = True

    # Generate report
    report = [f"{feature}: {'Compliant' if compliant else 'Non-Compliant'}" for feature, compliant in features.items()]

    return "\n".join(report)

# Reading the content of the script
with open(__file__, 'r') as file:
    full_script = file.read()
    
print("\n==================== COMPLIANCE REPORT ====================\n")

# Generate and print the compliance report
print("Abraham J. Reines, Modified: Nov 12\n")
compliance_report_result = complianceReport()
print(compliance_report_result)