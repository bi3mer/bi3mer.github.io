# LeetCode 20 Benchmarks

Benchmark code for the three solutions discussed in the [LeetCode 20 blog post](https://bi3mer.github.io/posts/leetcode-20/).

## Run

```
go test -bench=. -benchmem -count=10
```

`-benchmem` adds `B/op` and `allocs/op` columns. `-count=10` runs each benchmark ten times for stability.
