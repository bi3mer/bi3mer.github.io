# LeetCode 33 Benchmarks

Benchmark code for the [LeetCode 33 blog post](https://bi3mer.github.io/posts/leetcode-33/).

## Running

```
go test -bench=. -benchmem -count=10 | tee results.txt
benchstat results.txt
```
