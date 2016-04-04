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


def sample_pareto(n_samples, x_mode, alpha, seed=None, use_random=False):
    """
    Sample from the pareto distribution
    :param n_samples: number of samples
    :param x_mode: The scale parameter, also the mode
    :param alpha: shape parameter
    :param use_random: if true, uses a random dist
            versus a true uniform distribution (default False)
    :param seed: random seed, default None (only used
            if use_random is True)
    :return:
    """
    if alpha <= 1.0:
        raise ValueError
    random.seed(seed)
    alpha_inv = 1.0/alpha
    if use_random:
        # use a random sample
        uniform = [1.0-random.random() for i in xrange(n_samples)]
    else:
        # use a true uniform distribution rather than random sample
        uniform = [1.0-float(i)/n_samples for i in xrange(n_samples)]
    return [x_mode/(u**alpha_inv) for u in uniform]


def pareto_alpha_to_gini(alpha):
    """
    Compute Geni coefficient from Pareto alpha param
    :param alpha: pareto shape parameter
    :return: the gini coefficient for this distribution
    """
    if alpha <= 1.0:
        raise ValueError
    return 1.0/(2.0*alpha - 1.0)


def gini_to_pareto_alpha(gini_coeff):
    """
    Compute Pareto alpha param from Geni coefficient
    :param gini_coeff: gini coeff
    :return: the pareto shape parameter
    """
    return 0.5*(1.0 + 1.0/gini_coeff)


def gini_after_action(gini_coeff_before, n_population, n_affected,
                      percentile_before, income_increase, seed=42,
                      do_plot=False):
    """
    See how the Gini coefficient changes if you take some
    segment of the population and make them richer/poorer
    :param gini_coeff_before: initial gini coefficient
    :param n_population: size of population
    :param n_affected: number of people affected
    :param percentile_before: percentile of income at start
    :param income_increase: multiplicative factor of increase of income
    :return:
    """

    pop_max = 1e7
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

    if do_plot:
        from matplotlib import pylab as plt
        plt.clf()
        income_max = 1000
        income_cut = [i for i in income if i < income_max]
        income_adjusted_cut = [i for i in income_adjusted if i < income_max]

        range = (0, 10)
        n_bins = 200
        plt.hist(income_cut, n_bins, alpha=0.3, range=range, label="Before")
        plt.hist(income_adjusted_cut, n_bins, alpha=0.3, range=range, label="After")
    return gini_before, gini_after


