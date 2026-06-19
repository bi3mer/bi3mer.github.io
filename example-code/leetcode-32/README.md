# LeetCode 32 Benchmarks

Benchmark code for the [LeetCode 32 blog post](https://bi3mer.github.io/posts/leetcode-32/).

## Running

```
go test -bench=. -benchmem -count=10 | tee results.txt
benchstat results.txt
```
