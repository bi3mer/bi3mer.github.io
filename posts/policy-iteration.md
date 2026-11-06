+++
date = '2022-01-31T20:10:43-05:00'
draft = false
title = 'Policy Iteration'
+++
In this post I'll be covering policy iteration. As a brief reminder, here is the bellman equation that value iteration optimizes:

\[
\begin{align}
U(s) = R(s) + \gamma \max_{s \in S} \sum_{s'} P(s'|s, a)U(s')
\end{align}
\]

In policy iteration, the goal is not to find the perfectly optimal utility of states like value iteration. If one state is clearly better than another, then the precise difference isn't that important. After all, we care most about an agent making the correct decisions. This idea is how we come to policy iteration, which is broken into two steps: (1) *policy evaluation* and (2) *policy improvement*. Before going into each of these ideas, I want to give you the pseudo-code for the algorithm.

```
loop
    policy_evaluation(policy, U, mdp)
    unchanged = policy_improvement(policy, U, mdp)
while unchanged is false
```

A policy defines the best action for a given state. It can be deterministic (only one action is ever selected for a given state s) or stochastic (actions have probabilities of being selected). In grid world, the environment is deterministic so it is best to use a deterministic policy. For policy iteration, we initialize a policy with random actions for each state.

```python
self.pi = {} 
for s in S:
    self.pi[s] = choice(list(self.P[s].keys()))
```

Policy evaluation is attempting to find the optimal policy for a problem and uses a modified Bellman equation that is run `k` times.

\[
\begin{align}
U(s) = R(s) + \gamma \max_{s \in S} \sum_{s'} P(s'|s, \pi(s))U(s')
\end{align}
\]

The utility of a state is determined by the policy. Since our policy deterministic, the utility of a state is calculated with only one neighbor. If the policy was stochastic, we would multiply each action by the probability of it being selected by the policy.

```python
# policy evaluation
for _ in range(K):
    for s in self.S:
        self.utility[s] = self.R[s] + self.P[s][self.pi[s]] * self.utility[self.pi[s]]
```

Next is policy improvement which is very simple. For every state `s`, we compare the utility of the action found by the policy to the best neighbor. If the utility of the policy is better than no changes are made to the policy. If, however, the policy does not match the utility table, we update the policy to select the better neighbor and we store that the algorithm has not yet converged. Note that policy improvement does not break out of the loop once a change to the policy has been found; all changes are run and the loop goes back up to policy improvement.

```python
unchanged = True
for s in self.S:
    old = self.pi[s]

    best_s = None
    best_u = -inf
    for s_p in self.P[s]:
        if self.utility[s_p] > best_u:
            best_s = s_p
            best_u = self.utility[s_p]

    if old != best_s:
        self.pi[s] = best_s
        unchanged = False
```

That is policy iteration, the code can be found on [https://github.com/bi3mer/ADP_Test/tree/d7c9a28c61ad8fbf7a0ec9295fed837d74a51c26], and now we can look at how the algorithm does.

Recall that value iteration converged after 13 iterations and this algorithm is taking 100, but that was due to the stopping criteria. In that example, I gave value iteration a theta of 0.03. If I increase the size of grid world to 10x10, then theta is large enough that value iteration fails to find a suitable solution. I have to give it `theta = 1e-10` for value iteration to work. and it takes 81 iterations. Policy iteration actually takes more iterations at 300, but it is faster in terms of time taken at 0.049 seconds compared to 0.056 seconds, which is in line with the common wisdom that policy iteration is quicker to converge. On the note of convergence, a problem I ran into with value iteration is that it eventually fails to find solutions given a large enough grid world. At a certain point, you can only make theta so small, whereas the policy approach had no such issue. Likely there are other convergence metrics you can use for value iteration, but I have not yet looked into them.

**EDIT 2021/02/03:** `self.utility[s] = self.R[s] + self.P[s][self.pi[s]] * self.utility[self.pi[s]]` should be `self.utility[s] = self.R[s] + GAMMA*self.P[s][self.pi[s]] * self.utility[self.pi[s]]`, which has gamma. Policy iteration converges after 80 iterations for 1e-13.