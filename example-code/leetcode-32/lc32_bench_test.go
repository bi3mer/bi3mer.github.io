package lc32bench

import (
	"errors"
	"fmt"
	"math/rand/v2"
	"testing"
)

// --- Stack ---

var ErrEmptyStack = errors.New("pop from empty stack")

type Stack[T any] struct {
	items []T
}

func (s *Stack[T]) Push(v T) {
	s.items = append(s.items, v)
}

func (s *Stack[T]) Pop() (T, error) {
	var zero T
	if len(s.items) == 0 {
		return zero, ErrEmptyStack
	}
	n := len(s.items) - 1
	v := s.items[n]
	s.items[n] = zero
	s.items = s.items[:n]
	return v, nil
}

func (s *Stack[T]) Peek() (T, error) {
	if len(s.items) == 0 {
		var zero T
		return zero, ErrEmptyStack
	}
	return s.items[len(s.items)-1], nil
}

func (s *Stack[T]) Len() int {
	return len(s.items)
}

// --- Solution 1: Stack ---

func longestValidParenthesesStack(s string) int {
	var st Stack[int]
	st.Push(-1)
	longest := 0

	for i := 0; i < len(s); i++ {
		if s[i] == '(' {
			st.Push(i)
		} else {
			st.Pop()
			if st.Len() == 0 {
				st.Push(i)
			} else {
				top, _ := st.Peek()
				longest = max(longest, i-top)
			}
		}
	}

	return longest
}

// --- Solution 2: Double Pass ---

func longestValidParenthesesDoublePass(s string) int {
	longest := 0
	n := len(s)

	open, closed := 0, 0
	for i := 0; i < n; i++ {
		if s[i] == '(' {
			open++
		} else {
			closed++
		}
		if open == closed {
			longest = max(longest, open*2)
		} else if closed > open {
			open, closed = 0, 0
		}
	}

	open, closed = 0, 0
	for i := n - 1; i >= 0; i-- {
		if s[i] == '(' {
			open++
		} else {
			closed++
		}
		if open == closed {
			longest = max(longest, open*2)
		} else if open > closed {
			open, closed = 0, 0
		}
	}

	return longest
}

// --- Helpers ---

func buildInput(n int) string {
	rng := rand.New(rand.NewPCG(42, uint64(n)))
	buf := make([]byte, n)
	for i := range buf {
		if rng.IntN(2) == 0 {
			buf[i] = '('
		} else {
			buf[i] = ')'
		}
	}
	return string(buf)
}

// --- Unit Tests ---

func TestSolutions(t *testing.T) {
	for n := 100; n <= 1000; n += 100 {
		s := buildInput(n)
		got1 := longestValidParenthesesStack(s)
		got2 := longestValidParenthesesDoublePass(s)
		if got1 != got2 {
			t.Errorf("n=%d: Stack=%d DoublePass=%d", n, got1, got2)
		}
	}
}

// --- Benchmarks ---

var sink int

func benchmarkSolution(b *testing.B, fn func(string) int) {
	for _, n := range []int{100, 200, 300, 400, 500, 600, 700, 800, 900, 1000} {
		s := buildInput(n)
		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			for b.Loop() {
				sink = fn(s)
			}
		})
	}
}

func BenchmarkStack(b *testing.B)      { benchmarkSolution(b, longestValidParenthesesStack) }
func BenchmarkDoublePass(b *testing.B) { benchmarkSolution(b, longestValidParenthesesDoublePass) }
