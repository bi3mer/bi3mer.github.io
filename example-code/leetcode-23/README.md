# LeetCode 23 Benchmarks

Benchmark code for the solutions discussed in the [LeetCode 23 blog post](https://bi3mer.github.io/posts/leetcode-23/).

## Solutions

Five approaches are benchmarked:

1. **Flatten + Sort** — collect all node values into a slice, sort it, rebuild a new linked list. O(N log N) time, O(N) space.
2. **Sequential** — merge lists one at a time left to right. O(NK) time, O(1) extra space.
3. **Divide and Conquer (iterative)** — repeatedly merge pairs of lists in-place until one remains. O(N log K) time, O(1) extra space.
4. **Divide and Conquer (recursive)** — same approach via recursion. O(N log K) time, O(log K) stack space.
5. **Heap** — use `container/heap` to always pop the smallest head across all K lists. O(N log K) time, O(K) space.

## Running

`testing.B` gives raw numbers but does no statistical analysis. The standard analysis tool is [`benchstat`](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat) from the Go team. Install it once:

```
go install golang.org/x/perf/cmd/benchstat@latest
```

Then collect and analyze:

```
go test -bench=. -benchmem -count=10 | tee results.txt
benchstat results.txt
```

Use `-count=10` or higher.
