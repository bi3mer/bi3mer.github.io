+++
date = '2026-01-23T12:00:00+00:00'
draft = false
title = "I Ran My Game 30,000 Times to Find Bugs"
+++

{{< youtube 4PDm8JZTNhw >}}

----

I built a simple automated tester for my game—30,000 runs, zero crashes. Here's how it works.

Testing your own game is hard because you play it the way it's meant to be played. Players won't. Hiring a QA team is overkill for a solo project. So I built a fuzz tester instead: a Python script that runs my game thousands of times with random inputs and logs the results.
The whole setup took an afternoon. In this video I walk through the Python script, the conditional compilation, and the random "agent" that plays the game.

Referenced in this video:

- Tyler Glaiel's tweet on fuzz testing Mewgenics: https://x.com/TylerGlaiel/status/2011159126311612661
- AI and Games - The Secret AI Testers Inside Tom Clancy's The Division 2: https://www.youtube.com/watch?v=JpQd1Y7gYug

Socials:

- Twitter: https://x.com/colanbiemer
- GitHub: https://github.com/bi3mer
