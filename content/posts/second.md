+++
date = '2018-02-26T20:27:29-05:00'
draft = false
title = 'Generative Design in Mineraft: MCEdit Basics'
+++
# Generative Design in Minecraft (GDMC)

[GDMC](http://gendesignmc.engineering.nyu.edu/) is a competition to generate settlements within a selection of a minecraft map. The [project's website](http://gendesignmc.engineering.nyu.edu/) provides details on how the competition works and what is expected. However, the main point to get across right now is that they are judging based on adaptability, functionality, narrative, and aesthetics. Adaptability is about the generation technique working with the map rather than ignoring it. An example of ignoring the environment would be generating a wooden village where there are no trees. The functionality component is based on real world criteria such as access to food, defenses, etc. The narrative component is about how every area has a story to tell. An example is a castle with part of the tower knocked down. Lastly, aesthetics is about how it looks both in terms of believability and general appeal.

# MCEdit

To generate settlements, the competition has gone the route of using [MCEdit](http://www.mcedit.net/) to allow competitors to view, generate, and modify minecraft maps. GDMC provides a [wiki](https://github.com/mcgreentn/GDMC/wiki) with easy to use instructions for installing and general set up. The [wiki also provides an example](https://github.com/mcgreentn/GDMC/blob/master/stock-filters/CASG_Example.py) cellular automata script for generating structures seen in figure one. As you can see, the output isn’t great, but it provides a nice starting point. It, also, shows how to work with the MCEdit filters which is how we can interact with the maps.

![](/images/gdmc_0/ca_sample.png "Figure 1: Example cellular automata output from CASG_Example.py")

