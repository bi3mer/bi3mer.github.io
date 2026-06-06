+++
date = '2026-06-06T12:00:54-05:00'
draft = false
title = 'Leetcode 20'
+++

[LeetCode 20](https://leetcode.com/problems/valid-parentheses/) gives you a string made up of the six bracket characters `()[]{}` and asks whether they are properly matched and nested. "Properly" means every opener has a corresponding closer of the same type, and they close in the right order. So `()[]{}` is valid, `([])` is valid, but `([)]` is not.

Anywho, I'll start with a dumb implementation for fun and then move on to the better but less exciting version.

# Solution 1: The Dumb Version

The laziest correct approach: repeatedly delete every adjacent matched pair until the string stops changing. A valid string collapses to nothing; an invalid one gets stuck with leftover brackets.

The only trick here is to recognize that strings like `([)]` are not valid, which means you will always have one instance of `[]`, `()`, or `{}` somewhere in the string, unless the string is empty. From there, the solution is pretty clear: remove instances of those three until the string is empty or they can't be removed any longer.

```go
import "strings"

func isValid(s string) bool {
    for {
        before := s
        s = strings.ReplaceAll(s, "()", "")
        s = strings.ReplaceAll(s, "[]", "")
        s = strings.ReplaceAll(s, "{}", "")
        if s == before {
            break
        }
    }
    return len(s) == 0
}
```

`strings.ReplaceAll(s, "()", "")` returns a copy of `s` with every `()` removed. Strings in Go are immutable, so this hands back a new string rather than editing in place, which is why each line reassigns `s`.

# Solution 2: Stack

The real solution is to use stack, and push opening character (`(`, `{`, and `[`) onto it. When you hit a closing bracket, the top of the stack must be the matching opener, or the string is invalid.

```go
func isValid(s string) bool {
    var stack []rune
    for _, c := range s {
       switch c {
        case '(', '{', '[':
            stack = append(stack, c)
        case ')':
            if len(stack) == 0 {
                return false
            }

            if stack[len(stack) - 1] == '(' {
                stack = stack[:len(stack) - 1]
            } else {
                return false
            }

        case '}':
            if len(stack) == 0 {
                return false
            }

            if stack[len(stack) - 1] == '{' {
                stack = stack[:len(stack) - 1]
            } else {
                return false
            }
        case ']':
            if len(stack) == 0 {
                return false
            }

            if stack[len(stack) - 1] == '[' {
                stack = stack[:len(stack) - 1]
            } else {
                return false
            }
        }
    }
    return len(stack) == 0
}
```

Go has no stack type, but a slice does the job. Pushing is `append(stack, c)`. Peeking the top is `stack[len(stack)-1]`. Popping is `stack = stack[:len(stack)-1]`, which reslices to drop the last element. The one trap is popping an empty stack: `stack[len(stack)-1]` on a zero-length slice indexes `[-1]` and panics. That is why every closing-bracket case checks `len(stack) == 0` first. A closer with nothing on the stack is exactly the invalid case where a bracket closes something that was never opened.

# Solution 3: Bytes Instead

Ranging over a string yields runes, which means Go decodes UTF-8 on every character. The input here is guaranteed to be only the six ASCII bracket characters, so that decoding is wasted work. Indexing the string by byte skips it. The structure is identical to Solution 2, only the iteration and the stack element type change.

```go
func isValid(s string) bool {
    var stack []byte
    for i := 0; i < len(s); i++ {
        c := s[i]
        // ... no code changed from solution 2 otherwise
    }

    return len(stack) == 0
}
```

# Benchmark

I benchmarked all three with `testing.B` and `-benchmem`. The full benchmark code is [on GitHub](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-20). If you want to see how the harness is set up — random inputs with a fixed seed, the `sink` variable, and what the columns mean — I covered that in my [LeetCode 17](https://bi3mer.github.io/posts/leetcode-17/) and [LeetCode 18](https://bi3mer.github.io/posts/leetcode-18/) posts.

Generating inputs for this problem requires more care than prior problems. Purely random strings — picking from `()[]{}` uniformly — are almost never valid. The stack solutions detect invalid inputs on the first or second character and return false immediately, before the stack ever grows. That makes them look cost-free; they aren't. To get a fair comparison I wrote a generator that produces 90% valid strings and 10% random (likely invalid) strings.

```go
func randomInputs(count int) []string {
    openers := []byte{'(', '[', '{'}
    matching := map[byte]byte{'(': ')', '[': ']', '{': '}'}
    chars := []byte("()[]{}")
    rng := rand.New(rand.NewPCG(42, 0))
    inputs := make([]string, count)
    for i := range inputs {
        if rng.IntN(10) == 0 {
            length := rng.IntN(99) + 2
            buf := make([]byte, length)
            for j := range buf {
                buf[j] = chars[rng.IntN(6)]
            }
            inputs[i] = string(buf)
            continue
        }

        length := (rng.IntN(50) + 1) * 2 // 2..100, even
        var stack []byte
        result := make([]byte, 0, length)

        for len(result) < length {
            remaining := length - len(result)
            canOpen := remaining > len(stack)
            canClose := len(stack) > 0

            if canOpen && (!canClose || rng.IntN(2) == 0) {
                opener := openers[rng.IntN(3)]
                stack = append(stack, opener)
                result = append(result, opener)
            } else {
                top := stack[len(stack)-1]
                stack = stack[:len(stack)-1]
                result = append(result, matching[top])
            }
        }

        inputs[i] = string(result)
    }
    return inputs
}
```

The valid-string generator uses a stack. At each step, if there is still room to close everything that is open, it randomly opens a new bracket or closes the top one. The `remaining > len(stack)` guard ensures there are always enough positions left to close whatever is open, so the string is always complete and validht .

|                           | ns/op | B/op | allocs/op |
| :------------------------ | ----: | ---: | --------: |
| Solution 1: Dumb version  | 920.6 |  201 |         8 |
| Solution 2: Stack (runes) | 203.9 |   19 |         0 |
| Solution 3: Stack (bytes) | 193.5 |    0 |         0 |

{.styled-table}

Results on an AMD Ryzen AI 9 HX 370 (averages over 10 runs, 1000 random inputs cycled per benchmark). The three columns mean: **ns/op** is nanoseconds per call, **B/op** is heap bytes allocated per call, and **allocs/op** is the number of distinct heap allocations per call.

The dumb version is about 4.5× slower than either stack solution with realistic inputs: it allocates a new string copy on every `ReplaceAll` pass, and a deeply nested valid string needs many passes. The two stack solutions stay close; bytes edge out runes by roughly 5%. The `rune` stack shows 19 B/op but 0 allocs/op, which looks contradictory. It isn't: allocs/op is total allocations divided by iterations and then truncated, so 0 means fewer than one per call on average, not none. The asymmetry between `rune` and `byte` traces back to element size. A rune is 4 bytes, so the rune backing array reaches larger size classes sooner than the byte array; only a fraction of inputs push the rune stack deep enough to trigger a counted allocation, which is enough to register as bytes but truncates to zero allocations. The byte stack stays small enough to avoid counted allocations across nearly all inputs. Pinning down the exact allocator behavior would need profiling, but the direction follows from runes being four times larger per element.

# Conclusion

LeetCode listed this problem as "easy," and I agree. Still, hopefully, the dumb version was interesting to look at. And, more importantly, I learned that the `rune` type is convenient, but does extra work that, if not necessary, can and should be avoided. The benchmarks also had a non-obvious wrinkle: purely random bracket strings are almost never valid, so the stack solutions exited on the first or second character and appeared to allocate nothing. Switching to 90% valid inputs revealed the real picture — a 4.5× gap between the dumb version and the stack, a ~5% speed edge for bytes over runes, and an allocation asymmetry — 19 B/op for runes versus 0 for bytes — that traces back to runes being 4× larger per element, pushing the backing array into larger size classes sooner.

I think it goes to this general idea in software: "if performance doesn't matter, don't seek it." Another version of the idea is "premature optimization is bad." And I agree with it in theory, but the misapplication of it is, in part, why I think software can be so slow these days. The byte version is not a premature optimization. It is a conscious choice to not do unnecessary work, and it cost one extra line to write.
