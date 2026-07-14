+++
date = '2026-07-13T21:28:11-05:00'
draft = true
title = 'LeetCode 53: Maximum Subarray'
url = '/posts/leetcode-53/'
+++

[LeetCode 53](https://leetcode.com/problems/maximum-subarray/?envType=problem-list-v2&envId=dynamic-programming) asks the solver to find the subarray within an array that has the largest sum. So for, example, if we were given `[100,-1, 1]` the return would be `100` because the subarray with the largest sum is `[100]`.

A nice and simple problem.

Right?

I know I shouldn't start with the dumb solution, but I just can't help myself. I'm finding that it is helping my fingers get used to typing Go, so there is some benefit!

```go
func maxSubArray(nums []int) int {
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

You guessed it!

We can cache the results to avoid duplicate work. Specifically, we can cache the sums of the sub-arrays so we don't have to calculate them more than once. Unfortunately, though, we do have to be exhaustive, unlike the [previous problem](/posts/leetcode-45/).

```go
func maxSubArray(nums []int) int {
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

But we can actually make it even faster because we don't need a cache at all:

```go
func maxSubArray(nums []int) int {
    current := nums[0]
    maxValue := nums[0]

    for i := 1; i < len(nums); i++ {
        current  = max(nums[i]+current, nums[i])
        maxValue = max(maxValue, current)
    }

    return maxValue
}
```
