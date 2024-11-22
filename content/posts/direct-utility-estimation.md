+++
date = '2022-01-20T19:48:18-05:00'
draft = false
title = 'Direct Utility Estimation'
+++
In this post, I'm going to take you through one approach to solving the grid world environment with reinforcement learning, specifically direct utility estimation (DUE). (If you are unfamiliar with the grid world environment, fret not because that is the section directly below.) Before DUE can be covered, I'll give a brief overview of Markov decision processes and why they are not of great for problems with large state spaces. I'll then show how DUE works and can be implemented in Python. Following that, I'll show that DUE can solve MDPs, but the speed is low enough that a DUE is best seen as introduction for more powerful approaches.

# Grid World

| | | | |
|---|---|---|---|
| . | . | . | 1 |
| . | X | . |-1 |
| S | . | . | . |

The grid world is a 4x3 grid seen above. `S` is where the player starts in the grid world. `.` grid locations are places where the player can move to if neighboring. At the start, the player can either move up one square or to the right one square. The `X` spot at (1,1) cannot be transitioned to. -1 and 1 are the locations where the player can finish their run at, where the reward for 1 is 1 and -1 is -1; the agent wants to get to the positive reward.

# Markov Decision Process
While working on a research project, I was asked to make a [short video](https://www.youtube.com/watch?v=05Ozahj7WsQ&embeds_referring_euri=https%3A%2F%2Fbi3mer.github.io%2F&source_ve_path=Mjg2NjY) on Markov decision processes (MDP) that may be helpful for you. It goes a bit beyond the scope of what we're covering in this blog post, but I do want to reiterate some of the basics. A MDP is made up of a set of states `S`, a set of actions `A`, a set of probabilities `P` that action `a` from state `s` will result in state `s'` at time `t`, and a set of rewards `R` given for transition from state `s` to state `s'`. Finally, `π` represents a policy for mapping a state to an action, and `π*` is the optimal policy.

The problem with MDPs and attempting to find an optimal policy is that it can be costly in terms of required computation and memory. Take the example of chess where there is an estimated upper bound of 7.7*10^45 possible board states, all of which have to be represented in the MDP, which is physically impossible; further, attempting to find an optimal policy on such a large state space is computationally impossible. Despite this flaw, MDPs are a great tool for small- to medium-sized problems and can be of [great utility](https://stats.stackexchange.com/questions/145122/real-life-examples-of-markov-decision-processes/178393#178393).

# Direct Utility Estimation
Direct utility estimation (DUE) comes from Woodrow and Hoff in their paper [Adaptive Switching Coordinates](https://apps.dtic.mil/sti/pdfs/AD0241531.pdf) in 1960. The idea is very simple: the utility of a state is the expected total reward from that state onward.

\[
\begin{align}
U^*(s) = E \left[ \sum_{t=0}^{\infty} \gamma R(s_t)\right]
\end{align}
\]

Practically speaking, the way you train with DUE is run an agent with your policy till you get to an end state. Then update all the states encountered with the reward.

```python
def train(self, max_iterations):
    for _ in trange(max_iterations):
        states, reward = play_through(self, self.game)
        for s in states:
            val = self.utility[s]
            self.utility[s] = Average(val.num + reward, val.div + 1)
```

The code here has a named tuple `Average` which lets you keep track of the total reward and also the number of times encountered to easily calculate the average. You'll also notice that I'm not using gamma, that is just because I have it as 1. Otherwise, this is the algorithm with one missing component.

```python
from math import inf
from random import random, choice

def play_through(agent, game, eps=0.1):
    game.new()
    states = [game.state]

    while game.reward() == 0:
        best_s = None
        best_u = -inf

        if random() < eps:
            best_s = choice(game.next_states())
            best_u = agent.u(best_s)
        else:
            for s in game.next_states():
                next_u = agent.u(s)
                if next_u > best_u:
                    best_u = next_u
                    best_s = s

        states.append(best_s)
        game.state = best_s

    return states, game.reward()
```

If you run a play through where the policy's best answer is always selected, then you can run into a local optima. By having a small epsilon, you guarantee that there is a chance that alternative paths are selected, and a better policy can be found. It has the added benefit of guaranteeing that small environments like grid world will eventually be solved, which is necessary since otherwise the training can get stuck. Without this, you have no guarantee that the optimal policy will be found; which is, surprisingly, guaranteed with DUE. The problem, though, is that this process can take a very long time, which is why other approaches like Adaptive Dynamic Programming are used instead since they explicitly optimize the [Bellman Equation](https://en.wikipedia.org/wiki/Bellman_equation). And to show this, let's look at DUE applied to the grid world for a select number of iterations.

**t = 100**
| | | | |
|---|---|---|---|
| 1.00 | 1.00 | 0.91 | 1 |
| 1.00 | X | 0.21 |-1 |
| 1.00 | 0.97 | 0.5 | -1.00 |

**t = 1,000**
| | | | |
|---|---|---|---|
| 0.99 | 1.00 | 0.94 | 1 |
| 0.92 | X | 0.71 |-1 |
| 0.93 | 0.93 | 0.93 | 0.82 |

**t = 10,000**
| | | | |
|---|---|---|---|
| 1.00 | 1.00 | 0.99 | 1 |
| 0.99 | X | 0.82 |-1 |
| 0.98 | 0.97 | 0.04 | -0.92 |

**t = 100,000**
| | | | |
|---|---|---|---|
| 0.96 | 0.99 | 1.00 | 1 |
| 0.96 | X | 0.91 |-1 |
| 0.96 | 0.96 | 0.95 | -0.82 |

Notice that at `t=100`, the agent will first go up, but then has fifty-fifty chance of going either up or down and can get stuck. At t=1,000, we now explicitly get stuck at the top left going back and forth between `0.99` and `1.00`. The same happens at `t=10,000`, except now we get stuck one cell closer to the final goal. It isn't until `t=100,000` that a successful policy is found for grid world. Imagine if we used a more complex game or just increased the grid size to 10x10. DUE may get to the optimal answer but it sure does take its time!

# Conclusion
In this blog post, we've covered grid world which is a common test environment for reinforcement learn algorithms, Markov Decision Processes, and Direct Utility Estimation. The full code is available on GitHub. We showed that DUE, while interesting and able to solve a problem like the grid world environment, is slow to converge and not well situated for modern problems. I plan to create a blog post in the near future, which will go over adaptive dynamic programming, and show how these approaches can solve the bellman equations quick enough to be of real use.

Thanks for reading (if you did), and I hope you enjoyed the post.


**EDIT 25/01/22:** In the [next post](../direct-utility-estimation-revised) I provide a better implementation of MDPs.