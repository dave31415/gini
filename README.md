# gini coefficent changes due to action

Example

A country has a Geni of 0.4 starting out

population is 1 million people

Some action is going to affect 10% of people who are poor

They are around the 10-th percentile before

The action is going to increase their income by 50%

Do this

python

import geni

gini_before = 0.4

pop = 1e6

n_affected = 1e5

perc_before = 0.1

increase = 1.5

geni_after = gini.gini_after_action(gini_before, pop, n_affected,
                      perc_before, increase, seed=42)
