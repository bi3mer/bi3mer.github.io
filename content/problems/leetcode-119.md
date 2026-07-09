+++
date = '2026-07-10T08:07:39-05:00'
draft = false
title = "Leetcode 119: Pascal's Triangle II"
url = '/posts/leetcode-119/'
+++

[LeetCode 119](https://leetcode.com/problems/pascals-triangle-ii/description/) follows up on the previous problem, but instead of generating the whole triangle, we are only going to generate one row. So, please read [the previous post](/posts/leetcode-118/) before reading this one because I'm not going to re-explain the problem.

Moving on.

Each entry in Pascal's Triangle is a [binomial coefficient](https://en.wikipedia.org/wiki/Binomial_coefficient) for row \(i\) and position \(j\) (both 0-indexed):

\[
C(i, j) = \frac{i!}{j!(i-j)!}
\]

We can compute any single row without ever building the rows above it. Now, we could compute \(C(i,j)\) for every element in the row, but factorials aren't very fast to calculate. So, what we can do instead is try to use the previously calculated element in the row to calculate the next. The way we can do this is by checking if we can find a ratio or scale factor:

\[
\begin{aligned}
\frac{C(i, j)}{C(i, j-1)}
&= \frac{i!/(j!(i-j)!)}{i!/((j-1)!(i-j+1)!)} \\
&= \frac{(j-1)!(i-j+1)!}{j!(i-j)!} \\
&= \frac{i-j+1}{j}
\end{aligned}
\]

So with this ratio, we can avoid the factorials by defining \(C(i,j)\) recursively:

\[
C(i, j) = C(i, j-1) \cdot \frac{i - j + 1}{j}
\]

But we don't have to do the calculation recursively. We start with `row[0] = 1` (since \(C(i, 0)\) is always \(1\)) and walk left to right, deriving each entry from the one just before it using that ratio. And here is this implemented in Go:

```go
func getRow(rowIndex int) []int {
    row := make([]int, rowIndex+1)
    row[0] = 1

    for i := 1; i <= rowIndex; i++ {
        row[i] = row[i-1] * (rowIndex - i + 1) / i
    }

    return row
}
```

This solution is faster than 100% of solutions on LeetCode, and is about as fast as it can get, I think.

Till next time, friends.