+++
date = '2022-02-22T20:10:43-05:00'
draft = false
title = 'Q-Learning and SARSA'
+++
In this post I'm going to be covering two active reinforcement learning methods: q-learning and SARSA. Both methods do not depend on an MDP. Meaning, we are not guaranteed the presence of `P`. Instead, we learn which actions can be taken in a state during playthroughs. This is represented by a q-table, which is a table of states and actions that yield a q-value, which represents expected utility when taking an action in a given state. We can say that the expected utility of a state is the best action associated with that state. See the equation below.

\[
U(s) = \max_a Q(s, a)
\]

In active reinforcement learning, we are updating the q-table after the agent makes a decision on the next move to make. To get the next move, you can use an epsilon greedy approach like in the code below or you can use the q-values in the q-table as weights for a probability-based selection. Note that a valid strategy is a greedy q-learning agent where only the `max_next` action selection strategy is used. This will method will converge quicker, but at the cost of likely finding a sub-optimal policy.

```python
def max_next(self, s):
    valid_choices = [new_s for new_s in self.Q[s]]
    best_s = None
    best_u = -inf

    for new_s in valid_choices:
        next_u = self.Q[s][new_s]
        if next_u > best_u:
            best_u = next_u
            best_s = new_s

    return best_s, best_u
    
def get_next(self, s, eps=0.05):
    if random() < eps:
        best_s = choice([new_s for new_s in self.Q[s]])
        best_q = self.Q[s][best_s]
    else:
        best_s, best_q = self.max_next(s)

    return best_s, best_q
```

With an action selected, we can update the q-table. We do this with the following equation:

\[
Q(s,a) \leftarrow Q(s,a) + \alpha(R(s) + \gamma \max_a (Q(s', a') - Q(s, a)))
\]

As you can see, there is a look ahead here. Given the current state and action to be taken, we say that its q-value is dependent on `s'` which is the result of taking action `a` in state `s`, where we find the optimal action to take in s' based on the q-table. This equation is almost exactly the same as what we saw in temporal difference learning.

```python
def train(self, max_iterations):
    GAMMA = 0.9

    N = {}
    for s in self.S:
        N[s] = 1

    for _ in trange(max_iterations):
        s = self.START
        while s not in self.E:
            N[s] += 1
            new_s, _ = self.get_next(s)

            ALPHA = (60.0/(59.0 + N[s]))
            self.Q[s][new_s] += ALPHA*(self.R[s] + GAMMA*self.u(new_s) - self.Q[s][new_s])
            s = new_s

        self.Q[s][0] = self.R[s]
```

That is q-learning in a nutshell, and now I'm going to turn my attention to SARSA which received its name for s,a,r,s',a. In SARSA, we use a very similar seeming equation.

\[
Q(s,a) \leftarrow Q(s,a) + \alpha(R(s) + \gamma Q(s', a') - Q(s, a))
\]

The difference is that in q-learning we don't use the best action in the environment but we do use it in calculating the q-value. In SARSA, we don't use the max value but we do take whatever action is selected. This is why q-learning is considered an off-policy algorithm and SARSA is on-policy: the calculation of the q-values is based on the policy. In a sense, SARSA is learning what will actually happen whereas q-learning will eventually learn to behave well regardless of the policy, which is why SARSA is the better choice when we care about performance while the agent is learning.

```python
def train(self, max_iterations):
    GAMMA = 0.9

    N = {}
    for s in self.S:
        N[s] = 1

    for _ in trange(max_iterations):
        self.reset()
        s = self.START
        s_1, _ = self.get_next(s)
        while s not in self.E:
            N[s] += 1
            s_2, _ = self.get_next(s_1)

            ALPHA = (60.0/(59.0 + N[s]))
            self.Q[s][s_1] += ALPHA*(self.R[s] + GAMMA*self.Q[s_1][s_2] - self.Q[s][s_1])

            s = s_1
            s_1 = s_2

        self.Q[s][0] = self.R[s]
```

Running both of these algorithms on GridWorld with a 20x20 grid, they were able to find a solution after about 600 full playthroughs the majority of the time. Q-learning was slower by about a tenth of a second on successful runs on these successful runs. This makes sense because once SARSA requires less computation since it doesn't compute `U(s,a)`.

I hope you enjoyed this post. You can find the code on [GitHub](https://github.com/bi3mer/ADP_Test/tree/978f51048ad055dabd7e37866159fb5d28b18452).