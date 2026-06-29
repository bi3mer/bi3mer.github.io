+++
date = '2022-08-24T12:00:00+00:00'
draft = false
title = "On Linking Level Segments - CoG 2022 Talk"
+++

{{< youtube VrOBNP6UbRU >}}

----

This is the talk I did for the IEEE Conference on Games (CoG) 2022 on the paper I wrote with Seth Cooper, On Linking Level Segments, which was nominated for best paper. (The winner of the best paper award also has a talk which is available at https://www.youtube.com/watch?v=mnNKdOzi0F4&t=6s&ab_channel=TeaPea.) A link to the arxiv version of the paper and the abstract is below.

https://arxiv.org/pdf/2203.05057.pdf

An increasingly common area of study in procedural content generation is the creation of level segments: short pieces that can be used to form larger levels. Previous work has used concatenation to form these larger levels. However, even if the segments themselves are completable and well-formed, concatenation can fail to produce levels that are completable and can cause broken in-game structures (e.g. malformed pipes in \textit{Mario}). We show this with three tile-based games: a side-scrolling platformer, a vertical platformer, and a top-down roguelike. To address this, we present a Markov chain and a tree search algorithm that finds a link between two level segments, which uses filters to ensure completability and unbroken in-game structures in the linked segments. We further show that these links work well for multi-segment levels. We find that this method reliably finds links between segments and is customizable to meet a designer’s needs.
