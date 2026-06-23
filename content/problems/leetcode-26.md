+++
date = '2026-06-12T09:24:02-05:00'
draft = false
title = 'LeetCode 26: Remove Duplicates from Sorted Array'
url = '/posts/leetcode-26/'
+++

[Problem 26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) lives up to its label: <span style="color:green">easy</span>. You are given a sorted array, and you have to remove duplicates from it. It also asks that you include the number of unique elements in the array. Here are some samples.

```
Input: [1,1,2]
Output: 2, nums = [1,2,_]
```

The first solution I came up with was to find duplicates and remove them from the array:

```go
func removeDuplicates(nums []int) int {
    for i := 0; i < len(nums) - 1; i++ {
        j := i + 1

        if nums[i] == nums[j] {
            j++
            for ; j < len(nums) && nums[i] == nums[j]; j++ { }

            nums = slices.Delete(nums, i+1,j)
        }
    }

    return len(nums)
}
```

This, though, is `O(n²)`. The reason why is not the two `for` loops, it is the `slices.Delete`, which will shift all the elements from the right over to the left. We can avoid this cost and get the solution down to just `O(n)` by not shifting.

```go
func removeDuplicates(nums []int) int {
    if len(nums) == 0 {
        return 0
    }

    write_index := 1
    for i := 1; i < len(nums); i++ {
        if nums[write_index - 1] != nums[i] {
            nums[write_index] = nums[i]
            write_index++
        }
    }

    return write_index
}
```

A couple things to note about this solution:

1. This function works by overwriting values. So if we have `[1,1,2]`. Then it doesn't delete the middle `1`, what it does is overwrite the value with `2` at `nums[write_index]`. This is why the problem asks for the length of the output array as a return. This is also a clue that tells you how the problem should be solved.

2. If an empty array `[]` were passed to the function as defined, it would throw an out of bounds error. However, the problem definition has the constraint: "1 <= nums.length <= 3 \* 10⁴." So, we don't need to handle this case, and can simplify the code:

```go
func removeDuplicates(nums []int) int {
    write_index := 1
    for i := 1; i < len(nums); i++ {
        if nums[write_index - 1] != nums[i] {
            nums[write_index] = nums[i]
            write_index++
        }
    }

    return write_index
}
```

3. I'm not a huge fan of when a language asserts what is "idiomatic," but we can make this code a bit more idiomatic by using a `range`. The updated code is below. It is, I think, more readable.

```go
func removeDuplicates(nums []int) int {
    write_index := 1
    for _, value := range nums[1:] {
        if nums[write_index - 1] != value {
            nums[write_index] = value
            write_index++
        }
    }

    return write_index
}
```

Now, before concluding, two things. First, I won't be running a benchmark. There is no point in comparing `O(n)` vs `O(n²)`. Second, a thought occurred to me while writing this up that with a slight re-wording, they could have made this problem more difficult.

If you look at the example, they include as example output "`[1,2,_]`." So, the solver pretty much knows that they are going to do something "clever." What if they changed it so you have to return `[1,2]` instead? It takes away the hint, and the solution above works after changing the return type of the function and the last line to `return nums[:write_index]`.

The problem with this modification to the problem is that it would never work for C. Why not? C has no concept of a slice built into it. It doesn't even have a size associated with its arrays. You have to pass the size of an array around manually instead. So, LeetCode's version is more portable, but I think the modification makes the problem better since the solution isn't as obvious.

Anywho, I hope you enjoyed the post. Till next time, friends.
