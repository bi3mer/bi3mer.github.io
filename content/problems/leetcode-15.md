+++
date = '2026-07-05T08:48:22-05:00'
draft = true
title = 'Leetcode 15: 3Sum'
+++

[LeetCode 15](https://leetcode.com/problems/3sum/) is similar to [two sum,](/posts/leetcode-1/), except instead of looking for two numbers that add up to a target, we are looking for three numbers that add to zero. However, there can be no duplicate trios; not in terms of values, in terms of indices: `i != j`, `i != k`, and `j != k`. Here are the samples:

```
Example 1:
  Input: nums = [-1,0,1,2,-1,-4]
  Output: [[-1,-1,2],[-1,0,1]]

Example 2:
  Input: nums = [0,1,1]
  Output: []

Example 3:
  Input: nums = [0,0,0]
  Output: [[0,0,0]]
```

Notice from the input and the output that we are including the values inside the slice `nums` rather than the indices. Otherwise, I hope the problem is adequately described, and now we can get to solving it.

As it just so happened, a week ago I listened to part of [podcast](https://www.youtube.com/watch?v=AaK1SL2i_4Y) with Ryan Williams and this exact problem came up. The solution that he offered on the podcast was involved and very interesting, and I'll be implementing it in this blog post. However, I'm not going to start with it. Instead, I want to implement the common answer first.

To do that, though, it is helpful to consider the "bad" solution first:

```go
func threeSum(nums []int) [][]int {
    var res [][]int
    for i := 0; i < len(nums); i++ {
        for j := i + 1; j < len(nums); j++ {
            for k := j +  1; k < len(nums); k++ {
                if nums[i] + nums[j] + nums[k] == 0 {
                    n := []int {nums[i], nums[j], nums[k]}
                    res = append(res, n)
                }
            }
        }
    }

    return res
}
```

This solution fails for the example input above `[-1,0,1,2,-1,-4]`, and the reason why is because it does nothing to handle the no-duplicate indices requirement for the output. We can fix this two ways. We can either store in a set used index trios and then check before appending or we can sort `nums` first and then use that to skip indices. We are going to do the latter because it takes us closer to the solution that LeetCode is looking for.

```go
func threeSum(nums []int) [][]int {
    slices.Sort(nums)

    var res [][]int
    for i := 0; i < len(nums); i++ {
        if i > 0 && nums[i] == nums[i-1] { continue }

        for j := i + 1; j < len(nums); j++ {
            if j > i + 1 && nums[j] == nums[j-1] { continue }

            for k := j +  1; k < len(nums); k++ {
                if k > j + 1 && nums[k] == nums[k-1] { continue }

                if nums[i] + nums[j] + nums[k] == 0 {
                    n := []int {nums[i], nums[j], nums[k]}
                    res = append(res, n)
                }
            }
        }
    }

    return res
}
```

Okay, so we now have a `slices.Sort` call at the top of the function, and three new if statements, one for each loop. The first one says that if `i` is greater than zero and `nums[i]` equals `nums[i-1]`, skip it. This works because when `i` was `i-1`, its inner `j` and `k` loops already ran through every combination starting with that value, so revisiting it would just produce the same trios again. The same idea applies to `j` and `k`.

Now that we have the slow solution (\(O(n^3)\)),[^sort] we can get to the LeetCode solution that is fast (\(O(n^2)\)), but not the fastest.

The solution builds on what we learned from [Two Sum](/posts/leetcode-1/). For that problem, the obvious answer is to loop through the list twice to find numbers that add up to a target, but we can, instead, speed it up by storing the number we need given the current number. By doing this, we took an \(O(n^2)\) algorithm and reduced it to \(O(n)\). The downside was that we had to use a `map` with `n` elements.

We can use the same idea for this problem:

```go
func threeSum(nums []int) [][]int {
    slices.Sort(nums)

    var res [][]int
    for i := 0; i < len(nums); i++ {
        if i > 0 && nums[i] == nums[i-1] { continue }

        seen := map[int]bool{}
        for j := i + 1; j < len(nums); j++ {
            complement := -nums[i] - nums[j]
            if seen[complement] {
                res = append(res, []int{nums[i], complement, nums[j]})
                for j + 1 < len(nums) && nums[j] == nums[j+1] { j++ }
            }

            seen[nums[j]] = true
        }
    }

    return res
}
```

The time complexity for this function is \(O(n^2)\) and the space complexity is \(O(n)\). It feels like that means this should be a good solution. However, it isn't. It beats only 8.04% of submissions in terms of runtime. The reason why it is slow is the `map`. As I've said before in these LeetCode posts, [they're evil](/posts/leetcode-3/). So, can we get rid of it?

Yes.

[^sort]: A tighter bound would be \(O(n^3 + n log(n))\) because the sort has a cost too, but asymptotically the cost of the sort goes away.
