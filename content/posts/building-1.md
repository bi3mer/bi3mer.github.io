+++
date = '2026-07-17T08:55:09-05:00'
draft = false
title = 'Cira Centre Games: Origins'
+++

The year was 2013. I was a sophomore at Drexel University and I was given the opportunity to work on the Cira Centre Games Project by a professor named Frank Lee. To be frank, I'm not exactly sure why. My grades were subpar. I played too much _Dota 2_. I was a terrible programmer. But, I showed some initiative back when I was a freshman when I cold-emailed Frank asking if he had any advice for how to work on games. After a few months working on another project for Frank, he asked me to work on the Cira Centre Games Project.

<center>
    <img src="/images/pong-cira-centre.jpg" width=400>
        Figure 1: <i>Pong</i> on the Cira Centre in Philadelphia. (<a href="https://i.ytimg.com/vi/hnIK54dCbqI/maxresdefault.jpg">source</a>)
    <br/>
    <br/>
</center>

In the previous year, Frank built [_Pong_ for the Cira Centre](https://drexel.edu/news/archive/2013/november/cira-pong-guinness), see Figure 1. He had a team that helped. First was a professor named Gaylord Holder who was a major force behind figuring out how to programmatically talk to the lights with the help of an open-source library called [Kinet](https://github.com/vishnubob/kinet).[^kinet] Second was a professor named Santiago Ontañón. He helped with the game programming. Last but not least was a student named Marc Barrowclift. His job was to take the code that Gaylord wrote for sending pixel commands, and make a tiny game engine out of it. He has a [small blog post](https://barrowclift.me/projects/code/the-largest-video-game-ever-made/) where he wrote about the project.

When it was my time to work on the project, I inherited the codebase from Marc. It was written in Python 2.7, and I had never written a line of Python before.[^python] As a sophomore, using a new programming language was no simple task. Every line was weird and different coming from C++. The bigger hurdle, though, was to learn how to navigate a medium-sized codebase that wasn't my own. It didn't help that running the code was no simple task either.

You couldn't just play a game with a command like: `python pong.py`. The system that Gaylord and Marc had built was more complex. The reason why is that sending light commands to the building was slow, resulting in lights on the building not updating simultaneously, so you could get a kind of crawling effect of lights changing across the building.

The solution they came up with was to have a computer in the building that ran the game and sent light commands, and a computer outside the building that sent keystroke commands to the computer inside the building. The computer in the building could be accessed with [`SSH`](https://en.wikipedia.org/wiki/Secure_Shell), and keystrokes were sent over `SSH`:[^security]

```bash
python sendKeyStrokes.py | ssh USER@IP "python game.py" | python playSounds.py
```

Commands were also sent back across SSH and piped to a script called `playSounds.py`, and it would, you guessed it, play sounds based on strings that it received.

For running a game locally, though, it was simpler:

```bash
python sendKeyStrokes.py | python pong.py
```

For a sophomore in college who hadn't yet found a love for programming, though, this was esoteric as hell and it took me a long time to figure out. When I did, I still hadn't solved the larger problem of understanding the codebase.

To figure out the code, I went to _Blick_ and bought a large piece of rolled paper. I took it to my dorm, unrolled it, and I started diagramming. I didn't know what UML was at the time, and my disdain for it would come later in life. I just drew boxes connected to other boxes until I could see how everything was structured and what each thing did. Looking at the whole picture didn't help me, but the process of making it did. I had a clear idea of the structure, but I only really figured out what was happening in the codebase when I started coding.

My task was to program _Tetris_ for the Cira Centre. That wasn't the hard part, though. (It wasn't easy either.) The real task was for me to take the code that had been written for the _Pong_ event, and update it so that it could use all sides of the building. The previous version only worked on one side. Access to all sides of the building would allow for games to be mirrored so that everyone in the city could see the game being played. It would also allow for competitive games, but that would be its own challenge.

Doing all that, though, would take me months, and I would go from someone who wasn't sure about programming to someone who was overconfident about their skills, but mildly competent. In the next post, I'll cover a few of the changes I made (such as making the engine more generic with double buffering built in) and how I got to what you see in Figure 2, a double sided version of competitive _Tetris_.

<center>
    <img src="/images/tetris.avif" width=400>
        Figure 2: competitive version of <i>Tetris</i> on the Cira Centre in Philadelphia. (<a href="https://www.fastcompany.com/3028784/how-a-drexel-professor-created-the-worlds-biggest-game-of-tetris">source</a>)
    <br/>
    <br/>
</center>

[^kinet]: Python API to control Color Kinetics lights using the [kinet protocol](https://wiki.openlighting.org/index.php/KiNET).

[^python]: While Python 3.0 was released in 2008, it wasn't until about 2016 that many, in my experience, began the switch from Python 2 to Python 3.

[^security]: If you are concerned about security, rest assured that I have deliberately left out several details. The IP was not reachable to the public.
