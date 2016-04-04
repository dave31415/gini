"""
    Gini coefficient
"""

import random


def gini(x):
    """
    Calculate Gini coefficient
    :param x: list of incomes (or anything)
    :return: Gini coefficient
    """
    n = float(len(x))
    x_sorted = sorted(x)
    total = float(sum(x))
    income_weighted_average_percentile = \
        sum([i*x_i/n for i, x_i in enumerate(x_sorted)])/total
    return 2*income_weighted_average_percentile - ((n+1)/n)


def sample_pareto(n_samples, x_mode, alpha, seed=None):
    """
    Sample from the pareto distribution
    :param n_samples: number of samples
    :param x_mode: The scale parameter, also the mode
    :param alpha: shape parameter
    :param seed: random seed, default None
    :return:
    """
    if alpha <= 1.0:
        raise ValueError
    random.seed(seed)
    alpha_inv = 1.0/alpha
    uniform = [1.0-random.random() for i in xrange(n_samples)]
    return [x_mode/(u**alpha_inv) for u in uniform]


def pareto_alpha_to_gini(alpha):
    """
    :param alpha: pareto shape parameter
    :return: the gini coefficient for this distribution
    """
    if alpha <= 1.0:
        raise ValueError
    return 1.0/(2.0*alpha - 1.0)


def gini_to_pareto_alpha(gini_coeff):
    """
    :param gini_coeff: gini coeff
    :return: the pareto shape parameter
    """
    return 0.5*(1.0 + 1.0/gini_coeff)


def gini_after_action(gini_coeff_before, n_population, n_affected,
                      percentile_before, income_increase, seed=42):
    """
    :param gini_coeff_before: initial gini coefficient
    :param n_population: size of population
    :param n_affected: number of people affected
    :param percentile_before: percentile of income at start
    :param income_increase: multiplicative factor of increase of income
    :return:
    """

    pop_max = 1e6
    if n_population > pop_max:
        # scale both numbers down to make it faster
        scale = pop_max/float(n_population)
        n_population = scale * n_population
        n_affected = scale * n_affected

    n_population = int(round(n_population))
    n_affected = int(round(n_affected))

    alpha = gini_to_pareto_alpha(gini_coeff_before)
    x_mode = 1.0
    income = sorted(sample_pareto(n_population, x_mode, alpha, seed=seed))
    index_middle = percentile_before*n_population
    index_start = index_middle - n_affected/2
    index_end = index_start + n_affected

    def adjust(i, inc):
        if i >= index_start and i < index_end:
            return income_increase*inc
        return inc

    income_adjusted = [adjust(i, inc) for i, inc in enumerate(income)]

    gini_before = gini(income)
    gini_after = gini(income_adjusted)
    tol = 1e-8
    if n_population > 10000:
        assert abs(gini_coeff_before - gini_coeff_before) < tol

    print 'gini before: %s' % gini_before
    print 'gini after: %s' % gini_after
    return gini_after, income, income_adjusted


