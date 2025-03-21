+++
date = '2025-03-20T14:14:48-05:00'
draft = false
title = 'A* for Recformer'
+++

[*Recformer*](https://bi3mer.github.io/recformer/) is a simple [platformer](https://en.wikipedia.org/wiki/Platformer). To beat a level, the player has to collect every coin in the level. *Recformer* is implemented in [Typescript](https://www.typescriptlang.org/). I built it for the web because I am planning to run a player study with it, and it is a lot easier for people to open up a webpage than to install an executable. Another reason I made it is because I wanted to, and because of that, I want the game to be good; at the very least, I want *Recformer* to be decent. An image I have had in my mind for a while now is a main menu where you can watch an agent that plays the game. This blog post is going to show you how I accomplished exactly that.

In my [last post](../graph-simplification-for-a-faster-astar/), I opened up by saying that [A*](https://en.wikipedia.org/wiki/A*_search_algorithm) is a ridiculously well-covered topic. So well-covered that there is no point in writing anything more on the topic.[^astarintro] I stand by that, but there is a less-covered topic: Setting up your game for A*. 

A* needs a forward model of your game that it can interact with. The model must have some version of the following:

- `update` - A function that moves the simulation one step forward.[^updatecaveat]
- `actions` - A list of actions that the agent can take.[^actioncaveat]
- `clone` - A function which clones the entire model.[^clonecaveat]
- `hash` - A function which returns a number that represents the current state of the model.
- `heuristic` - A method that returns a number which indicates how close the agent is to the goal.[^heuristiccaveat]

## Update

My first implementation of *Recformer* had no model. The code was broken into [scenes](https://github.com/bi3mer/recformer/blob/main/src/core/scene.ts). Every scene has the following functions: `onEnter`, `update`, `render`, and `onExit`. The game logic was in the `update` loop, which mostly involved calling `update` on every entity in the scene and then handling collisions. To make a forward model, I made a new [`GameModel`](https://github.com/bi3mer/recformer/blob/main/src/gameModel.ts) class, and took all the code in the `update` function and moved it over. After that, I added the `GameModel` to the game scene, and handled any bugs that I accidentally introduced in the process of migrating the code.

## Actions

```js
import { Point } from "../DataStructures/point";

export class Action {
  moveRight: boolean;
  moveLeft: boolean;
  jump: boolean;

  constructor(moveRight: boolean, moveLeft: boolean, jump: boolean) {
    this.moveRight = moveRight;
    this.moveLeft = moveLeft;
    this.jump = jump;
  }
}

export const ACTIONS: Action[] = [
  // new Action(false, false, false),
  new Action(true, false, false),
  new Action(false, true, false),
  new Action(false, false, true),
  new Action(true, false, true),
  new Action(false, true, true),
];

export const NUM_ACTIONS = ACTIONS.length;
```

An action is related to a key press. *Recformer* allows the player to move to the left, move to the right, and to jump. While the player is jumping, they can also move to the left or to the right. And, of course, the player can do nothing, but you'll notice that that is commented out. Just because the player can do nothing, doesn't mean our agent should do nothing.

## Clone

```js
clone(): GameModel {
    const clone = new GameModel(null, AGENT_EMPTY);
    const dLength = this.dynamicEntities.length;
    let i = 0;

    // clone dynamic entities
    for (; i < dLength; ++i) {
      const currentEntity = this.dynamicEntities[i];
      if (currentEntity.dead) {
        continue;
      }

      const de = currentEntity.clone();
      de.game = clone;
      clone.dynamicEntities.push(de);

      if (de instanceof Coin) {
        clone.coins.push(de);
      }
    }

    // order coins
    const playerPosition = clone.dynamicEntities[0].pos;
    clone.coins.sort((a, b) => {
      return (
        pointSquareDistance(playerPosition, a.pos) -
        pointSquareDistance(playerPosition, b.pos)
      );
    });

    // static entities never change, so we don't need to clone them
    clone.staticEntities = this.staticEntities;

    return clone;
  }
```

Depending on how you have structured your game, cloning may be very simple or very arduous. In my case, I have two entity types: static and dynamic. The static entities are great because they never change no matter what happens in the game state. So, during the clone, we don't have to do a deep copy, we can just update the reference in the clone and move on---as you see in the penultimate line of the function above. However, the same is not true for the dynamic game objects. 

Each game object type has different variables that affect how they behave in the game. Therefore, the `clone` function for each game object type has to be implemented separately. This lead to a lot of coding. My approach was to implement each one clone at a time to try and avoid bugs. If I were to do this again in the future, I would consider a [structure of arrays](https://en.wikipedia.org/wiki/AoS_and_SoA) kind of approach, but there wouldn't be much point in JS, and may even have worse performance. So, there may not be away around it without some painful indexing into arrays.

```js
function pointSquareDistance(p1: Point, p2: Point): number {
  const x = p1.x - p2.x;
  const y = p1.y - p2.y;
  return x * x + y * y;
}
```

The last part of the code that I want to point out is the special behavior for coins. The `GameModel` class has an array of objects called `coins`. It is ordered such that the closest coin to the player—based on the `pointSquareDistance` function—is the first element and the furthest away element is the last element. This will be relevant when we get to the section on running A* for *Recformer*.

## Hash

```js
hash(): number {
  // get player position
  const pos = this.dynamicEntities[0].pos; 

  // turn x and y coordinates into one number
  return Math.round(pos.x * 100) + Math.round(pos.y * 100) * 1000000;
}
```

A [hash](https://en.wikipedia.org/wiki/Hash_function#:~:text=Hash%20functions%20are%20used%20in%20conjunction%20with%20hash%20tables%20to,to%20index%20the%20hash%20table) function in this context refers to a function that can generate a numerical value that links to the game state. The first option, and the first option that I tried, was to use every dynamic entity as part of the hash function. I even included information like velocity. However, as you can probably see, that is not the code you see above. The code above is only using the player's position. Why? 

One of the ways that tree searches are sped up is by keeping track of states that have already been visited, and not visiting them again. If the player has already been to `(10,5)`, we don't want to visit that position again because we will be redoing search operations. If a hash function is perfectly detailed, then that helps us guarantee an optimal path. However, this is a game. There are no stakes. We don't care if the path is optimal. All we care about is that the agent solves the level. What we really want is an algorithm that is fast. The more often we find a state that has been visited, the less we have to search. The less we have to search, the faster we find a solution path.

At this point we are getting ahead of ourselves, but when I ran with a hash function that mapped everything, the approach was slow, really slow. The idea of it being able to run on a player's browser was laughable. What followed was a bunch of trial and error, but I eventually landed on just using the player's position. Even the player's velocity wasn't important. All that mattered was the player's position.

## Heuristic

To find the next node to explore in A*, you either need a [priority queue](https://github.com/bi3mer/recformer/blob/main/src/DataStructures/priorityQueue.ts) or you need to do an `0(n)` search through the array to find the node with the lowest or highest priority. Sometimes it is [faster to do the search](https://github.com/amidos2006/Mario-AI-Framework/blob/master/src/agents/robinBaumgarten/AStarTree.java) than to use a priority queue. It really depends on the size of the array. In the case of this work, I didn't do any testing to see which one would be faster. Instead, I made an assumption. In the case of the agent that I linked, it is solving for a set time for a limited portion of the level. In the case of this agent, it is solving the whole level, and will therefore explore more space and have a larger queue. 

```js
nodes.insert(
  newDepth +
    pointSquareDistance(
      nextState.protaganist().pos,
      nextState.coins[target].pos,
    ),
  new Node(newDepth, nextState, A, curNode),
);
```

`nodes` is a priority queue. As an arguments to `insert`, it takes in the priority and a node. The priority is calculated based on the `depth` which is how far into the tree we are and a heuristic which is the square distance from the player to the target coin. There are two things to notice here. First, we are searching for one single coin. I'll come back to this in the next section, so let's go to the second point: we are using `pointSquareDistance`. This is an inadmissable heuristic. The path found is therefore not guaranteed to be optimal. I made this choice because running A* with an admissible heuristic was slow.

## Running A*

A level may have 1 coin or it may have 100. Running A* on the model to find every coin at once is possible, but would be slow because the problem space is huge. Sometimes it is better to solve 100 small problems than 1 giant problem, and that is the case for building A* for *Recformer*. The search algorithm is broken into two parts.

```js
export function astar(model: GameModel): Action[] | undefined {
  let curModel = model.clone();
  let actions: Action[] = [];

  const numCoins = model.coins.length;
  while (curModel.protaganist().coinsCollected < numCoins) {
    // the next coin will always be at index 0 because it is removed when it
    // dies and the clone method for game model updates the coins array
    // accordingly
    const [endState, stateActions] = astarSearch(curModel);

    if (stateActions === undefined) {
      console.error(
        `Pathing failed for coin at (${pointStr(curModel.coins[0].pos)})`,
      );
      return undefined;
    }

    curModel = endState;
    actions = actions.concat(stateActions);
  }

  return actions;
}
```

The first part is shown above, and deals with running A* for a single coin. You can see that it concatenates all the actions together to create an actions array which can be used to re-solve the level.

```js
function astarSearch(
  model: GameModel,
  target: number = 0,
): [GameModel, Action[] | undefined] {
  // set up search
  const seen = new Set<number>();
  seen.add(model.hash());

  const nodes = new PriorityQueue<Node>();
  nodes.insert(0, new Node(0, model, null));

  let endNode: Node | undefined = undefined;
  let actionIndex = 0;

  // Start search for target
  while (nodes.length() > 0) {
    const curNode = nodes.pop();

    const newDepth = curNode.depth + 1;
    for (actionIndex = 0; actionIndex < NUM_ACTIONS; ++actionIndex) {
      // Create a new state with an action
      const A = ACTIONS[actionIndex];
      const nextState = curNode.model.clone();
      nextState.protaganist().agent.set(A);
      nextState.update(ASTAR_FRAME_TIME, ASTAR_UPDATES_PER_FRAME);

      // Skip if the player died
      if (nextState.protaganist().dead) {
        continue;
      }

      // Check if we have reached the target
      if (nextState.coins[target].dead) {
        endNode = new Node(newDepth, nextState, A, curNode);
        nodes.queue.length = 0;
        break;
      }

      // Check if we have seen this state before
      const hash = nextState.hash();
      if (seen.has(hash)) {
        continue; // If we have, skip it
      }

      // Else we haven't, so add it to the seen set
      seen.add(hash);

      // And then make a new node and insert it into the priority queue
      nodes.insert(
        newDepth +
          pointSquareDistance(
            nextState.protaganist().pos,
            nextState.coins[target].pos,
          ),
        new Node(newDepth, nextState, A, curNode),
      );
    }
  }

  if (endNode === undefined) {
    console.error("A* Error: Could not find target.");
    return [model, undefined];
  }

  // reconstruct the path and return
  const endState = endNode.model;
  const actions: Action[] = [];

  while (endNode!.pastNode !== undefined) {
    actions.push(endNode.action);
    endNode = endNode.pastNode;
  }

  actions.reverse();
  return [endState, actions];
}
```

This function is called to find every coin. I'm not going to be going over this because A* is covered more than enough, and I don't want to waste your time. If any of the code is unclear and you have a question/concern/etc. then please reach out to me.[^email]

## Increasing \(\Delta t\)

A majority of games will use a variable `dt` (i.e., \(\Delta t\)) to represent the time between frames. With A*, we aren't rendering anything so there is technically no time between frames, but we need there to be otherwise entities won't move since movement is updated based on it. The larger the \(\Delta t\), the more entities and the agent will move between frames. Increasing \(\Delta t\) will therefore reduce the size of the search space, which will result in a faster search. 

The problem with increasing \(\Delta t\), though, is that if an entity moves to far between frames, then we may miss collisions. A simple example of this is when you are falling in a video game, you're velocity is increasing due to gravity. If the game does not have a max velocity, then your velocity will increase and increase. At a certain point, your character will fall past the ground without a collision registering. The same is true if \(\Delta t\) is too large.

```js
update(dt: number, divisor: number = 1) {
  dt = dt / divisor;

  for (let subframe = 0; subframe < divisor; ++subframe) {
    ...
  }
}
```

Too accommodate increasing \(\Delta t\), I added sub-frames to *Recformer*. The code above shows it, and, as you can see, a sub-frame is way more simple than it sounds. Instead of running one update, we run `k` updates with a smaller \(\Delta t\). 


## Caching Paths

Alright, now we are on the last step. Even though we used a very simplified `hash` function and an inadmissible heuristic, the resulting A* search was slow. Then when I broke the problem down into multiple sub-problems by searching for one coin at at time, the search could run on a browser but it took time and dropped frames. Then I increased \(\Delta t\) and added sub-frames and it got fast enough, but the search wasn't cheap. Fans started running. A menu scene that makes your player's computer struggle is a bad menu scene. The solution I came up with was to cache the paths for every level.

```js
import { AGENT_EMPTY } from "../src/Agents/agentType";
import { idToLevel } from "../src/LevelGeneration/levels";
import { ASTAR_FRAME_TIME, ASTAR_UPDATES_PER_FRAME, astar } from "../src/aStar";
import { GameModel } from "../src/gameModel";

const start = performance.now();

let replaysFile = "// Generated by scripts/replayBuilder.ts\n";
replaysFile += `import { Action } from "./Agents/action"\n\n`;

replaysFile += `export const REPLAY_FRAME_TIME = ${ASTAR_FRAME_TIME};\n`;
replaysFile += `export const REPLAY_UPDATES_PER_FRAME = ${ASTAR_UPDATES_PER_FRAME};\n\n`;
replaysFile += `export const replays = {\n`;

const keys = Object.keys(idToLevel);

for (let i = 0; i < keys.length; ++i) {
  const K = keys[i];
  console.log(`=================== K = ${K} ===================`);
  const gm = new GameModel(idToLevel[K], AGENT_EMPTY);
  const actions = astar(gm);

  if (actions === undefined) {
    console.log(`A* failed for level ${K}`);
  } else {
    replaysFile += `  "${K}": [\n`;
    for (let jj = 0; jj < actions.length; ++jj) {
      const a = actions[jj];
      replaysFile += `    new Action(${a.moveRight},${a.moveLeft},${a.jump}),\n`;
    }

    replaysFile += "  ],\n";
  }
}

replaysFile += "\n};";

const end = performance.now();

const file = Bun.file("./src/replays.ts");
await Bun.write(file, replaysFile);
console.log(`DONE: took ${end - start} ms`);
```

You'll notice a few things in the code above. The code above is a script written in TypeScript that runs offline, and the script is run by [Bun.](https://bun.sh/)[^Bun] Because of this, I use Bun's API for writing a file called `replays.ts`. This means that all the code above is to write TypeScript file that has been generated.

The code to generate the file is pretty simple. It uses `idToLevel` to get every level that is playable in the game. It then loops through each level and gets the actions to beat that level. Then it writes to the file the array of actions that is associated with the `id` that links the target `level`. It formats the array's to be human readable which is nice for me.

Finally, note that there is a performance timer, and this is a nice to have because, when I was building out the A* optimizations, I could see how things were improving. One of my regrets is that I did not track everything while working on the code. If I had, this post could have been a lot better. But, oh well. That is the end of the post. If you go to the [webpage for Recformer,](https://bi3mer.github.io/recformer/index.html?default=true) then you can see all of this in action.[^github]


[^astarintro]: See [Red Blob Games](https://www.redblobgames.com/pathfinding/a-star/introduction.html) for a good introduction to A*.

[^updatecaveat]: Note that `update` has nothing to do with rendering. In fact, it is better if rendering is not part of the model because that will result in faster execution.

[^actioncaveat]: Some implementations will forego exposing a list of actions, and instead create a function like `nextStates` which returns all the possible next states in a list. In fact, sitting here, writing this, I think `nextStates` is a cleaner approach than having the `actions` list as part of the A* code, which you will see later in this blog post.

[^clonecaveat]: This must be a [deep clone](https://developer.mozilla.org/en-US/docs/Glossary/Deep_copy) otherwise you will have an incorrect simulation.

[^heuristiccaveat]: If the [heuristic is inadmissible](https://en.wikipedia.org/wiki/Admissible_heuristic) then the path found is not guaranteed to be optimal. 

[^email]: My email is on my [resume.](/pdf/resume.pdf)

[^Bun]: I use Bun rather than [Node](https://nodejs.org/en) or [Deno](https://deno.com/) for the simple reason that I like the idea of the programming language [Zig.](https://ziglang.org/) That's it. Sure, the emphasis on speed is cool, but the other two options are fast enough that I doubt the difference would be noticeable.

[^github]: The code is on [GitHub.](https://github.com/bi3mer/recformer/tree/main)