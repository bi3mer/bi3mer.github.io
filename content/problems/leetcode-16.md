+++
date = '2026-07-07T07:19:18-05:00'
draft = true
title = 'Leetcode 16: 3Sum Closest'
url = '/posts/leetcode-16/'
+++

Hello!

Let's solve [LeetCode 16.](https://leetcode.com/problems/3sum-closest/) We want to find three integers at distinct indexes that sum up closest to `target`. If you recall the [previous problem,](/posts/leetcode-15/) then you'll recognize that this problem and the previous one are _extremely_ similar. The main difference is that instead of looking for every exact match, we just want the closest one and we only return that closest sum rather than the whole set of indexes that sum up to the `target`.

Given that, I'm not going to waste my time or your time with any further descriptions. Here is the code:

```go
func abs(a int) int {
    if a < 0 { return -a }
    return a
}

func threeSumClosest(nums []int, target int) int {
    slices.Sort(nums)

    closest := math.MaxInt
    diff := math.MaxInt

    for i := 0; i < len(nums); i++ {
        left := i + 1
        right := len(nums) - 1

        for left < right {
            newClosest := nums[i] + nums[left] + nums[right]

            if newClosest < target {
                left++
                for left < right && nums[left] == nums[left-1] { left++ }
            } else if newClosest > target {
                right--
                for left < right && nums[right] == nums[right+1] { right-- }
            } else {
                return newClosest
            }

            newDiff := abs(target - newClosest)
            if newDiff < diff {
                closest = newClosest
                diff = newDiff
            }
        }
    }

    return closest
}
```

If it doesn't make sense, [the post for LeetCode 15](/posts/leetcode-15/) explains almost the exact same code in what I hope is a comprehensive and easy-to-understand manner.

The only slight annoyance is that if you run the code above, you may not get a submission that beats 100% of submissions. This is because of the `slices.Sort`. If you change it to `sort.Ints(nums)`, then the otherwise unchanged code beats 100% of submissions in terms of runtime. I assume this is due to LeetCode's compiler not doing a strong optimization before running, but without digging into it, I can't be certain. So, I guess use `sort.Ints` for LeetCode.

Before ending, in a [previous post,](/posts/leetcode-10-2/) I said that I would change up how I was approaching the solving of these problems. I originally wanted to solve one problem a day with an accompanying blog post. However, after working on dynamic programming, it was clear to me that I needed to dedicate some time to just solving problems with dynamic programming. So, the next set of posts will be me doing just that. I have a whole list of problems that I want to work on. They start easy and slowly get harder. Hopefully, I'll get better.

Till next time, friends.