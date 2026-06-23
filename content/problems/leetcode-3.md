+++
date = '2026-06-22T10:16:57-0500'
draft = false
title = 'LeetCode 3: Longest Substring Without Repeating Characters'
url = '/posts/leetcode-3/'
+++

[LeetCode Problem 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) is titled "Longest Substring Without Repeating Characters." As titles go, it's a bit on the nose for my taste.

```
Example 1:
  Input: s = "abcabcbb"
  Output: 3
  Longest substring: "abc"

Example 2:
  Input: s = "bbbbb"
  Output: 1
  longest substring: "b"

Example 3:
  Input: s = "pwwkew"
  Output: 3
  Longest substring: "wke"
```

The return is the length of the longest substring, not the string itself.[^aside]

# Failure is Just the Beginning

```go
func lengthOfLongestSubstring(s string) int {
    if len(s) == 0 || len(s) == 1 {
        return len(s)
    }

    done := true
    seen := make(map[byte]bool)
    var i int
    for i = 0; i < len(s); i++ {
        c := s[i]
        if _, ok := seen[c]; ok {
            done = false
            break
        }

        seen[c] = true
    }

    if done {
        return len(s)
    }

    return max(lengthOfLongestSubstring(s[0:i]), lengthOfLongestSubstring(s[i:]))
}
```

When I first started these problems, I really relished making the obvious but wrong solution. However, as time has gone by, I've decided to focus less on coding double for loops and instead just try to get the problem done so I can work on other stuff. Unfortunately, sometimes I go for glory and end up missing.

In the code above, I had the idea that once I run into a repeated character, I can use that as a split point and then return the max of the two substrings. This, though, was wrong because of the input: `"dvdf"`. The code breaks at the second `d` (i=2), which gives `max(longest("dv"), longest("df"))`, but the answer is `"vdf"`. The split cuts off the correct answer.

Then, for fun, I figured that I might as well see if I can make the wrong answer right.

```go
return max(
	lengthOfLongestSubstring(s[1:]),
	lengthOfLongestSubstring(s[:len(s) - 1]),
)
```

And this should work for every input. The problem is that it is way too slow, and it gets the error <span style="color:red">Time Limit Exceeded</span> for the input: `"qjoztdxbbwioczdwjddshnln"`.

# Giving Up On Being Smart

```go
func lengthOfLongestSubstring(s string) int {
    if len(s) == 0 || len(s) == 1 {
        return len(s)
    }

    longest := 1
    seen := make(map[byte]bool)

    for i := 0; i < len(s); i++ {
        clear(seen)
        seen[s[i]] = true

        for j := i+1; j < len(s); j++ {
            if seen[s[j]]{
                break
            }

            longest = max(longest, j - i + 1)
            seen[s[j]] = true
        }
    }

    return longest
}
```

So you may not know, but I write these posts while I solve the problem. So, when I wrote above that I was trying to move on from solving the solution the dumb way, I meant it. However, here I am solving the problem the dumb way.

The dumb way uses two loops. The outer loop starts at index 0 and goes to the right while the inner loop loops through to find the largest substring with non-repeating characters. It uses `map` to be a bit faster in terms of time complexity when checking to see if a character has been seen before, and that's it.

Super simple.

It has a terrible runtime, beating only 10.67% of submissions and the memory usage beats only 14.68%.

What is fun, though, is that I can make two changes to the code and the performance drastically improves.

```go
seen := make(map[byte]bool) -> var seen [256]bool
clear(seen) -> clear(seen[:])
```

Make these two changes to the code, and it now beats 43.53% of submissions in terms of runtime and 99.98% in terms of memory usage.

Dictionaries are evil.

# Through the Looking Window

```go
func lengthOfLongestSubstring(s string) int {
    if len(s) == 0 || len(s) == 1 {
        return len(s)
    }

    var lastKnownPosition [256]int
    for i := 0; i < len(lastKnownPosition); i++ {
        lastKnownPosition[i] = -1
    }

    start := 0
    longest := 1
    for i := 0; i < len(s); i++ {
        c := s[i]

        if lastKnownPosition[c] >= start {
            start = lastKnownPosition[c] + 1
        }

        lastKnownPosition[c] = i
        longest = max(longest, i - start + 1)
    }

    return longest
}
```

Sliding window it is.[^names] Before we look at the solution code, I want to start by looking at one part of the function:

```go
var lastKnownPosition [256]int
for i := 0; i < len(lastKnownPosition); i++ {
	lastKnownPosition[i] = -1
}
```

I'm unhappy with this block of code. `256` iterations? Maybe the compiler will optimize this away into some default initialize, but I don't know, and I'm unhappy with it. So unhappy that I almost made a program to generate `256` comma-separated negative ones. There are, theoretically, ways to get around this with bulk setting:

```go
func bulkSet(slice []int, val int) {
	if len(slice) == 0 {
		return
	}

	slice[0] = val

	for bp := 1; bp < len(slice); bp *= 2 {
		copy(slice[bp:], slice[:bp])
	}
}
```

And this should, in theory, be much faster. Note, though, that I didn't write this code. I looked it up because I was unhappy with writing the for loop to initialize `lastKnownPosition` with all negative ones.

I digress. Let's get back to the algorithm, and I'll put the relevant code below given the length of that aside.

```go { linenos=true }
for i := 0; i < len(s); i++ {
	c := s[i]

	if lastKnownPosition[c] >= start {
	    start = lastKnownPosition[c] + 1
	}

	lastKnownPosition[c] = i
	longest = max(longest, i - start + 1)
}
```

We again loop through the array, one byte at a time. Line 4 checks to see if the last known position for `c` is greater than `start`. Since we initialized `lastKnownPosition` to have all negative ones, this also implicitly handles the case of `c` never being seen before. Regardless, all it is doing is updating the `start` position because we found a duplicate. After that, it updates `lastKnownPosition` for `c` to be equal to `i`. Essentially, `start` chases `i`.

## Side quest: Benchmarking Bulk Set Versus One at a Time

I couldn't live with not knowing if the bulk copy was faster than iterating. So, here is a [benchmark](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-3) to settle the question with slice sizes of 1000, 10000, and 100000. Results are from running locally with `benchstat` (10 runs, AMD Ryzen AI 9 HX 370):

| n      | Loop (ns/op) | Bulk (ns/op) |
| ------ | ------------ | ------------ |
| 1000   | 215.6 ± 1%   | 58.95 ± 1%   |
| 10000  | 2005.0 ± 2%  | 512.5 ± 1%   |
| 100000 | 19750.0 ± 1% | 5713.0 ± 1%  |

Loop is much, much slower than Bulk. Not surprising.

So, unless there is a way to avoid the cost of initializing the array yourself, you should, instead, work around zero-initializing. In the case of this LeetCode problem, we could offset indexes by one and then subtract when necessary.

# The End

Overall, I'm not terribly thrilled with my performance on this one. My attempt at a recursive solution was a bad one, and I didn't like having to go to the slow double for loop, but oh well. No one is perfect.

Till next time, friends.

[^aside]: I'm going to start using cheesier section titles. Silly is fun. Serious is dull.

[^names]: It would have been better to name `start` `left` and `i` `right`.
