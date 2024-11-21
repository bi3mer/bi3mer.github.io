+++
date = '2018-03-18T11:53:47-05:00'
draft = false
title = 'Making Rush Hour: Requirements and Basic Structuring'
+++

This is the first in a series of posts where I discuss implementing a version of [Unblock Me](https://apps.apple.com/us/app/unblock-me/id315019111) and [Rush Hour](https://en.wikipedia.org/wiki/Rush_Hour_(puzzle)); sample screen shots can be seen in figure one. For the implementation, I’ve decided to use Python 2.7, however, you should be able to follow along with any language. My hope is that each of these posts will be more than just a copy and paste tutorial. To facilitate this, I will be taking deep dives into design decisions, test-driven design, common game AI architecture, general software structure, requirements gathering, servers, and more.

# Why Python?
Choosing a language for a project is one of the most important decisions that you’ll have to make. It will define how you approach problems, what problems you feel comfortable solving, and even how fast your code will execute. For these reasons, and more, it is imperative to choose a language for a better reason than, “It’s my favorite programming language.”

Ironically, one of the main reasons I decided to use python for this project is that it is favorite language. My original goal was to show prospective employers an example project that goes beyond the usual, “I stopped once I got it working.” I wanted to create something that I would feel comfortable showing off not only for the functionality but also the code quality. WIth that in mind, I decided to use python because it would allow me to completely focus on the design and code quality thanks to my level of familiarity with the language.

In addition, I knew python would be the best bet in the long run because after implementing the game I intend to look into procedural generation of valid boards and machine learning techniques to generate a valid heuristic for [A* pathfinding](https://en.wikipedia.org/wiki/A*_search_algorithm). Both of these goals are well suited for python and the bonus isomorphism makes a life a tad bit easier in the future.

# Requirements
It may seem like common sense, but the most important part in programming is knowing exactly what the end goal is for the project. If you know the end goal, you can quickly program to those exact specifications without worry that something will change midway through. Unfortunately, the reality of software development is that things will change and the program will have to change with them. Therefore, it is necessary to develop fully knowing that code you’ve written yesterday will change to accomodate a new feature or idea. The best way to handle these changes is to design with flexibility in mind. Usually this means expecting the changes before they have been requested.

This can lead some to make the program so flexible that becomes unreasonable and out of scope. One particular moment of mine that stands as is when I decided to make a simple chess game. At the start I was programming with the obvious constraint of the board being in two dimensions. But I had a thought that it may be cool to make the game configurable so someone could play in two dimensions or higher. What resulted was a series of headaches and unnecessary pain for a feature that would never be used. Knowing the right kind of flexibility to add when developing software is key and something that comes with time.

In our case, we won’t have to worry about a project manager changing requirements midway through the project but we still have to worry about getting a bright idea that can change everything. Therefore, before even writing our first line of code we need to develop a set of requirements that will be true throughout the project. These requirements will define the core of the game.

- The board will be represented by a two dimensional matrix that contains unique identifiers for each block.
- The board will have a unique identifier which represents the goal.
- The board will have a unique identifier which represents the red block or main block.
- A block that is longer lengthwise than heightwise can only be moved horizontally one space or more.
- A block that is longer heightwise than lengthwise can only be moved vertically one space or more.
- A block that is equal in length and height cannot exist.
- A block can not be moved through another block.
- Only the main block can take the spot of the goal on the board.
- The game will end when the player has managed to slide the main block into the goal.

This is not a complete set of requirements, for more on this topic you can view [BelitSoft's standard](https://belitsoft.com/custom-application-development-services/software-requirements-specification-document-example-international-standard), but it does serve as a baseline for future development. Nothing we develop will go against these requirements. More rigorous requirements building in a professional environment is essential because they force everyone to be on the same page for what is going to be built.

# Structuring the Project
With our requirements complete, we can now work on defining how we want everything to be structured. The first decision is to figure out a proper file structure knowing we will have one main project with multiple, dependent, side projects. Therefore, a simple flat structure of python files being in the root directory is far too simple for our use case. We want to make everything clear and streamlined so users can easily find what they want.

The two popular solutions for this problem are to create separate repositories with [submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) to the required repositories or to use a a monolithic repository. The first solution isn’t ideal because it sets up cases where we can make changes to one repository that will force multiple dependent repositories to update. This issue becomes exacerbated when repositories are thrown of sync due to simply forgetting to update. Meaning, the main weakness of this approach is that we have to be hyper vigilant when making changes to any repository. The second option means we will have folders at the root for each part of the project we’ll want to build. This means linking them up may not be ideal. For example, one folder will contain the implementation of the game’s logic where another may be an implementation of the GUI. The GUI will be dependent on the games folder, just like with the submodule approach, and there will have to be a weird import set up to go to the root directory and grab the requirements. However, everything will always be in sync and thorough unit testing will make it clear when something has broken.

Neither of the two approaches are necessarily better than the other, but I ultimately went with the monolithic approach. The inconvenience of getting imports to work seemed minor to the headaches that would ensue with the submodules approach.

# Next Time
Next time, we’ll be starting off with setting up our github repository with our monolithic structure in mind. Once that is complete, we can get the basics of the game working by defining a format for a board that can be read from text files. Lastly, we’ll look into a structure for AI in games and how it will affect our design and implementation.