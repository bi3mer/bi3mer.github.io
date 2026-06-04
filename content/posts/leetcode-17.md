+++
date = '2026-06-03T22:49:07-04:00'
draft = true
title = 'Leetcode 17'
+++

# From Array Confusion to a Mixed-Radix Decoder: Solving LeetCode 17 in Go

[LeetCode 17, *Letter Combinations of a Phone Number*](https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/), looks deceptively simple: given a string of digits like `"23"`, return every combination of letters those digits could spell on an old phone keypad (`["ad","ae","af","bd",...]`). The classic solution is a recursive backtrack, but I went a different way — an iterative build that ends in a flat loop with almost no allocations. This is the whole journey, including the wrong turns, because the wrong turns are where the learning happened.

## Step 1: Where do the letters even live?

The first question wasn't the algorithm at all — it was how to store the digit-to-letters mapping in Go. My instinct was a 2D rune array:

```go
number_to_keys [8][3]rune
```

This has three problems. The digits are 2–9, so an 8-element array forces a `digit - 2` offset on every access. The fixed inner length of 3 doesn't fit `7` (pqrs) or `9` (wxyz), which have four letters. And padding the short rows with zero-value runes means skipping zeros while iterating.

A plain `[]string` (or fixed array of strings) sidesteps all of it — variable lengths handled natively, and ranging over a string yields runes anyway:

```go
var numberToKeys = [...]string{
    "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz",
}
```

I dropped the two empty leading slots for digits 0 and 1, which means the index math is `c - '0' - 2` (digit `'2'` maps to index `0`). A small tax, but the array stays compact.

## Step 2: A few Go fundamentals

A handful of language details came up that are worth stating plainly:

- **Array vs. slice.** `[N]T` is a fixed-size array whose length is part of its type; `[]T` is a dynamic slice. `[...]T{...}` infers the array length at compile time.
- **`make([]T, length, capacity)`.** The second argument is *length* (elements that exist now), the third is *capacity* (room before a reallocation). `append`-style building uses `(0, cap)`; index-style building uses `(length)`.
- **`append` returns a new header.** You must reassign: `s = append(s, x)`. Ignoring the return is the classic Go bug.
- **String + rune doesn't concatenate.** `someString + r` won't compile; you need `someString + string(r)`.
- **Reslicing.** `s[k:]` drops the first `k` elements; `s[:k]` keeps the first `k`. The colon position is the whole difference.

## Step 3: The iterative "expand from previous" approach

Instead of recursion, the idea is that `result` holds every partial combination built so far, and each new digit *transforms the whole list*: pair every existing string with every letter of the new digit.

The elegant trick is to seed `result` with a single empty string. Then the first digit's round pairs `""` with its letters and produces `"a","b","c"` — handled by the same loop as every other digit:

```go
result := []string{""}
for _, c := range digits {
    letters := numberToKeys[c-'0'-2]
    next := make([]string, 0, len(result)*len(letters))
    for _, prefix := range result {
        for _, l := range letters {
            next = append(next, prefix+string(l))
        }
    }
    result = next
}
```

I actually preferred a two-phase version — one loop to seed from the first digit, another for the rest — because it makes the special case explicit instead of leaning on the empty-string sentinel. Both are correct. The tradeoff is duplicated build logic (two-phase) versus a slightly implicit "aha" (unified).

Two things mattered here regardless of phrasing:

- **The empty-input guard.** `letterCombinations("")` must return `[]`, not a panic and not `[""]`. `if len(digits) == 0 { return []string{} }` goes at the top.
- **Build into a fresh `next`, don't reslice in place.** Reading the previous round while writing the new one needs two buffers; the separate `next` *is* that second buffer.

This works and is `O(4^n · n)` — optimal for the output size. But it allocates a new `next` every digit and throws the old one away.

## Step 4: Stealing the right idea from a "faster" solution

A faster submission I came across used recursion plus a `map[string][]string`. Its real speed win wasn't the recursion — it was **precomputing the exact result size and allocating once**:

```go
resultLength := 1
for _, c := range digits {
    resultLength *= len(numberToKeys[c-'0'-2])
}
```

Notably, the map actually works *against* it — string-keyed lookups hash a string every call, slower than a direct array offset. The lesson to keep was the single preallocation; the map and recursion were not worth copying.

But here's the catch: preallocating `resultLength` only pays off if you fill **one** buffer all the way to the end. In the expand-from-previous structure, each `next` already sizes itself exactly, so the big preallocation buys nothing — the final result just ends up in a per-round slice. To make the size earn its keep, the whole build had to change.

## Step 5: The mixed-radix insight

This is the heart of it. Number every combination `0` to `resultLength - 1`. Each number `k` *encodes* one specific combination, and you can decode it digit by digit — exactly like reading a number in a positional system, except each position has its own base (the letter count of that digit). Mixed radix.

Concretely, for `"23"` the nine combinations are:

```
k=0: ad   k=3: bd   k=6: cd
k=1: ae   k=4: be   k=7: ce
k=2: af   k=5: bf   k=8: cf
```

Look at the **second** letter: it cycles `d e f d e f d e f` — that's `k % 3`, the fast wheel. The **first** letter goes `a a a b b b c c c` — that's `k / 3`, the slow wheel. Like an odometer: the rightmost wheel spins fastest, each wheel to the left advances only when the one to its right wraps.

The general formula for the letter index at a position with letter count `base`:

```
index = (k / place) % base
```

where `place` is **how many `k`-steps pass before this position's letter changes once** — equivalently, the product of the bases of all positions to its *right*. The rightmost position has `place = 1`; moving left, you multiply in the base you just passed. This handles any mix of 3-letter and 4-letter digits with no special-casing — the earlier `% 3` shortcut was just this formula with every base equal.

Because each output slot is computed independently from `k`, there's no aliasing, no traversal order, and crucially **no recursion**.

## Step 6: Writing it — and the bugs along the way

A flat loop over `k`, decoding right-to-left while carrying `place`:

```go
result := make([]string, resultLength)
for k := range resultLength {
    place := 1
    for i := len(digits) - 1; i >= 0; i-- {
        letters := numberToKeys[digits[i]-'0'-2]
        // ... index = (k / place) % len(letters) ...
        place *= len(letters)
    }
}
```

Three bugs surfaced in order:

1. **Wrong loop direction.** Ranging `digits` left-to-right broke `place` accumulation. The decode has to walk positions right-to-left, which means an index loop, not `range`.
2. **`make([]string, 0, resultLength)` then `result[k] = ...` panics.** Capacity isn't length. Index-style filling needs `make([]string, resultLength)`.
3. **`combo += string(...)` reverses the string.** Computing right-to-left and *appending* produces `"da"` instead of `"ad"`. The fix is a `[]byte` buffer written *by index* — `buf[i] = letter` lands each character in its correct slot regardless of computation order. No reversal needed; the index write handles ordering for free.

## Step 7: Allocation discipline

The buffer should be cheap, but Go's escape analysis heap-allocates `make([]byte, len(digits))` because the length is a runtime value. Two fixes:

- **Reuse one buffer** by hoisting it out of the `k` loop. `string(buf)` copies the bytes into each result string, so overwriting `buf` next iteration is safe. This drops `resultLength` allocations to one.
- **Use a fixed-size array** to get it off the heap entirely. LeetCode caps input at 4 digits, so `var buf [4]byte` has a compile-time-known size and can stack-allocate. The one catch: `string(buf)` would stringify all four bytes including stale/zero trailing bytes, so slice to the real length: `string(buf[:len(digits)])`.

## The final solution

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

What makes it lean:

- Package-level lookup table — built once at load, not per call.
- Single `result` allocation, sized exactly via the precomputed product.
- Stack-allocated `[4]byte` buffer, reused, sliced to length on output.
- Flat iterative mixed-radix decode — no map, no recursion, no intermediate slices.

The only unavoidable heap allocations are the `result` slice and the output strings themselves, which the caller needs to keep.

## A note on measuring memory

LeetCode reported memory bouncing between roughly 3.8 and 4.0 MB across submissions. That figure is whole-process RSS — the Go runtime, GC, and test harness dominate, and the sampling has ±0.3 MB jitter. At that scale it literally cannot resolve a buffer optimization measured in bytes. To actually measure the difference, `testing.B` with `-benchmem` reports `allocs/op` and `B/op` deterministically — that's where this version's fewer allocations would actually show up.

## Takeaways

- Pick the data structure that fits the data, not the first one that comes to mind. A `[]string` beat a padded `[N][M]rune` decisively.
- An explicit special case and a folded-in general case are both valid; know which you're choosing and why.
- The fastest version often steals one idea (here: preallocate the exact size) from a slower one while discarding the rest (the map, the recursion).
- Mixed-radix decoding turns "enumerate all combinations" into an independent, flat, recursion-free computation per output slot.
- Write into a fixed buffer *by index* to decouple computation order from output order.
- Trust deterministic benchmarks over coarse RSS sampling when chasing allocations.