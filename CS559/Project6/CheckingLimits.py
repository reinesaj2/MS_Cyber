"""
Author: Abraham Reines
Created: Mon Apr  1 12:55:40 PDT 2024
Modified: Wed Apr  3 13:29:07 PDT 2024
Name of file: CheckingLimits.py
"""

from sympy import symbols, limit, oo

n = symbols('n')
f = 10**12 * n**3 + 10**6 * n**2 + n + 1

def AsymptoteTime(f, g, n):
    """
    Analyze asymptote behavior of f(n) against g(n) using Big O, small o, and Omega
    
    Parameters:
    f (sympy expression): asymptotic f(n) should be analyzed
    g (sympy expression): g(n) comparison
    n (sympy symbol): variable with respect to limit computed
    """

    #  limit for conditions
    asymptoteLimit = limit(f/g, n, oo)

    #  Big O condition
    BigO = asymptoteLimit.is_finite
    BigO_result = "True" if BigO else "False"
    print(f"Big O: {BigO_result}, because the limit of f(n)/g(n) as n approaches infinity is {asymptoteLimit}, which is finite.")

    # small o condition
    SmallO = asymptoteLimit == 0
    SmallO_result = "True" if SmallO else "False"
    print(f"Small o: {SmallO_result}, because the limit of f(n)/g(n) as n approaches infinity is {asymptoteLimit}, which confirms f(n) grows slower than g(n).")

    # Omegas condition for inverse of limit
    OmegaLimit = limit(g/f, n, oo)
    omega = OmegaLimit == 0
    omega_result = "True" if omega else "False"
    print(f"Omega: {omega_result}, because the limit of g(n)/f(n) as n approaches infinity is {OmegaLimit}, which confirms f(n) does not grow as fast as g(n).")

# g(n) is n**4 for comparison
AsymptoteTime(f, n**4, n)