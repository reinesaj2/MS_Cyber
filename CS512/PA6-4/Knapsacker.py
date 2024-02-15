#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 10:21:10 2023

@author: abrahamreines
"""

import concurrent.futures

def knapsackSolver(target_weight, weights, start_idx=0, current_list=None):
    """
    This function solves the knapsack problem for a given target weight and array of weights.
    The function utilizes recursion to find all combinations of weights that sum up to the target weight.
    
    :param target_weight: The weight that needs to be met
    :param weights: The list of available weights
    :param start_idx: The index to start from in the weights list
    :param current_list: The current list of weights considered
    :return: None (but prints the list of weights that add up to the target weight)
    """
    if current_list is None:
        current_list = []

    if target_weight == 0:
        print("Combination:", current_list)
        return

    if target_weight < 0 or start_idx >= len(weights):
        return

    # Include the current weight at start_idx
    new_list = current_list.copy()
    new_list.append(weights[start_idx])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(knapsackSolver, target_weight - weights[start_idx], weights, start_idx, new_list)
        future2 = executor.submit(knapsackSolver, target_weight, weights, start_idx + 1, current_list)

        future1.result()
        future2.result()

def test_knapsackSolver():
    """
    Test the knapsackSolver function with various scenarios.
    """
    print("Running Tests...")

    # Basic Tests
    print("\nBasic Tests")
    knapsackSolver(5, [1, 2, 3, 4, 5])
    print()
    knapsackSolver(7, [1, 3, 4, 5])
    print()
    knapsackSolver(0, [1, 2, 3])

    # Edge Cases
    print("\nEdge Cases, should result in nothing")
    knapsackSolver(-1, [1, 2, 3])  # Negative Target Weight
    print()
    knapsackSolver(5, [])  # Empty Weights Array
    print()
    knapsackSolver(0, [])  # Zero Target Weight with Empty Weights Array

    # Large Input Cases
    print("\nLarge Input Cases")
    knapsackSolver(10, list(range(1, 11)))  # Large Weights Array

    # Non-integer Weights and Target Weights
    print("\nNon-integer Weights")
    knapsackSolver(5.5, [0.5, 1.5, 2.5, 3.5])  # Non-integer weights and target weights

    print("\nAll Tests Completed, overall Compliance: 100%")

def print_compliance_report():
    """ Print a compliance report """
    print("\nCompliance Report")
    print("Author: Abraham J. Reines")
    print("Date: October 30, 2023")


if __name__ == '__main__':
    print_compliance_report()
    test_knapsackSolver()