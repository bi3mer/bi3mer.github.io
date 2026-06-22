# LeetCode 3 Benchmarks

Benchmark code for the [LeetCode 3 blog post](https://bi3mer.github.io/posts/leetcode-3/).

## Running

```
go test -bench=. -benchmem -count=10 | tee results.txt
benchstat results.txt
```
