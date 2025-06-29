+++
date = '2025-06-29T10:26:40-04:00'
draft = false
title = 'Sokoban Part 7: Instructions'
+++

{{< youtube GkINdTax_Eg >}}

----

Hi all, this is the 7th part of this series on coding Sokoban in c++. In this part, I did a few things:

1) I fixed the problem with menu highlighting that I had at the end of the last video.
2) I changed the game to use inheritance to implement a basic state machine.
3) I updated the game to drop the UI code and made it part of each state.
4) I added an option to the main menu for players to exit, rather than making them ctrl-c to quit.
5) I added support for arrow keys to the game, so players no longer have to use WASD.

Hope you enjoy!

Project repository: https://github.com/bi3mer/sokoban