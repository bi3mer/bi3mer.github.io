+++
date = '2026-07-06T08:48:22-05:00'
draft = false
title = 'Leetcode 15: 3Sum'
url = '/posts/leetcode-15/'
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

We'll start with the "bad" solution first.

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

This solution fails for the example input above `[-1,0,1,2,-1,-4]`, and the reason why is because it does nothing to handle the no-duplicate indices requirement for the output. We can fix this in two ways. We can either store in a set used index trios and then check before appending or we can sort `nums` first and then use that to skip indices. We are going to do the latter because it takes us closer to the solution that LeetCode is looking for.

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

Yes. To do that we have to do two things. One, we can use the fact that the list is sorted and use a two-pointer solution to adjust how the search is done (i.e. instead of left to right, we can do outside to inside). Two, we can loop past duplicates on the left and right side when we increment or decrement.

```go
func threeSum(nums []int) [][]int {
    slices.Sort(nums)

    var res [][]int
    for i := 0; i < len(nums); i++ {
        if i > 0 && nums[i] == nums[i-1] { continue }

        left := i + 1
        right := len(nums) - 1

        for left < right {
            v := nums[i] + nums[left] + nums[right]

            if v > 0 {
                right--
            } else if v < 0 {
                left++
            } else { // v == 0
                res = append(res, []int{nums[i], nums[left], nums[right]})

                for left < right && nums[left] == nums[left+1] { left++ }
                left++

                for left < right && nums[right] == nums[right-1] { right-- }
                right--
            }
        }
    }

    return res
}
```

Our solution is now beating 98.18% of submissions in terms of runtime. The two pointers let us find any valid pairs in \(O(n)\) time and the for loops when we find a valid pair let us skip duplicates.

This is where most submissions stop, and rightfully so. I originally wanted to take this post one step further by implementing and explaining part of [_Threesomes, Degenerates, and Love Triangles_.](https://arxiv.org/abs/1404.0799)[^titlenote] This paper is about the decision tree complexity of 3Sum. They show how you can get an algorithm with fewer comparisons by bucketing the sorted array into groups, and using the min/max of each group to throw out entire groups at once instead of walking through them one element at a time. The problem, though, is that they are only trying to find one valid solution, not _every_ valid solution. As a result, the trick doesn't carry over cleanly and actually results in a slower solution on LeetCode.

Till next time, friends.

---

## Appendix: Grouped Version

```go
func threeSum(nums []int) [][]int {
    slices.Sort(nums)
    n := len(nums)

    g := 1
    for g*g < n { g++ }

    var res [][]int
    for i := 0; i < n-2; i++ {
        if i > 0 && nums[i] == nums[i-1] { continue }

        target := -nums[i]
        left, right := i+1, n-1

        for left < right {
            lg, rg := left/g, right/g

            if lg != rg {
                lgEnd := (lg + 1) * g
                if lgEnd > n { lgEnd = n }
                rgStart := rg * g

                maxSum := nums[lgEnd-1] + nums[right]
                minSum := nums[left] + nums[rgStart]

                if maxSum < target {
                    left = lgEnd
                    continue
                }
                if minSum > target {
                    right = rgStart - 1
                    continue
                }
            }

            v := nums[left] + nums[right]
            if v > target {
                right--
            } else if v < target {
                left++
            } else {
                res = append(res, []int{nums[i], nums[left], nums[right]})

                for left < right && nums[left] == nums[left+1] { left++ }
                left++

                for left < right && nums[right] == nums[right-1] { right-- }
                right--
            }
        }
    }

    return res
}
```

[^sort]: A tighter bound would be \(O(n^3 + n \log(n))\) because the sort has a cost too, but asymptotically the cost of the sort goes away.

[^titlenote]: What a great title for a paper.
