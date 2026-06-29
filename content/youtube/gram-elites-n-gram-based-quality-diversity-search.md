+++
date = '2021-08-05T12:00:00+00:00'
draft = false
title = "Gram-Elites: N-Gram Based Quality Diversity Search"
+++

{{< youtube CRK1YlSFb3c >}}

----

This is a talk I did for the PCG Workshop on the paper by the same name as this video. The abstract for the paper is below, and once the paper is uploaded I will include a link.

In the context of procedural content generation via machine learning (PCGML), quality-diversity (QD) algorithms are a powerful tool to generate diverse game content. A branch of QD uses genetic operators to generate content (e.g. MAP-Elites). Problematically, levels generated with these operators have no guarantee of matching the style of a game. This can be addressed by incorporating whether a level is generable by an n-gram into the fitness function. Unfortunately, this leads to wasted computation and poor results. In this work, we introduce n-gram genetic operators, which produce only solutions that are generable by the n-gram model; we call MAP-Elites combined with these operators Gram-Elites. We test on a tile-based side-scrolling platformer, vertical platformer, and roguelike. For all three, n-gram operators outperform standard operators and random n-gram generation, finding more usable (i.e. completable and generable) solutions at a faster rate. By integrating structure into operators, instead of fitness, these genetic operators could be beneficial to QD in PCGML.
