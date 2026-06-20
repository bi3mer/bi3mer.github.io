+++
date = '2026-06-20T12:11:03-05:00'
draft = false
title = 'Leetcode 1'
+++

As mentioned in [the last post,](/posts/leetcode-32/#conclusion) we are going back to the start of the LeetCode problem set, and doing [LeetCode 1](https://leetcode.com/problems/two-sum/description/). The problem is to find two elements in the input array that add up to a target value that is also input. The output, then, is the indices of those two elements:

```
Example 1:
  Input: nums = [2,7,11,15], target = 9
  Output: [0,1]

Example 2:
  Input: nums = [3,2,4], target = 6
  Output: [1,2]

Example 3:
  Input: nums = [3,3], target = 6
  Output: [0,1]
```

We are also given several constraints, the most important of which is that there is only one valid answer. Meaning, an input of `nums=[1,1,1]` and `target=2` is impossible because that means there would be multiple valid ouputs: `[[0,1], [0,2], [1,2]]`.

# Solution 1: Nice and Slow

```go
func twoSum(nums []int, target int) []int {
    output := make([]int, 2)
    for i, val1 := range nums {
        for j, val2 := range nums[i + 1:] {
            if val1 + val2 == target {
                output[0] = i
                output[1] = i + j + 1

                return output
            }
        }
    }

    return output;
}
```

This is an `O(n²)` algorithm in terms of runtime. Memory is constant.

It works by looping through `nums` and storing the value and index. Then we do a second, inner loop to see if any of the elements when added to the outer loop's value is equal to `target`. There is one slightly tricky element which is `output[1] = i + j + 1`. This had to be done because `j` is local to the slice `nums[i+1:]` from the inner-loop. A way to have avoided this is:

```go
for j := i+1; j < len(nums); j++ {
	val2 = nums[j]; // ...
}
```

# Solution 2: One Loop

```go
func twoSum(nums []int, target int) []int {
    seen := make(map[int]int)
    for i, val := range nums {
        if j, ok := seen[target - val]; ok {
            return []int{i, j} // correct ordering would be {j, i}
        }

        seen[val] = i
    }

    return nil
}
```

Personally, I hate using a `map`, but this solution requires it. What it does is cache the elements in the `map` that I named `seen` where the element's value is the key and index is the value. What this lets us do is loop through `nums` once and check if `seen[target-val]` exists. If so, we're done. If this doesn't make sense:

```
nums[i] + nums[j] = target
nums[i] = target - nums[j]
```

It just flips what the search is for. Now we don't look for the sum that equals `target` directly. Instead, we populate `seen` with values we know we have and if we find the value that completes the second equation, we have completed the two-sum problem.

# Conclusion

This was a nice problem. The easy solution was easy to code, and the fast solution required a little inversion to figure out. I could have benchmarked, but it is the weekend and I could use a nap.

Till next time, friends.
