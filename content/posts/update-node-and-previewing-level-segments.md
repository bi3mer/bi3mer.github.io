---
date: '2024-11-25T09:18:27-05:00'
draft: false
title: 'Previewing Files with Tkinter'
showtoc: true
---
# Introduction
This is related to an [earlier post](../panning-and-zooming-for-a-node-graph-editor-with-tkinter) which was on panning and scaling a node graph visualized with [Tkinter](https://docs.python.org/3/library/tkinter.html). In this post, the goal is to implement a level preview function where when the user hovers over a node they can see the associated file in a rectangle that appears. When they stop hovering over the node, the preview should go away. 

Additionally, there is a section on writing an `update_node` function that simplified the [codebase](https://github.com/bi3mer/GDM-Editor).

# Implementing Preview File
![](/images/gdm-editor/preview.gif)

The gif above is the final product. It works by creating a frame and a label. The frame is where the label will be placed. The label is where the text goes.

```python
self.preview_frame = tk.Frame(self.canvas)
self.preview_frame.place(x=-1000, y=-1000) # off screen

self.preview_label = tk.Label(
    self.preview_frame, 
    width=32, 
    height=17, 
    font="TkFixedFont"
)
self.preview_label.pack()
```

- Preview frame is placed offscreen at `(-1000, -1000)`. It was recommended to use `pack` to make things appear and `pack_forget` to make them disappear. When I tried this, the window was resized to the size of the frame. Rather than waste a day figuring out exactly how it should be done in Tkinter, I decided to initialize the frame offscreen and place it onscreen when relevant.
- Width and height are hardcoded because I was lazy. They could be calculated based the string that is to be placed inside.
- `TkFixedFont` is a default monospace font. Monospace is important because the preview is for levels, and columns need to be aligned for a better view.

```python
def on_enter(event):
    self.preview_label.config(text=N.level)
    self.preview_frame.place(
        x=(N.x + NODE_WIDTH + 1) * self.scale, 
        y=N.y*self.scale
    )

def on_exit(event):
    self.preview_frame.place(x=-1000, y=-1000)

frame.bind('<Enter>', on_enter)
frame.bind('<Leave>', on_exit)
```

The code above is not exactly what you will find in the [codebase](https://github.com/bi3mer/GDM-Editor), but this is a the basic idea. Tkinter has events `<Enter>` and `<Leave>`. So, all we have to do is bind a function to each event. When the user's mouse enters the frame, we set the preview label to the text of the level, which is a member of node `N`. Then, the frame is moved based on node `N`'s position. However, note that this has to be scaled, else the preview window will be far away from where it should be. When the user's cursor leaves the frame, the `preview_frame` is placed offscreen again.

# Update Node
In my [last post](../panning-and-zooming-for-a-node-graph-editor-with-tkinter#implementing-zooming-in-and-out), I pointed out that the functions for moving a node and scaling one were very similar, and that it would be smart to make one function to handle both. I also said that I wasn't going to do it because I wasn't a perfectionist, and the code was only for me. While both of those facts remain true, I found myself implementing the preview function, and I wanted to clean up the code. So, I combined the two functions into one: `update_node`.

```python
def update_node(self, n: CustomNode, dx: float, dy: float):
    ## Update rectangle placement
    self.canvas.move(n.rect_id, dx, dy)
    self.canvas.itemconfig(n.rect_id, tags=("rect", "dragged"))

    x1, y1, _x2, _y2 = self.canvas.coords(n.rect_id)
    n.x += dx
    n.y += dy

    # rectangle
    self.canvas.coords(
        n.rect_id,
        n.x * self.scale,
        n.y * self.scale,
        (n.x + NODE_WIDTH) * self.scale,
        (n.y + NODE_HEIGHT) * self.scale
    )

    # frame
    n.frame.place(
        x = (n.x + 1) * self.scale,
        y = (n.y + 1) * self.scale
    )

    # entry
    n.entry.config(width=ceil(3*self.scale))

    ## Update Edge coordinates
    # incoming
    for tgt in n.neighbors:
        line_id = self.G.get_edge(n.name, tgt).line_id
        coords = self.canvas.coords(line_id)
        self.canvas.coords(
            line_id, 
            (n.x + NODE_WIDTH) * self.scale, 
            (n.y + NODE_HEIGHT / 2) * self.scale, 
            coords[2] , 
            coords[3]  
        )

    # outgoing
    for edge in self.G.incoming_edges(n.name):
        coords = self.canvas.coords(edge.line_id)
        self.canvas.coords(
            edge.line_id, 
            coords[0],
            coords[1],
            n.x * self.scale,
            (n.y + NODE_HEIGHT / 2) * self.scale
        )
```