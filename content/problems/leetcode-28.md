+++
date = '2026-06-14T07:58:24-05:00'
draft = false
title = 'LeetCode 28: Find the Index of the First Occurrence in a String'
url = '/posts/leetcode-28/'
+++

[LeetCode 28](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) is another very easy problem. You are given two strings, and you have to see if the second string exists in the first string. If so, return the index of the start of that string. If it can't be found, return -1.

# Solution 1: `strings.Index`

This kind of problem is so common in programming, that the majority of standard libraries include it. In C, you can use `strstr`. In Go, you can use `strings.Index()`.

```go
import "strings"

func strStr(haystack string, needle string) int {
    return strings.Index(haystack, needle)
}
```

I doubt, though, that the problem's maker wanted us to use the standard library. So, let's implement the function ourselves.

# Solution 2: Iterating by Character

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
The only trick to notice is that the for loop uses `i <= len_haystack - len_needle` as its stopping condition. I think the best way to explain this condition is with an example. Let's say we receive as input `haystack="haystack", needle="genetic"`. The difference between the lengths of both strings is `8-7=1`. So, rather than doing comparisons that are doomed to fail after the letter 'a', we stop the loop.
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

The code is doing effectively the same thing. The difference is that instead of doing character by character comparisons, we compare two strings. However, there is a difference when we get to performance.

# Solution 4: Best of Both Worlds

```go
func strStr(haystack string, needle string) int {
    for i := 0; i <= len(haystack) - len(needle); i++ {
        if haystack[i] == needle[0] {
            if haystack[i+1:i+len(needle)] == needle[1:] {
                return i
            }
        }
    }

    return -1
}
```

While I was finishing up the first version of this blog post, I realized that I could improve the performance in the general case. What led to this was an observation that the `char` solution was fast when the `needle` was later in the string and slower than the slice solution when the `needle` was early. I'll explain why in the benchmark section. This solution uses that observation to check the first character quickly and then only do a full compare if the first characters were the same. (I kind of gave away the why with that sentence. Oh well.)

# Benchmark

Benchmarks were run on an AMD Ryzen AI 9 HX 370 across three haystack lengths (n=100, 1000, 10000), a needle-to-haystack ratio of 5%, and three scenarios: the needle appears at the start (`early`), middle (`middle`), or end (`late`). The full benchmark code is [available on GitHub](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-28). Solution 1 is `strings.Index`. Solution 2 is Char. Solution 3 is Slices. Solution 4 is CharSlice.

**Early**

| n     | `strings.Index` | Char    | Slices  | CharSlice |
| ----- | --------------- | ------- | ------- | --------- |
| 100   | 3.885ns         | 4.305ns | 2.588ns | 2.688ns   |
| 1000  | 5.030ns         | 21.67ns | 3.962ns | 3.930ns   |
| 10000 | 8.410ns         | 278.9ns | 6.707ns | 7.232ns   |

The needle matches at position 0, so every solution finds it on the first try. Slices is the fastest of the bunch. This is because the string comparison compiles to `CALL runtime.memequal(SB)`, which compares a block of memory at once and so the comparison is very fast. Compare this to Char which has to match byte-by-byte. With a needle that is 5% of `n`, that means you have 5 bytes at `n=100` and 500 bytes at `n=10000`, showing why the cost soars to 278.9ns.

The other two solutions, `strings.Index` and CharSlice, are slower than Slices and faster than Char. The reason is that both have a cost. CharSlice's cost is that it checks the first character first so it can be faster if the needle is later in `haystack`. `strings.Index` has a similar cost, but it also analyzes the strings first to determine which algorithm it will run.

**Middle**

| n     | `strings.Index` | Char    | Slices  | CharSlice |
| ----- | --------------- | ------- | ------- | --------- |
| 100   | 17.28ns         | 42.18ns | 86.29ns | 19.70ns   |
| 1000  | 89.24ns         | 485.6ns | 701.2ns | 155.7ns   |
| 10000 | 919.1ns         | 4985ns  | 6710ns  | 1597ns    |

With the needle in the middle, every solution scans roughly half the haystack. CharSlice comes closest to `strings.Index`, running 2–4x slower rather than 5–7x. This works because CharSlice skips `memequal` at most positions and only runs it when the first byte agrees. Slices has no such guard and pays for a `memequal` call at every position, making it the slowest naive solution. Char bails on the first mismatched byte, which is better than a full wasted `memequal`, but slower than CharSlice's guard.

**Late**

| n     | `strings.Index` | Char    | Slices  | CharSlice |
| ----- | --------------- | ------- | ------- | --------- |
| 100   | 32.09ns         | 85.61ns | 190.0ns | 36.87ns   |
| 1000  | 191.9ns         | 884.6ns | 1376ns  | 313.0ns   |
| 10000 | 1860ns          | 10216ns | 13481ns | 3253ns    |

The late case amplifies the middle pattern. CharSlice's first-character guard still filters most positions cheaply, keeping it roughly 2x slower than `strings.Index`. Slices remains worst: every position triggers a full `memequal` that comes back false. Char beats Slices because it bails on the first mismatched byte, but is still much slower than `strings.Index` and `CharSlice`.

# Conclusion

`strings.Index` wins by a large margin in every non-trivial case. My three implementations were fun, but, unsurprisingly, slower. So, why are my solutions worse? CharSlice was one step in a long path people have taken to make really fast algorithms. The next step would be to examine one of the major points of wasted work, which is that every string comparison throws away work. Meaning, after string comparison fails, we step one character forward and then do another comparison. What if, instead, we could skip further ahead based on that string comparison?[^1]

That question has motivated algorithms like [Boyer-Moore](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm), [Knuth-Morris-Pratt](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm), and the [many other variants](https://en.wikipedia.org/wiki/String-searching_algorithm) that exist. Go's `strings.Index` itself uses [Rabin-Karp](https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm) for longer needles and a variant of [Boyer-Moore-Horspool](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore%E2%80%93Horspool_algorithm) for short ones ([GitHub](https://github.com/golang/go/blob/master/src/internal/stringslite/strings.go#L28)). These algorithms are out of scope for this blog post, but their existence shows how even a problem listed as "easy" can be surprisingly deep if you care to look.

Till next time, friends.

[^1]: This is a good time to point out that my benchmark did not have the worst case. The worst case is a haystack full of repeated characters with a needle that almost-matches at every position (e.g. haystack=`"aaaaaa…a"`, needle=`"aaab"`). Char would perform significantly worse, since it would do `len(needle)-1` character comparisons `len(haystack)` times. It would also cause CharSlice to perform worse than Slice. `strings.Index`, though, would, I bet, maintain a strong performance.
