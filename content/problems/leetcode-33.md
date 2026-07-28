+++
date = '2026-07-28T08:10:43-04:00'
draft = true
title = 'LeetCode 33: Search in Rotated Sorted Array'
url = '/posts/leetcode-33/'
+++

[LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/description/) is, I think, a bad problem. The idea is that you are given an array and you have to find the index of a value in that array. If you can't find the value, return \(-1\).

This is a super common problem in programming. So common that most standard libraries include this exact function. For Go, the function is [`slices.Index`](https://pkg.go.dev/slices#Index).

The folks at LeetCode, though, have two twists. First, the input slice is sorted. This means that we can find the index in \(O(log(n))\) time. So, we should use use [`slices.BinarySearch`](https://pkg.go.dev/slices#BinarySearch) instead. However, there is a second twist: the input slice is rotated to the left. What that means is that they took the sorted array, and then shifted it to the left:

```
Example Slice: [1,2,3,4,5,6]
Left Shift 1:  [2,3,4,5,6,1]
Left Shift 2:  [3,4,5,6,1,2]
Left Shift 3:  [4,5,6,1,2,3]
Left Shift 4:  [5,6,1,2,3,4]
Left Shift 5:  [6,1,2,3,4,5]
Left Shift 6:  [1,2,3,4,5,6]
```

The challenge, then, is how to figure figure out what the left shift of the slice is such that we can run a binary search. The obvious answer is to search until the array is not sorted. This, though, is an \(O(n)\) operation, and do you know what is also \(O(n)\)? `slices.Index`.

```go
func search(nums []int, target int) int {
   return slices.Index(nums, target)
```

This beats 100% of the solutions in terms of runtime, and that's why I don't like this problem. There is no penalty for being lazy. The requirement that the solution must have a runtime of \(O(log(n))\) is contrived. Regardless, we might as well find the correct solution.

```go
func search(nums []int, target int) int {
    left, right := 0, len(nums) - 1

    for left <= right {
        mid := left + (right-left)/2

        if nums[mid] == target {
            return mid
        }

        if nums[left] <= nums[mid] {
            if nums[left] <= target && target < nums[mid] {
                right = mid - 1
            } else {
                left = mid + 1
            }
        } else {
            if nums[mid] < target && target <= nums[right] {
                left = mid + 1
            } else {
                right = mid - 1
            }
        }
    }

    return -1
}
```

As for dynamic programming practice, I'm hoping to come back to it in a week or two. Things are a bit busy for me at the moment.

Till next time, friends.
