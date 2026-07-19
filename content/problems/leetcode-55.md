+++
date = '2026-07-16T14:27:12-05:00'
draft = false
title = 'LeetCode 55: Jump Game'
url = '/posts/leetcode-55/'
+++

[LeetCode 55](https://leetcode.com/problems/jump-game/description/?envType=problem-list-v2&envId=dynamic-programming) is another jump game problem. We've already solved [Jump Game II](/posts/leetcode-45/), which was, confusingly, titled "Jump Game." In that one, we wanted to return the minimum number of jumps to get to the end of the input array `nums` where each element told you how far you could jump from that index. This is the same, except instead of return an `int`, we are going to return a `bool` for whether you can reach the last index. The previous problem guaranteed that we could get to the end. So, that's the real difference.

The implementation, though, is very similar:

```go
func canJump(nums []int) bool {
	r := 0
	for i := 0; i <= r; i++ {
		r = max(r, i+nums[i])
		if r >= len(nums)-1 {
			return true
		}
	}

	return false
}
```

The way this works is we use `r := 0` to say that this is the furthest right that the jumps can go. Then the `for` loop iterates up to `r` with `i`. For every iteration, it checks whether `r` can be increased. If yes, then we increase it with `max`, and this allows us to continue looping through the array. If no, then eventually the loop will stop because of `i <= r`. After increasing `r`, we check if `r >= len(nums)-1`, and, if so, return `true` because that means we can jump to the last element. Else, the loop will stop and we can return `false`.

This solution beats 100% of submissions in terms of runtime.

Unfortunately, none of the <span style="color:orange">medium</span> problems I marked for dynamic programming have been what I was looking for. However, the next several problems I'm going to work on are <span style="color:red">HARD</span>, and I hope, I pray that they will let me start practicing real dynamic programming.

Till next time, friends.
