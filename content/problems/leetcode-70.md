+++
date = '2026-07-08T08:00:27-05:00'
draft = false
title = 'Leetcode 70: Climbing Stairs'
url = '/posts/leetcode-70/'
+++

[LeetCode 70](https://leetcode.com/problems/climbing-stairs/description/) is listed as an <span style="color:green">easy</span> problem AND is a dynamic programming problem, which is essential because, as of the [last post](/posts/leetcode-16/), I'm going to exclusively practice dynamic programming problems until I have them down.

The problem, in this case, is that we want to figure out how many ways there are to climb up a set of stairs. As input, we are given the number of stairs to climb. The trick that makes this a dynamic programming problem is that at any step, we can climb up one step or two.

```go
func helper(n int, memo []int) int {
    if n < 0 { return 0 }
    if n == 0 { return 1 }
    if memo[n] > 0 { return memo[n] }

    memo[n] = helper(n - 1, memo) + helper(n-2, memo)
    return memo[n]
}

func climbStairs(n int) int {
    memo := make([]int, n+1)
    return helper(n, memo)
}
```

Rather than implement the recursive version first and then follow up with the recursive + memoization (i.e. top-down dynamic programming), I decided to do it in one go. The idea is pretty simple. First we implement our base cases, which is when `n < 0` or when `n == 0`. The reason why `n < 0` returns `0` is because it is invalid to go up two stairs when only one stair is possible. After that we have our memoization specific code, but the core logic is `helper(n - 1, memo) + helper(n-2, memo)` which simulates taking one step and two steps.

That, though, is just one way to implement it. Another way is to implement it with bottom-up dynamic programming. What I like about bottom-up is that it isn't recursive. What I don't like about it is that it is more difficult for me to wrap my head around it, which is the reason I'm doing this in the first place. So, let's do the bottom up version.

```go
func climbStairs(n int) int {
    if n <= 2 { return n }

    cache := make([]int, n + 1)
    cache[1] = 1
    cache[2] = 2

    for i := 3; i < n+1; i++ {
        cache[i] = cache[i - 1] + cache[i - 2]
    }

    return cache[n]
}
```

This, though, is super simple because it is one-dimensional. I'll struggle much more when we get to a problem with a grid. Regardless, this one fits the exact form of the recursive version, only now we are building from the bottom and using the past results to get to the top.

At this point, you may recognize a pattern about how this works. We don't need every value of the cache, only the previous two. So, rather than a space complexity of \(O(n)\), we can actually use two integers and be perfectly fine:

```go
func climbStairs(n int) int {
    if n <= 2 { return n }

    a := 1
    b := 2

    for i := 3; i < n+1; i++ {
        b, a = a + b, b
    }

    return b
}
```

At this point, you have noticed that what this problem actually is is a reformulation of calculating [Fibonacci numbers](https://en.wikipedia.org/wiki/Fibonacci_sequence). The indexing is slightly different, though. Regardless, if we were running in a scenario where we needed the first 46 numbers (the constraint of the problem is \(n <= 45\), and the array is 0-indexed) and we needed it to be near instantaneous, then we could pre-calculate the results to get an \(O(1)\) solution:

```go
var fib = []int{
	1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987,
	1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393,
	196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887,
	9227465, 14930352, 24157817, 39088169, 63245986, 102334155,
	165580141, 267914296, 433494437, 701408733, 1134903170, 1836311903,
}

func climbStairs(n int) int {
    return fib[n]
}
```

This solution, and all the previous ones, beats 100% of submissions in terms of runtime. However, this one, I know, is easily the fastest.

And that is where I'm going to end this post. It was a genuinely fun one to write.

Till next time, friends.
