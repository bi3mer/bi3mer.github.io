# LeetCode 28 Benchmarks

Benchmark code for the [LeetCode 28 blog post](https://bi3mer.github.io/posts/leetcode-28/).

## Running

```
go test -bench=. -benchmem -count=10 | tee results.txt
benchstat results.txt
```
