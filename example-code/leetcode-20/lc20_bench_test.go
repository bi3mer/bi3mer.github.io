package lc20bench

import (
	"math/rand/v2"
	"strings"
	"testing"
)

func isValidDumb(s string) bool {
	for {
		before := s
		s = strings.ReplaceAll(s, "()", "")
		s = strings.ReplaceAll(s, "[]", "")
		s = strings.ReplaceAll(s, "{}", "")
		if s == before {
			break
		}
	}
	return len(s) == 0
}

func isValidRunes(s string) bool {
	var stack []rune
	for _, c := range s {
		switch c {
		case '(', '{', '[':
			stack = append(stack, c)
		case ')':
			if len(stack) == 0 {
				return false
			}
			if stack[len(stack)-1] == '(' {
				stack = stack[:len(stack)-1]
			} else {
				return false
			}
		case '}':
			if len(stack) == 0 {
				return false
			}
			if stack[len(stack)-1] == '{' {
				stack = stack[:len(stack)-1]
			} else {
				return false
			}
		case ']':
			if len(stack) == 0 {
				return false
			}
			if stack[len(stack)-1] == '[' {
				stack = stack[:len(stack)-1]
			} else {
				return false
			}
		}
	}
	return len(stack) == 0
}

func isValidBytes(s string) bool {
	var stack []byte
	for i := 0; i < len(s); i++ {
		c := s[i]
		switch c {
		case '(', '{', '[':
			stack = append(stack, c)
		case ')':
			if len(stack) == 0 {
				return false
			}
			if stack[len(stack)-1] == '(' {
				stack = stack[:len(stack)-1]
			} else {
				return false
			}
		case '}':
			if len(stack) == 0 {
				return false
			}
			if stack[len(stack)-1] == '{' {
				stack = stack[:len(stack)-1]
			} else {
				return false
			}
		case ']':
			if len(stack) == 0 {
				return false
			}
			if stack[len(stack)-1] == '[' {
				stack = stack[:len(stack)-1]
			} else {
				return false
			}
		}
	}
	return len(stack) == 0
}

func randomInputs(count int) []string {
	openers := []byte{'(', '[', '{'}
	matching := map[byte]byte{'(': ')', '[': ']', '{': '}'}
	chars := []byte("()[]{}")
	rng := rand.New(rand.NewPCG(42, 0))
	inputs := make([]string, count)
	for i := range inputs {
		if rng.IntN(10) == 0 {
			length := rng.IntN(99) + 2
			buf := make([]byte, length)
			for j := range buf {
				buf[j] = chars[rng.IntN(6)]
			}
			inputs[i] = string(buf)
			continue
		}
		length := (rng.IntN(50) + 1) * 2 // 2..100, even
		var stack []byte
		result := make([]byte, 0, length)
		for len(result) < length {
			remaining := length - len(result)
			canOpen := remaining > len(stack)
			canClose := len(stack) > 0
			if canOpen && (!canClose || rng.IntN(2) == 0) {
				opener := openers[rng.IntN(3)]
				stack = append(stack, opener)
				result = append(result, opener)
			} else {
				top := stack[len(stack)-1]
				stack = stack[:len(stack)-1]
				result = append(result, matching[top])
			}
		}
		inputs[i] = string(result)
	}
	return inputs
}

var sink bool

func BenchmarkDumb(b *testing.B) {
	inputs := randomInputs(1000)
	idx := 0
	b.ResetTimer()
	for b.Loop() {
		sink = isValidDumb(inputs[idx])
		idx = (idx + 1) % 1000
	}
}

func BenchmarkStackRunes(b *testing.B) {
	inputs := randomInputs(1000)
	idx := 0
	b.ResetTimer()
	for b.Loop() {
		sink = isValidRunes(inputs[idx])
		idx = (idx + 1) % 1000
	}
}

func BenchmarkStackBytes(b *testing.B) {
	inputs := randomInputs(1000)
	idx := 0
	b.ResetTimer()
	for b.Loop() {
		sink = isValidBytes(inputs[idx])
		idx = (idx + 1) % 1000
	}
}
