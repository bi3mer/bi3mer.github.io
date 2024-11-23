---
date: '2024-11-24T05:40:43-05:00'
draft: false
showtoc: true
title: 'Panning and Zooming for a Node Graph Editor with Tkinter'

---
# Motivation 
As part of the work for my dissertation, I am building a tool that allows users to edit a [Markov Decision Process (MDP)](https://en.wikipedia.org/wiki/Markov_decision_process). This relates to my paper, [*Level Assembly as a Markov Decision Process*](https://arxiv.org/pdf/2304.13922). This work is different because I am representing the MDP as a graph. Every node in the graph is a state, and a state is a level segment. Every edge represents an action. Levels are formed by connecting states together. I also have some metadata in the edges, which are [links](https://arxiv.org/pdf/2203.05057) between level segments. 

The UI had a couple of requirements:

- Nodes are related to text files
- Nodes need an editable field for `reward`
- Nodes can be connected to each other with directed edges
- Nodes can be moved throughout the user interface

To do this, I made the decision to use [Tkinter](https://docs.python.org/3/library/tkinter.html) based on two factors. One, I've used it before with some success. Two, Tkinter has an easy way to draw arrows: [`create_line`](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html). The function can be passed an argument to put an arrow at either the beginning or the end. 

The process was fairly smooth, and I don't want to write about simple things like [how to draw a rectangle](https://stackoverflow.com/questions/42039564/tkinter-canvas-creating-rectangle) when that information is readily available online. Instead, this post is on the problem I ran into after implementing the above requirements.

# The Problem
![](/images/gdm-editor/graph.png "Sample graph in the editor." )

The picture above hints at the problem with making a node graph editor: the size of the graph. An editor implementing only the above requirements is fine if the graph is small. However, a graph with 100 nodes won't fit inside the screen. Therefore, the UI needs a way for the user to pan around the UI. Ideally, they could also zoom in or out to get a birds-eye-view of the graph. It's a feature seen in most node graph editors, but the standard functions from Tkinter weren't getting the job done for me. So, I had to implement panning and zooming myself.

# Implementing Panning

![](/images/gdm-editor/panning.gif "Example of panning. Without meaning to, I almost made a perfect loop.")


I used pressing down on the mouse wheel for panning. It's maybe not the most friendly design choice for laptop and Apple users, but the tool is mainly for my use anyway, so I decided to go with what felt natural. To do this, you have to bind some functions with Tkinter.

```python
self.root.bind("<Button-3>", self.pan_start)
self.root.bind("<B3-Motion>", self.pan)
```

The first function, `pan_start`, is very simple. It marks the location of the mouse when the mouse wheel is pressed.

```python
def pan_start(self, event):
    self.pan_x = event.x
    self.pan_y = event.y
```

The second function, `pan`, runs for as long as the mouse wheel is pressed down.

```python
def pan(self, event):
    dx = event.x - self.pan_x
    dy = event.y - self.pan_y

    for N in self.G.nodes.values():
        self.move_node(N, dx, dy)

    self.pan_x = event.x
    self.pan_y = event.y
```

It calculates the difference between the previous mouse position and the current one, uses it inside the for loop, and updates the mouse position for the next frame. The more complicated part is in the function called in the `for` loop: `move_node`.

```python
def move_node(self, n: CustomNode, dx: float, dy: float):
    ## Update rectangle placement
    self.canvas.move(n.rect_id, dx, dy)
    self.canvas.itemconfig(n.rect_id, tags=("rect", "dragged"))

    x1, y1, _x2, _y2 = self.canvas.coords(n.rect_id)
    n.frame.place(x=x1+self.scale, y=y1+self.scale)
    n.x += dx
    n.y += dy

    ## Update Edge coordinates
    # outgoing
    for tgt in n.neighbors:
        line_id = self.G.get_edge(n.name, tgt).line_id
        coords = self.canvas.coords(line_id)
        self.canvas.coords(
            line_id, 
            x1 + NODE_WIDTH * self.scale, 
            y1 + NODE_HEIGHT / 2 * self.scale, 
            coords[2], 
            coords[3]
        )
    
    #incoming
    for edge in self.G.incoming_edges(n.name):
        coords = self.canvas.coords(edge.line_id)
        self.canvas.coords(
            edge.line_id, 
            coords[0],
            coords[1],
            x1,
            y1 + NODE_HEIGHT / 2 * self.scale
        )
```

You'll notice the class `CustomNode` in the function definition. That is an extension to [`Node`](https://github.com/bi3mer/GDM/blob/main/GDM/Graph/Node.py), which is part of a library I made called [GDM](https://github.com/bi3mer/GDM/tree/main). The specifics aren't important, but having a tool that modeled a graph underneath the UI representation improved my life when implementing panning and zooming. You'll also notice the use of the `self.scale` variable, which is relevant for the next section, so just ignore it for now. 

`move_node` works in two sections. The first section moves the node. The second section moves the edges, incoming and outgoing. Starting with the node, you can see that the rectangle and the frame---the frame has the label (i.e., the title of the node) and the entry field for the `reward`. Moving those is all that is necessary for the UI to be updated. After that, you can see that the node's `x` and `y` coordinates were updated. This is for the underlying data in the node graph. While this was not strictly necessary, a bit of data duplication made working with Tkinter way more easy. This consideration, and ones like it, were why I ultimately regretted the choice of using Tkinter. In hindsight, I should have used [pygame](https://www.pygame.org/news) or something more like it, and my life would have been a lot better overall. 


The second part updates incoming and outgoing edges. The underlying data structure of a graph with GDM made it very simple to find these edges. Each edge also had a member variable `line_id`, which was how the UI for the edge could be accessed. The code in both `for` loops updates the relevant coordinates based on where the node was just moved to. It does not update both because that is relevant to another node, which may or may still need to be moved. 

With that done, you can see the behavior in the gif above. 

# Implementing Zooming In and Out

![](/images/gdm-editor/zooming.gif "Example of zooming in and out.")

Zooming in and out was more challenging than I had initially thought. The reason is that everything is connected to the current zoom or `scale` level, as shown by the fact that `self.scale` was necessary for all the `move_node` code. Without the scale being part of that code, edges looked disconnected from nodes, and arrows pointed at nothing. So, in short, there were just a bunch of edge cases to take care of. 

I made `self.scale` part of the [JSON](https://www.json.org/) representation that was stored by the editor. Then, when creating a node `self.scale` had to be used whenever a coordinate was used. It had to be used whenever a node was being dragged. It had to be used whenever an edge was being added. It had to be used everywhere. So, there isn't much to actually write specifically. Instead, I'll point you to the [code](https://github.com/bi3mer/GDM-Editor/blob/main/editor.py) if you are interested. Just search for `self.scroll`, and you can see all the uses. There isn't anything complicated once you see it. It just takes a while to get done.

# Conclusion

![](/images/gdm-editor/zooming-and-panning.gif "Example of zooming and panning together.")

One particular problem I ran into was combining panning and zooming. Before I had the implementation right, I had arrows flying around to all sorts of wrong coordinates. Again, the solution wasn't complex or particularly difficult to find. It just took fiddling with the implementation to find where I had made mistakes or forgotten to add a multiplication by `self.scale`. So, the conclusion here is that panning and scaling are not hard to implement. Tedious for sure, but not hard.