+++
date = '2026-07-01T08:33:34-05:00'
draft = false
title = 'LeetCode 11: Container With Most Water'
url = '/posts/leetcode-11/'
+++

Hello, hello, hello.

We're on [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) today. Here is the example input:

```
Example 1:
  Input: height = [1,8,6,2,5,4,8,3,7]
                     ^             ^
  Output: min(8, 7) * (8 - 1) = 7 * 7 = 49

Example 2:
  Input: height = [1,1]
  Output: 1
```

The idea here is that we are given an array of integers, and those integers represent a height. We then want to find the largest possible area based on the minimum of the two heights where the width is determined by the distance between the two heights. (Area of a rectangle is width multiplied by height.) The reason we use the minimum is that water can only fill up to the height of the shorter wall. If one wall has a height of three and the other eight, the water level is capped at three.

```go
func maxArea(height []int) int {
    l := 0
    r := len(height) - 1
    a := 0

    for l < r {
        newArea := min(height[l], height[r]) * (r - l)
        a = max(a, newArea)

        if height[l] < height[r] {
            l++
        } else {
            r--
        }
    }

    return a
}
```

The code above has a runtime of `O(n)` with a space complexity of `O(1)`. It works by using two pointers to start from the outside and move to the inside of the `heights` slice. The intuition is that we should always move the shorter side inward. Moving the taller side is pointless because the shorter side is already the bottleneck. The only way to potentially get a bigger area is to replace the shorter side with something new. But that statement feels flimsy. So, let me give you a paragraph to informally prove it:

Consider the case of `height[l] < height[r]`. The two pointer solution would move `l` inward. What if we moved `r` inward instead? No matter what height we found for the new `r'`, it would be capped: `min(height[l], height[r']) <= height[l]`. So, every value will be less than the area at `l` and `r` for any inner `r'` when `height[l] < height[r]` due to the height never being increased and the width of the rectangle (`r'-l`) shrinking. That is why we have to move the minimum forward, because every pair with the inner `r'` values can't result in a larger area. So, we skip them. The same argument applies symmetrically when `height[r] <= height[l]`.

And, I spent more time on that paragraph than I did on writing the code. So, hopefully, it was helpful.

Till next time, friends.
