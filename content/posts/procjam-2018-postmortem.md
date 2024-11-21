+++
date = '2024-11-21T15:08:15-05:00'
draft = false
title = 'Procjam 2018 Postmortem'
+++
A few months ago I completed the annual [ProcJam](https://www.procjam.com/) jam. I wish I had considered doing a postmortem beforehand when everything was fresh, but now I am preparing for [7DRL](http://www.roguebasin.com/index.php?title=7DRL). I figure a retrospective on how I did in the last jam will be useful for the upcoming one.

Before beginning, I would like to preface this with the fact that I was sick for the entire jam. It’s not an excuse but it is one of the reasons why I did not complete as much as I would have liked to in the game. My original design was a weapon based roguelike, minus turn-based, where the player is trying to get through as many levels as possible. The weapons would be dropped by enemies and they would be adversarially generated. Meaning, a player that spams weapon shots would receive guns that shoot slower. A player that was extremely accurate would receive guns that would spray, such as a shotgun. In addition, all levels would be procedurally generated. I hoped to get in a few enemies and had a stretch goal of creating a boss. Lastly, I hoped to make the game a platformer. In short, I had an ambitious scope for a ten-day jam even if I wasn’t sick.

On my first night working on the project, I set up the project and built a basic scene to show player movement and basic shots. There wasn’t anything special being done here, however, I did waste time playing with variables to make jumping feel right. I say it was a waste of time because it is more important to get functionality in a jam than polish. At this point, I was feeling fine about my scope but half nervous about level generation. I didn’t, and still don’t, know a great way to procedurally generate compelling platformer levels.

On day two Trevor, someone who worked with me on the project, improved the shooting code I wrote the day before and improved player movement. I started the night by implementing a basic enemy framework. Where the `BaseEntity` had a few stats, like health and functions to handle damage, and other classes implemented on top of it. For example, the `BaseEnemy` inherited from the `BaseEntity` and added dropping loot to the entity. At the end of the enemy implementation, I added a single enemy that would fly towards you and explode on impact. In addition, I also added room generation which convinced me that the current platformer idea was too much of a stretch for the jam.

The generation was pretty simple. I set up a `MonoBehavior` class which I knew would handle multiple kinds of generation but at the moment would be hardcoded with the one generation method. The generation method I implemented was very simple. Start with a matrix of all dead cells. Turn the bottom leftmost cell alive, the starting point, and find points that it can explore. In this case, it will be moving up one cell or to the right. Both of these are added as leaves and the algorithm chooses a random leaf. The newly explored leaf will check dead cells with the constraint that this dead cell cannot be next to any alive cells in the four cardinal directions. After the new leaves are added, the explored cell is turned alive and it repeats until the top rightmost cell is turned on.

![](/images/procjam-2018-postmortem/correct_level_1.png "Figure 1: Example level generated with the randomly explored branching tree method")

The results of the algorithm can be seen in figure 1 and it shows a few flaws in the generation. The first flaw is that the left side will always be more explored than the right side. The second is that it only creates corridors. The third is that the algorithm does not guarantee exploration to the top right as described. It is easy to fix with a special case where we check if the second most top right point is turned alive, if so then we finish the path by hardcoding. However, it is a flaw in the algorithm. Regardless of these flaws, the first mistake was not having the generation method planned ahead of time for the jam. At this point, I was still thinking about doing a platformer and this method clearly doesn’t work for a platformer and does not create interesting levels.

On day three, Trevor moved the structure of enemies, and the player, to an entity component system. Classes are broken down to pieces and avoid an inheritance headache that comes from the system I built the day before for entities. In addition, he implemented a tougher enemy that took the kamikaze bot I created and set it up so it would ram into you and do damage. After you’ve done enough damage to kill it, it had eight eggs around it hatch and eight kamikaze enemies came after you. It was a solid display of the strengths of the entity component system and was a fun enemy to play against.

I started off the day by fixing the error in my generation code where the top right was not reached with the special case I mentioned above. I then improved the level generation by adding two noise functions based on [Conway’s Game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). The first was a direct implementation of the algorithm where you could choose the number of epochs and can be seen in figure three. The second was Conway’s Game of Life with the killing cells removed and can be seen in figure two. The noise function used is applied to the generated level after the first generation method carved out the map.

| Epochs: 1 | Epochs: 2 | Epochs: 5 | Epochs: 10 |
|:---------:|:---------:|:---------:|:----------:|
| ![](/images/procjam-2018-postmortem/1_epoch.png) | ![](/images/procjam-2018-postmortem/2_epochs.png) | ![](/images/procjam-2018-postmortem/5_epochs.png) | ![](/images/procjam-2018-postmortem/10_epochs.png) | 

As can be seen above, Conway keep alive creates maps that aren’t that interesting and fairly open. The regular Conway noise, figure three, creates interesting looking maps but doesn’t guarantee a path after two epochs. Even at two epochs, it isn’t a sure thing.

| Epochs: 1 | Epochs: 2 | Epochs: 5 | Epochs: 10 |
|:---------:|:---------:|:---------:|:----------:|
| ![](/images/procjam-2018-postmortem/1_epoch-1.png) | ![](/images/procjam-2018-postmortem/2_epochs-1.png) | ![](/images/procjam-2018-postmortem/5_epochs-1.png) | ![](/images/procjam-2018-postmortem/10_epochs-1.png) | 

At this point, I knew my dreams of making the game a platformer would not be realized. So for my last act of the night, I removed the platformer scripts and reimplemented movement for a top-down game. Luckily nothing had to be done to the rest of the enemies since they were still fairly simple.

On day four Trevor updated the Unity version of the project and changed the generation to use tilemaps instead. Before I had been placing them in space with code. Now the tilemap handled the placing for us. I started by removing single dead cells. Meaning that if a tile was surrounded by alive cells it was turned alive. It made the maps a bit easier to navigate and feel a lot better. I then added a UI for health so the player can see their health on the screen. This also made it much easier to confirm that enemies were doing damage as intended. After that, I added a pause menu to the game.

![](/images/procjam-2018-postmortem/bug_or_feature.gif "Figure 2: Example map with new tiles and a fun bug")

On day five Trevor became an artist and replaced my white and black tiles with a simple tilemap; the results can be seen in Figure 2. You can also see a fun bug where there was no cap on the players shooting speed. I then implemented [A*](https://en.wikipedia.org/wiki/A*_search_algorithm) in the game. It wasn’t hard since it feels like I’ve implemented it a thousand times. Though it does take some time, and, in this case, it was time completely wasted.


![](/images/procjam-2018-postmortem/astar_in_map.png "Figure 3: A* example on generated map")

I wanted to use A* to guarantee pathing for level generation. I wanted to use it for enemies. I wanted to use it but never had the time to. It was time that was completely wasted. In a jam like this, especially when sick and during a work week, time wasted is huge. I think it’s one of the main reasons that I never did end up getting to work on the adversarial weapons. Mistakes aside, I added a start screen with a basic menu. Then I set up level incrementing so when the player died they’d go back to level 1. I still did not have any ability for the player to move up a level at this point.

I started off day six by adding quit buttons to the main menu and the pause menu in the game. I also fixed a bug where the level generation would run infinitely. It was very rare and I never did figure out why it occurred. As a band aid, I set it up so it returned a null value and then the level generation algorithm would be called again. It was a lazy solution, but necessary given the time constraints.

![](/images/procjam-2018-postmortem/ladder_working.gif "Figure 4: an example of the game loop with ladders.")

After I got started on adding ladders to the game so there was a full game loop, see figure 6. It wasn’t that hard to implement. When the player came in contact with the ladder, the level would be incremented and the scene reloaded. I didn’t add any requirements for the player to kill every enemy before she could advance. It was something I considered for the future, but not the first iteration of the game.

The last thing I did on day six was add a spawner to the game. It was fairly simple. At the start of every level, the spawner would see what level the player was on and multiply the amount by 4 and divide the result by 1.5. The ceiling of that value was how many enemies would spawn. I came up with the numbers by playing with variables until something felt right and the plot looked reasonable. To choose spots for enemies to spawn, I chose random positions that were a minimum distance from the player. I kept a hashtable of all the used positions. Once every enemy had a place to spawn, they were placed. I also set up three arrays of enemies: easy, medium, and hard. The next day I planned to make it so higher tiered enemies would count for more when spawning.

Day 7 was the last day of the jam and I was in trouble. Technically, the jam lasts for 10 days but I hadn’t been well enough to compete for three days. I also had a lot to do. I still didn’t have any weapons being generated or any sense of progression as you moved through the game. I started off by implementing player death. I did this by having the player go back to the main menu which would auto reset the level to 1 every time.

Afterward, I moved onto updating the generation so all three corners of the map could be where the ladder spawned instead of just the top right. I didn’t update the generation method for this. Instead, I checked if the top left and bottom right corners were available for ladder spawning. If they were I added them to an array and choose randomly from the array. This is one of those things I’m happy I added but was not essential. It was a waste of time when I still needed to add something like weapons.

In hindsight, at this point, I had given up on the weapons. I was already considering using the entity components used for enemies as a way to enhance player attributes. While considering this I improved the enemy generation to now use the tiered approach I discussed above. I also took away the hardcoded multiple arrays and made it an array of arrays to be more dynamic and useful if I decided to continue working on the game.

Following the improvement to spawning, I added the third and final enemy the game would ever see: the pest. The pest was the exact same as the kamikaze enemy but it would not explode on impact, instead do damage, and it could fly over obstacles. It is truly a pest and a very annoying enemy in the game. It is small enough so hitting it is kind of hard. Overall, I’m a big fan of the pest.

![](/images/procjam-2018-postmortem/level_generator_ui.gif "Figure 5: level generator UI")

Next up, was my biggest mistake seen in Figure 5. Because this was ProcJam I wanted to show off the procedural generation with a UI that showed all the noise functions. However, the game should have done this on its own without the help of this extra UI. I enjoyed making it, but it was a complete waste of time and did not add any value to the end result.

My last act for the game was to add progression to the player’s character. I updated the enemy loot system so each destroyed enemy would drop a box. Each box represented a different stat: health, fire rate, damage, movement speed, and shot lifetime. Unfortunately, I didn’t communicate to the player at all what each box represented. Or do anything to clarify that the boxes were good. But I did set up a Ratchet and Clank bolts like collection system where they just flowed into you. Setting up the components to interact with the player was already implemented thanks to the entity component system. And whenever a new box was added, it added another component to the player.

Once the player had defeated the level, all the components for each stat type were added up and saved. On load, the stats would be added up into one big component and the process would restart. On entering the main menu the stats would be set back to one. Setting up the saving was a bit more complicated than I would have liked but overall was not too horrible to get right.

And that is the process I had for ProcJam 2018. My main takeaway is that I wasn’t focused enough on the [MVP](https://en.wikipedia.org/wiki/Minimum_viable_product). I wanted to get adversarial weapon selection but didn’t have time because I didn’t have a plan going into the development. That is why for 7DRL I am planning for it now. When it comes time for development, I want to know exactly what I am going to be making. I want to know the technology I’m going to use. I want to know the procedural generation techniques I’ll be using. I want to have as many components of the game, application, etc. planned as possible for any future jam I participate in.
