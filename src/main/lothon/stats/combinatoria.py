"""
   Package lothon.stats
   Module  combinatoria.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import itertools
import math

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# FUNCOES UTILITARIAS
# ----------------------------------------------------------------------------

def combina(n, r):
    # Number of combinations of 'n' elements for sets of size 'r'
    return (math.factorial(n) // math.factorial(r) // math.factorial(n-r)) if n - r >= 0 else 0


def rank(c):
    # Rank for C(60, 6). 'c' must be sorted.
    # https://en.wikipedia.org/wiki/Combinatorial_number_system
    return 50063860 - (combina(60 - c[0], 6) + combina(60 - c[1], 5) + combina(60 - c[2], 4) +
                       combina(60 - c[3], 3) + combina(60 - c[4], 2) + (60 - c[5]))


def partial_matches(s, n):
    # All winning combinations for 's' set with 'n' matches. 'n' must be less than 6.

    def new_set_with(st, x):
        result = set(st)
        result.update(x)
        return sorted(result)

    remainder = {x for x in range(1, 61) if x not in s}
    wrongs = [x for x in itertools.combinations(remainder, 6 - n)]
    rights = [x for x in itertools.combinations(s, n)]
    return [new_set_with(r, w) for r in rights for w in wrongs]


def all_combinations(s):
    # All combinations for 's' set with 6 elements. 's' must have at least 6 elements
    return [x for x in itertools.combinations(s, 6)]

# ----------------------------------------------------------------------------
