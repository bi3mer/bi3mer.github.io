+++
date = '2024-11-21T12:03:38-05:00'
draft = false
title = 'Making Rush Hour 2: Github and Matrix Formats'
+++

# Source Control and GitHub
[GitHub](https://github.com/) is an awesome website that allows you to have unlimited repositories, for free, that are backed up with [git](https://git-scm.com/) on a remote server. In addition, it provides you with helpful tools like [issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues) that allow you to keep track of bugs, features, and anything else you want. It is not the end all be all of [source control](https://aws.amazon.com/devops/source-control/) and has [pros and cons that should be considered](https://www.timedoctor.com/blog/git-mecurial-and-cvs-comparison-of-svn-software/) before being used.

For our use case, github is the perfect option because it is a free service that allows anyone to see our code easily. Other services, are either going to cost money or make it difficult to distribute the code. With that said, we are using version control for more than just visibility. For every project, working with version control is mandatory. If you plan on working with a group, then it provides a single workspace where you don’t have to manage a set of files and combining them. It allows you to revert back if you’ve made a huge mistake. It allows you to experiment on separate branches while not breaking the main branch.

The list that I provided is drastically shorter than the whole, but feel free to search google for more examples of why you should use source control. Regardless, please do not make the mistake of thinking that version control is only for group projects. It is for all projects.

![](/images/unblockme/python-gitignore.png "Adding Python as the `.gitignore` file")

With that said we can now create our repository. To create a github account, go to their create an account page and sign up (it’s free). From there, follow their [instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories) on creating a repository and make sure to set the dropdown menu “Add .gitignore” to “Python” as seen in figure one. I named my repository [UnBlockMeSolver](https://github.com/bi3mer/UnBlockMeSolver), but any name that is descriptive and follows these [guidelines](https://gravitydept.com/blog/devising-a-git-repository-naming-convention) is fine (make sure to avoid special characters like #, %, :, etc.).

# Matrix Board Formats

For me, defining a program that is configurable is of the utmost importance. I personally believe it leads to better design and creates more robust programs. When making games, I want to make it so designers can easily change behavior without having to come to me to get the changes in. Usually this means exposing some kind of file that they can modify. The first step in our game’s configurability is to create a file format for defining a board.

Looking at the requirements we defined in the [last post](../making-rush-hour-1), we know that every piece on the board has a unique identifier. This means `'1'`, `'abc'`, and `'b'` are technically viable piece names. However, I personally would like to exclude the id ‘abc’ if possible. If we restrict an id to having at most one character than we lose some flexibility but have an easier implementation. The flexibility we lose is an, almost, unlimited number of unique identifiers. Instead we will only have approximately 36 ids (26 letters in the alphabet plus 10 numbers of zero to nine). With that said, we technically have more with symbols and special characters but it would be an inconvenience for designers to type out. We can have even more if we include capitals and lower case characters.

Only having around 36 items on a board really isn’t going to hinder us. Our initial goal is to work with boards that are 6x6 which is the standard for both Rush Hour and Unblock Me. It is impossible, therefore, for us to have greater than 18 pieces on the board (18 2x1 pieces would perfectly fill the board). Since we know 36 unique identifiers will not hinder us, we now have to ask whether we can see cases in the future where this will change. I personally can see a case where I may want to test on a bigger board, however, I see that future as very unlikely. So, instead I’m going to update the first requirement to be, “The board will be represented by a two dimensional matrix that contains unique character identifiers for each block."

With that update completed, we now to handle the second and third requirements:

- The board will have a unique identifier which represents the goal.
- The board will have a unique identifier which represents the red block or main block.

We need to define constants for the goal and the the main block. But that is actually incomplete. We also need to define a constant for empty space. In addition, I’ve decided to add some extra complexity to our version by allowing there to be walls. These walls will be unable to move and take up one or more spots.

```python
wall        = "|"
goal        = "$"
empty       = "0"
playerPiece = "*"
```

These constants could be random characters, but since they will be exposed to designers it is important to make them as easy to understand as possible.

![](/images/unblockme/example.png "Sample Unblock Me board")

The last step is to produce a sample map that we can use when testing our parser. To do so, we can copy the map seen in figure two into our format:

```text
010000
010020
**3020$
003000
400555
400000
```

What you probably notice is that our goal is sticking out. This complicates are implementation because we will have unequal dimensions. This now puts us in a situation where can either modify a requirement, again, or update the definition of the matrix to hide this issue.

Updating the requirement would likely mean removing the goal from the matrix. Instead we would create a required field where we defined the x and y coordinates of the goal.

```text
(6,2)
010000
010020
**3020
003000
400555
400000
```

I personally don’t like this option because it complicates our parsing and sets up weird edge cases where we aren’t technically worried about going out of bounds of the matrix to find the solution for the game.

Alternatively, we could simply surround the whole matrix with walls. This makes it so we can still define a goal wherever we want and now have a full matrix where special cases are not needed to be handled. With that update we would now have the following matrix in a file:

```
||||||||
|010000|
|010020|
|**3020$
|003000|
|400555|
|400000|
||||||||
```

Technically, the walls on top can be avoided but I’m imagining cases in the future where we use these walls to help the GUI properly render the board. It may not come into fruition, but it won’t hurt.


# Update (2024/11/21)

Part of the [process of updating my website](../updating-my-site-to-hugo) has been converting converting all my old posts to new ones. Coming across this one was odd because I know I worked a lot on the codebase. If you look at the [repository](https://github.com/bi3mer/UnBlockMeSolver), you'll see that I implemented the game, a server with [Heroku](https://www.heroku.com/) working with documentation, and a solver. I was working on puzzle generation, and I had some work going on improving the solver with heuristics. In short, I had a lot of stuff to write about. However, I didn't and I don't remember why. So, for anyone who enjoyed these two posts, apologies that I didn't continue.