# LeetCode 21 Benchmarks

Benchmark code for the two solutions discussed in the [LeetCode 21 blog post](https://bi3mer.github.io/posts/leetcode-21/).

## Run

```
go test -bench=. -benchmem -count=5
```

`-benchmem` adds `B/op` and `allocs/op` columns. `-count=5` runs each benchmark ten times for stability.
