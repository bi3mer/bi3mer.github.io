+++
date = '2026-06-08T10:10:27-05:00'
draft = false
title = 'LeetCode 22: Generate Parentheses'
url = '/posts/leetcode-22/'
+++

Welcome back. This time we are going to work on [problem 22](https://leetcode.com/problems/generate-parentheses/). The idea is simple. We need to generate every possible valid string of open and closed parenthesis for an integer `n`. The example they give is for `n=1` and `n=3`:

```
Input: n = 1
Output: ["()"]

Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]
```

# Failed Attempt

```go
func generateParenthesis(n int) []string {
    var strings []string
    switch n {
    case 0:
        // do nothing
    case 1:
        strings = append(strings, "()")
    default:
        old_strings := generateParenthesis(n - 1)
        for _, o := range old_strings {
            strings = append(strings, "()" + o)
            strings = append(strings, "(" + o + ")")
        }
    }
    return strings
}
```

This was my first solution, but it failed. The reason why can be shown with `n=3`, where it can't generate the string "(())()". This may lead you to think that you should add one more line in the `for` loop: `strings = append(strings, o + "()")`. This, though, will cause duplicate strings, which breaks the rules. So, after that we could go the de-duplication route like we did for [#18](https://bi3mer.github.io/posts/leetcode-18/), but I'd rather not. So, let's abandon this solution and go to the smarter approach.

# Actual Solution: Recursive Backtracking

```go
func generateParenthesis(n int) []string {
    var strings []string
    var backtrack func(current string, open int, close int)
    backtrack = func(current string, open int, close int) {
        if open == n && close == n {
            strings = append(strings, current)
            return
        }
        if open < n {
            backtrack(current + "(", open + 1, close)
        }
        if close < open {
            backtrack(current + ")", open, close + 1)
        }
    }
     backtrack("", 0, 0)
     return strings
}
```

The idea here is to count how many open and closed parenthesis that are currently in the string, and then add accordingly. However, rather than count the open and closed counts every time, we add them as function parameters and track them. After that, the only trick is to get the base case right, and to make sure that you don't add a closing parenthesis if there isn't an open one.

## Does the Inline Function Matter?

Instead of declaring a function inline, we can declare it outside of the `generateParenthesis` function:

```go
func backtrack(current string, open, close, n int, result *[]string) {
	if open == n && close == n {
		*result = append(*result, current)
		return
	}
	if open < n {
		backtrack(current+"(", open+1, close, n, result)
	}
	if close < open {
		backtrack(current+")", open, close+1, n, result)
	}
}

func generateParenthesis(n int) []string {
    var strings []string
		backtrack("", 0, 0, n, &strings)
    return strings
}
```

Does that, though, have any effect on performance in Go?

To find out, I benchmarked both with `testing.B` and `-benchmem -count=5`. The full benchmark code is [on GitHub](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-22). Each solution generates all valid combinations for n ∈ {1, 5, 8, 10}. Results are averages over five runs on an AMD Ryzen AI 9 HX 370.

| n   | Inline (ns/op)      | External (ns/op)    |
| --- | ------------------- | ------------------- |
| 1   | 34 ± 1              | 39 ± 3              |
| 5   | 4,177 ± 405         | 4,296 ± 762         |
| 8   | 157,386 ± 16,664    | 168,797 ± 8,416     |
| 10  | 2,982,214 ± 281,562 | 2,534,567 ± 176,877 |
{ .styled-table }

`B/op` and `allocs/op` were identical across both approaches for every value of `n`. There was noise for `ns/op` at `n=1` and `n=5`. At `n=8` the inline version pulled ahead, but at `n=10` the two crossed back over and the error bars overlap, so the most we can honestly say is that the effect, if real, is too small for this benchmark to pin down. Still, it's worth looking at [the compiled code](https://godbolt.org/#z:OYLghAFBqd6QCxAYwPYBMCmBRdBLAF1QCcAaPECAMzwBtMA7AQwFtMQByARg9KtQYEAysib0QXACx8BBAKoBnTAAUAHpwAMvAFYTStJg1DBUpJfWQE8Ayo3QBhVLQCuLBnrsAZPA0wA5VwAjTGIQSQBWUgAHVAVCawZHFzc9GLirAW9fAJZg0IizTAsMhiECJmICJNd3LkLihLKKgiz/IJCwyIVyyuqUuu7m1py8zoBKM1RnYmR2DgB6eYBqABUATyjMJbWp4iW0LCWEEMxSJZIl2lQmdCXDJcxVVij6ADoAUg0AQSimZABrJjALZRT5fMFUZwMZBLYG%2BYhMAgqCqMAjHOIKCAMJY%2BAhjJbvcIAIUJABFusQfMACQB2EnfJaMpYANwqSwpVIUBOJZI5RjBYKZLLZgT%2B/wICIBS0h0IgyGmxFR7IlVLOqE22NxZ2QVyUOMEY0FTNFAIlYoJAGZSdKocg5QqlXzgGqNfqCNrdVtcfj3nSjULGXgqOdXe8rWHrdj3gAmABsMdj%2B09ltJEaWUb9DID2adXLTTCiGvQEFz2odBv92aZioI0wYlaFvtT3wbTKDIcYlvs6dp9K%2BVYDJvFkv%2B9uIisEBOjRKn0YgMejLs7MZndSTsUwhqz2abAu3AfbOo3XY7Gb7A6FQ7NALHE4IU5nC8N0cXp49x5XSy4W/7Vd3%2B//cF9yWK8R3nF8FzODQoJ/AMazrZVKSMBQBRpZsgK%2BGUYVAsVb0dFUjCXBh3yUM5NUEM5FQUZxaHvAAqQkSXCckCOAH1MyAgBOdt1WXcMrR7BME3XPUIzTM8904z5OLoqiaPvfNCzsCBZMwajaLLcdUR/aTpPg4h6xbDQpLQySeNDC1uwkoypOMnCb3lLTBBXBdwNfXj62nNcj1I9NKLU%2BSdOMwDpMPZMw27Dze0k6T7NHRy7xcl9n3cjUSMwFc12IpY5NooKTPQkLviw2FGBCRFkTvdE8AUOdyLxbkmJYpDqV9PtpNZPZcoUnlmKdSS4rcyClmgkayLOBNuvy/TsW61D0I4CZaE4cJeHcDgtFIVBOAAcVQdldlmKcLR4UgCE0RaJn%2BEBwmg5aOEkNaLq2zheAUEBoPOjbFtIOBYCQNAWCiOgQnIShAeB%2BhQmAWguDjaCaFokJ3ogQJnsCHwKjWThTox5hiDWAB5QJtEwSwcd4QG2EEQmGFobHvtILBAmcYB7DEWh3u4XgsBYQwYbmTb8EVSw8GZNTnseMnnCRZ7cSKZ7aDwQIEQJxwsGelUWAp0hxeIQIN1JTA%2BaMJWjAuiYqAMYAFAANTwTAAHdCY1HX%2BEEEQxHYKQZEERQVHURndDqAxzZMfRlfeyAJnVEoud4VA9cpLAo4gCZzDJkpbAYBwnBqEBY2kLwfDaXIOgtcJOOiWJ4gEPp3EL6v0gSYZ2lCCuq4z0WBCaXo8/6epM8aHoWhLkYOgGEf670QZKlbsvQm/SZplmCQlpWp7Ge2jgllUAAOWMAFpC9hGEuFeONXg0JYIFwQgLhjE6xl4L6tDGK6bruzhHtIdbNu3t6H0zoW3XhwaMm9/6vWAd9d%2ButkYJDCEAA%3D%3D).

The difference between the generated assembly is minimal, but the compiled code is not the same. To call the inline function, the assembly does the following:

```assembly
MOVQ    command-line-arguments.&backtrack+72(SP), DX  ; DX = &backtrack (stack addr of the func var)
MOVQ    (DX), DX                                      ; DX = closure struct ptr
MOVQ    (DX), R8                                      ; R8 = first field of closure = function pointer
...
CALL    R8
```

In comparison, the external function uses a direct call `CALL command-line-arguments.backtrack(SB)`. At this point, the difference hopefully makes sense. The inline call is one indirect call preceded by an extra few loads; the external one is a single direct call. When we call `backtrack` only a few times, there is virtually no cost to either. Call it ten thousand times and there are more of those tiny loads in the inline path. They can add up in principle, but as the `n=10` row shows, at this scale the effect is small enough that the benchmark can't actually measure it.

# Iterative Backtracking

```go
type state struct {
    current     string
    open, close int
}

func generateParenthesis(n int) []string {
    var result []string
    stack := []state{{"", 0, 0}}
    for len(stack) > 0 {
        s := stack[len(stack)-1]
        stack = stack[:len(stack)-1]
        if s.open == n && s.close == n {
            result = append(result, s.current)
            continue
        }
        if s.open < n {
            stack = append(stack, state{s.current + "(", s.open + 1, s.close})
        }
        if s.close < s.open {
            stack = append(stack, state{s.current + ")", s.open, s.close + 1})
        }
    }
    return result
}
```

The iterative version has more code than the recursive one. This is, in my experience, something that always seems to happen. The reason is that the recursive version implicitly handles the relevant data for you, while in the iterative version you have to manually manage the data. The folk wisdom is that iterative code, when done well, is more performant than a recursive solution.

At this point I hope you know that I can't let some general rule dictate the truth. So, let's benchmark the two.

# Benchmark: Iteration Versus Recursion

|           | ns/op            | B/op    | allocs/op |
| --------- | ---------------- | ------- | --------- |
| Recursive | 163,777 ± 14,072 | 169,041 | 6,927     |
| Iterative | 196,417 ± 23,125 | 169,552 | 6,928     |
{ .styled-table }

To my surprise and horror, the recursive solution was faster. (Note, I simplified benchmarking to use just `n=8`.) You'll also note that the `B/op` was higher for iterative. So, something is up with the iterative solution that isn't satisfactory.

|                      | ns/op            | B/op    | allocs/op |
| -------------------- | ---------------- | ------- | --------- |
| Recursive (GOGC=off) | 126,823 ± 18,306 | 169,040 | 6,927     |
| Iterative (GOGC=off) | 127,085 ± 1,731  | 169,552 | 6,928     |
{ .styled-table }

I thought that the problem may be related to the garbage collector, so I turned it off. The speed improved for both — about 1.3x for recursive and 1.5x for iterative — and, more importantly, the iterative version caught up. Everything is okay again.

Well, kind of.

The standard deviation for the recursive code is gigantic. Part of this is likely that `testing.B` runs each benchmark in a goroutine, and Go goroutine stacks start small and grow by copying when deep recursion exceeds the current limit. Subsequent invocations reuse the already-grown stack, so the first call pays a cost the rest don't. CPU frequency scaling on the first few iterations probably contributes too. Either way, a warm-up call helps:

```go
func BenchmarkRecursiveWithWarmUp(b *testing.B) {
    sink = external(8)
    time.Sleep(500 * time.Millisecond)
    b.ResetTimer()
    for b.Loop() {
        sink = external(8)
    }
}
```

The first call pre-grows the goroutine stack and warms the CPU, then the `sleep` gives the CPU time to reach full boost frequency before `b.ResetTimer()` starts the clock.

|                              | ns/op            |
| ---------------------------- | ---------------- |
| Recursive (warmup)           | 162,214 ± 4,336  |
| Recursive (warmup, GOGC=off) | 120,773 ± 10,523 |
{ .styled-table }

The standard deviation dropped, but `10,523` is still too much. The fix would probably require either a longer `sleep` call or something more specific to the CPU I'm using. In either case, I've decided that this is going to be good enough.

What isn't good enough is the iterative version. Now that I've made the benchmark a more fair comparison, recursive is faster than iteration, again. The iterative version does behave differently from the recursive one when you consider memory. Each step can push two children onto the manual stack (one for `(`, one for `)`) before either is explored, so at its peak the stack holds a whole frontier of partial strings. The recursive version, by contrast, only keeps a single root-to-leaf path alive at once, since it explores one branch fully before backing up.

So, I figured that the next thing to do was test for a larger `n`. (I really wanted iteration to be faster.) I ran both at `n=15`. Each iteration takes several seconds, so I used `-benchtime=1x -count=4`.

|                            | ns/op                      |
| -------------------------- | -------------------------- |
| Recursive (n=15)           | 1,041,989,106 ± 40,932,000 |
| Iterative (n=15)           | 1,046,836,118 ± 14,673,000 |
| Recursive (n=15, GOGC=off) | 901,201,218 ± 41,777,000   |
| Iterative (n=15, GOGC=off) | 945,404,222 ± 6,485,000    |
{ .styled-table }

For this test case, the warmup + timeout still wasn't doing the job, so I ran with `-count=4` and threw out the first run. If I had more time, the better solution would be to run a hundred and throw out the first ten, or use some actual math to find the outliers, but let's not get too technical.

Looking at the results, we can see that the world is not sane. Recursion is faster than iteration. Will this always be the case? No. But it seems that this problem was tailor made for recursion, and the reason is the way recursion requires less partial memory.

# One Last Optimization

```go
func catalan(n int) int {
    c := 1
    for i := 0; i < n; i++ {
        c = c * 2 * (2*i + 1) / (i + 2)
    }
    return c
}

func backtrack(open, close, n int, buf *[]byte, result *[]string) {
    if len(*buf) == 2*n {
        *result = append(*result, string(*buf))
        return
    }
    if open < n {
        *buf = append(*buf, '(')
        backtrack(open+1, close, n, buf, result)
        *buf = (*buf)[:len(*buf)-1]
    }
    if close < open {
        *buf = append(*buf, ')')
        backtrack(open, close+1, n, buf, result)
        *buf = (*buf)[:len(*buf)-1]
    }
}

func generateParenthesis(n int) []string {
    result := make([]string, 0, catalan(n))
    buf := make([]byte, 0, 2*n)
    backtrack(0, 0, n, &buf, &result)
    return result
}
```

Two changes here:

1. Instead of building `current` by string concatenation at every recursive call, we pass a shared `[]byte` buffer and append/truncate in place. This avoids allocating a new string for every partial path. Only the final `string(buf)` at each leaf allocates. The next optimization would be to not use `string` at all, but that would be cheating since LeetCode uses it as the expected output type.
2. We pre-size the result slice to exactly `catalan(n)` so `append` never has to grow it. The Catalan number counts exactly how many valid parenthesis strings exist for n pairs.

The baseline column below is the previous string-based recursive (external) version. Because those numbers were gathered across the earlier experiments, treat the comparison as indicative rather than perfectly controlled — but the gap is large enough that the direction is not in doubt.

| n   | String-based (ns/op)       | Optimized (ns/op)        |
| --- | -------------------------- | ------------------------ |
| 1   | 38 ± 3                     | 34 ± 2                   |
| 5   | 4,467 ± 290                | 1,177 ± 123              |
| 8   | 172,973 ± 21,134           | 40,755 ± 2,159           |
| 10  | 2,694,138 ± 115,445        | 540,138 ± 55,797         |
| 15  | 1,050,607,230 ± 56,288,000 | 213,335,212 ± 12,107,000 |
{ .styled-table }

Even at `n=1` the optimized version edges ahead slightly, though the difference is within noise. From `n=5` onward the speed difference is undeniable: ~3.8x at `n=5`, ~4.2x at `n=8`, ~5x at `n=10`, and ~4.9x at `n=15`. The lesson for this is always the same: dynamic allocation is convenient, but it slows everything down.

# Conclusion

This one started out kind of boring, but quickly got interesting once I opened Godbolt. It never occurred to me that an inline function compiles to a more expensive call. Even though the difference was plain in assembly, its effect was negligible when benchmarking. So it isn't like the conclusion is to never inline your functions in Go. But, I'll probably never inline a function going forward.

I was also genuinely surprised that the iterative version was slower than the recursive one; this problem happens to fit recursion well because recursion keeps less partial state alive. I'll also have to do better benchmarking in the future to handle outliers, since I spent far more time than I expected tracking down what was going wrong. What didn't surprise me was that the biggest win came from killing the per-call allocations and pre-allocating the result.

Till next time.
