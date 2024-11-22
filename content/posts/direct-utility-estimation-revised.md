+++
date = '2022-01-25T20:03:25-05:00'
draft = false
title = 'Revised Direct Utility Estimation For Better MDP'
+++

In the [previous post](../direct-utility-estimation), I provided an implementation that was technically correct but lacking in two ways: (1) optimization and (2) formalism. The optimization was weak, because I was using the function `game.next_states()` which was computing the next possible states given a state. Instead, precompute all valid transitions and your code will be much more efficient. This also leads to formalism where I had a MDP but I never directly defined the set of actions or transitions. So, let's do that.

```python
def action_to_tuple(action):
    if action == Action.LEFT:
        return Position(-1, 0)
    elif action == Action.RIGHT:
        return Position(1,0)
    elif action == Action.UP:
        return Position(0,1)
    elif action == Action.DOWN:
        return Position(0,-1)
    
    raise ValueError(f'Unregistered action type: {action}')

MAX_X = 4
MAX_Y = 3
BLANK_STATE = Position(1,1)
START = Position(0,0)   

S = [Position(x, y) for y in range(3) for x in range(4)]
A = [Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN]
P = {}
R = {}

for s in S:
    # slight movement penalty
    R[s] = -0.04 

    # probability for actions
    P[s] = {}
    for a in A:
        new_s = add_pos(s, action_to_tuple(a))  

        if new_s != BLANK_STATE and new_s.x >= 0 and new_s.x < MAX_X and new_s.y >= 0 and new_s.y < MAX_Y:
            P[s][new_s] = 1
        else:
            P[s][new_s] = 0

WIN_STATE = Position(3,2)
LOSE_STATE = Position(3,1)
R[Position(3,1)] = -1
R[Position(3,2)] = 1

E = [Position(3,1), Position(3,2)] # End states
```

Now, we can do `reinforcment_learning(S, A, P, R, E, START)` and direct utility estimation or any other solver will work. This change makes the code not only much faster, but also much more flexible. The updated code is available on [GitHub](https://github.com/bi3mer/ADP_Test/tree/4e4e5af40d5aff53fd55367709cff22e928c6c48). The impetus for this update was not only optimization and flexibility; in future posts, I'll be implementing policy iteration, value iteration, and q-learning. This update will make the implementation of those algorithms much simpler.