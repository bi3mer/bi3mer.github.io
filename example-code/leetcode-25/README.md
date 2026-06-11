# LeetCode 25 Benchmarks

Benchmark code for the [LeetCode 25 blog post](https://bi3mer.github.io/posts/leetcode-25/).

## Running

```
go test -bench=. -benchmem -count=10 | tee results.txt
benchstat results.txt
```
