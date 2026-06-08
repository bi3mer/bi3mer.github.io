package lc22bench

import (
	"fmt"
	"testing"
	"time"
)

func recursive(n int) []string {
	var result []string

	var backtrack func(current string, open, close int)
	backtrack = func(current string, open, close int) {
		if open == n && close == n {
			result = append(result, current)
			return
		}
		if open < n {
			backtrack(current+"(", open+1, close)
		}
		if close < open {
			backtrack(current+")", open, close+1)
		}
	}

	backtrack("", 0, 0)
	return result
}

func bt(current string, open, close, n int, result *[]string) {
	if open == n && close == n {
		*result = append(*result, current)
		return
	}
	if open < n {
		bt(current+"(", open+1, close, n, result)
	}
	if close < open {
		bt(current+")", open, close+1, n, result)
	}
}

func external(n int) []string {
	var result []string
	bt("", 0, 0, n, &result)
	return result
}

type state struct {
	current     string
	open, close int
}

func iterative(n int) []string {
	var result []string
	stack := []state{{"", 0, 0}}

	for len(stack) > 0 {
		s := stack[len(stack)-1]
		stack = stack[:len(stack)-1]

		if s.open == n && s.close == n {
			result = append(result, s.current)
			continue
		}

		if s.open < n {
			stack = append(stack, state{s.current + "(", s.open + 1, s.close})
		}

		if s.close < s.open {
			stack = append(stack, state{s.current + ")", s.open, s.close + 1})
		}
	}

	return result
}

func catalan(n int) int {
	c := 1
	for i := 0; i < n; i++ {
		c = c * 2 * (2*i + 1) / (i + 2)
	}
	return c
}

func btOpt(open, close, n int, buf *[]byte, result *[]string) {
	if len(*buf) == 2*n {
		*result = append(*result, string(*buf))
		return
	}
	if open < n {
		*buf = append(*buf, '(')
		btOpt(open+1, close, n, buf, result)
		*buf = (*buf)[:len(*buf)-1]
	}
	if close < open {
		*buf = append(*buf, ')')
		btOpt(open, close+1, n, buf, result)
		*buf = (*buf)[:len(*buf)-1]
	}
}

func optimized(n int) []string {
	result := make([]string, 0, catalan(n))
	buf := make([]byte, 0, 2*n)
	btOpt(0, 0, n, &buf, &result)
	return result
}

var sink []string

func benchmarkGenerate(b *testing.B, fn func(int) []string) {
	for _, n := range []int{1, 5, 8, 10} {
		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			for b.Loop() {
				sink = fn(n)
			}
		})
	}
}

func BenchmarkInline(b *testing.B) {
	benchmarkGenerate(b, recursive)
}

func BenchmarkExternal(b *testing.B) {
	for _, n := range []int{1, 5, 8, 10, 15} {
		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			for b.Loop() {
				sink = external(n)
			}
		})
	}
}

func BenchmarkOptimized(b *testing.B) {
	for _, n := range []int{1, 5, 8, 10, 15} {
		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			for b.Loop() {
				sink = optimized(n)
			}
		})
	}
}

func BenchmarkRecursive(b *testing.B) {
	for b.Loop() {
		sink = external(8)
	}
}

func BenchmarkRecursiveWithWarmup(b *testing.B) {
	sink = external(8)
	time.Sleep(500 * time.Millisecond)
	b.ResetTimer()

	for b.Loop() {
		sink = external(8)
	}
}

func BenchmarkIterative(b *testing.B) {
	for b.Loop() {
		sink = iterative(8)
	}
}

func BenchmarkRecursive15(b *testing.B) {
	sink = external(15)
	time.Sleep(500 * time.Millisecond)
	b.ResetTimer()
	for b.Loop() {
		sink = external(15)
	}
}

func BenchmarkIterative15(b *testing.B) {
	sink = iterative(15)
	time.Sleep(500 * time.Millisecond)
	b.ResetTimer()
	for b.Loop() {
		sink = iterative(15)
	}
}

