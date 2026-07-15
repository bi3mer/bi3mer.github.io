+++
date = '2026-07-15T07:00:11-05:00'
draft = false
title = 'LeetCode 53: Maximum sub-array'
url = '/posts/leetcode-53/'
+++

[LeetCode 53](https://leetcode.com/problems/maximum-sub-array/?envType=problem-list-v2&envId=dynamic-programming) asks the solver (you/me) to find the sub-array within an array that has the largest sum. So, for example, if we were given `[100,-1, 1]` the return would be `100` because the sub-array with the largest sum is `[100]`. If the array was `[100,1,-1]`, then the return would be `101` because the sub-array with the largest sum is `[100,1]`.

A nice and simple problem.

I know I shouldn't start with the dumb solution, but I just can't help myself. I'm finding that it is helping my fingers get used to typing Go, so there is some benefit!

```go
func maxsub-array(nums []int) int {
    maxValue := math.MinInt
    for start := 0; start < len(nums); start++ {
        sum := nums[start]
        maxValue = max(maxValue, sum)

        for end := start + 1; end < len(nums); end++ {
            sum += nums[end]
            maxValue = max(maxValue, sum)
        }
    }

    return maxValue
}
```

Unsurprisingly, this solution is too slow. The runtime complexity is \(O(n^2)\), and `nums` can have a max length of \(10^5\). So, how can we make it faster?

We can cache the results to avoid duplicate work. Specifically, `cache[i]` holds the max sub-array sum that ends exactly at index `i`. That value is either just `nums[i]` on its own, or `nums[i]` tacked onto whatever the best sub-array ending at `i-1` was, whichever is bigger.

```go
func maxsub-array(nums []int) int {
    cache := make([]int, len(nums))
    cache[0] = nums[0]
    maxValue := cache[0]

    for i := 1; i < len(nums); i++ {
        cache[i] = max(nums[i], cache[i-1] + nums[i])
        maxValue = max(maxValue, cache[i])
    }

    return maxValue
}
```

But we can actually make it even faster because we don't need a cache at all. Look at the recurrence above: `cache[i]` only ever depends on `cache[i-1]`, never anything further back. So we don't need the whole array, just the previous value:

```go
func maxsub-array(nums []int) int {
    current := nums[0]
    maxValue := nums[0]

    for i := 1; i < len(nums); i++ {
        current  = max(nums[i]+current, nums[i])
        maxValue = max(maxValue, current)
    }

    return maxValue
}
```

To see how this works, let's see two quick runs with the examples at the top:

```
Example 1:
  Input: [100,-1,1]

    current <- 100
    maxValue <- 100

    i = 1
      current <- 99 <- max(-1 + 100, -1)
      maxValue <- 100 <- max(100, 99)

    i = 2
      current <- 100 <- max(1 + 99, 1)
      maxValue <- 100 <- max(100, 100)

  Output = 100


Example 2:
  Input: [100,1,-1]

    current <- 100
    maxValue <- 100

    i = 1
      current <- 101 <- max(1 + 100, 1)
      maxValue <- 101 <- max(100, 101)

    i = 2
      current <- 100 <- max(-1 + 101, -1)
      maxValue <- 101 <- max(101, 100)

  Output = 101
```

This function works by building the max sub-array until it finds a way to start another larger sum sub-array. And that is the whole solution, beating 100% of submissions in terms of runtime.

Till next time, friends.
