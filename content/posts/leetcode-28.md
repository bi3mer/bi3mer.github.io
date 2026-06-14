+++
date = '2026-06-13T18:58:24-05:00'
draft = true
title = 'LeetCode 28'
+++

[LeetCode 28](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) is another very easy problem. You are given two strings, and you have to see if the second string exists in the first string. If so, return the index of the start of that string. If it can't be found, return -1.

# Solution 1: `strings.Index`

This kind of a problem is so common in programming, that the majority of standard libraries include it. In C, you can use `strstr`. In Go, you can use `strings.Index()`.

```go
import "strings"

func strStr(haystack string, needle string) int {
    return strings.Index(haystack, needle)
}
```

I doubt, though, that the problem's maker wanted us to use the standard library. So, let's implement the function ourselves.

# Solution 2: Iterating by Hand

```go
func strStr(haystack string, needle string) int {
    len_haystack := len(haystack)
    len_needle := len(needle)

    for i := 0; i <= len_haystack - len_needle; i++ {
        valid := true
        i_copy := i

        for j := 0; j < len(needle) && valid; j, i_copy = j+1, i_copy+1 {
            if i_copy >= len(haystack) || haystack[i_copy] != needle[j] {
                valid = false
            }
        }

        if valid {
            return i
        }
    }

    return -1
}
```

This solution has a runtime of 0ms, and beats 100% of submissions.
The only trick to notice is that the for loop uses `i <= len_haystack - len_needle` as its stopping condition. I think the best way to explain this condition is with an example. Lets say we receive as input `haystack="haystack", needle="genetic"`. The difference between the lengths of both strings is `8-7=1`. So, rather than doing comparisons that are doomed to fail after the letter 'a', we stop the loop.
The downside of this approach is that the code is a bit hard to read. So, let's improve that using slices.

# Solution 3: Slices

```go
func strStr(haystack string, needle string) int {
    for i := 0; i <= len(haystack) - len(needle); i++ {
        if haystack[i:i+len(needle)] == needle {
            return i
        }
    }

    return -1
}
```

The code is doing effectively the same thing. The difference is that instead of doing character by character comparisons, we compare two strings.

# Benchmark

Benchmarks were run on an AMD Ryzen AI 9 HX 370 across three haystack lengths (n=100, 1000, 10000), three needle-to-haystack ratios (1%, 5%, 10%), and three scenarios: the needle appears at the start (`early`), at the end (`late`), or not at all (`nomatch`). The full benchmark code is [available on GitHub](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-28). Solution 1 is represented by `strings.Index`. Solution 2 is represented by Char. Solution 3 is represented by Slices.

**Early**

| n     | `strings.Index` | Char    | Slices  |
| ----- | --------------- | ------- | ------- |
| 100   | 2.873ns         | 1.788ns | 2.695ns |
| 1000  | 3.965ns         | 5.989ns | 2.793ns |
| 10000 | 5.128ns         | 63.91ns | 3.865ns |

The needle matches at position 0 here, so every solution finds it on the first try. The interesting part is how each one degrades as n grows. Because the needle is a fixed 1% of the haystack, a larger n means a longer needle to confirm at position 0. Char pays for this linearly: it confirms the match one byte at a time, so its cost climbs with needle length (1.788ns to 63.91ns). Slices stays nearly flat because that single comparison compiles down to `CALL runtime.memequal(SB)`, which compares a block of memory at once rather than byte by byte. `strings.Index` carries some fixed setup overhead but scales well for the same reason.

**Late**

| n     | `strings.Index` | Char    | Slices  |
| ----- | --------------- | ------- | ------- |
| 100   | 3.031ns         | 9.926ns | 22.72ns |
| 1000  | 246.2ns         | 923.4ns | 1503ns  |
| 10000 | 2005ns          | 10250ns | 14430ns |

Now the needle sits at the end, so all three scan most of the haystack before finding it. The block comparison that helped Slices in the `early` case hurts it here because at every failing position it builds a slice header and runs a full `memequal`, only to throw the result away. (This, by the way, is a clue for how you could make a faster version, if you were inclined to do so.) Char, by contrast, bails on the first mismatched byte at each position. That early exit is why Char beats Slices across the board here, by over 2x at n=100 (9.926ns vs 22.72ns).

**No Match**

| n     | `strings.Index` | Char    | Slices  |
| ----- | --------------- | ------- | ------- |
| 100   | 3.534ns         | 73.93ns | 177.3ns |
| 1000  | 11.00ns         | 665.0ns | 1436ns  |
| 10000 | 91.47ns         | 7327ns  | 14360ns |

`strings.Index` is the clear winner. For `nomatch` at n=10000 it finishes in **91ns**, versus **7327ns** for Char and **14360ns** for Slices, roughly 80x and 150x slower respectively. This is not a coincidence: Go's `strings.Index` uses [Rabin-Karp](https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm) for longer needles and a variant of [Boyer-Moore-Horspool](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore%E2%80%93Horspool_algorithm) for short ones, both of which skip ahead in the haystack instead of checking every position. The same first-mismatch early exit that helped Char in the `late` case helps it again here: with no match, the mismatch usually comes within the first byte or two at each position, so Char stays ahead of Slices.

# Conclusion

`strings.Index` wins by a large margin in every non-trivial case. My two implementations were fun, but, unsurprisingly, slower.
My two solutions also trade places depending on the input. Slices wins when matches are common and early, where one `memequal` beats a hand-rolled byte loop. Char wins when comparisons fail fast, because it bails on the first mismatched byte instead of comparing a whole block it is about to discard. But neither ever catches the standard library. Where both of mine check every position one at a time, `strings.Index` skips ahead.

That skip-ahead is also why this benchmark does not represent a worst case for the naive solutions. A haystack full of repeated characters with a needle that almost-matches at every position (e.g. haystack=`"aaaaaa…a"`, needle=`"aaab"`) would make both Char and Slices significantly worse, while `strings.Index` would still handle it efficiently.

This is exactly the kind of problem that motivated algorithms like [Boyer-Moore](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm), [Knuth-Morris-Pratt](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm), and the [many other variants](https://en.wikipedia.org/wiki/String-searching_algorithm) that exist. Go's `strings.Index` itself uses [Rabin-Karp](https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm) for longer needles and a variant of [Boyer-Moore-Horspool](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore%E2%80%93Horspool_algorithm) for short ones. They are out of scope here, but their existence shows how even a problem listed as "easy" can be surprisingly deep if you care to look. If you are curious, you can see Go's implementation on [GitHub.](https://github.com/golang/go/blob/master/src/internal/stringslite/strings.go#L28)

Till next time, friends.
