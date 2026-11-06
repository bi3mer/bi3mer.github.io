+++
date = '2018-04-20T12:25:07-05:00'
draft = false
title = 'Visualizing Sorting Algorithms with OpenGL'
+++
If you’ve read my previous posts, then you know I love python. Regardless, it has been a goal of mine to be proficient in c++. I’m not exactly sure why I’m fascinated with this language that I have no uses cases for, but I think it stems from my love of video games. C++ is used extensively by my favorite company, Blizzard Entertainment, and sees a wide range of use across the industry. In addition, it also is apart of a field that is of particular interest for me, AI. For example, [tensorflow](https://github.com/tensorflow/tensorflow) is implemented in c++.

With my interest in c++ in mind, I decided to write a few sorting algorithms as a way to practice using the language without doing anything too extensive. What resulted was a series of dull [challenges](https://github.com/bi3mer/challenges) which really tells you nothing about me as a programmer and if I can do anything. However, I recalled watching these [youtube videos](https://www.youtube.com/watch?v=kPRA0W1kECg) from when I was freshman first learning the algorithms and decided visualizing my implementations may be a way to add some spice to what was otherwise a very dull set of implementations.

# Quick Sort Implemented in c++

```c++
int partition(int* a, int low, int high) {
    int lowIndex = low - 1;
    int pivot    = a[high];

    for(int i = low; i < high; ++i) {
        if(a[i] <= pivot) {
            ++lowIndex;
            std::swap(a[lowIndex], a[i]);
        }
    }

    ++lowIndex;
    std::swap(a[lowIndex], a[high]);

    return lowIndex;
}

void quickSortImplemented(int* a, int low, int high) {
    if(low < high) {
        int pi = partition(a, low, high);

        quickSort(a, low, pi - 1);
        quickSort(a, pi + 1, high);
    }
}

void quickSort(int* a, int length) {
    quickSortImplemented(a, 0, length - 1);
}
```

# Installing Glut on Ubuntu
Glut is a way for c++ to be able to talk to [OpenGL](https://www.opengl.org/) and draw things. For installing glut I found a helpful [article](https://www.codeproject.com/Articles/182109/Setting-up-an-OpenGL-development-environment-in-Ub) which gave me the installation commands I needed to run:

```bash
sudo apt-get install mesa-common-dev
sudo apt-get install freeglut3-dev
```

They also provide a sample program that will draw a white square on a black background.

```c++
#include "GL/freeglut.h"
#include "GL/gl.h"

/* display function - code from:
     http://fly.cc.fer.hr/~unreal/theredbook/chapter01.html
This is the actual usage of the OpenGL library. 
The following code is the same for any platform */
void renderFunction() {
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(1.0, 1.0, 1.0);
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0);
    glBegin(GL_POLYGON);
        glVertex2f(-0.5, -0.5);
        glVertex2f(-0.5, 0.5);
        glVertex2f(0.5, 0.5);
        glVertex2f(0.5, -0.5);
    glEnd();
    glFlush();
}

/* Main method - main entry point of application
the freeglut library does the window creation work for us, 
regardless of the platform. */
int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE);
    glutInitWindowSize(500,500);
    glutInitWindowPosition(100,100);
    glutCreateWindow("OpenGL - First window demo");
    glutDisplayFunc(renderFunction);
    glutMainLoop();    
    return 0;
}
```

With our packages and program we can now test to see if it will run. To test, input the following in your terminal. Please note, I assume you’ve named this file main.cpp in the commands below.

```bash
g++ main.cpp -lGL -lGLU -lglut
./a.out
```

# Drawing in OpenGL with Glut
Now that we can draw things, we need to understand how exactly we are drawing. The first thing to notice in the sample program above, is how it draws the square where every vertex has either `-0.5` or `0.5` for the x and y axis.

![](/images/opengl-sorting/drawing.png "Representation of square generated in sample code for OpenGL")

As you can see in figure one, [source code here](https://github.com/bi3mer/graphing_code/blob/master/opengl_sorting/opengl_rectangle.py), the blue square is the square we see when running our c++ code. The black lines represent the axis and ultimately show us how we are expected to draw with this framework. -1 to 1 are the boundaries on both the x and y axis. So the vertex `(-1,-1)` would be the bottom left of the screen and `(1,1)` would be the top right.

# Drawing a Frame
A frame for us is a visual representation of the array we are sorting and the progress. Therefore, before we can starting writing code we have to define the array we want to visualize. Luckily, this is fairly simple because our goal isn’t to write something super generic. Our one and only goal is to write something that visualizes the sort. WIth that in mind let’s assume an array is a set of integers ordered from 0 to n, where n is some arbitrary length greater than 0.

```c++
int* arr = (int*) malloc(sizeof(int) * length);
for(int i = 0; i < length; ++i) {
    arr[i] = i;
}
```

Please note, I’m aware that the `malloc` isn’t necessary but it will come into play later so please just bear with me. With our array now defined, we need a render function that will be able to draw rectangles for each and every element of the array inside of our window. These rectangles need to scale based on the size of the array.

```c++
void renderFunction() {
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(1.0, 1.0, 1.0);
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0);
    
    float l = (float) length;
    float widthAdder = 1/l;

    for(int i = 0; i < length; ++i) {
        glBegin(GL_POLYGON);
        
        // + 1 so value of 0 has height of 1
        float arrayIndexHeightRatio = 2*(arr[i] + 1)/l;
        float widthIndexAdder = 2*i/l;

        float leftX   = -1 + widthIndexAdder;
        float rightX  = leftX + widthAdder;
        float bottomY = -1;
        float topY    = bottomY + arrayIndexHeightRatio;

        // bottom left
        glColor4f(1,0,0,0);
        glVertex2f(leftX, bottomY);

        // bottom right
        glColor4f(0,1,0,0);
        glVertex2f(rightX, bottomY);

        // top right
        glColor4f(0,0,1,0);
        glVertex2f(rightX, topY);

        // top left
        glColor4f(0,0,0,1);
        glVertex2f(leftX, topY);

        glEnd();
    }

    glFlush();
}
```

Now there is a decent bit going on here, so let’s break it down. The most important thing to notice is that I’m using variables `arr` and `length` without ever having declared them or passed them into the function. The unfortunate reality here is that there is no way, that I could find, to pass a variable into the render function. Now I imagine a class would resolve this, but I used a global because I knew this code would only be used once. If I thought, for even a second, that I would use it again then I would have attempted the class approach or anything to avoid having these horrible globals.

The first set of commands is clearing the screen so we can draw on it without drawing over anything else. After that we convert the length to a float so we can divide by it without worrying about integer rounding. We then create this variable called `widthAdder` which is how long, widthwise, a rectangle will be. Also, please note, you could do `2/l` instead which would cause the rectangles to touch as seen in figure two.

| `1/l` | `2/l` |
|:-----:|:-----:|
| ![](/images/opengl-sorting/i_over_l.png)  | ![](/images/opengl-sorting/2i_over_l.png)  |


We now begin looping over every element of the array to draw the rectangle that represents the given element. We use the element’s index to determine where it is located along the x axis and the actual value to determine the height. To start we call a function `glBegin` with an enumeration to a polygon. With every `glBegin` call there will always be a `glEnd` call that you see at the end of the loop. After the begin call we create a variable which represents the height of the index. We calculate this by taking the value and adding one, this ensures the zero value will be shown, and multiplying the result by two. This multiplication allows us to use the entire screen of negative one to one. We then divide by the length of the array to properly scale the result. You’ll notice that the +1 we used for making 0 show on the screen also set the scaling to a proper factor. The other way to resolve this would have been to divide by the length subtracted by 1.

The next variable allows us to find the starting x coordinate before subtracting by one. We take the index of the element and divide by the length. From there we multiply it by two. Once we subtract by one we will have the starting left x coordinate.

With this math completed, all we have to do is finish up our variable definitions for the four corners of the rectangle and draw out the vertices. You’ll notice that I added colors to the vertices as well so the resulting graphs would be prettier. The results of this can be seen in Figure 2 after [randomizing the array](https://www.geeksforgeeks.org/shuffle-a-given-array-using-fisher-yates-shuffle-algorithm/) for an array of size `500`.

![](/images/opengl-sorting/sample_graph.png "Figure 2: Sample graph generated for a randomized array")

# Visualizing the Sort
Now we want to redraw the entire screen after every single swap (an optimization for this would be to only redraw the areas of the screen for the two rectangles that are swapped). The easiest way to do this is to write our own version of swap that will still use the std::swap function, but also call the render function.

```c++
void swap(int index1, int index2) {
    std::swap(arr[index1], arr[index2]);
    renderFunction();
    usleep(delay);
}
```

You’ll notice that I take advantage of the horrible global and actually don’t pass it in. In addition, I’ve added an extra line `usleep(delay)` which pauses the execution for however many milliseconds. This makes it so we can actually see the sort happening. This function call isn’t necessarily ideal for all operating systems and using boost instead would be optimal. In addition, you’ll notice that delay is also undefined and must therefore be a global. This is the third and second to last global (length is the second).

With swapping implemented, we now need a generic way of passing our sorting algorithm to the visualizer. Luckily, c++ gives us an easy way to pass functions.

```c++
int setUpGlutAndArray(int argc, char** argv, void (*sortingAlgorithm)(int*, int)) {
    sort = sortingAlgorithm;
    arr = (int*) malloc(sizeof(int) * length);
    for(int i = 0; i < length; ++i) {
        arr[i] = i;
    }

    randomizeArray(arr, length);

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE);
    glutInitWindowSize(length,length);
    glutInitWindowPosition(100,100);
    glutCreateWindow("Sort Visualization");

    glutDisplayFunc(renderFunction);
    glutKeyboardFunc(keyboardEvent);

    glutMainLoop();
}
```

This function sets our fourth and final global, the swapping algorithm. After that, it does the exact same things from the original main function we have above, except, there is now a keyboard function and a randomize array function.

The keyboard function is called on keyboard events and takes in a few arguments. In our case we use this event to handle the escape key, 27, and s key, 115. When the escape key is pressed we quit out. When the s key is pressed, we start the sort.

```c++
void keyboardEvent(unsigned char c, int x, int y) {
    if(c == 27) {
        // exit on escape key pressed
        exit(0);
        free(arr);
    } else if(c == 115) {
        // start on `s` key pressed
        sort(arr, length);
    }
}
```

What we now have is a complete program and all we have to do is set up our main function. Say we wanted to see how quicksort looked. Then we could create a main function underneath our quicksort code from above; please note that the sorting algorithm will have to use the new swap function. Sample source code can be found [here](https://github.com/bi3mer/challenges/blob/master/Challenge021_QuickSort/main.cpp).

```c++
int main(int argc, char* argv[]) {
    srand(time(NULL));
    delay  = 1500;
    length = 500;
    setUpGlutAndArray(argc, argv, quicksort);
    free(arr);

    return 0;
}
```

And when running and after pressing s, we would get the gif seen in Figure 3.

![](/images/opengl-sorting/quick_sort.gif "Figure 3: Example gif produced from running quicksort.")

# Conclusion

If I wanted to spend more time on this then the first thing I would do is remove all four of those horrible globals. However, besides that one element I’m pretty happy with the result. I think the visualization came out looking pretty good and it was shocking to see just how much faster quicksort really is then something like bubble sort. In addition, it was also just good experience to work in OpenGL and familiarize myself with tools that are a little outside of my comfort zone.