+++
date = '2026-07-13T12:19:19-05:00'
draft = true
title = 'LeetCode 45: Jump Game II'
url = '/posts/leetcode-45/'
+++

[LeetCode 45](https://leetcode.com/problems/jump-game-ii/description/?envType=problem-list-v2&envId=dynamic-programming) is fairly similar to problem #70, which we already [did](/posts/leetcode-70). The idea for this problem is that we want to find if we can get to the last index in the array by using the values in the array to jump around it.

```
Example 1:
  Input: nums = [2,3,1,1,4]
  Output: 2

Example 2:
  Input: nums = [2,3,0,1,4]
  Output: 2
```

So in example 1, we can jump one index forward or two indexes forward. This balloons out because now we are testing at index 1 and 2, and those will cause more search points. So, the easiest way to try and solve this problem, I think, is with recursion.

```go { linenos=true }
func helper(nums []int, index int) int {
    if index >= len(nums)-1 { return 0 }

    minJumps := 100000
    for i := 1; i <= nums[index]; i++ {
        if index+i >= len(nums) { break }

        minJumps = min(minJumps, 1+helper(nums, index+i))
    }

    return minJumps
}

func jump(nums []int) int {
    return helper(nums, 0)
}
```

`jump` is the entry point of the function, and it all it does is call the poorly named function: `helper`. It doesn't need to do this but because this is a dynamic programming problem, we are going to be using [memoization](https://en.wikipedia.org/wiki/Memoization) in a moment.

`helper` has a base case where if the index is `>= len(nums) - 1`, it will return `1`. Otherwise, we loop through the value at `nums[index]`, starting at 1. This allows us to simulate each jump, and there is no point in simulating a jump at `i=0`. The actual jump occurs on line 8. Because we want the minimum jumps required to get the last element in `nums`, we only store the minimum and nothing more.

This, though, is too slow, which isn't a surprise. However, we can speed it up with the aforementioned idea of memoization, which is basically just storing previous results to inform later results. Another way to think of it is we cache results and then use that cache to avoid computation we've already done:

```go
func helper(nums []int, index int, memo []int) int {
    if index >= len(nums) - 1 { return 0 }
    if memo[index] != -1 { return memo[index] }
    memo[index] = 100000

    for i := 1; i <= nums[index]; i++ {
        if index + i >= len(nums) {
            break
        }

        memo[index] = min(memo[index], 1 + helper(nums, index + i, memo))
    }

    return memo[index]
}

func jump(nums []int) int {
    memo := make([]int, len(nums))
    for i := range memo {
        memo[i] = -1
    }

    return helper(nums, 0, memo)

```

The code above is almost exactly the same. The only difference is that we use `memo` whenever we can to avoid recomputing the minimum number of jumps to the end of the `nums` slice.

To my surprise, this wasn't the fastest solution possible. I assumed it would be, blindly, because the problem was listed as dynamic programming. It only beat 7.46% of solutions. So, what did I miss when I beelined for the top-down dynamic programming solution?

... explaining the solution

```go
func jump(nums []int) int {
    jumps, currentEnd, farthest := 0, 0, 0

    for i := 0; i < len(nums)-1; i++ {
        farthest = max(farthest, i+nums[i])

        if i == currentEnd {
            jumps++
            currentEnd = farthest
        }
    }

    return jumps
}
```

It beats 100% of submissions. So yeah, don't blindly reach for the solution you know will work because there may be another one that is way faster and fairly obvious if you give yourself a second to think.

Till next time, friends.
