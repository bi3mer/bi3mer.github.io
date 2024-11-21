+++
date = '2019-09-08T18:03:23-05:00'
draft = false
title = 'Ring Buffers'
+++
In my [last post](../harry-potter-n-grams/) I discussed n-grams and gave an example of them being used on the text of Harry Potter but I didn't cover the implementation and instead linked the source. Today, I want to go over a key data structure used in my implementation: ring buffers (also known as a circular buffer).

A ring buffer needs a max size, `N`, that represents its max capacity. Until the buffer has reached its max capacity, it is exactly like a list. However, once the max capacity is reached the buffer will drop elements when new ones are added resulting in a first in first out (FIFO) behavior. An example of this data structure in action can be seen below. We initialize a ring buffer of size three. At first the ring buffer acts like a list but stops when the fourth element is added. On this add, the ring buffer drops the 0 because it was the first element added and the buffer has reached its max capacity of three. Say, for example, we ran this again and added a four. The buffer would then be `[2,3,4]` because the one would be the next element to be dropped.

```python
>>> from DataStructures import RingBuffer
>>> rb = RingBuffer(3)
>>> rb.buffer
[]
>>> rb.add(0)
>>> rb.buffer
[0]
>>> rb.add(1)
>>> rb.buffer
[0, 1]
>>> rb.add(2)
>>> rb.buffer
[0, 1, 2]
>>> rb.add(3)
>>> rb.buffer
[1, 2, 3]
```

Now that we have an idea of how the ring buffer is supposed to behave, we can implement it. The first thing we should do is define are initialization function for the class. In this case, we know that we must receive `N` but don't need anything else from the user.

```python
def __init__(self, buffer_limit):
    self.buffer_limit = buffer_limit
    self.buffer = []
```

With our buffer and size handled in the initialization, we can then go into the important function of the buffer: `add`. This is the function that implements the circular behavior we saw above. To do this we have first have to check whether or not the array is full by using `N` and comparing it to the length of the buffer. If the buffer has reached max capacity then we remove the first element of the buffer with `self.buffer.pop(0)`. Afterwards, we can then add the value to the buffer by appending it to the end.

```python
def add(self, value):
  if self.full():
    self.buffer.pop(0)

  self.buffer.append(value)

def full(self):
  return len(self.buffer) == self.buffer_limit
```

You can also add additional functions like `get` as a way to get individual elements from the buffer by index which can be seen in the [source implementation](https://github.com/bi3mer/nlp_experiments/blob/master/DataStructures/RingBuffer.py). There is also a great implementation on [github](https://github.com/UCRBrainGameCenter/BGC_Tools/blob/master/DataStructures/Generic/RingBuffer.cs) that a good friend of mine coded in C#. The code I have provided is not the most efficient implementation of the data structure but does, in my opinion, get across the way it is supposed to function best. It is a data structure that I use fairly regularly and wish came with languages but since it does not I recommend to most programmers to learn about it and how to implement it. It's a very good tool to have in the toolbox.