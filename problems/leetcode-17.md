+++
date = '2026-06-03T08:49:11-00:00'
draft = false
title = 'LeetCode 17: Letter Combinations of a Phone Number'
url = '/posts/leetcode-17/'
+++

# From Array Confusion to a Mixed-Radix Decoder: Solving LeetCode 17 in Go

[LeetCode 17, _Letter Combinations of a Phone Number_](https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/) is simple: given a string of digits like `"23"`, return every combination of letters those digits could spell on an old phone keypad. For example, `2` maps to `['a', 'b', 'c']` and if given the input `22`, we would expect the output: `["aa", "ab", "ac", "ba", "bb", "bc", "ca", "cb", "cc"]`.

The classic solution would be to use a depth-first recursion that adds to a data structure when it gets to a leaf. Recursive solutions, though, are generally slower than equivalent loop-based solutions due to the overhead of allocating and tearing down a stack frame — saved registers, return addresses, parameters — on every call. One of the ways that [functional languages](https://en.wikipedia.org/wiki/Functional_programming) attack this problem is [tail recursion](https://en.wikipedia.org/wiki/Tail_call), but [Go](https://go.dev/) does not support tail recursion.

That takes me to the fact that I'm using Go. Why? I currently know three languages well (C, JavaScript, and Python), but I want to add a garbage collected language that is compiled to the list; hence Go.

The rest of this post is the journey with the wrong turns included in how I solved LeetCode 17.

## Step 1: Where Do the Letters Even Live?

The first question wasn't the algorithm at all; it was how to store the digit-to-letters mapping in Go. My instinct was a 2D rune array:

```go
number_to_keys [8][3]rune
```

The digits for the problem are 2–9, so an 8-element array forces a `digit - 2` offset on every access. The problem, though, was that the fixed inner length of 3 doesn't fit `7` (pqrs) or `9` (wxyz). A plain `[]string` handles this because you can call `len()` on a string to get the length. I initially thought this came with a dynamic memory cost, but that was a misconception — string literals in Go are stored in read-only program data, not the heap:

```go
var numberToKeys = [...]string{
    "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz",
}
```

Now, with this we can get the available outputs for every number, but there is a slight hitch. The input for the program is a string. An array of numbers would be more convenient because we could take the number and subtract two from it to get the correct index into `numberToKeys`. Instead we have to take the character `c` and first subtract `'0'` from it and then subtract two: `c - '0' - 2`. The reason we subtract `'0'` is that we are guaranteed by LeetCode that the input will be a string of characters which are numbers. If you know ASCII, then you know that every character is really just a number and the digit characters (0–9) are all in a row. So `'1' - '0'` is `1`, `'2' - '0'` is `2`, and so on.

## Step 2: The Iterative "Expand from Previous" Approach

Instead of recursion, the idea is that `result` (a slice of strings) holds every partial combination built so far, and each new digit _transforms the whole list_: pair every existing string with every letter of the new digit.

The version I came up with seeds `result` from the first digit explicitly, then a second loop handles the rest:

```go
func letterCombinations(digits string) []string {
    if len(digits) == 0 {
        return []string{}
    }

    result := []string{}

    for _, c := range numberToKeys[digits[0]-'0'-2] {
        result = append(result, string(c))
    }

    for _, c := range digits[1:] {
        letters := numberToKeys[c-'0'-2]
        next := make([]string, 0, len(result)*len(letters))
        for _, prefix := range result {
            for _, l := range letters {
                next = append(next, prefix+string(l))
            }
        }
        result = next
    }

    return result
}
```

This works and is `O(4^n · n)`, which is optimal for the output size. But it allocates a new `next` slice every digit and throws the old one away. Can we do better?

## Step 3: Stealing the Right Idea from a "Faster" Solution

I checked what solutions faster than mine were doing, and I came across one that was using recursion. Being me, I was a little annoyed that a recursive solution was beating my iterative one. It was faster because it precomputed the result size once and then allocated exactly once. We can do this as well, by first calculating the correct number of solutions:

```go
resultLength := 1
for _, c := range digits {
    resultLength *= len(numberToKeys[c-'0'-2])
}

result := make([]string, resultLength)
```

But there is a problem with this. Once we have calculated `resultLength` and allocated it, we only have one buffer to use. If we still allocate a `next` slice each round as before, the single preallocation buys nothing. To make it pay off, the whole approach has to change.

## Step 4: The Mixed-Radix Insight

This is the heart of the optimization. Number every combination `0` to `resultLength - 1`. Each number `k` _encodes_ one specific combination, and you can decode it digit by digit — exactly like reading a number in a positional system, except each position has its own base (the letter count of that digit, so either `3` or `4`). Mixed radix.

Concretely, for `"23"` the nine combinations are:

```
k=0: ad
k=1: ae
k=2: af
k=3: bd
k=4: be
k=5: bf
k=6: cd
k=7: ce
k=8: cf
```

Look at the **second** letter: it cycles `d e f d e f d e f`. That's `k % 3`. The **first** letter goes `a a a b b b c c c` — that's `k / 3`, the slow wheel. Like an odometer: the rightmost wheel spins fastest, each wheel to the left advances only when the one to its right wraps.

The general formula for the letter index at a position with letter count `base`:

```
index = (k / place) % base
```

where `place` is **how many `k`-steps pass before this position's letter changes once** — equivalently, the product of the bases of all positions to its _right_. The rightmost position has `place = 1`; moving left, you multiply in the base you just passed. This handles any mix of 3-letter and 4-letter digits with no special-casing — the earlier `% 3` shortcut was just this formula with every base equal.

Because each output slot is computed independently from `k`, there's no aliasing, no traversal order, and no recursion.

We can implement this with a flat loop over `k`, decoding right-to-left while carrying `place`:

```go
result := make([]string, resultLength)

for k := range resultLength {
    place := 1
    buf := make([]byte, len(digits))

    for i := len(digits) - 1; i >= 0; i-- {
        letters := numberToKeys[digits[i]-'0'-2]
        buf[i] = letters[(k/place)%len(letters)]
        place *= len(letters)
    }

    result[k] = string(buf)
}
```

I came across two bugs while working through this:

1. **Wrong loop direction.** Ranging `digits` left-to-right broke `place` accumulation. The decode has to walk positions right-to-left, which means an index loop, not `range`.
2. **`combo += string(...)` reverses the string.** Computing right-to-left and _appending_ produces `"da"` instead of `"ad"`. The fix is a `[]byte` buffer written _by index_ — `buf[i] = letter` lands each character in its correct slot regardless of computation order. No reversal needed; the index write handles ordering for free.

## Step 5: Allocation Discipline

The buffer should be cheap, but Go's escape analysis heap-allocates `make([]byte, len(digits))` because the length is a runtime value. Two fixes:

- **Reuse one buffer** by hoisting it out of the `k` loop. `string(buf)` copies the bytes into each result string, so overwriting `buf` next iteration is safe. This drops `resultLength` allocations to one.
- **Use a fixed-size array** to get it off the heap entirely. LeetCode caps input at 4 digits, so we can use `var buf [4]byte` which has a compile-time-known size and can stack-allocate. The one catch: `string(buf)` would stringify all four bytes including stale/zero trailing bytes, so slice to the real length: `string(buf[:len(digits)])`.

```go
var numberToKeys = [...]string{
    "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz",
}

func letterCombinations(digits string) []string {
    if len(digits) == 0 {
        return []string{}
    }

    resultLength := 1
    for _, c := range digits {
        resultLength *= len(numberToKeys[c-'0'-2])
    }

    result := make([]string, resultLength)
    var buf [4]byte

    for k := range resultLength {
        place := 1
        for i := len(digits) - 1; i >= 0; i-- {
            letters := numberToKeys[digits[i]-'0'-2]
            buf[i] = letters[(k/place)%len(letters)]
            place *= len(letters)
        }

        result[k] = string(buf[:len(digits)])
    }

    return result
}
```

## A Note on Measuring Memory

LeetCode reported memory bouncing between roughly 3.8 and 4.0 MB across submissions. That figure is whole-process RSS — the Go runtime, GC, and test harness dominate, and the sampling has ±0.3 MB jitter. At that scale it cannot resolve a buffer optimization measured in bytes. The right tool is `testing.B` with `-benchmem`, which reports `allocs/op` and `B/op` deterministically.

To benchmark both solutions, put them in a `_test.go` file. Rather than hardcoding one input, generate 1000 random digit strings (lengths 1–4, digits 2–9) with a fixed seed and cycle through them:

```go
var sink []string

func randomInputs(n int) []string {
    rng := rand.New(rand.NewPCG(42, 0))
    inputs := make([]string, n)
    for i := range inputs {
        length := rng.IntN(4) + 1
        buf := make([]byte, length)
        for j := range buf {
            buf[j] = byte('2' + rng.IntN(8))
        }

        inputs[i] = string(buf)
    }
    return inputs
}

func BenchmarkV1(b *testing.B) {
    inputs := randomInputs(1000)
    idx := 0
    b.ResetTimer()

    for b.Loop() {
        sink = letterCombinationsV1(inputs[idx])
        idx = (idx + 1) % 1000
    }
}

func BenchmarkV2(b *testing.B) {
    inputs := randomInputs(1000)
    idx := 0
    b.ResetTimer()
    for b.Loop() {
        sink = letterCombinationsV2(inputs[idx])
        idx = (idx + 1) % 1000
    }
}
```

The `sink` variable prevents the compiler from optimizing away the call. The fixed seed (`PCG(42, 0)`) makes runs reproducible. Run with:

```
go test -bench=. -benchmem -count=3
```

`-benchmem` adds the `B/op` and `allocs/op` columns. `-count=3` runs each benchmark three times to check stability.

Results on an AMD Ryzen AI 9 HX 370 (averages over 5 runs, 1000 random inputs cycled per benchmark):

|                      |  ns/op | B/op | allocs/op |
| :------------------- | -----: | ---: | --------: |
| Iterative (Step 2)   | 1339.6 | 1199 |        59 |
| Mixed-radix (Step 5) |  778.6 |  816 |        39 |

{.styled-table}

The three columns mean: **ns/op** is nanoseconds per function call, **B/op** is heap bytes allocated per function call, and **allocs/op** is the number of distinct heap allocations per function call. The mixed-radix version is ~1.7× faster, uses 32% less memory, and makes 34% fewer allocations.

### Why I'm Unhappy

I like the solution, but I'm unhappy with the number of allocations. If I were writing this in C, I could get the allocations down to probably just 1. So, why can't I do this with Go?

## Step 6: Two Allocations

Instead of a stack buffer that I copy into an output string, I can allocate on contiguous backing array for all the combinations up front. Then I can write each combination directly into its slice of that array and construct each output string as a header pointing into it via `unsafe.String`:

```go
func letterCombinations(digits string) []string {
    if len(digits) == 0 {
        return []string{}
    }

    resultLength := 1
    for _, c := range digits {
        resultLength *= len(numberToKeys[c-'0'-2])
    }

    n := len(digits)
    backing := make([]byte, resultLength*n)
    result := make([]string, resultLength)

    for k := range resultLength {
        place := 1
        for i := n - 1; i >= 0; i-- {
            letters := numberToKeys[digits[i]-'0'-2]
            backing[k*n+i] = letters[(k/place)%len(letters)]
            place *= len(letters)
        }

        result[k] = unsafe.String(&backing[k*n], n)
    }

    return result
}
```

`backing` and `result` are the only heap allocations. So, we are down to TWO allocs/op regardless of input length. Getting to `1` would require changing the return type: if the caller could accept a flat `[]byte` with a known stride of `len(digits)`, the string header slice disappears and only `backing` remains. LeetCode requires `[]string`, so, unfortunately, I believe that `2` is the floor.

There is a trade-off: all returned strings share one backing buffer. A single long-lived string keeps the entire array in memory. With `string(buf[:n])`, each output string owns its bytes independently.

### Benchmark

|                        |  ns/op | B/op | allocs/op |
| :--------------------- | -----: | ---: | --------: |
| Iterative (Step 2)     | 1339.6 | 1199 |        59 |
| Mixed-radix (Step 5)   |  778.6 |  816 |        39 |
| unsafe.String (Step 6) |  689.0 |  822 |         2 |

{.styled-table}

Compared to Step 5: 37 fewer allocations, similar memory footprint, ~12% faster. Compared to Step 2: ~1.9× faster, 31% less memory, 97% fewer allocations.

## Conclusion

I hope that you enjoyed this post. I'll be doing more, I think, as I need to practice these hellish problems if I am ever to get a job. But, more importantly, it isn't a terrible way to learn Go.
