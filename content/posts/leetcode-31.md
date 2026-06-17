+++
date = '2026-06-17T06:30:45-05:00'
draft = false
title = 'LeetCode 31'
+++

[Problem 31](https://leetcode.com/problems/next-permutation/description/) is <span style="color:orange">medium</span> difficulty. The title is "Next Permutation," which partially relates to [yesterday's problem](../leetcode-30/) where I tried to use permutations, but the goal is different. To see, let's look at the examples that LeetCode gave:

```
Example 1:
  Input: nums = [1,2,3]
  Output: [1,3,2]

Example 2:
  Input: nums = [3,2,1]
  Output: [1,2,3]

Example 3:
  Input: nums = [1,1,5]
  Output: [1,5,1]
```

The goal, as the problem's title suggest, is to generate the next permutation. Not just any permutation, though. That would be too easy. They want the "next" one, and they defined next by, "The next permutation of an array of integers is the next lexicographically greater permutation of its integer."

# The Solution

```go
func nextPermutation(nums []int)  {
    if len(nums) == 0 {
        return
    }

    var k int
    for k = len(nums) - 2; k >= 0; k-- {
        if nums[k] < nums[k+1] { break }
    }

    if (k < 0) {
        slices.Reverse(nums)
        return
    }

    var l int
    for l = len(nums) - 1; l > k; l-- {
        if nums[l] > nums[k] { break }
    }

    nums[k], nums[l] = nums[l], nums[k]
    slices.Reverse(nums[k+1:])
}
```

This is the solution, and I want to say with full transparency that I did not come up with it. I looked at a piece of paper for three minutes and asked myself, "Is this how I'm going to spend my morning?" I decided that the answer was an easy no. So, I checked the solutions tab and saw a c++ solution that looked reasonable and translated it into Go.

The [solution is credited](https://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order) to [Narayana Pandita](<https://en.wikipedia.org/wiki/Narayana_Pandita_(mathematician)>) who lived from 1340 to 1400. How and why he came up with this is beyond me, but it works and it solves the problem.

# How You could Get to This

This is the first solution that I really don't understand. So, rather than benchmark with no comparison, I'm going to spend the rest of the post trying to explain (and discover for myself) how this algorithm works. To start, let's look at the lexicographically ordered permutations for an array `[1,2,3]`:

```
[1, 2, 3]
[1, 3, 2]
[2, 1, 3]
[2, 3, 1]
[3, 1, 2]
[3, 2, 1]
```

When you look at the array, I think the pattern to notice is the first number. Two 1's, two 2's, and, finally, three 3's. Then you can see that the second number swaps from least to highest (i.e. for `[1, X, X]` you get `[2,3]` first and `[3,2]` second) and the third is the remaining. From there, we can get to a tree, like the one below:

```
              · (root)
    ┌─────────┼────────┐
    1         2        3
  ┌─┴─┐     ┌─┴─┐    ┌─┴─┐
  2   3     1   3    1   2
  │   │     │   │    │   │
 123  132  213 231  312 321
```

So, we have two cases to handle when the array is length three. We either have to swap the two end numbers or we have to change the start number (e.g. 1 to 2 or 2 to 3), and then swap the other two back into a sorted order. That, though, is a bit too specialized, so let's look at `[1,2,3,4]`

```
                               · (root)
        ┌───────────────┬──────┴────────┬───────────────┐
        1               2               3               4
   ┌────┼────┐     ┌────┼────┐     ┌────┼────┐     ┌────┼────┐
   2    3    4     1    3    4     1    2    4     1    2    3
  ┌┴┐  ┌┴┐  ┌┴┐   ┌┴┐  ┌┴┐  ┌┴┐   ┌┴┐  ┌┴┐  ┌┴┐   ┌┴┐  ┌┴┐  ┌┴┐
  3 4  2 4  2 3   3 4  1 4  1 3   2 4  1 4  1 2   2 3  1 3  1 2
  │ │  │ │  │ │   │ │  │ │  │ │   │ │  │ │  │ │   │ │  │ │  │ │
  4 3  4 2  3 2   4 3  4 1  3 1   4 2  4 1  2 1   3 2  3 1  2 1
```

The tree is getting too big, so I can't put in the completed numbers, like for the tree above. However, you'll see basically the same pattern but one that is more complicated since there are more levels to consider. But with this, I think the idea behind the algorithm can become clear.

`nextPermutation` starts with a simple guard to handle an empty input. But the next four lines of code are a bit ambiguous:

```go
var k int
for k = len(nums) - 2; k >= 0; k-- {
	if nums[k] < nums[k+1] { break }
}
```

The first thing to notice is that `k` is being declared outside of the loop. So, we want to keep it around and use it for later. But, what exactly is `k`? The declaration is your clue: `k = len(nums) - 2`. From this, we can see that `k` is going to be used to iterate through `nums` in reverse. This is confirmed with the `k--`.

The odd part is that there is a `-2` instead of a `-1`. So, we can go to the next line: `if nums[k] < nums[k+1] { break }`. This line checks to see if the value `k` is at is less than the value ahead of `k`. This tells us (1) why we subtracted by two instead of one and (2) tells us what we are looking for. We are looking for where we are in the lexicographical tree above.

As an example, imagine we have the the input `[3,2,1]`. The block of code above will end with `k <- -1`. This is the end of the road, and we know that we have to give back the sorted array, and call it. That is what these lines do:

```go
if (k < 0) {
	slices.Reverse(nums)
	return
}
```

`nextPermutation` uses `k` for more than just the last case, though. We didn't iterate through the whole array in reverse to check if the array was sorted. So, what is it?

```
      3 (root)
 ┌────┼────┐
 1    2    4
┌┴┐  ┌┴┐  ┌┴─┐
2 4  1 4 *1* 2
│ │  │ │  │  │
4 2  4 1  2  1
```

Let's say that we are using `[1,2,3,4]` and at root `3`. We want to figure out where we are in the tree. Notice that the tree at every level is ordered. So if we have `[3,4,1,2]`, then know that `k` will be equal to 1.

`k` is where the order of the array needs to be modified, based on that, but there is more to the picture.

In terms of the tree, though, it is where everything below it has the largest elements that it can have. If we run a swap from `[3,4,1,2]`, we'll get: `[3,4,2,1]`. In this `k=1`, and you can see the order like this: `3 < *4* > 2 > 1`. We need to swap `3` and `4` and to do that, we have to go to the next tree.

`k` is the rightmost element in `nums` that still has a larger element to its right.

Sorry, quick breather. We're almost there. Six more lines of code to go.

Now we are going to figure out what the poorly named variable `l` represents.

```go
var l int
for l = len(nums) - 1; l > k; l-- {
	if nums[l] > nums[k] { break }
}
```

Similar to `k`, we iterate backwards through `nums`. Unlike `k`, we initialize with the value `len(nums) - 1`. Then we iterate backwards until `l <= k`. Simple enough, but the real thing to notice is the `if` statement below. We are looking for the index where `nums[l] > nums[k]`. The question is: Why?

To answer, lets work through an example of what `l` will be for `[1,3,2]`.[^132-note]

```
1. nums[l=2] > nums[k=0] -> 2 > 1 -> true -> break
```

Now, that we know `l=2`, look at the tree below---sorry that it is a bit confusing that `l=2` and `nums[l]=2`.

```
              · (root)
    ┌─────────┼────────┐
    1         2        3
  ┌─┴─┐     ┌─┴─┐    ┌─┴─┐
  2   3     1   3    1   2
      │     │
     cur   next
```

In this case `l` is pointing out the new root: 2. So, what `l` represents is the smallest value that can be promoted, where "promoted" means moved up the tree. And the way to do this with code is:

```go
nums[k], nums[l] = nums[l], nums[k]
slices.Reverse(nums[k+1:])
```

You swap the values at `k` and `l`, and then you reverse all the values after `k`. The reverse is the last clever thing and it is a byproduct of the ordering and the shifting. I think the easiest way to see why it works is to look at the examples for `[1,2,3]` at the top of this blog post.

Before calling it, let's try one more example with `[3,2,4,1]` since I think the concept of `l` may still be a bit fuzzy.

```
1. nums[l=3] > nums[k=1] -> 1 > 2 -> false -> l--
2. nums[l=2] > nums[k=1] -> 4 > 2 -> true  -> break
```

If you look at the tree above, you'll see that the next permutation will be: `[3,4,1,2]`. In terms of code, we can see what happens with both lines:

```go
                                    // [3,2,4,1]
nums[k], nums[l] = nums[l], nums[k] // -> [3,4,2,1]
slices.Reverse(nums[k+1:])          // -> [3,4,1,2]
```

`l` is the smallest value right of `k` that's larger than `nums[k]`, and `k` is the rightmost element in `nums` that still has a larger element to its right.

# Conclusion

Well, that was a lot. I feel like this problem could have been classified as <span style="color:red">hard</span>. I definitely spent more time analyzing this solution than I did any other one so far. It is also the only solution so far that felt completely out of reach for me without spending a bunch of time in front of a whiteboard.

Regardless, I hope this post was helpful. It was helpful for me to write it out at least.

Till next time, friends.

[^132-note]: For [1,3,2], `k=0` because the first check in the loop checks `3 < 2` which will be false, so the `break` will not occur. That takes us to `k=0` which does break since `1 < 3` is true.
