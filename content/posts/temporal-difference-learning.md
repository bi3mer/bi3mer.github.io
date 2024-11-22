+++
date = '2022-02-01T20:10:43-05:00'
draft = false
title = 'Temporal Difference Learning'
+++
This post is on temporal difference learning (TDL). TDL does not rely on a a Markov Decision Process (MDP). Instead, it traditionally uses a table where each state has a row and column so that the table represents the utility of all possible transitions. TDL uses observations to learn which transitions are valid.

\[
\begin{align}
U^{\pi}(s) \leftarrow U^{\pi} + \alpha (R(s) + \gamma U^{\pi}(s') - U^{\pi}(s))
\end{align}
\]

This is a very similar to the Bellman equation that we've seen in the past posts, but we aren't using neighbors because temporal difference learning does not assume a model. Instead, an agent plays through the game, and returns a set of states that were taken along the path. So, the utility of a state `s` is determined by itself plus the reward of that state plus the utility of the state next in the path minus its own utility all multiplied by a learning rate alpha, which is typically a small number between 0 and 1.

```python
def train(self, max_iterations):
    GAMMA = 0.9

    N = {}
    for s in self.S:
        N[s] = 1

    for _ in range(max_iterations):
        states, reward = self.play_through()
        if states == None:
            continue

        for i in range(len(states) - 1):
            s = states[i]
            s_p = states[i + 1]
            r_p = reward[i + 1]

            N[s] += 1
            self.U[s] += (60.0/(59 + N[s]))*(r_p + GAMMA*self.U[s_p] - self.U[s])
```

TDL is a two step algorithm, which is run for `k` iterations: (1) play through and (2) update the utility table. Not that complicated. One addition, you'll notice, is that I'm not using a fixed learning rate alpha. Instead, I use `N` to keep track of how many times a state has been visited. The first time the state has been seen, the weight is (60/59+1)=1. The second time it is 60/61, and then 60/62, and then 60/63, and so on. The result is that the weight of the state slowly gets smaller and smaller to improve the likelihood of convergence the longer the algorithm runs. On the topic of convergence, one issue with TDL is that there does not appear to be a nice stopping criteria like with Policy Iteration, and instead the algorithm just stops after some number of iterations.

When TDL runs on 4x3 grid world, it consistently finds solutions after 20 iterations, but there are rare occasions where it does fail. Meaning, it is is better to overestimate the minimum number of iterations when running TDL. More interesting is a problem when you increase the size of the grid in grid world. As we saw before, this results in a larger number of iterations for policy and value iterations, but both algorithms do not rely on a play through like TDL. On larger grids, we start with a random policy, which means we have to luck into a solution at the start. By the time we get to an 8x8 grid, this becomes very unlikely and TDL fails even at 10,000 iterations of the random agent trying to find a solution.

I hope you enjoyed this post. You can find the code on [GitHub](https://github.com/bi3mer/ADP_Test/tree/87b965f0abe5165195f72dc08c5d2e94db751189).