---
date: "2024-11-22T09:34:57-05:00"
draft: false
title: "Go Code"
showtoc: false
hideMeta: true
showTitle: false
showReadingTime: false
disableShare: true
---

# Go Code

## Stack

```go
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
	s.items[n] = zero // remove previous val for GC
	s.items = s.items[:n]

	return v, nil
}

func (s *Stack[T]) Peek() (T, error) {
	if len(s.items) == 0 {
		var zero T
		return zero, ErrEmptyStack
	}

	return s.items[len(s.items) - 1], nil
}

func (s *Stack[T]) Len() int {
	return len(s.items)
}
```
