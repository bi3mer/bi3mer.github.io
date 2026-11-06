+++
date = '2026-06-19T07:30:25-05:00'
draft = false
title = 'LeetCode 32: Longest Valid Parentheses'
url = '/posts/leetcode-32/'
+++

We are now on [LeetCode 32](https://leetcode.com/problems/longest-valid-parentheses/). It is titled, "Longest Valid Parentheses," and the problem definition is wonderfully sparse: "Given a string containing just the characters '(' and ')', return the length of the longest valid (well-formed) parentheses substring."

```
Example 1:
  Input: s = "(()"
  Output: 2

Example 2:
  Input: s = ")()())"
  Output: 4

Example 3:
  Input: s = ""
  Output: 0
```

Oh! This problem is listed as... <span style="color:red">HARD</span>!!!

# Solution 1: Single Pass Stack

The worst solution would have been `O(n³)` where `n=len(s)`, and I was tempted, but I didn't bother. After doing so many leetcode problems---as if 15 problems were a lot when I know others have done hundreds, maybe thousands of these hellish things---I decided that I would rather get the problem done quickly. Especially a "hard" problem.

I digress.

```go
func longestValidParentheses(s string) int {
    var st Stack[int]
    st.Push(-1)
    longest := 0

    for i := 0; i < len(s); i++ {
        if s[i] == '(' {
            st.Push(i)
        } else {
            st.Pop()
            if st.Len() == 0 {
                st.Push(i)
            } else {
                top, _ := st.Peek()
                longest = max(longest, i-top)
            }
        }
    }

    return longest
}
```

The solution above is a [stack-based](<https://en.wikipedia.org/wiki/Stack_(abstract_data_type)>) solution. So we `push` and we `pop`. (Imagine putting plates on top of other plates and then taking them off when you use them and you get what a `stack` is.) Instead of plates, we are using indices into `s`. You'll also notice the use of this `Stack` type but it doesn't exist anywhere in the code. You can find it [here.](/go_code/#stack) (I decided that I'm using a stack too often not to have a convenient helper.)

The solution loops through `s`, one character at a time.[^bytenote] Then there are two cases to handle. The first case is the open parentheses case. In this case, we push to the stack the current index and move on to the next iteration of the loop. Why are we pushing an index? Great question. I'll answer it in a moment.

The second case is when `c==')'` and is implicitly handled by the `else`. Inside the `else`, we have two cases. Before either, we `pop` from the stack. We do this because we are going to use that index. One question you may have, though, is what about the case of `s=")"`. Won't that break? Go back to the top of the function and you'll see that we initialized the stack with the value of negative one. No out of bounds case.

If the stack is length zero, then we push to the stack the current index and we can continue the loop. This does more than that, though. It closes a previously open parenthesis. Otherwise, we have reached an invalid closing parenthesis.

This is the only "clever" part of the solution.[^clever] The line of code is: `longest = max(longest, i-top)`. The intent is to see if a new `longest` set of valid parentheses have been found. The tricky part is `i-top`, where `top` is the index peeked from the stack. Figuring out this one statement is pretty much the reason why this problem is listed as hard.

To see what it does, let's use an example: `s=")()()"`. The longest valid string for this input is `"()()"`, and the expected output is four. Simple. Now let's look at the internals for each iteration through the `s`:

```
i=0, c=')', pop -1, push 0, stack=[0]
i=1, c='(', push 1, stack=[0,1]
i=2, c=')', pop 1, longest=max(longest, 2-0->2), stack=[0]
i=3, c='(', push 3, stack=[0,3]
i=4, c=')', pop 3, longest=max(longest,4-0->4), stack=[0]
```

So, what this is doing is using the last known location of an invalid start. That is why we seed with `-1` at the start, and that is why we push invalid locations knowingly. The logic is almost inverted: instead of tracking valid runs directly, we track the boundaries between them.

# Solution 2: Double Pass

```go
func longestValidParentheses(s string) int {
    longest := 0
    n := len(s)

    // left-to-right pass
    open, closed := 0, 0
    for i := 0; i < n; i++ {
        if s[i] == '(' {
            open++
        } else {
            closed++
        }

        if open == closed {
            longest = max(longest, open*2)
        } else if closed > open {
            open, closed = 0, 0
        }
    }

    // right-to-left pass
    open, closed = 0, 0
    for i := n - 1; i >= 0; i-- {
        if s[i] == '(' {
            open++
        } else {
            closed++
        }

        if open == closed {
            longest = max(longest, open*2)
        } else if open > closed {
            open, closed = 0, 0
        }
    }

    return longest
}
```

Before I explain how this function works, I want to look at the runtime and the memory complexity. The runtime is `O(n)`. The reason being is that the function loops through the string twice and `2n` reduced down to `n` asymptotically. The space complexity is `O(1)`; only four `int` variables were used. Compare this to the stack-based solution. The runtime is `O(n)`, but there is a difference since it will only loop through the string once. The space complexity, though, is `O(n)` since you have to handle the worst case of `"(((((..."` where the stack grows and grows. So we get a nice tradeoff.

Now, let's see how the algorithm works.

It has two passes. Left to right and then right to left. In the left to right pass, it tracks the number of open and closed parentheses and increments the trackers. Then after incrementing `open` or `closed`, it has an if which checks if open is equal to closed. If so, `longest` is set if possible via `max`. The branch after the first `if` is an `else if` which checks if there are more closed parentheses than open, and, if so, it will reset the count. This will work for many inputs like `"()("` and `")))()()((()))("`, but it won't work for `"(()`. In that case we finish the loop with two open and one closed, so longest is never set.

That is why we have a second pass, but this time it is right to left. The logic inside the loop is the exact same as the logic of the previous pass except the `else if` condition which now checks if `open > closed`.

And that's the algorithm. It uses less memory and is, in my opinion, way easier to read, so I really like this solution.

# Benchmark

If you want to see the benchmarking code you can find it on [GitHub](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-32). Each benchmark runs with string lengths `n ∈ {100, 200, ..., 1000}` using `-count=10`, analyzed with `benchstat`, on an AMD Ryzen AI 9 HX 370.

<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>

<canvas id="chart-runtime" style="max-height:400px"></canvas>

<script>
new Chart(document.getElementById('chart-runtime'), {
  type: 'line',
  data: {
    labels: [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
    datasets: [
      {
        label: 'Stack',
        data: [163.5, 354.6, 454.0, 683.2, 743.1, 681.8, 928.0, 819.6, 1103, 980.9],
        borderColor: '#e15759',
        backgroundColor: '#e15759',
        fill: false,
      },
      {
        label: 'DoublePass',
        data: [140.3, 299.2, 436.3, 595.5, 754.3, 922.8, 1049, 1228, 1366, 1526],
        borderColor: '#4e79a7',
        backgroundColor: '#4e79a7',
        fill: false,
      }
    ]
  },
  options: {
    plugins: { title: { display: true, text: 'Runtime by string length' } },
    scales: {
      x: { title: { display: true, text: 'n (string length)' } },
      y: { title: { display: true, text: 'ns/op' }, beginAtZero: true }
    }
  }
});
</script>

At small `n`, DoublePass is faster: 140ns vs 164ns at `n=100`. This isn't surprising. DoublePass uses only four local integers and zero heap allocations, while Stack has to grow its internal slice. The cost of two loops begins to show at `n=500` where the two solutions are essentially tied (743ns vs 754ns). After that, Stack pulls ahead. The cost of two full passes becomes more costly than heap allocations for Stack.

Stack's variance in terms of time is also much higher (±11–20%) compared to DoublePass (±0–1%). This is because Stack's max depth depends on the input. If a string has many consecutive `'('`, then the stack will grow much larger. DoublePass just increments an integer.

On memory, Stack allocates between 120 B and 1016 B per call with 4–7 allocs, varying with how deep the stack grows. DoublePass allocates nothing to the heap.

# Conclusion

Implementing the stack-based solution was genuinely challenging. I had trouble getting the logic right for the indexes, and I think it shows in the length of that section. I really tried to explain it in a way that anyone with a programming background could understand. I hope I succeeded. In contrast, the second solution was much, much easier to program. It wasn't as easy to see exactly why I needed the two passes, but one quick example was all it took.

```go
func LongestValidParentheses(s string) int {
	if len(s) > 500 {
		return longestValidParenthesesStack(s)
	}

	return longestValidParenthesesDoublePass(s)
}
```

If we wanted to make a utility tool that had some optimizations, we could use something like the function above, where `longestValidParenthesesStack` and `longestValidParenthesesDoublePass` are just the two solutions renamed. I don't know if there is any big "lesson" here. I'm not a fan of the authoritative way it comes across when someone says "here are the key takeaways..." I just hope this post helped.

One last thing. I started these posts at [problem 17](/posts/leetcode-17/) because that was the first problem on the list that I hadn't done before. It feels wrong, though. So, I'm going to go back and do the earlier ones before moving on to the next problem in the list.

Till next time, friends.

[^bytenote]: I used `for i := 0; i < n; i++` rather than `for i, c := range s`. The reason can be seen in my post for [LeetCode 20.](/posts/leetcode-20#benchmark) If you don't want to click the link to the other post, the basic idea is simple. Ranging over a string in Go gives you runes, which means UTF-8 decoding on every character in `s`. Since we only ever see '(' and ')' in this problem, that work is completely unnecessary. It is also completely unnecessary to optimize a LeetCode problem in this manner.

[^clever]: When I say clever what I am trying to say is that what the code does is non-obvious or it has layers to it. I'm not complimenting myself. In some ways I am insulting myself since I prefer my code to be simple and obvious.
