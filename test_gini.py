import unittest
from unittest import TestCase
from gini import gini, sample_pareto
from gini import gini_to_pareto_alpha, pareto_alpha_to_gini


class TestGini(TestCase):
    def test_gini_all_same(self):
        x = [1.0 for i in xrange(1000)]
        self.assertLess(gini(x), 0)

    def test_geni_one_has_all(self):
        x = [0.0 for i in xrange(1000)]
        x[0] = 1000.0
        self.assertGreater(gini(x), 0.99)

    def test_gini_uniform(self):
        a_list = [0.37, 2.6, 0.2]
        b_list = [1.89, 5.6, 0.2]
        tol = 1e-3
        num = 3000
        for a, b in zip(a_list, b_list):
            x = [a + (b-a)*(i/float(num)) for i in xrange(num)]
            g = gini(x)
            g_expected = (b-a)/(3.0*(b+a))
            self.assertLess(abs(g-g_expected), tol)


class TestSamplePareto(TestCase):
    def setUp(self):
        self.x_mode = 55
        self.alpha = 4.5
        self.num = 10000
        self.x = sample_pareto(self.num, self.x_mode, self.alpha, seed=42)

    def test_min(self):
        tol = 0.05
        self.assertEquals(len(self.x), self.num)
        self.assertTrue(self.x_mode <= min(self.x) < self.x_mode + tol)

    def test_mean(self):
        tol = 0.1
        expected = self.alpha*self.x_mode/(self.alpha-1.0)
        mean = sum(self.x)/float(self.num)
        print mean, expected
        self.assertLess(abs(expected - mean), tol)


class TestGiniPareto(TestCase):
    def test_inversion(self):
        alpha = 2.5
        gini_coeff = pareto_alpha_to_gini(alpha)
        alpha_calc = gini_to_pareto_alpha(gini_coeff)
        tol = 1e-9
        self.assertLess(abs(alpha - alpha_calc), tol)


if __name__ == "__main__":
    unittest.main()