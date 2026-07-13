+++
date = '2026-07-13T12:19:19-05:00'
draft = false
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

`jump` is the entry point of the function, and all it does is call the poorly named function: `helper`. It doesn't need to do this but because this is a dynamic programming problem, we are going to be using [memoization](https://en.wikipedia.org/wiki/Memoization) in a moment.

`helper` has a base case where if the index is `>= len(nums) - 1`, it will return `0`. Otherwise, we loop through the value at `nums[index]`, starting at 1. This allows us to simulate each jump, and there is no point in simulating a jump at `i=0`. The actual jump occurs on line 8. Because we want the minimum jumps required to get the last element in `nums`, we only store the minimum and nothing more.

This, though, is too slow, which isn't a surprise. However, we can speed it up with the aforementioned idea of memoization, which is basically just storing previous results to inform later results. Another way to think of it is we cache results and then use that cache to avoid computation we've already done:

```go { linenos=true }
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
}
```

The code above is almost exactly the same. The only difference is that we use `memo` whenever we can to avoid recomputing the minimum number of jumps to the end of the `nums` slice.

To my surprise, this wasn't the fastest solution possible. It only beat 7.45% of solutions. I assumed it would be, though. So, what did I miss when I beelined for the top-down dynamic programming solution? I missed an algorithm that I have been implementing for over a decade: breadth-first search.

```go { linenos=true }
func jump(nums []int) int {
    jumps, l, r := 0, 0, 0

    for r < len(nums) - 1 {
        farthest := 0
        for i := l; i <= r; i++ {
            farthest = max(farthest, i + nums[i])
        }

        l = r + 1
        r = farthest
        jumps++
    }

    return jumps
}
```

This is a greedy breadth-first search where we track a window of reachable indexes per jump. I think a breakdown of the actual behavior is more helpful than a description of the code:

```
input: [3,0,0,1,2,3,1]

1 Jump:  [3,0,0,1,2,3,1]
            l   r

2 Jumps: [3,0,0,1,2,3,1]
                  l
                  r

3 Jumps: [3,0,0,1,2,3,1]
                    l r

r >= len(nums) - 1, so the minimum number of jumps is 3.
```

So, as long as we can store the minimum and maximum reachable points per jump, we can find the jumps to get to the end. Note that it doesn't have any error handling. So, if there was any input where the end of the input slice couldn't be reached, this algorithm would return an incorrect result. This, though, is okay because of the constraint: "It's guaranteed that you can reach `nums[n - 1]`."

The solution itself is simple, and much more elegant, I think, than the dynamic programming (DP) version. It is also much faster since its runtime complexity is \(O(n)\) whereas the DP version is \(O(n^2)\). It beats 100% of submissions.

The moral for me is to not blindly reach for the solution I know will work because there may be another one that is way faster and fairly obvious if you give yourself a second to think.

Till next time, friends.
