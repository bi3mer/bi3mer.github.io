+++
date = '2026-06-04T16:06:41-04:00'
draft = true
title = 'Leetcode 18'
+++

[LeetCode 18, _4Sum_](https://leetcode.com/problems/4sum/description/) asks for every _unique_ quadruplet `[a, b, c, d]` in an array `nums` that sums to a `target`. For example, given `nums = [1, 0, -1, 0, -2, 2]` and `target = 0`, the answer is `[[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]`. The word _unique_ is the whole game here. It is easy to find quadruplets that sum to the target; it is annoying to make sure you never report the same one twice.

This is a continuation of my [LeetCode 17 post](https://bi3mer.github.io/posts/leetcode-17/), where I'm using these problems as an excuse to learn Go. Same as before, this post is the journey with the wrong turns left in, because the wrong turns are where I actually learned something.

## Step 1: The Dumbest Thing That Could Work

The starting point is the dumbest correct approach: four nested loops that check every possible quadruplet. It has no redeeming performance qualities, but it is a useful blank canvas for seeing how Go handles sorting, slices, and the `slices` package before any of the interesting machinery shows up.

The trick that keeps the loops honest is the indexing: `i < j < k < l`. By forcing each loop to start one past the previous one, I never reuse an element and I never visit the same four positions in a different order. That alone removes a huge class of duplicates — the ones that come from _position_ rather than _value_.

```go
import "sort"

func fourSum(nums []int, target int) [][]int {
    var result [][]int
    sort.Ints(nums)

    // Find all possible combinations
    for i := 0; i < len(nums); i++ {
        for j := i + 1; j < len(nums); j++ {
            for k := j + 1; k < len(nums); k++ {
                for l := k + 1; l < len(nums); l++ {
                    sum := nums[i] + nums[j] + nums[k] + nums[l]

                    if sum == target {
                        result = append(result, []int{nums[i], nums[j], nums[k], nums[l]})
                    }
                }
            }
        }
    }

    // De-duplicate
    length := len(result)
    for i := 0; i < length; i++ {
        for j := i + 1; j < length; j++ {
            if slices.Equal(result[i], result[j]) {
                result = slices.Delete(result, j, j+1)
                j--
                length--
            }
        }
    }

    return result
}
```

A few Go things are worth pointing out here.

I sort `nums` up front with `sort.Ints`. This matters more than it looks. Because the loops pull elements in array order, sorting first means every quadruplet comes out in ascending order, _and_ two quadruplets with the same set of values come out byte-for-byte identical. Without the sort, `[2, 3, 4, 2]` and `[2, 2, 3, 4]` are the "same" answer but would not compare equal, so the dedup pass would miss them.

The dedup itself is a deliberately inefficient nested loop. Two Go behaviors are worth knowing here. First, `slices.Delete` returns the new slice rather than shrinking the old one in place, exactly like `append`, so you must reassign with `result = slices.Delete(...)`. Second, after deleting at index `j`, every element shifts left, so the thing that _was_ at `j+1` is now at `j`. If I let the loop do its normal `j++`, I would skip right over it. The fix is `j--` after a delete so the loop re-examines the new occupant of that slot.

|                      | ns/op       | B/op    | allocs/op |
| -------------------- | ----------- | ------- | --------- |
| Brute force (Step 1) | 1,822,444.6 | 216,701 | 1815      |

This is correct. It is also catastrophically slow. LeetCode's adversarial input is an array of nothing but `2`s:

```
[2,2,2,2,2,2, ... ,2]   // 200 of them
```

With this input the four nested loops produce on the order of C(200, 4) ≈ 65 million matching quadruplets, all funneled into `result` before the dedup pass ever runs. The result is **Time Limit Exceeded**, and on a bad day, an out-of-memory crash before the timer even fires.

## Step 2: Using a Map

The dedup pass above is `O(m²)` in the number of matches, and slice deletion shifts elements every time, which makes it worse. Before fixing the generation cost, it is worth seeing how Go handles dedup — Go has no built-in set type, so the idiomatic move is a `map` used as a set.

The wrinkle is that a `[]int` cannot be a map key — slices are not comparable in Go. The standard workaround is to turn each quadruplet into a `string`, which _is_ comparable. I reached for `fmt.Sprintf` to build the key:

```go
import "sort"
import "fmt"

func fourSum(nums []int, target int) [][]int {
    sort.Ints(nums)

    seen := make(map[string][]int)

    // Find all possible combinations
    for i := 0; i < len(nums); i++ {
        for j := i + 1; j < len(nums); j++ {
            for k := j + 1; k < len(nums); k++ {
                for l := k + 1; l < len(nums); l++ {
                    sum := nums[i] + nums[j] + nums[k] + nums[l]

                    if sum == target {
                        key := fmt.Sprintf("%d,%d,%d,%d", nums[i], nums[j], nums[k], nums[l])
                        seen[key] = []int{nums[i], nums[j], nums[k], nums[l]}
                    }
                }
            }
        }
    }

    // Change map into desired output format
    var result [][]int
    for _, quad := range seen {
        result = append(result, quad)
    }

    return result
}
```

I made the map value the quadruplet itself (`map[string][]int`) rather than a `bool`, so the final step just ranges over the map's values and appends each one. One thing to know: Go randomizes map iteration order on purpose, so `result` comes out in arbitrary order. 4Sum's judge compares answers as a set, so this is fine here, but it would bite on a problem that cared about order.

|                      | ns/op       | B/op    | allocs/op |
| -------------------- | ----------- | ------- | --------- |
| Brute force (Step 1) | 1,822,444.6 | 216,701 | 1815      |
| Map dedup (Step 2)   | 281,144.8   | 125,848 | 6928      |

This compiles, runs, and is correct. It is also **still Time Limit Exceeded** on the all-`2`s input. The map fixes the _symptom_ (duplicate storage) but not the _disease_ (generating 65 million quadruplets in the first place). When the iteration count itself is the bottleneck, no amount of dedup cleverness helps. The generation has to change.

## Step 3: Two Pointers

The fix is to drop from `O(n⁴)` to `O(n³)`. Keep two outer loops to fix the first two numbers, but replace the inner two loops with a single two-pointer scan over the rest of the (sorted) array.

The idea behind the scan: for a fixed `i` and `j`, I want two more numbers that sum to `target - nums[i] - nums[j]`. Because the array is sorted, I can put one pointer at `left` (just past `j`) and one at `right` (the end), and walk them toward each other. If the current sum is too big, the only way to shrink it is to move `right` left. If it is too small, move `left` right. If it matches, record it and move both inward. Each pointer sweeps the region once, so the inner search is linear instead of quadratic.

```go
import "sort"
import "fmt"

func fourSum(nums []int, target int) [][]int {
    sort.Ints(nums)

    seen := make(map[string][]int)

    for i := 0; i < len(nums); i++ {
        for j := i + 1; j < len(nums); j++ {
            sum := nums[i] + nums[j]

            left := j + 1
            right := len(nums) - 1

            for left < right {
                currentSum := sum + nums[left] + nums[right]

                if currentSum > target {
                    right--
                } else if currentSum < target {
                    left++
                } else {
                    key := fmt.Sprintf("%d,%d,%d,%d", nums[i], nums[j], nums[left], nums[right])
                    seen[key] = []int{nums[i], nums[j], nums[left], nums[right]}
                    left++
                    right--
                }
            }
        }
    }

    // Change map into desired output format
    var result [][]int
    for _, quad := range seen {
        result = append(result, quad)
    }

    return result
}
```

One thing to get right: on a match, both pointers move (`left++` and `right--`), not just one. Moving only one would, on a sorted array, immediately overshoot or undershoot the target, but more importantly there may be additional matching pairs further inward, so the scan has to keep going.

|                             | ns/op       | B/op    | allocs/op |
| --------------------------- | ----------- | ------- | --------- |
| Brute force (Step 1)        | 1,822,444.6 | 216,701 | 1815      |
| Map dedup (Step 2)          | 281,144.8   | 125,848 | 6928      |
| Two pointers + map (Step 3) | 101,004.6   | 52,509  | 2287      |

This finally passes, but the LeetCode performance was embarrassing: **176 ms, beats 7.84%**. The algorithm is now the right complexity, so something else is eating the time. That something is `fmt.Sprintf`.

## Step 4: Dropping `fmt.Sprintf`

`fmt.Sprintf` is convenient, but it works through reflection — it inspects the type of each argument at runtime to decide how to format it. On a hot path that runs on every single match, that overhead dominates. The fix is to build the key by hand with `strconv.Itoa`, which converts an int to a string directly with no reflection:

```go
import "sort"
import "strconv"

func fourSum(nums []int, target int) [][]int {
    sort.Ints(nums)

    seen := make(map[string][]int)

    for i := 0; i < len(nums); i++ {
        for j := i + 1; j < len(nums); j++ {
            sum := nums[i] + nums[j]

            left := j + 1
            right := len(nums) - 1

            for left < right {
                currentSum := sum + nums[left] + nums[right]

                if currentSum > target {
                    right--
                } else if currentSum < target {
                    left++
                } else {
                    key := strconv.Itoa(nums[i]) + "," + strconv.Itoa(nums[j]) + "," +
                        strconv.Itoa(nums[left]) + "," + strconv.Itoa(nums[right])
                    seen[key] = []int{nums[i], nums[j], nums[left], nums[right]}
                    left++
                    right--
                }
            }
        }
    }

    // Change map into desired output format
    var result [][]int
    for _, quad := range seen {
        result = append(result, quad)
    }

    return result
}
```

|                             | ns/op       | B/op    | allocs/op |
| --------------------------- | ----------- | ------- | --------- |
| Brute force (Step 1)        | 1,822,444.6 | 216,701 | 1815      |
| Map dedup (Step 2)          | 281,144.8   | 125,848 | 6928      |
| Two pointers + map (Step 3) | 101,004.6   | 52,509  | 2287      |
| `strconv` key (Step 4)      | 70,881.8    | 44,599  | 2287      |

This dropped the runtime to **86 ms, beats 9.98%**. Roughly twice as fast, which confirms `fmt.Sprintf` was the culprit. But beating 10% of submissions is still bad, and the reason is structural: even the fastest key is still a string allocation plus a hash plus a map insert on every match. The map itself is the ceiling.

## Step 5: Dropping the Map

The real fix is to never build a duplicate in the first place, which makes the map unnecessary. Because the array is sorted, equal values sit next to each other, so I can dedup by skipping over neighbors that share a value.

There are four places duplicates can sneak in — the two outer values and the two pointer values — and the cure is the same idea everywhere: only ever _start_ a combination from the first occurrence of a given value, and skip any repeats.

For the `i` loop, the logic is "if this value equals the one I just processed, skip it." The previous value is `nums[i-1]`, with an `i > 0` guard so I don't index `nums[-1]`:

```go
if i > 0 && nums[i] == nums[i-1] {
    continue
}
```

The `j` loop is the same idea with one wrinkle. The guard is `j > i+1`, not `j > 0`. The reason is that `i` and `j` are _allowed_ to hold the same value — a valid quadruplet like `[2, 2, 3, 4]` uses two 2s. If I used `j > 0`, the very first `j` of a round would compare against `nums[i]` and wrongly skip a legitimate pairing. The guard `j > i+1` means "only skip once `j` has moved past its own starting position."

After a match, I walk each pointer past its duplicate neighbors before the normal `left++; right--`:

```go
for left < right && nums[left] == nums[left+1] {
    left++
}
for left < right && nums[right] == nums[right-1] {
    right--
}
```

Put together:

```go
import "sort"

func fourSum(nums []int, target int) [][]int {
    sort.Ints(nums)

    var result [][]int

    for i := 0; i < len(nums); i++ {
        if i > 0 && nums[i] == nums[i-1] {
            continue // same value as last i — skip, already did it
        }

        for j := i + 1; j < len(nums); j++ {
            if j > i+1 && nums[j] == nums[j-1] {
                continue // same value as last j — skip, already did it
            }

            sum := nums[i] + nums[j]

            left := j + 1
            right := len(nums) - 1

            for left < right {
                currentSum := sum + nums[left] + nums[right]

                if currentSum > target {
                    right--
                } else if currentSum < target {
                    left++
                } else {
                    result = append(result, []int{nums[i], nums[j], nums[left], nums[right]})

                    // skip duplicate values at left
                    for left < right && nums[left] == nums[left+1] {
                        left++
                    }

                    // skip duplicate values at right
                    for left < right && nums[right] == nums[right-1] {
                        right--
                    }

                    left++
                    right--
                }
            }
        }
    }

    return result
}
```

The hot path is now nothing but integer comparisons. No key string, no hash, no map allocation. This is the version that actually places well, because the dedup is folded into the scan rather than bolted on afterward.

|                             | ns/op       | B/op    | allocs/op |
| --------------------------- | ----------- | ------- | --------- |
| Brute force (Step 1)        | 1,822,444.6 | 216,701 | 1815      |
| Map dedup (Step 2)          | 281,144.8   | 125,848 | 6928      |
| Two pointers + map (Step 3) | 101,004.6   | 52,509  | 2287      |
| `strconv` key (Step 4)      | 70,881.8    | 44,599  | 2287      |
| Inline skip (Step 5)        | 6,122.8     | 8,250   | 88        |

## A Note on Measuring Performance

LeetCode's millisecond timings are noisy — they bounce around between submissions and only let you compare against a percentile that shifts over time. To actually measure the difference between these versions, the right tool is `testing.B` with `-benchmem`, which reports `ns/op`, `B/op`, and `allocs/op` deterministically.

To benchmark fairly across versions, I generate a batch of random inputs once with a fixed seed and cycle through them, so every benchmark sees the same data. 4Sum is sensitive to input shape — arrays with many duplicates exercise the skip logic, arrays with few exercise the scan — so a single hardcoded input would not be representative:

```go
var sink [][]int

func randomInput(rng *rand.Rand) ([]int, int) {
    n := rng.IntN(50) + 4 // 4..53 elements
    nums := make([]int, n)
    for i := range nums {
        nums[i] = rng.IntN(21) - 10 // values in [-10, 10] to force duplicates
    }
    target := rng.IntN(21) - 10
    return nums, target
}

func randomInputs(count int) ([][]int, []int) {
    rng := rand.New(rand.NewPCG(42, 0))
    numsList := make([][]int, count)
    targets := make([]int, count)
    for i := range numsList {
        numsList[i], targets[i] = randomInput(rng)
    }
    return numsList, targets
}

func BenchmarkBruteForce(b *testing.B) {
    numsList, targets := randomInputs(1000)
    idx := 0
    b.ResetTimer()
    for b.Loop() {
        sink = fourSumBruteForce(numsList[idx], targets[idx])
        idx = (idx + 1) % 1000
    }
}

func BenchmarkMapDedup(b *testing.B) { /* same pattern, calls fourSumMapDedup */ }
func BenchmarkTwoPointersFmt(b *testing.B) { /* calls fourSumTwoPointersFmt */ }
func BenchmarkTwoPointersStrconv(b *testing.B) { /* calls fourSumTwoPointersStrconv */ }
func BenchmarkInlineSkip(b *testing.B) { /* calls fourSumInlineSkip */ }
```

The catch is that Go does not allow two top-level functions with the same name in the same package. Each step's `fourSum` has to be renamed — `fourSumBruteForce`, `fourSumMapDedup`, and so on — before they can coexist in one `_test.go` file. For the numbers in this post, all five versions lived in a single `package foursum` with a shared `foursum_test.go` containing the harness above and one `Benchmark*` function per renamed variant.

A few notes on why the harness looks like this. The `sink` package variable receives the result so the compiler can't decide the call is dead code and optimize it away. The fixed seed `rand.NewPCG(42, 0)` makes the random inputs identical across runs, so the comparison is apples to apples. Narrowing values to `[-10, 10]` deliberately manufactures duplicates, which is exactly the case the dedup logic exists to handle. Run with:

```
go test -bench=. -benchmem -count=5
```

`-benchmem` adds the `B/op` and `allocs/op` columns, and `-count=5` runs each benchmark five times so you can eyeball stability.

The three columns mean: **ns/op** is nanoseconds per call, **B/op** is heap bytes allocated per call, and **allocs/op** is the number of distinct heap allocations per call.

Results on an AMD Ryzen AI 9 HX 370 (averages over 5 runs, 1000 random inputs cycled per benchmark):

Step 5 is roughly 298× faster than Step 1, uses 96% less heap memory, and makes 95% fewer allocations. The jump from Step 4 to Step 5 — eliminating the map entirely — accounts for almost all of that gain.

## Conclusion

We got a pretty good solution. Trying to make the non-two pointer solution work quickly enough to passs was frankly more interesting than the two pointer solution, but it couldn't be avoided. This, for me, goes under a category of prorgramming that I've never used in the real world, so it is why I quesiton the point of practicing it for interviews, but oh well. Regardless, I hope that someone finds this post useful. Till next time.
