+++
date = '2018-06-17T13:59:57-05:00'
draft = false
title = 'Generative Design in Mineraft: Nuking the Ground'
+++
# A Quick Note
I ended up getting pretty sick and I was out of commission for about two months. The good news is that I’m now in perfectly good health. The bad news is that it kind of destroyed my hopes of building a decent submission for GDMC. The competition ends in about thirteen days which is not enough time to come up with a submission I would be proud of. In addition, my 40+ hours at the [Brain Game Center](https://braingamecenter.ucr.edu/), where I work, every week is the very large nail in the coffin. Regardless, I plan on continuing to work on this problem until I have something cool I can show off.

# Counting Materials In a Selection
The [last post](../gdmc1/) featured basic drawing methods to be able to write changes to the map. In this post, I’m attempting to get a better understanding of the level data structure we are given. WIth that in mind, the first thing I want to do is go over how to inspect a block in [MCEdit](https://www.mcedit.net/).

My initial attempt at this was a failure because I assumed getting a block would follow a similar naming convention to the `setBlockAt` function. Much to my surprise, this was not the case. Searching through the the code showed that the correct function is actually `blockAt`. With that unfortunate mistake behind, it was super easy to modify my [fill selection code](../gdmc1/#fill-selection) from the last post.

```python
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

inputs = (
    ("Selection Material Counter", "label"),
    ("Creator: Colan Biemer", "label")
)

def perform(level, box, options):
    final_x = box.origin.x + box.size.x
    final_y = box.origin.y + box.size.y
    final_z = box.origin.z + box.size.z

    materials = {}

    for x in range(min(box.origin.x, final_x), max(box.origin.x, final_x)):
        for y in range(min(box.origin.y, final_y), max(box.origin.y, final_y)):
            for z in range(min(box.origin.z, final_z), max(box.origin.z, final_z)):
                material = level.blockAt(x,y,z)

                if material not in materials:
                    materials[material] = 0

                materials[material] += 1

    print "Material Counts"
    for key in materials:
        print "\t" + str(key) + ": " + str(materials[key])
```

I used a dictionary with a key to the material and a value of the count. Each material checks to see if it exists in the dictionary and if not it adds itself with a value of 0. After this check, the dictionary value for the key is incremented. After looping through the selection, a loop is used to print out all the values. The output after running on a random selection I made can be seen below.

```
Material Counts
    0: 2361
    1: 80
    2: 728
    3: 917
    37: 7
    12: 12
    17: 93
    18: 726
    31: 44
```

# Rewriting Every Block Except Empty

From the last post we already know how to fill in a space with a material and even make it modifiable from the the UI. We can take the exact same code and add an if statement at the end of the three for loops to check if the block in question is empty and does not have an ID of 0. If it doesn't we can overwrite it, else we can continue onwards.

![](/images/gdmc_1/replace_all_except_air.png "Figure 1: Sample where all non-empty blocks are turned into coal.")

As a note, in mcedit there is a file [minecraft.json](https://github.com/mcgreentn/GDMC/blob/master/pymclevel/minecraft.json) which defines every block and it’s data. Unfortunately, there isn’t one for empty space. However, looking at the the code in [materials.py](https://github.com/Podshot/MCEdit-Unified/blob/master/pymclevel/materials.py#L259) there is a hardcoded value for air that can be used.

```python
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

inputs = (
    ("Replace All Except Air", "label"),
    ("Material", alphaMaterials.CoalBlock),
    ("Creator: Colan Biemer", "label")
)

def draw_block(level, x, y, z, material):
    level.setBlockAt(x, y, z, material.ID)
    level.setBlockDataAt(x, y, z, 0)

def fill_box(level, origin, size, material):
    final_x = origin.x + size.x
    final_y = origin.y + size.y
    final_z = origin.z + size.z

    for x in range(min(origin.x, final_x), max(origin.x, final_x)):
        for y in range(min(origin.y, final_y), max(origin.y, final_y)):
            for z in range(min(origin.z, final_z), max(origin.z, final_z)):
                if level.blockAt(x,y,z) != 0:
                    draw_block(level, x, y, z, material)

def perform(level, box, options):
    fill_box(level, box.origin, box.size, options["Material"])
```

# Nuke
Now we can focus on recreating what was done by Christoph Salge in his [tweet](https://x.com/ChristophSalge/status/967148791248932864) also seen in figure two. It replaces the top layer of the world with obsidian and tree blocks with coal. In addition, I’ve decided to replace water with lava. All of this is pretty easy except for replacing the top layer of the world. So we are going to break this problem down into two parts. First, we are going to replace the top layer of the world with any material. After that, we are going to combine the result of the first part with the extra replacements to recreate the entire filter.

![](/images/gdmc_1/nuke.jpg "Figure 2: Christoph Salge’s filter in action from his tweet.")

## Replacing the Top Layer
Up until now every for loop that we have used has been looping through every `x`, then every `y`, and then every `z` to look through the map. This works pretty well but now we have to change it. Mcedit uses a coordinate system where the `y` coordinate is representative of the height. Therefore, we are going to change our loop to go `x`, `z`, and then `y`. In addition, instead of going from the smallest `y` to the largest `y`, we are now going to do the opposite. This means that for every `x` and `z` coordinate we will loop from the top of the users selection to the bottom.

![](/images/gdmc_1/replace_top_layer.png "Figure 3: Replacing the to layer with coal.")

From there, we can loop through the `y` coordinates and stop once we find a material that isn’t air. The effect can be seen in figure three and the code is directly below.

```python
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

inputs = (
    ("Replace Top Layer", "label"),
    ("Material", alphaMaterials.CoalBlock),
    ("Creator: Colan Biemer", "label")
)

def draw_block(level, x, y, z, material):
    level.setBlockAt(x, y, z, material.ID)
    level.setBlockDataAt(x, y, z, 0)

def fill_box(level, origin, size, material):
    final_x = origin.x + size.x
    final_y = origin.y + size.y
    final_z = origin.z + size.z

    for x in range(min(origin.x, final_x), max(origin.x, final_x)):
        for z in range(min(origin.z, final_z), max(origin.z, final_z)):
            # loop from the top until we reach a material that is not empty
            for y in reversed(range(min(origin.y, final_y), max(origin.y, final_y))):
                if level.blockAt(x,y,z) != alphaMaterials.Air.ID:
                    draw_block(level, x, y, z, material)
                    break

def perform(level, box, options):
    fill_box(level, box.origin, box.size, options["Material"])
```

## Replacing the Top Layer and All Other Materials
We can break this problem into 3 parts to get the effect seen in figure four:

1. Replace the top layer with obsidian
2. Replace all water with lava
3. Replace all trees with coal and remove the leaves

![](/images/gdmc_1/nuke_in_action.png "Figure 4: Nuke effect in action.")

The first effect is now easy, we use the code from the section above and give it the material of Obsidian. The second effect is also easy, we use our replace all function and change it to only change the value to lava if the given block is water. The only thing to note is that we have to use the materials `ID` instead of just the material. Lastly, we do the same thing as the second part but also check for leaves. With wood we replace it with coal and with leaves we replace it with air. It is important to note that the the replace top layer function must be called last or you will end up with obsidian blocks where leaves used to be. The code below directly represents this line of thought but you’ll probably notice it is fairly inefficient.

```python
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from pymclevel.box import Vector
from mcplatform import *

inputs = (
    ("Nuke", "label"),
    ("Creator: Colan Biemer", "label")
)

def draw_block(level, x, y, z, material):
    level.setBlockAt(x, y, z, material.ID)
    level.setBlockDataAt(x, y, z, 0)

# We do this last, so we can assume leaves have been destroyed and
# wood has been changed to coal
def fill_top_layer_with_obsidian(level, origin, size):
    for x in range(min(origin.x, size.x), max(origin.x, size.x)):
        for z in range(min(origin.z, size.z), max(origin.z, size.z)):
            # loop from the top until we reach a material that is not empty
            for y in reversed(range(min(origin.y, size.y), max(origin.y, size.y))):
                block = level.blockAt(x,y,z)
                if block != alphaMaterials.Air.ID and \
                   block != alphaMaterials.CoalBlock.ID and \
                   block != alphaMaterials.Lava.ID:
                    draw_block(level, x, y, z, alphaMaterials.Obsidian)
                    break

def replace_all_water_with_lava(level, origin, size):
    for x in range(min(origin.x, size.x), max(origin.x, size.x)):
        for y in range(min(origin.y, size.y), max(origin.y, size.y)):
            for z in range(min(origin.z, size.z), max(origin.z, size.z)):
                block = level.blockAt(x,y,z)

                if block == alphaMaterials.Water.ID or block == alphaMaterials.WaterActive.ID:
                    draw_block(level, x, y, z, alphaMaterials.Lava)

def replace_all_trees_with_coal(level, origin, size):
    for x in range(min(origin.x, size.x), max(origin.x, size.x)):
        for y in range(min(origin.y, size.y), max(origin.y, size.y)):
            for z in range(min(origin.z, size.z), max(origin.z, size.z)):
                block = level.blockAt(x,y,z)

                if block == alphaMaterials.Wood.ID:
                    draw_block(level, x, y, z, alphaMaterials.CoalBlock)
                elif block == alphaMaterials.Leaves.ID:
                    draw_block(level, x, y, z, alphaMaterials.Air)

def perform(level, box, options):
    size = Vector(box.origin.x + box.size.x, box.origin.y + box.size.y, box.origin.z + box.size.z)

    replace_all_water_with_lava(level, box.origin, size)
    replace_all_trees_with_coal(level, box.origin, size)
    fill_top_layer_with_obsidian(level, box.origin, size)
```

The above code is inefficient because it does the same three loops three times in three different functions. It was convenient to write the program this way the first time because it was clear and helped organize our thoughts. However, now that we have a working version it is worthwhile to go back and figure out a way to combine all three loops.

This means copying the inner loops and pasting them into one for loop, however there is some conflict with the replace top layer loop. A first step could be to to write two for loops for the `y` coordinate at the end: one for the water and trees and the other for the top layer.

```python
def nuke(level, origin, size):
    for x in range(min(origin.x, size.x), max(origin.x, size.x)):
        for z in range(min(origin.z, size.z), max(origin.z, size.z)):
            for y in range(min(origin.y, size.y), max(origin.y, size.y)):
                block = level.blockAt(x,y,z)
                
                if block == alphaMaterials.Water.ID or block == alphaMaterials.WaterActive.ID:
                    draw_block(level, x, y, z, alphaMaterials.Lava)
                elif block == alphaMaterials.Wood.ID:
                    draw_block(level, x, y, z, alphaMaterials.CoalBlock)
                elif block == alphaMaterials.Leaves.ID:
                    draw_block(level, x, y, z, alphaMaterials.Air)

            # loop from the top until we reach a material that is not empty
            for y in reversed(range(min(origin.y, size.y), max(origin.y, size.y))):
                block = level.blockAt(x,y,z)

                if block != alphaMaterials.Air.ID and \
                   block != alphaMaterials.CoalBlock.ID and \
                   block != alphaMaterials.Lava.ID:
                    draw_block(level, x, y, z, alphaMaterials.Obsidian)
                    break
```

This is a good first step, however, we can improve it by making it work in one loop rather than two. The only step is to create a set of `if`, `else if` statements where the top layer statement is last. You may have concerns about the break ruining the filter, however, this break actually makes it so we do less work and still get the same effect. I’m leaving it as a thought experiment for anyone who wants to figure out how this works.

```python
def nuke(level, origin, size):
    for x in range(min(origin.x, size.x), max(origin.x, size.x)):
        for z in range(min(origin.z, size.z), max(origin.z, size.z)):
            # loop from the top until we reach a material that is not empty
            for y in reversed(range(min(origin.y, size.y), max(origin.y, size.y))):
                block = level.blockAt(x,y,z)

                if block == alphaMaterials.Water.ID or block == alphaMaterials.WaterActive.ID:
                    draw_block(level, x, y, z, alphaMaterials.Lava)
                elif block == alphaMaterials.Wood.ID:
                    draw_block(level, x, y, z, alphaMaterials.CoalBlock)
                elif block == alphaMaterials.Leaves.ID:
                    draw_block(level, x, y, z, alphaMaterials.Air)
                elif block != alphaMaterials.Air.ID and \
                   block != alphaMaterials.CoalBlock.ID and \
                   block != alphaMaterials.Lava.ID:
                    draw_block(level, x, y, z, alphaMaterials.Obsidian)
                    break
```