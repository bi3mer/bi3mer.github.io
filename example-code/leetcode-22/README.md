# LeetCode 22 Benchmarks

Benchmark code for the solutions discussed in the [LeetCode 22 blog post](https://bi3mer.github.io/posts/leetcode-22/).

## Benchmark 1: Inline Closure vs External Function

Compares recursive backtracking with the helper declared as an inline closure (capturing `n` and `result`) against the same logic as a top-level function (taking `n` and `result` as parameters). Runs n ∈ {1, 5, 8, 10}.

```
go test -bench="Inline|External" -benchmem -count=5
```

## Benchmark 2: Recursive vs Iterative

Compares recursive backtracking against iterative backtracking with an explicit stack. Runs n=8 and n=15.

```
go test -bench="Recursive|Iterative" -benchmem -count=5
```

For n=15 (each iteration takes several seconds, use `-benchtime=1x`):

```
go test -bench="Recursive15|Iterative15" -benchmem -benchtime=1x -count=3
```

## All Benchmarks

```
go test -bench=. -benchmem -count=5
```

`-benchmem` adds `B/op` and `allocs/op` columns. `-count=5` runs each benchmark five times for stability.
