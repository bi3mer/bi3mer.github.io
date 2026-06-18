+++
date = '2026-06-18T09:30:25-05:00'
draft = true
title = 'LeetCode 32'
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

I feel safe assuming that other valid parentheses would be "(())", but the problem doesn't tell us whether that length would be one or two. I assume two, but I have no way to tell, so let's just figure it out. Oh! This problem is listed as... <span style="color:red">HARD</span>!!!

# Solution 1: Stack

```go
func longestValidParentheses(s string) int {
    stack := []int{-1}
    longest := 0
    n := len(s)

    for i := 0; i < n; i++ {
        c := s[i]
        if c == '(' {
            stack = append(stack, i) // push
        } else {
            stack = stack[:len(stack)-1] // pop
            if len(stack) == 0 {
                stack = append(stack, i) // push
            } else {
                longest = max(longest, i-stack[len(stack)-1])
            }
        }
    }

    return longest
}
```

The worst solution would have been `O(n³)` where `n=len(s)`, and I was tempted, but I didn't bother. After doing so many leetcode problems---as if 15 problems were a lot when I know others have done hundreds, maybe thousands of these hellish things---I decided that I would rather get the problem done quickly. Especially a "hard" problem.

I digress.

The solution above is a [stack-based](<https://en.wikipedia.org/wiki/Stack_(abstract_data_type)>) solution. So we `push` and we `pop`. (Imagine putting plates on top of other plates and then taking them off when you use them and you get what a `stack` is.) Instead of plates, we are using indices into `s`.

The solution loops through `s`, one character at a time.[^bytenote] Then there are two cases to handle. The first case is the open parentheses case. In this case, we push to the stack the current index and move on to the next iteration of the loop. Why are we pushing an index? Great question. I'll answer it in a moment.

The second case is when `c==')'` and is implicitly handled by the `else`. Inside the `else`, we have two cases. Before that, we `pop` from the stack. We do this because we are going to use that index. One question you may have, though, is what about the case of `s=")"`. Won't that break? Go back to the top of the function and you'll see that we initialized the stack with the value of negative one. No out of bounds case.

If the stack is length zero, then we push to the stack the current index and we can continue the loop. This does more than that, though. It closes a previously open parenthesis. Otherwise, we have reached an invalid closing parenthesis.

This is the only "clever" part of the solution.[^clever] The line of code is: `longest = max(longest, i-stack[len(stack)-1])`. The intent is to see if a new `longest` set of valid parentheses have been found. The tricky part is `i-stack[len(stack)-1])`. Figuring out this one statement is pretty much the reason why this problem is listed as hard.

To see what it does, let's use an example: `s=")()()"`. The longest valid string for this input is `"()()"`, and the expected output is four. Simple. Now let's look at the internals for each iteration through the `s`:

```
i=0, c=')', pop -1, push 0, stack=[0]
i=1, c='(', push 1, stack=[0,1]
i=2, c=')', pop 1, longest=max(longest, 2-0->2), stack=[0]
i=3, c='(', push 3, stack=[0,3]
i=4, c=')', pop 3, longest=max(longest,4-0->4), stack=[0]
```

So, what this is doing is using the last known location of an invalid start. That is why we seed with `-1` at the start, and that is why we push invalid locations knowingly. The logic is almost inverted: instead of tracking valid runs directly, we track the boundaries between them.

# Solution 2: O(1) Memory

# Benchmark

# Conclusion

[^bytenote]: I used `for i := 0; i < n; i++` rather than `for i, c := range s`. The reason can be seen in my post for [LeetCode 20.](/posts/leetcode-20#benchmark) If you don't want to click the link to the other post, the basic idea is simple. Ranging over a string in Go gives you runes, which means UTF-8 decoding on every character in `s`. Since we only ever see '(' and ')' in this problem, that work is completely unnecessary. It is also completely unnecessary to optimize a LeetCode problem in this manner.

[^clever]: When I say clever what I am trying to say is that what the code does is non-obvious or it has layers to it. I'm not complimenting myself. In some ways I am insulting myself since I prefer my code to be simple and obvious.
