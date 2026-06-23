+++
date = '2026-06-23T09:11:53-05:00'
draft = true
title = 'LeetCode 4: Median of Two Sorted Arrays'
+++

Hi! Welcome back.

No idea why I started this post like that but I'm keeping it.

We're going to work on [LeetCode 4: Median of Two Sorted Arrays.](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) I'm not going to bother with copying and pasting their examples and making slight formatting adjustments like I usually do. There's no point since the title tells you everything that you need to know about the problem.

# The Dumb Solution

```go
func median(nums []int) float64 {
    mid := len(nums) / 2
    if len(nums) % 2 == 0 {
        return float64(nums[mid - 1] + nums[mid]) / 2.0
    }

    return float64(nums[mid])
}

func findMedianSortedArrays(nums1 []int, nums2 []int) float64 {
    combined := append(nums1, nums2...)
    slices.Sort(combined)

    return median(combined)
}
```

The way this lil function works is it ignores the requirement of creating a function that has a time complexity `O(log(m + n))` where `m = len(nums1)` and `n = len(nums2)` and instead combines both lists and then sorts them. After that, the median is `O(1)`, but the previous operations were not. On the other hand, this solution beats 100% of solutions in terms of runtime. So, is it _that_ dumb? It is readable. It is succinct. It is simple. On the other hand, it allocates a whole new array that is a copy of `nums1` and `nums2`. So, kind of dumb, but also kind of not dumb.

Also, just as an aside. I strongly dislike this kind of problem where the solution is not a natural requirement due to the test cases. A great example is in my post for [LeetCode 2](/posts/leetcode-2/#failure-due-to-overflow) where one of the inputs made simple addition impossible.

Alright, moving on.

# Two Pointers

```go
func findMedianSortedArrays(nums1 []int, nums2 []int) float64 {
    size := len(nums1) + len(nums2)
    half := size / 2
    i1, i2 := 0, 0
    prev, cur := 0, 0

    for range half+1 {
        prev = cur

        if i1 < len(nums1) {
            if i2 < len(nums2) {
                if nums1[i1] <= nums2[i2] {
                    cur = nums1[i1]
                    i1++
                } else {
                    cur = nums2[i2]
                    i2++
                }
            } else {
                cur = nums1[i1]
                i1++
            }
        } else {
            cur = nums2[i2]
            i2++
        }
    }


    if size % 2 == 0 {
        return float64(prev + cur) / 2.0
    }

    return float64(cur)
}
```

We have two pointers, one for each input array. Then we move them to the right until we get to the halfway point based on the size of both. The only tricky part is to realize that you need to track the previous value and the current value while you are moving the two pointers so you can calculate the median.

This doesn't solve the problem, though. If you analyze the time complexity, you'll realize that it is `O(m+n)`. Counterintuitively, despite having a lower theoretical time complexity than the dumb solution's `O((m+n)log(m+n))`, it only beats 17.36% of submissions in practice. The constants and overhead of the pointer logic make it slower in practice than the sort-based approach. So, it is still not fast enough for the goal.

# Binary Search

```go

```
