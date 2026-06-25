+++
date = '2026-06-25T08:24:00-05:00'
draft = false
title = 'Leetcode 6: Zigzag Conversion'
url = '/posts/leetcode-6/'
+++

[LeetCode 6](https://leetcode.com/problems/zigzag-conversion/description/) is obnoxious. I say this without having solved it or written any code. I've only read the examples.

```
Example 1:
  Input: s = "PAYPALISHIRING", numRows = 3
  Output: "PAHNAPLSIIGYIR"
  Explanation:
  P   A   H   N
  A P L S I I G
  Y   I   R

Example 2:
  Input: s = "PAYPALISHIRING", numRows = 4
  Output: "PINALSIGYAHRPI"
  Explanation:
  P     I    N
  A   L S  I G
  Y A   H R
  P     I

Example 3:
  Input: s = "A", numRows = 1
  Output: "A"
```

The obvious solution is to use `numRows` to allocate the required number of rows as strings. Then you append characters going down the rows, then back up, then down again, and so on until you've reached the last character in `s`. But, I'm not going to code that, because I said I wouldn't in the [previous post.](/posts/leetcode-5/) Instead, I'm going to go with what I'm sure is the correct answer.

The correct answer is index based. Instead of allocating data, we should be able to use the index to figure out where each character goes in the output string.

How?

The key thing to notice is what I'm going to call the _stride_, which is to say how far you have to move along the string to get to the next character in the same row. In examples 1 and 2, the input string is "PAYPALISHIRING." Example 1 uses `numRows=3`:

```
P   A   H   N
A P L S I I G
Y   I   R
```

The stride is the distance from 'P' to 'A' on the top row. You go down `numRows-1` steps, then back up `numRows-1` steps to complete one full cycle, so we calculate that with:

```go
stride = 2*(numRows - 1)
```

So in the case of example 1, we have `stride=2*(3-1)=4`. This tells us how we get to the next character 'A'. What this doesn't do, though, is handle the characters that cross upwards. So, in effect, we can only make the first row correctly:

```go
import "fmt"

func convert(s string, numRows int) string {
    if numRows == 1 {
        return s
    }

    chars := make([]byte, len(s))
    stride := 2 * (numRows - 1)
    cIndex := 0

    for i := 0; i < len(s); i += stride {
        chars[cIndex] = s[i]
        cIndex++
    }

    return string(chars[:cIndex])
}

func main() {
	fmt.Printf("convert(3): %s\n", convert("PAYPALISHIRING", 3))
	fmt.Printf("convert(4): %s\n", convert("PAYPALISHIRING", 4))
}
```

Outputs:

```
convert(3): PAHN
convert(4): PIN
```

So, now, if we want, we can construct all the rows (except the zigzags) with one simple change.

```go
func convert(s string, numRows int) string {
    if numRows == 1 {
        return s
    }

    chars := make([]byte, len(s))
    stride := 2 * (numRows - 1)
    characterIndex := 0

    for offset := 0; offset < numRows; offset++ {
	    for index := offset; index < len(s); index += stride {
	        chars[characterIndex] = s[index]
	        characterIndex++
	    }
    }

    return string(chars[:characterIndex])
}
```

Outputs:

```
convert(3): PAHNALIGYIR
convert(4): PINASGYHPI
```

The change is adding an outer loop that iterates over each row, and `index` is initialized to `offset`. The only thing to add is the zigzag. To do that, we have to notice a few things:

```
P     I    N
A   L S  I G
Y A   H R
P     I
```

1. Zigzag characters are never on the top or bottom row.
2. Between each pair of major columns, there is exactly one zigzag character per middle row.
3. Distance from column is based on `offset`.

So based on the second note, we know that we can add the in-between `char` after the letter just placed. For example, after we place 'Y', we can place 'A' in the example above. To do that, though, we need to first make sure that we aren't in the top or bottom row. We can do that with `offset` because offset is the row:

```go
// inside second for loop after character placement
if offset > 0 && offset < numRows - 1 {
	chars[characterIndex] = s[???]
	characterIndex++
}
```

Now we need to figure out what the index is for `s`, which is where the third point comes into play. Each cycle (one full down-and-up pass through the zigzag) has length `stride`, and within that cycle the main character lands at position `offset` from the start. The zigzag character lands at its mirror: `stride - offset`. So the distance between them is `stride - offset - offset`, or `stride - 2*offset`.

```go
zagIndex := index + stride - 2*offset
if offset > 0 && offset < numRows - 1 && zagIndex < len(s){
	chars[characterIndex] = s[zagIndex]
	characterIndex++
}
```

That's the solution, and it works.

The downside of trying to one-shot without other solutions is that there is nothing to benchmark. The upside is that this post took much less time than usual. But, I hope the increased emphasis on the problem-solving aspect made up for the lack of a benchmark.

Till next time, friends.

---

```go
func convert(s string, numRows int) string {
    if numRows == 1 {
        return s
    }

    chars := make([]byte, len(s))
    stride := 2 * (numRows - 1)
    characterIndex := 0

    for offset := 0; offset < numRows; offset++ {
	    for index := offset; index < len(s); index += stride {
	        chars[characterIndex] = s[index]
	        characterIndex++

            zagIndex := index + stride - 2*offset
            if offset > 0 && offset < numRows - 1 && zagIndex < len(s){
                chars[characterIndex] = s[zagIndex]
                characterIndex++
            }
	    }
    }

    return string(chars)
}
```
