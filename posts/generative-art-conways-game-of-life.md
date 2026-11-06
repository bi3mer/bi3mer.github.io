+++
date = '2022-01-13T19:44:11-05:00'
draft = false
title = "Generative Art: Conway's Game of Life"
+++
With the [lightning algorithm](../generative-art-lightning) out of the way, let's look at [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). The idea is pretty cool: we create a grid (nxm), and randomly assign cells to alive or dead. We then apply a set of rules for some number of iterations and we get a very hard to predict result. The rules are pretty simple:

1. Any live cell with fewer than two live neighbors dies, as if by under-population.
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

|  |  |
|--|--|
| ![](/images/genart/conway_0.png) | ![](/images/genart/conway_1.png) |

It turns out that despite the relative fame of Conway's Game of Life, implementing it is very simple. I think that there are three points of note. First, you are checking not only the four cardinal directions, you are also checking the corners for a total of 8 cells. Second, Conway's Game of Life was designed for an infinite grid, but that is not feasible, nor useful is it useful in our case of generating images. In this implementation I've made the grid the size of the image. A better way would be to make the grid larger than the image to approximate the larger grid space. Third, the grid is not modified in place (i.e. a new grid is modified in each iteration, and the old grid is used to get neighbor counts).

```python
from random import randrange, seed, randint, choice
from PIL import Image, ImageDraw, ImageFont
from itertools import repeat

PIXEL_SIZE = 6
TOTAL_RUNS = 20
font = ImageFont.truetype("ProzaLibre-Medium.ttf", size=16)

def is_alive(grid, x, y, width, height):
    if not (x >= 0 and x < width and y >= 0 and y < height):
        return False

    return grid[y][x]

def draw_conway(run_id):
    image = Image.new('RGB', (720, 480))
    draw_image = ImageDraw.Draw(image)
    width, height = image.size

    grid_width = width // PIXEL_SIZE
    grid_height = height // PIXEL_SIZE

    alive_fill = (
        randint(100, 255),
        randint(100, 255),
        randint(100, 255),
        255
    )

    dead_fill = (
        randint(0, 40),
        randint(0, 40),
        randint(0, 40),
        255
    )

    current = [[choice([False, True]) for _ in repeat(None, grid_width)] for __ in repeat(None, grid_height)]

    for _ in repeat(None, randrange(10, 250)):
        new = [[False for _ in repeat(None, grid_width)] for __ in repeat(None, grid_height)]
        for y in range(grid_height):
            for x in range(grid_width):
                neighbors_alive = \
                    is_alive(current, x + 1, y, grid_width, grid_height) + \
                    is_alive(current, x - 1, y, grid_width, grid_height) + \
                    is_alive(current, x, y + 1, grid_width, grid_height) + \
                    is_alive(current, x, y - 1, grid_width, grid_height) + \
                    is_alive(current, x + 1, y + 1, grid_width, grid_height) + \
                    is_alive(current, x - 1, y + 1, grid_width, grid_height) + \
                    is_alive(current, x + 1, y - 1, grid_width, grid_height) + \
                    is_alive(current, x - 1, y - 1, grid_width, grid_height) 

                # Any live cell with fewer than two live neighbors dies, as if by underpopulation.
                if current[y][x] == True and neighbors_alive < 2:
                    new[y][x] = False
                # Any live cell with two or three live neighbors lives on to the next generation.
                elif current[y][x] == True and neighbors_alive == 2 or neighbors_alive == 3:
                    new[y][x] = True
                # Any live cell with more than three live neighbors dies, as if by overpopulation.
                elif current[y][x] == True and neighbors_alive > 3:
                    new[y][x] = False
                # Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
                elif current[y][x] == False and neighbors_alive == 3:
                    new[y][x] = True

        current = new
    
    for y in range(0, grid_height):
        for x in range(0, grid_width):
            if current[y][x]:
                draw_image.rectangle(
                    [(
                        x*PIXEL_SIZE, y*PIXEL_SIZE),
                        (x*PIXEL_SIZE + PIXEL_SIZE, y*PIXEL_SIZE + PIXEL_SIZE)],
                    alive_fill)
            else:
                draw_image.rectangle(
                    [(
                        x*PIXEL_SIZE, y*PIXEL_SIZE),
                        (x*PIXEL_SIZE + PIXEL_SIZE, y*PIXEL_SIZE + PIXEL_SIZE)],
                    dead_fill)

    draw_image.text((width-200,height-32), f'bi3mer :: 0004 :: {run_id + 1}/{TOTAL_RUNS}', (255,255,255), align='right', font=font)
    image.save(f'./output/0004_{run_id}.png')

for run_id in range(TOTAL_RUNS):
    seed(run_id)

    print(f'Processing run_id: {run_id}')
    draw_conway(run_id)
```

Thanks for reading (if you did), and I hope you enjoyed the post.