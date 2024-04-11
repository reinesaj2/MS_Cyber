"""
Author: Abraham Reines
Created: Mon Apr  1 12:55:40 PDT 2024
Modified: Wed Apr 10 14:19:06 PDT 2024
Name of file: CheckingLimits.py
"""

from sympy import symbols, limit, oo

n = symbols('n')
f = 10**12 * n**3 + 10**6 * n**2 + n + 1
g = n**4

def AsymptoteTime(f, g, n):
    """
    Analyze asymptote behavior of f(n) against g(n) using Big O, small o, and Omega
    
    Parameters:
    f (sympy expression): asymptotic f(n) should be analyzed
    g (sympy expression): g(n) comparison
    n (sympy symbol): variable with respect to limit computed
    """
    analysis_results = {}

    # Calculate the limit for f(n)/g(n) as n approaches infinity
    limit_f_over_g = limit(f/g, n, oo)
    # Calculate the limit for g(n)/f(n) as n approaches infinity
    limit_g_over_f = limit(g/f, n, oo)

    # Big O condition: f(n) is O(g(n)) if limit of f(n)/g(n) is finite
    analysis_results['Big O'] = limit_f_over_g.is_finite

    # small o condition: f(n) is o(g(n)) if limit of f(n)/g(n) is zero
    analysis_results['Small o'] = limit_f_over_g == 0

    # Omega condition: f(n) is Ω(g(n)) if limit of f(n)/g(n) is infinite
    analysis_results['Omega'] = limit_f_over_g == oo

    return analysis_results

# g(n) is n**4 for comparison
results = AsymptoteTime(f, g, n)
print(results)