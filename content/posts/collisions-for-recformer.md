+++
date = '2025-03-20T10:10:14-04:00'
draft = true
title = 'Collisions for Recformer'
+++


## Collision Speed Up
### Grid Collisions for Static Entitites

```js
for (let i = 0; i < dynamicSize; ++i) {
  const e = this.dynamicEntities[i];
  for (jj = i + 1; jj < dynamicSize; ++jj) {
    e.collision(this.dynamicEntities[jj]);
  }

  for (jj = 0; jj < staticSize; ++jj) {
    e.collision(this.staticEntities[jj]);
  }
}
```

The code above is bad. Anyone familiar with collision detection would tell you so. But if you aren't sure, you may be asking, "Why is it bad?" The answer is that the code is O(n^2), meaning the execution will get slower and slower as `n`, which is the number of entities in the scene, gets larger.

Collision detection can be sped up by reducing the search space. One approach is to build a [quadtree](https://en.wikipedia.org/wiki/Quadtree) which partitions space, and collisions are found by navigating the tree to see if any entities exist in the space the entity wishes to reside in. If there an entity, then you have a collision.[^quad] Another approach, and this is the one I took for Recformer, is to use uniform grid collision detection. This method is ideal because Recformer levels are broken into tiles already. There is a problem, though. Recformer is continuous, so a grid isn't necessarily ideal for dynamic entities where an entity can be at position `(2.12,10.94)`. However, a grid is perfect for static entities, because the only static entity in the game is a block which takes up the whole grid.

```js
const positions = [
  e.pos,
  pointAdd(e.pos, new Point(BLOCK_SIZE.x, 0)),
  pointAdd(e.pos, new Point(0, BLOCK_SIZE.y)),
  pointAdd(e.pos, BLOCK_SIZE),
];

for (jj = 0; jj < 4; ++jj) {
  const point = pointFloor(positions[jj]);
  if (
    point.y >= 0 &&
    point.y < this.staticEntities.length &&
    point.x >= 0 &&
    point.x <= this.staticEntities[0].length &&
    this.staticEntities[point.y][point.x]
  ) {
    e.collision(new Block(point));
  }
}
```

as you can see, the code for detecting a collision with static entities is now a bit more complicated looking. We now need bounds checks, and we need to check for a collision in the grid. However, the important thing in all this is to answer one simple question: Is our code faster?

I won't pretend that I have written a perfect benchmark. I am going to run both versions of collision detection with the A* code described above on 14 levels that I have made. I'm not going to run this on a server. I'm not going to run multiple times to find an average. I'm not going to do a lot of things that make for a proper benchmark. I have a crude benchmark, but I'm okay with it because the difference between running with grid collisions versus a big loop is so severe that an argument is pointless.

|A* `for loop` | A* `grid collision`|
|--|--|
|9751.728166 ms | 2462.8335 ms |

So, based on this, I think our efforts were rewarded. As a bonus, the game will now run better on other people's computers. Plus, I will be using this to generate levels with [ponos](https://github.com/bi3mer/ponos) down the line, so faster execution is always a good thing.

### Sweep and Prune Collisions for Dynamic Entities

|Double `for` Loop | Sweep & Prune |
|--|--|
| 2462.8335 ms | 2339.5377 ms |


[^astarintro]: The best introduction I have seen was made by [Red Blob Games](https://www.redblobgames.com/pathfinding/a-star/introduction.html).

[^updatecaveat]: Another approach is for the game model to have a function `nextStates` which returns a list of the next possible states. 

[^rendernote]: The code that went into the game model class has nothing to do with rendering, which is a nice side effect of this because we now have the benefit of [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) in the game part of the codebase.

[^quad]: There is an [example here on my website](https://bi3mer.github.io/quad_tree_visualization/).
