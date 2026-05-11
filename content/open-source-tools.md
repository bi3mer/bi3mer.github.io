---
date: '2024-11-22T09:34:57-05:00'
draft: false
title: 'Open Souce Tools'
showtoc: false
hideMeta: true
showTitle: false
showReadingTime: false
disableShare: true
---
## Post-Dissertation Work
- [adjust.h](https://github.com/bi3mer/adjust.h/blob/main/adjust.h) - A single header library written in `c11` for adjusting hardcoded values while the application is running.
- [fsm.h](https://github.com/bi3mer/fsm.h) - A single header library written in `c11` used for simple state management in games.

## Dissertation Work
- [Ponos](https://github.com/bi3mer/ponos) - A tool for building a [Markov Decision Process](https://en.wikipedia.org/wiki/Markov_decision_process) that assembles video game levels for dynamic difficulty adjustment. It is the work behind my dissertation, and it combines the work of three of my papers into one.
  - [ponos-example](https://github.com/bi3mer/ponos-example) - A repo to provide an example of how Ponos could be used for *Mario*.
- [GDM](https://github.com/bi3mer/GDM) - GDM stands for graph based decision making. This repo allows the user to define a graph that is operated on as a [Markov Decision Process](https://en.wikipedia.org/wiki/Markov_decision_process) to compute an optimal policy. This tool is used in my paper ([Level Assembly as a Markov Decision Process](https://arxiv.org/pdf/2304.13922)) and [my dissertation.](https://bi3mer.github.io/pdf/2025_colan_biemer_dissertation.pdf)
  - [GDM-TS](https://github.com/bi3mer/GDM-TS) - A [TypeScript](https://www.typescriptlang.org/) version of [GDM](https://github.com/bi3mer/GDM) that is used for online player studies.
  - [GDM-Editor](https://github.com/bi3mer/GDM-Editor) - A tool for modifying and building [GDM](https://github.com/bi3mer/GDM) graphs by hand.