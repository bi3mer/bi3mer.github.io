+++
date = '2026-06-13T09:59:33-05:00'
draft = false
title = 'LeetCode 27'
+++

[LeetCode 27](https://leetcode.com/problems/remove-element/description/) is, like [the last problem](../leetcode-26/), an <span style="color:green">easy</span> problem. The problem itself is to remove elements from an array that equal `v`. Here is an example:

```
Input:  nums = [1,2,3,1,2], val = 1
Output: nums = [2,3,2,_,_], size = 3
```

If you read the [post for problem 26](../leetcode-26/), then I think you'll know the solution.

```go
func removeElement(nums []int, val int) int {
    write_index := 0

    for _, v := range nums {
        if val != v {
            nums[write_index] = v
            write_index++
        }
    }

    return write_index
}
```

`write_index` tracks where the next kept element goes, so each value that isn't `val` gets compacted toward the front while everything else is skipped. If the code doesn't make sense, then I recommend that you read the last post.

This solution has a runtime of 0ms, beating 100% of submissions. The memory usage beat 93.82% of submissions. As already established in previous posts, I don't trust these numbers at all, but it feels wrong not reporting something.

There is one other way we can try to solve this problem, which is a bit more interesting I think.

```go
func removeElement(nums []int, val int) int {
    n := len(nums)
    i := 0

    for i < n {
        if nums[i] == val {
            nums[i] = nums[n-1]
            n--
        } else {
            i++
        }
    }

    return n
}
```

This code has slightly different behavior from the previous solution, but it is still `O(n)`. The difference lies in how elements in the array are shifted. In the first one, we scanned to the right while overwriting invalid values with valid ones. This one scans to the right and then overwrites with potentially invalid values from the end. This removes any guarantee of ordering, but it also has a theoretical advantage where it will require fewer shifts on arrays with sparse repeats of the target value.

Now, let's verify if that is true with a benchmark. From here, the first solution will be called WriteIndex and the second SwapFromEnd.

The full benchmarking code is on [GitHub](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-27). Each benchmark runs with array length `n ∈ {100, 1000, 10000}` and `density ∈ {10%, 50%, 90%}` (density means the percent of values in the array that need to be removed), using `-count=5` analyzed with `benchstat`. Density is deterministic: exactly `n * density / 100` elements equal `val`, shuffled with a fixed seed. `val` is set to `n + density` per sub-benchmark. Both solutions modify the array in-place, so each benchmark iteration copies a pre-built template into a buffer to reset state before calling the function. Both solutions pay that identical copy cost, so the relative comparison is still valid.[^1] And, lastly, the benchmark was run on my computer, not on a server. So, I won't claim this benchmark was perfect or definitive.

| n     | density | WriteIndex (ns/op) | SwapFromEnd (ns/op) |
| ----- | ------- | ------------------ | ------------------- |
| 100   | 10%     | 35.2               | 46.1                |
| 100   | 50%     | 27.4               | 50.3                |
| 100   | 90%     | 24.9               | 47.9                |
| 1000  | 10%     | 341                | 453                 |
| 1000  | 50%     | 251                | 376                 |
| 1000  | 90%     | 238                | 326                 |
| 10000 | 10%     | 3506               | 4962                |
| 10000 | 50%     | 3251               | 3854                |
| 10000 | 90%     | 2684               | 3606                |

Both solutions report 0 B/op and 0 allocs/op. Neither allocates, so memory isn't important for this. Speed, though, is.

WriteIndex wins at every combination. At `density=10` and `n=10000`, SwapFromEnd is 1.4x slower (4962ns vs 3506ns). The gap narrows at higher density but never closes: at `density=90` and `n=10000`, SwapFromEnd is 1.3x slower (3606ns vs 2684ns).

The theoretical argument for SwapFromEnd — fewer writes when target values are sparse — doesn't hold up in practice. WriteIndex scans left to right with sequential writes, which plays well with the CPU's prefetcher and branch predictor. SwapFromEnd reads from the end of the array when it finds a match, introducing irregular memory access patterns that hurt cache performance. Perhaps at a very large `n` and a very low `density`, though, we would see actual benefits.

Other than that, I hope all is well. I didn't love that this problem was directly after the previous one. It felt lazy. It would have been better to spread the problems out. But, it isn't like many people do these problems sequentially anyways. I know people do subsets of problems like [LeetCode 75](https://leetcode.com/studyplan/leetcode-75/) or the [Top Interview 150](https://leetcode.com/studyplan/top-interview-150/). It may be worth moving to one of those, because it isn't like I plan on, as of writing this, solving all 3958 (!) problems.

Till next time, friends.

[^1]: An earlier version used `b.StopTimer()`/`b.StartTimer()` around the copy to exclude it from timing. That turned a ~2 minute run into 10+ minutes. Go's benchmark framework only counts "active" time toward its target duration, so for a ~35ns function it runs tens of millions of iterations to accumulate enough active time.
