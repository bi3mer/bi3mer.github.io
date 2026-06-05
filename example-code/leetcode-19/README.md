# LeetCode 19 Benchmarks

Benchmark code for the three solutions discussed in the [LeetCode 19 blog post](https://bi3mer.github.io/posts/leetcode-19/).

## Run

```
go test -bench=. -benchmem -count=5
```

`-benchmem` adds `B/op` and `allocs/op` columns. `-count=5` runs each benchmark five times for stability.
