+++
date = '2026-07-09T08:07:39-05:00'
draft = false
title = "LeetCode 118: Pascal's Triangle"
url = '/posts/leetcode-118/'
+++

[LeetCode 118](https://leetcode.com/problems/pascals-triangle/description/) wants you to construct Pascal's Triangle based on an integer.

```
Example 1:
  Input: numRows = 5
  Output: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]
  Visual:

    1
   1 1
  1 2 1
 1 3 3 1
1 4 6 4 1

Example 2:
  Input: numRows = 1
  Output: [[1]]
  Visual:

1

Example 3:
  Input: numRows = 2
  Output: [[1],[1,1]]
  Visual:

 1
1 1
```

Each number is the sum of the two numbers diagonally above it, with the missing spots off the edge treated as `0`. To do this, we can build the triangle one row at a time, using the previous row to build the next.

```go
func generate(numRows int) [][]int {
	var t [][]int
	for i := range numRows {
		if i == 0 {
			t = append(t, []int{1})
		} else {
			prev := t[i-1]
			var row []int

			for j := range i + 1 {
				leftIndex := j - 1
				if leftIndex >= 0 && j < len(prev) {
					row = append(row, prev[leftIndex]+prev[j])
				} else {
					row = append(row, 1)
				}
			}

			t = append(t, row)
		}
	}

	return t
}
```

The code above is not my finest work. (I actually hate it.) The way it works is it loops through `numRows`. On the first iteration, it just makes a row of size one with the element `1`. After, it is always in the else condition and it uses the previous row `prev` to create the next row `row`. It uses `i` to figure out how many elements should be in each row, and then loops through that many times with an index `j`. (Note: an optimization would be to define `row`'s size in terms of `i+1` to reduce dynamic memory allocations.) From there, we use `j` to index into `prev` if and only if it is neither too big nor too small. If so, we append `prev[j-1]+prev[j]` to the `row`. Else we append `1`.

And that's the algorithm.

There is another way to do it, though:

```go
func generate(numRows int) [][]int {
	t := make([][]int, numRows)
	for i := 0; i < numRows; i++ {
		row := make([]int, i+1)
		row[0] = 1

		for j := 1; j <= i; j++ {
			row[j] = row[j-1] * (i - j + 1) / j
		}

		t[i] = row
	}

	return t
}
```

The problem is named after the mathematician [Blaise Pascal.](https://en.wikipedia.org/wiki/Blaise_Pascal) The name, ["Pascal's Triangle,"](https://en.wikipedia.org/wiki/Pascal's_triangle) is all you need to know there's a mathematical solution rather than a data one. The code above is exactly that, and it gets rid of unexpected and unnecessary allocations.

Now, in terms of dynamic programming practice, this wasn't the best. The reason why, I think, is because there is no way not to use the previous iteration to generate the next in a cache-like way. So, the solution is pretty obvious. Regardless, I am a fan of _Pascal's Triangle_. It was on the cover of my discrete mathematics book back in undergrad, and I remember liking that class.

Till next time, friends.
