+++
date = '2024-12-03T11:12:00-06:00'
draft = false
title = 'Visualizing Hilbert Curves With Raylib'
+++
In my most [recent post](../visualizing-conways-game-of-life-with-raylib/), I showed how to implement [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in C++ and visualize it with [raylib](https://www.raylib.com/). This post is of the same kind, except we are going to visualize [Hilbert Curves](https://en.wikipedia.org/wiki/Hilbert_curve) with raylib. However, this post will only have an example of the final result and the code.[^1] I am of the opinion that that the two sources below are of a high enough quality that I don't have anything more to add.

- If you want to know why you should care about Hilbert Curves, [3Blue1Brown (Grant Sanderson)](https://en.wikipedia.org/wiki/3Blue1Brown) has made an [awesome video](https://www.youtube.com/watch?v=3s7h2MHQtxc) on the topic.

- If you want an explanation on how it can be implemented, [The Coding Train](https://thecodingtrain.com/) has [video](https://www.youtube.com/watch?v=dSK-MW-zuAc) on the topic.[^2]

**Result**

![](/images/hilbert-curve.gif)


**Hilbert Curve Implementation**\
*Hilbert.hpp*
```c++
#pragma once

#include <stdio.h>
#include <raylib.h>
#include <raymath.h>

class Hilbert {
public:
    std::size_t N;

    Hilbert();
    Vector2 generate_next();
    bool is_done() const;
    void increase_order();
private:
    std::size_t order;
    std::size_t index;
    Vector2 last_pos;
    std::size_t max_size;
};
```

*Hilbert.cpp*
```c++
#include "Hilbert.hpp"

const Vector2 HILBERT_POSITIONS[] = {
    {0.0f, 0.0f},
    {0.0f, 1.0f},
    {1.0f, 1.0f},
    {1.0f, 0.0f}
};

Hilbert::Hilbert() {
    order = 1;
    N = pow(2, order);
    max_size = pow(N, 2);
    index = 1; // skip first, we know what it always is
    last_pos = HILBERT_POSITIONS[0];
}

Vector2 Hilbert::generate_next() {
    std::size_t i = index;
    std::size_t pos_index = i & 3;
    Vector2 pos = HILBERT_POSITIONS[pos_index];

    for (std::size_t j = 1; j < order; ++j) {
        i = i >> 2;
        pos_index = i & 3;
        const float length = pow(2, j);

        switch (pos_index) {
            case 0: {
                const float temp = pos.x;
                pos.x = pos.y;
                pos.y = temp;
                break;
            }
            case 1: {
                pos.y += length;
                break;
            }
            case 2: {
                pos.x += length;
                pos.y += length;
                break;
            }
            case 3: {
                const float temp = length - 1.0f - pos.x;
                pos.x = length + length - 1.0f - pos.y;
                pos.y = temp;
                break;
            }
            default: {
                printf("Unhandled index value: %zu\n", pos_index);
                exit(1);
                break;
            }
        }
    }

    ++index;

    return pos;
}

bool Hilbert::is_done() const {
    return index >= max_size;
}

void Hilbert::increase_order() {
    ++order;
    N = pow(2, order);
    max_size = pow(N, 2);
    index = 1; // skip first, we know what it always is
    last_pos = HILBERT_POSITIONS[0];
}
```

**Visualization Code**
```c++
void update(State& state) {
    const float dt = GetFrameTime();

    switch(state.state) {
        case HilbertState::HILBERT: {
            if(state.hilbert.is_done()) {
                state.state = HilbertState::PAUSE;
            } else {
                state.points.push_back(state.hilbert.generate_next());
            }

            break;
        }
        case HilbertState::PAUSE: {
            state.time += dt;
            if (state.time > 1.0f) {
                state.time = 0.0f;
                state.state = HilbertState::HILBERT;
                state.hilbert.increase_order();

                state.points.clear();
                state.points.push_back(HILBERT_POSITIONS[0]);
            }

            break;
        }
        default: {
            printf("Unhandled state type: %d\n", (int) state.state);
            exit(1);
        }
    }
}

void render(const State& state) {
    ClearBackground(BLACK);

    const float W = GetScreenWidth();
    const float H = GetScreenHeight();

    const float x_length = W / (float) state.hilbert.N;
    const float y_length = H / (float) state.hilbert.N;

    Vector2 p = state.points[0];
    Vector2 last_point = {
        p.x * x_length + x_length / 2.0f,
        p.y * y_length + y_length / 2.0f
    };

    for (std::size_t i = 1; i < state.points.size(); ++i) {
        p = state.points[i];
        const float x = p.x * x_length + x_length/2.0f;
        const float y = p.y * y_length + y_length/2.0f;

        DrawLineEx({x ,y}, last_point, 2, RED);

        last_point.x = x;
        last_point.y = y;
    }
}
```



[^1]: Full source code available on [GitHub](https://github.com/bi3mer/raylib_tests/tree/main/hilbert_curves).
[^2]: The video references a blog post that can no longer be reached due to the domain no longer being owned. I have since found a [GitHub repository](https://github.com/marcin-chwedczuk/hilbert_curve) written by Marcin Chwedczuk, who wrote the blog post.
