+++
date = '2024-11-26T14:20:53-05:00'
draft = false
title = "Visualizing Conway's Game of Life with Raylib"
showtoc = true
+++
# Introduction
[Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) was created by [John Horton Conway](https://en.wikipedia.org/wiki/John_Horton_Conway). The idea is simple: you have a grid of cells that can either be `alive` or `dead`. In every iteration, a new grid is made from the current grid by following a set of rules based on a cell's neighbors. Since this is a grid, there are 8 possible neighbors when diagonals are included. The rules are the following:

1. Any live cell with less than two neighbors dies.
2. Any live cell with two or three neighbors stays alive.
3. Any live cell with more than three neighbors dies.
4. Any dead cell with three live neighbors becomes a live cell.

The rules are simple, but the [results can be mesmerizing](https://youtu.be/C2vgICfQawE?si=o7ODSCIxiCeaPBy5&t=104). However, there are more reasons to care about Conway's Game of Life than the fact that it is nice to look at. For example, it has been shown that a [turing machine](https://en.wikipedia.org/wiki/Turing_machine#:~:text=A%20Turing%20machine%20is%20a,A%20physical%20Turing%20machine%20model.) can be [simulated with it](https://www.nicolasloizeau.com/gol-computer). It is also proof of how seemingly incredibly complex phenomena can appear from straightforward rules. 

However, for this blog post, we only care about the results looking nice.

# Goal

![](/images/raylib/conway.gif)

The goal is to code Conway's Game of Life in C++ and visualize it with [raylib](https://www.raylib.com/). Why raylib? Great question, but I don't have a great answer. Any library that allows the programmer to draw rectangles would have worked fine. I chose raylib for this particular project because I wanted to try it out, and I knew that it could be compiled to [WASM](https://en.wikipedia.org/wiki/WebAssembly) for a web build with [emscripten](https://github.com/emscripten-core/emscripten). 

If you want to see the web version of the final product, you can see it [here](https://bi3mer.github.io/raylib_tests/conways_game_of_life/).

# Implementing Conway's Game of Life

To start implementing Conway's Game of Life (CGoL), randomly initialize a matrix with true or false values.

```c++
// matrix
const std::size_t N = 100;
bool curState[N][N]; 

// set up random number generator
std::default_random_engine generator;
generator.seed(time(NULL));
std::uniform_real_distribution<float> distribution(0.0, 1.0);

// populate the matrix
for (std::size_t y = 0; y < N; ++y) {
    for (std::size_t x = 0; x < N; ++x) {
        curState[y][x] = distribution(generator) >= 0.5f;
    }
}
```

The state needs to be updated for every iteration. A common mistake in implementations of CGoL is to loop through `curState` and update values in `curState`. The correct implementation is to update a new matrix. If you update `curState`, then the live neighbor counts for each cell are incorrect. 

```c++
// list of all neighbors
const std::pair<int, int> NEIGHBORS[] = {
    {-1,-1},{-1,0},{-1,1},{0,-1},
    {0,1},{1,-1},{1,0},{1,1}
};

// matrix to update to
bool nextState[N][N]; 

// loop through matrix
for(int y = 0; y < N; ++y) {
    for (int x = 0; x < N; ++x) {
        // count neighbors
        int liveNeighbors = 0;
        for (auto& n : NEIGHBORS) {
            const int nx = x + n.first;
            const int ny = y + n.second;

            if (nx >= 0 && nx < N && ny >= 0 && ny < N) {
                liveNeighbors += curState[ny][nx];
            }
        }

        // rules 1-4 simplified
        if (curState[y][x]) {
            nextState[y][x] = (liveNeighbors == 2 || liveNeighbors == 3);
        } else {
            nextState[y][x] = (liveNeighbors == 3);
        }
    }
}
```
Here are a few notes for the above implementation that may be helpful:

- `NEIGHBORS` has the neighbors in all 8 directions.
- The new matrix is called as `nextState`. 
- Counting the neighbors requires a bounds check for the new `x` and `y` coordinates. Otherwise, the coordinates can be less than zero or greater than the size of the matrix.

This is all you need to implement one iteration of CGoL. If you want to run more, you need to update `curState` to the current value of `nextState`. You can do this by running two loops. Or you can be a bit more clever. The full implementation below tries to do the latter. It uses [`std::swap`](https://en.cppreference.com/w/cpp/algorithm/swap) to swap the matrices; memory is constant, and the swap is much more efficient. 

```c++
#pragma once

#include <cstddef>
#include <random>

const std::pair<int, int> NEIGHBORS[] = {
    {-1,-1},{-1,0},{-1,1},{0,-1},
    {0,1},{1,-1},{1,0},{1,1}
};

template <std::size_t N>
class Conway {
public:
    Conway() {
        // create random matrix for Conway's game of life
        std::default_random_engine generator;
        generator.seed(time(NULL));
        std::uniform_real_distribution<float> distribution(0.0, 1.0);

        for (std::size_t y = 0; y < N; ++y) {
            for (std::size_t x = 0; x < N; ++x) {
                curState[y][x] = distribution(generator) >= 0.5f;
            }
        }
    };

    void step() {
        for(int y = 0; y < N; ++y) {
            for (int x = 0; x < N; ++x) {
                int liveNeighbors = 0;
                for (auto& n : NEIGHBORS) {
                    const int nx = x + n.first;
                    const int ny = y + n.second;

                    if (nx >= 0 && nx < N && ny >= 0 && ny < N) {
                        liveNeighbors += curState[ny][nx];
                    }
                }

                if (curState[y][x]) {
                    nextState[y][x] = (liveNeighbors == 2 || liveNeighbors == 3);
                } else {
                    nextState[y][x] = (liveNeighbors == 3);
                }
            }
        }

        std::swap(curState, nextState);
    };

    const bool cellIsActive(const std::size_t row, const std::size_t col) const {
        return curState[row][col];
    };

private:
    bool curState[N][N];
    bool nextState[N][N];
};
```

All this should go into a header file. The name I went with is `conway.hpp`. 

# Visualizing with Raylib

```c++
typedef struct State {
    float time;
    Conway<GRID_SIZE> conway;
} State;
```

The `State` struct is going to be passed to two functions (`update` and `render`). Hopefully, `Conway` makes sense, but `time` may not. `time` will be explained in a little bit, so for now, ignore it. Instead, let's focus on rendering the the alive cells. 

```c++
void render(const State& state) {
    // screen dimensions
    const float W = (float) GetScreenWidth();
    const float H = (float) GetScreenHeight();

    // Figure out where the grid should be drawn based on the dimensions
    const float min = std::min(H, W); 
    const float grid_length = 0.8f* min;
     
    float startX;
    float startY;

    if (H > W) {
        startX = 0.1f*min;
        startY = (H - grid_length) / 2;
    } else {
        startY = 0.1f*min;
        startX = (W - grid_length) / 2;
    }

    // Calculate size of a grid cell
    const float cell_dimension = grid_length / GRID_SIZE;
    
    // Draw the grid
    ClearBackground(BLACK);

    for(std::size_t y = 0; y < GRID_SIZE; ++y) {
        float y_pos = startY + y*cell_dimension;
        for(std::size_t x = 0; x < GRID_SIZE; ++x) {
            if (state.conway.cellIsActive(y, x)) {
                DrawRectangle(
                    startX + x*cell_dimension, 
                    y_pos, 
                    cell_dimension - 1, // we don't want cells connecting
                    cell_dimension - 1, 
                    RED
                );
            }
        }
    }
}
```

This function is doing two things. At the top, it figures out where to draw a square grid on the screen based on the dimensions. It uses `GetScreenWidth` and `GetScreenHeight` to get the screen's dimensions. Then, it finds which is smaller and uses that. The grid should only take 80% of the minimum screen dimension; this way, there is space. I found 80% by playing around with the number until I found something that I thought looked best. After, it defines the start coordinates for `x` and `y`. Finally, it finds the cell dimension, which results in rendering squares that fit the designated screen space. (I tried allowing for rectangles, but it looked terrible.)

Next, `render` draws the grid. It starts by clearing the whole screen. Then, it iterates through the grid, which is `curState`. The definition for `cellIsActive` is above. If the cell is active, it is drawn. One is subtracted from both dimensions so that the drawn squares don't connect. Again, this just came down to preference. I thought that the separation made for a better-looking visualization. The same reason is why I went with `RED` and not `GREEN` or some custom color. 

```c++
void update(State& state) {
    state.time += GetFrameTime();

    if (state.time > 0.075f) {
        state.time = 0;
        state.conway.step();
    }
}
```

Now that we can draw the grid, the next problem is to `update` it. This is where `time` comes into play. A valid implementation would be to run `state.conway.step()` every frame. However, doing this makes for an incredibly busy and hard-to-understand visualization. As a result, I put in a delay before `step` could be run. The number I found that worked for me was `0.075`. 

The delay works by using `GetFrameTime`, which returns the time between frames. When the total time is greater than `0.075`, `time` is reset to `0`, and the `step` function for CGoL is run. 

# Conclusion
I have not shown the complete code for running this visualization, nor have I given you any directions on compiling it. To do so, you can go to the [GitHub repo](https://github.com/bi3mer/raylib_tests/tree/main/conways_game_of_life). It has a [makefile](https://en.wikipedia.org/wiki/Make_(software)) for compiling the code either for local use or for running in your browser. It also has the complete [`main.cpp`](https://github.com/bi3mer/raylib_tests/blob/main/conways_game_of_life/src/main.cpp) file. You can see one way to structure your code for local and WASM development. 

Regardless, this is the end of the post. I have shown one way to implement Conway's Game of Life in C++ and then how to visualize it with raylib. For anyone out there reading this post, I hope that it helped. If you find any mistakes, please let me know.