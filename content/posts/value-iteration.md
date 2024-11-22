+++
date = '2022-01-26T20:10:43-05:00'
draft = false
title = 'Value Iteration'
+++
In this post I'll be covering value iteration. To best understand why it works, I want to first cover the Bellman equation:

\[
\begin{align}
U(s) = R(s) + \gamma \max_{s \in S} \sum_{s'} P(s'|s, a)U(s')
\end{align}
\]

We've already covered R(s), P(s' | s, a), and U(s') so I won't waste your time on those in a [previous post](../direct-utility-estimation/#markov-decision-process). Gamma is a discount constant that is greater than 0 and less than or equal to 1. What this equation is saying is that the utility of state s is the reward plus a discount of the best neighboring state according to the transition probability multiplied by that states utility. Value iteration is the application of this formula over multiple iterations till convergence.

```python
def train(self, max_iterations):
    GAMMA = 0.75
    for i in trange(max_iterations):
        new_u = self.utility.copy()
        delta = 0

        for s in self.S:
            vals = [self.P[s][next_s] * self.utility[next_s] for next_s in self.P[s] if self.P[s][next_s] > 0]
            new_u[s] = self.R[s] + GAMMA * max(vals)
            delta = max(delta, abs(self.utility[s] - new_u[s]))

        self.utility = new_u
        if delta < self.theta:
            print(f'Stopped after {i} iterations')
            break
```

Apologies for that one line of code which runs a bit longer than I'd like. This code shows a python implementation of value iteration. There is a small optimization in this code which runs for every possible neighboring state rather than all states. Otherwise the code is essentially a direct translation of the formula. There is also a convergence check with delta and theta, where theta should be some small number and delta is the absolute value of the difference between the previous utility and the newly calculated utility. Once delta is smaller than theta after a full value iteration update, we stop iterations.

With that, we can look at how efficient this thing is, and it is pretty crazy when you compare to [Direct Utility Estimation](direct-utility-estimation/#direct-utility-estimation). Recall that DUE took about 100,000 iterations to find an optimal policy. I did slightly change the grid world problem so now R(s) is going to be -0.04 unless it is one of the end states, and this did not affect how long it took DUE to find the best result. That said, value iteration takes thirteen iterations! I've included the utility table below. I hope you enjoyed reading this post and the code can be found on [GitHub](https://github.com/bi3mer/ADP_Test/tree/9857949a05ec9ac64cae59365fb6b3bbeed0efb3).