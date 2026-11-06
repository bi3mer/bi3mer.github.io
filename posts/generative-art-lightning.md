+++
date = '2021-12-12T19:33:54-05:00'
draft = false
title = 'Generative Art: Lightning'
+++
In the [previous post](../generative-art-circles-and-squares), we generated images with circles and squares in Python with the package [Pillow](https://pillow.readthedocs.io/en/stable/). The code was simple and the results are not that compelling. So, in this post I'm looking to step it up a bit. A while back [Numberphile](https://www.youtube.com/watch?v=akZ8JJ4gGLs) posted a video of [Matt Henderson](https://x.com/matthen2) explaining how maze generation and breadth-first search can be used to generate a compelling animation of lightning. We are going to use a similar approach to generate images of lightning.

|  |  |
|--|--|
| ![](/images/genart/lightning_0.png) | ![](/images/genart/lightning_1.png) |
| ![](/images/genart/lightning_2.png) | ![](/images/genart/lightning_3.png) |

We're taking a different approach from Henderson's to generate lightning, but I have a few suggestions if you want to recreate Henderson's work. For those interested in maze generation, Wikipedia has a stellar [article](https://en.wikipedia.org/wiki/Maze_generation_algorithm) that is an excellent starting point. Breadth-first search also has a very good Wikipedia [article](https://en.wikipedia.org/wiki/Breadth-first_search), but I would recommend looking at the [post](https://www.redblobgames.com/pathfinding/a-star/introduction.html) from the blog Red Blob Games, which has code and excellent animations with an interactive demo.

When I started considering how to approach generating a lightning-like image, I initially was going to implement maze generation (probably with Kruskal's algorithm) and a breadth-first search, but it seemed like a lot of work for a blog no one reads. So, how can I do the same thing with less work? Well, the maze and the search are not actually required. They make a beautiful animation, but you can get around it if you're only generating the final image.

The idea of the approach is essentially a depth-first search where we randomly choose directions (down, left, right). However, if we are currently moving to the left then we cannot move to the right. Only once we have gone down at least once can we move again to the right. And that's it. Add some bounds checking and you get the images above. The code to generate these images is below.

```python
from random import randrange, seed, randint, random, choice
from PIL import Image, ImageDraw, ImageFont

PIXEL_SIZE = 2
TOTAL_RUNS = 50
font = ImageFont.truetype("ProzaLibre-Medium.ttf", size=16)


def draw_lightning(run_id):
    image = Image.new('RGB', (720, 480))
    draw_image = ImageDraw.Draw(image)
    width, height = image.size
    x = randrange(100, width-100)
    y = 0

    LEFT = (-PIXEL_SIZE, 0)
    RIGHT = (PIXEL_SIZE, 0)
    DOWN = (0, PIXEL_SIZE)
    
    turned_right = False
    turned_left = False

    fill=(
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
        255
    )

    draw_image.rectangle(
        [(x, y),(x + PIXEL_SIZE, y + PIXEL_SIZE)],
        fill)

    while y < height:
        if turned_left:
            direction = choice([LEFT, DOWN])
            if direction != LEFT:
                turned_left = False
        elif turned_right:
            direction = choice([RIGHT, DOWN])
            if direction != RIGHT:
                turned_right = False
        else:
            direction = choice([LEFT, RIGHT, DOWN])
            if direction == LEFT:
                turned_left = True
            elif direction == RIGHT:
                turned_right = True

        x += direction[0]
        y += direction[1]

        if x < 20:
            x = 20
        elif x > width - 20:
            x = width - 20
        else:
            draw_image.rectangle(
                [(x, y),(x + PIXEL_SIZE, y + PIXEL_SIZE)],
                fill)


    draw_image.text((width-200,height-32), f'bi3mer :: 0003 :: {run_id + 1}/{TOTAL_RUNS}', (255,255,255), align='right', font=font)
    image.save(f'./output/0002_{run_id}.png')

for run_id in range(TOTAL_RUNS):
    seed(run_id)

    print(f'Processing run_id: {run_id}')
    draw_lightning(run_id)
```

Thanks for reading (if you did), and I hope you enjoyed the post.