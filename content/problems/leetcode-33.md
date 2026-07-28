+++
date = '2026-07-28T08:10:43-04:00'
draft = false
title = 'LeetCode 33: Search in Rotated Sorted Array'
url = '/posts/leetcode-33/'
+++

[LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/description/) is, I think, a bad problem. The idea is that you are given an array and you have to find the index of a value in that array. If you can't find the value, return \(-1\).

This is a super common problem in programming. So common that most standard libraries include this exact function. For Go, the function is [`slices.Index`](https://pkg.go.dev/slices#Index).

The folks at LeetCode, though, have two twists. First, the input slice is sorted. This means that we can find the index in \(O(log(n))\) time. So, we should use [`slices.BinarySearch`](https://pkg.go.dev/slices#BinarySearch) instead. However, there is a second twist: the input slice is rotated to the left. What that means is that they took the sorted array, and then shifted it to the left:

```
Example Slice: [1,2,3,4,5,6]
Left Shift 1:  [2,3,4,5,6,1]
Left Shift 2:  [3,4,5,6,1,2]
Left Shift 3:  [4,5,6,1,2,3]
Left Shift 4:  [5,6,1,2,3,4]
Left Shift 5:  [6,1,2,3,4,5]
Left Shift 6:  [1,2,3,4,5,6]
```

The challenge, then, is how to figure out what the left shift of the slice is such that we can run a binary search. The obvious answer is to search until the array is not sorted. This, though, is an \(O(n)\) operation, and do you know what is also \(O(n)\)? `slices.Index`.

```go
func search(nums []int, target int) int {
    return slices.Index(nums, target)
}
```

This beats 100% of the solutions in terms of runtime, and that's why I don't like this problem. There is no penalty for being lazy. The requirement that the solution must have a runtime of \(O(log(n))\) is contrived. Regardless, we might as well find the correct solution, which is a modified binary search:

```go { linenos=true}
func search(nums []int, target int) int {
    left, right := 0, len(nums) - 1

    for left <= right {
        mid := left + (right-left)/2

        if nums[mid] == target {
            return mid
        }

        if nums[left] <= nums[mid] {
            if target > nums[mid] || target < nums[left] {
                left = mid + 1
            } else {
                right = mid - 1
            }
        } else {
            if target < nums[mid] || target > nums[right] {
                right = mid - 1
            } else {
                left = mid + 1
            }
        }
    }

    return -1
}
```

Unfortunately, the algorithm is both simple because it is binary search and difficult because it has special cases that require you to think them through. I'm going to describe it in bullets:

- Define `left` and `right` which point to the start and end of the slice.
- Iterate on line 4 while `left <= right`.
  - Calculate the midpoint (i.e., the mean) of `left` and `right` and store in `mid`.
  - If `nums[mid]` is equal to `target`, return that index. Search is done.
  - Otherwise, we check if `nums[left]` is less than or equal to `nums[mid]` on line 11.
    - True (this means that the values between `nums[left]` and `nums[mid]` are sorted with no pivot):
      - Check if `target` is greater than `nums[mid]` or smaller than `nums[left]`. In the first case, `target` is too big for the sorted left half, so it has to be on the right if it is anywhere. In the second case, `target` is too small for that half (`target < nums[left]`), and since the pivot is on the right, the only values smaller than `nums[left]` must be on the right side.
        - TRUE: set `left` to `mid+1`
        - FALSE: `target` sits inside the sorted left half, so set `right` to `mid-1`
    - False (the pivot is somewhere in the left half, which means the values between `nums[mid]` and `nums[right]` are the sorted ones):
      - Check if `target` is smaller than `nums[mid]` or greater than `nums[right]`. Same reasoning as before, just mirrored. Too small for the sorted right half means it can only be on the left, and too big for it means it is one of the large values before the pivot, which is also on the left.
        - TRUE: set `right` to `mid-1`
        - FALSE: `target` sits inside the sorted right half, so set `left` to `mid+1`
- Outside of the loop, `return` \(-1\) because `target` could not be found.

This code also beats 100% of solutions in terms of runtime, so you'd expect this algorithm to have a similar runtime to `slices.Index`, but, if you've read any of the previous posts with benchmarking, you know that that is obviously bogus. So, I benchmarked both solutions. You can find the code on [GitHub](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-33). Each benchmark runs with slice lengths `n ∈ {100, 200, ..., 1000}` using `-count=10`, analyzed with `benchstat`, on an AMD Ryzen AI 9 HX 370. Each slice is the values `0..n-1` rotated left by a random amount, seeded so every `n` gets the same shift on every run. The shifts landed anywhere from 24% to 100% of the length.

How long `slices.Index` takes depends entirely on where the target sits. So I ran two cases. In the "present" case I pick the target after the rotation, by reading index `n/2` of the already rotated slice, so the scan does exactly `n/2` comparisons no matter what the shift happened to be. In the "missing" case the target isn't in the slice at all, so the scan does all `n` of them.

You might worry that putting the target at the midpoint results in an \(O(1)\) search, but don't. The first lookup is at `(n-1)/2` and every `n` I benchmarked is even, so it lands one slot to the left of the target and misses.

<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>

<canvas id="chart-runtime" style="max-height:400px"></canvas>

<script>
new Chart(document.getElementById('chart-runtime'), {
  type: 'line',
  data: {
    labels: [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
    datasets: [
      {
        label: 'Linear (missing)',
        data: [20.86, 56.64, 74.48, 94.49, 119.8, 137.6, 157.9, 178.1, 196.2, 217.2],
        borderColor: '#e15759',
        backgroundColor: '#e15759',
        fill: false,
      },
      {
        label: 'Linear (present)',
        data: [10.82, 20.62, 39.71, 58.61, 67.78, 77.04, 85.25, 94.07, 106.7, 119.5],
        borderColor: '#e15759',
        backgroundColor: '#e15759',
        borderDash: [5, 5],
        fill: false,
      },
      {
        label: 'Binary (missing)',
        data: [5.994, 7.046, 7.761, 7.987, 7.860, 9.026, 9.171, 9.155, 9.062, 9.077],
        borderColor: '#4e79a7',
        backgroundColor: '#4e79a7',
        fill: false,
      },
      {
        label: 'Binary (present)',
        data: [4.696, 5.535, 6.545, 6.406, 6.504, 7.373, 7.400, 7.409, 7.400, 7.439],
        borderColor: '#4e79a7',
        backgroundColor: '#4e79a7',
        borderDash: [5, 5],
        fill: false,
      }
    ]
  },
  options: {
    plugins: { title: { display: true, text: 'Runtime by slice length' } },
    scales: {
      x: { title: { display: true, text: 'n (slice length)' } },
      y: { title: { display: true, text: 'ns/op' }, beginAtZero: true }
    }
  }
});
</script>

The results are clear. Linear scan always loses. This isn't that surprising since we are talking about binary search versus linear. What is surprising is that LeetCode's runtime calculation is poor enough that it misses this.

As for dynamic programming practice, I'm hoping to come back to it in a week or two. Things are a bit busy for me at the moment.

Till next time, friends.
