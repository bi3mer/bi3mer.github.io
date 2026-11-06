+++
date = '2026-06-23T09:11:53-05:00'
draft = false
title = 'LeetCode 4: Median of Two Sorted Arrays'
url = '/posts/leetcode-4/'
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

The way this lil function works is it ignores the requirement of creating a function that has a time complexity `O(log(m + n))` where `m = len(nums1)` and `n = len(nums2)` and instead combines both lists and then sorts them. After that, the median is `O(1)`, but the previous operations were not.

On the other hand, this solution beats 100% of solutions in terms of runtime. So, is it _that_ dumb? It is readable. It is succinct. It is simple. On the other hand, it allocates a whole new array combining `nums1` and `nums2`. Well, it allocates a new array when `nums1` has no spare capacity. If it does, `append` reuses the backing array and mutates it. On LeetCode, none of this matters.

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

This doesn't solve the problem, though. If you analyze the time complexity, you'll realize that it is `O(m+n)`. Counterintuitively, despite having a lower theoretical time complexity than the dumb solution's `O((m+n)log(m+n))`, it only beats 17.36% of submissions in practice. Also, this is LeetCode, so a re-run may give a better performance.

# Binary Search

```go
func findMedianSortedArrays(nums1 []int, nums2 []int) float64 {
    // we want to binary search on the shorter of the two arrays
    var a []int
    var b []int

    if len(nums1) < len(nums2) {
        a, b = nums1, nums2
    } else {
        a, b = nums2, nums1
    }

    // binary search
    aLeft, aRight := math.MinInt, math.MaxInt
    bLeft, bRight := math.MinInt, math.MaxInt
    size := len(a) + len(b)
    half := size / 2
    lo, hi := 0, len(a)

    for lo <= hi {
        i1 := (hi + lo) / 2 // midpoint
        i2 := half - i1     // index to nums2 moved based on binary search

        aLeft, aRight = math.MinInt, math.MaxInt
        bLeft, bRight = math.MinInt, math.MaxInt

        if i1 > 0 { aLeft = a[i1 - 1] }
        if i1 < len(a) { aRight = a[i1] }

        if i2 > 0 { bLeft = b[i2 - 1] }
        if i2 < len(b) { bRight = b[i2] }

        if aLeft > bRight {
            hi = i1 - 1
        } else if aRight < bLeft {
            lo = i1 + 1
        } else {
            break
        }
    }

    // get the median
    if size % 2 == 0 {
        left := max(aLeft, bLeft)
        right := min(aRight, bRight)

        return float64(left + right) / 2.0
    }

    return float64(min(aRight, bRight))
}
```

I hated working on this. I don't find the solution to be intuitive at all when I look at it. The idea, though, is simple. It runs a binary search.

The trick is that the binary search on the shortest slice `a` is looking for the midpoint for the concatenation of `a` and `b`. It does this by simulating that the index finds a partition. The way this works is with:

```go
i1 := (hi + lo) / 2
i2 := half - i1
```

`i1` is your classic binary search midpoint, and then `i2` is equal to `((len(a) + len(b)) / 2) - i1`. So, `i1 + i2 = half`. This means we are at a potential midpoint every time, but we have to evaluate if we are actually at the right midpoint. To do that we initialize:

```go
aLeft, aRight = math.MinInt, math.MaxInt
bLeft, bRight = math.MinInt, math.MaxInt

if i1 > 0 { aLeft = a[i1 - 1] }
if i1 < len(a) { aRight = a[i1] }

if i2 > 0 { bLeft = b[i2 - 1] }
if i2 < len(b) { bRight = b[i2] }
```

What this is doing is finding the left and right values for calculating the median for both slices `a` and `b`, but it does bounds checking. That is why above the `if` statements you have the values being preset to minimum and maximum values for integers.

```go
if aLeft > bRight {
	hi = i1 - 1
} else if aRight < bLeft {
	lo = i1 + 1
} else {
	break
}
```

This is our binary search, but as you can see, we are doing it based on those values we just found and and that affects how we index into `a`. If the left (low) value in `a` is greater than the high value in `b`, then we need to move the index into `a` to `hi`. Very similar but opposite logic applies in the `else if` case for `lo`. Finally, if neither condition fires, that means we have found the right partition and we can calculate the median and move on with our lives.

Unfortunately, calculating the median isn't simple. We have to use `aLeft`, `aRight`, `bLeft`, and `bRight` to do it, which is why they were declared outside the `for` loop.

```go
if size % 2 == 0 {
	left := max(aLeft, bLeft)
	right := min(aRight, bRight)

	return float64(left + right) / 2.0
}

return float64(min(aRight, bRight))
```

The way to find the median is done with two cases. The first case is when the total `size` is even and we have to take the average of the two midpoints. To do that, though, we need to find what the midpoints are with the two left variables in `a` and `b` and the two right variables. We do it by finding the max of the left ones and the min of the right ones.

Why do we do this?

Because the binary search found a valid partition where everything on the left of both `a` and `b` is `<=` everything on the right. `aLeft` is the largest element in the left half of `a`, and `bLeft` is the largest element in the left half of `b`. The true left midpoint of the merged array is whichever of those two is larger. The same logic applies in reverse for the right midpoint: `min(aRight, bRight)` is the smallest element just to the right of center.

And that is it. Let's see the actual performance now.

# Benchmark

Benchmarks run on an AMD Ryzen AI 9 HX 370 with 6 runs per configuration using [benchstat](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat). Each iteration uses a different pair of pre-generated random sorted arrays. Source is available on [GitHub](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-4).

| Solution      | n=1,000  | n=10,000 | n=100,000 |
| ------------- | -------- | -------- | --------- |
| Dumb          | 42.3 µs  | 361 µs   | 3,740 µs  |
| Two Pointers  | 2.60 µs  | 30.1 µs  | 306 µs    |
| Binary Search | 0.013 µs | 0.022 µs | 0.024 µs  |

The dumb solution and two pointers both scale with input size, while binary search barely moves. At n=100,000, binary search is `~155,833x` faster than the dumb solution.

# Conclusion

This was the kind of problem where if I was asked to solve it a week from today, I would struggle. The reason being is that implementing the binary search solution is not intuitive; at least it isn't for me. I could, though, instantly type up the dumb solution and I could work my way to the two-pointer solution. However, I know that without the internet, I'm not solving the binary search version without a whiteboard and a lot of time on my hands.

That's why I'm thinking of an interview I had a couple months ago. They gave me a version of this problem, except instead of it being two sorted arrays, it was `k` sorted arrays. How insane is that? They wanted me to answer two questions in 50 minutes and that was one of them. I didn't get the job.

Anyways, I hope that this post was useful.

Till next time, friends.
