+++
date = '2026-07-18T22:22:45-05:00'
draft = false
title = 'LeetCode 35: Search Insert Position'
url = '/posts/leetcode-35/'
+++

Apologies for the brief interruption in the dynamic programming posts. The air in Chicago has been terrible and I've been a little sick/dizzy as a result. Also, my AC is down. But, you don't want to hear about that. Let's talk about today's LeetCode problem.

I have deliberately selected [LeetCode 35](https://leetcode.com/problems/search-insert-position/description/) because it is listed as an <span style="color:green">easy</span> problem. The goal, should we choose to accept, is to use an input slice `nums` and an integer `target` to either find the index of `target` OR say what that index should be. Since `nums` is sorted, that insertion index is well-defined even when `target` isn't present.

They also have the requirement that the solution have a runtime complexity of \(O(log(n))\). I'm feeling contrarian, though. So, let's start with the easy one that is \(O(n)\).

```go
func searchInsert(nums []int, target int) int {
    for index, value := range nums {
        if value >= target {
            return index
        } 
    }

    return len(nums)
}
```

Fun fact, this beats 100% of solutions in terms of runtime. Rebellion rules. Let's rebel again:

```go
func searchInsert(nums []int, target int) int {
    idx, _ := slices.BinarySearch(nums, target)
    return idx
}
```

That showed them. Instead of implementing binary search like the problem wanted us to do, we can just use Go's standard library. 

Alright, that's enough of that. Let's do it the way the problem's creator(s) intended.

```go
func searchInsert(nums []int, target int) int {
    l, r := 0, len(nums)
    
    for l < r {
        mid := (l + r) / 2
        if nums[mid] < target {
            l = mid + 1
        } else {
            r = mid
        }
    }
    
    return l
}
```


If the value is too big at the middle, look to the left. If too small, look to the right. We keep narrowing until `l` and `r` meet, which lands on the target's index or its insertion point. Fun fact, though, code exactly like this, but written in Java, would be buggy.[^f]

Till next time, friends.

[^f]: Check out the [blog post](https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/) to see why. It's short and a really good read.