package lc25bench

import (
	"fmt"
	"math/rand/v2"
	"testing"
)

type ListNode struct {
	Val  int
	Next *ListNode
}

// wireList wires pool into a linked list in-place with random values.
// Fully resets every node so the pool can be reused across benchmark iterations.
func wireList(pool []ListNode, rng *rand.Rand) *ListNode {
	for i := range pool {
		pool[i].Val = rng.IntN(100) + 1
		if i < len(pool)-1 {
			pool[i].Next = &pool[i+1]
		} else {
			pool[i].Next = nil
		}
	}
	return &pool[0]
}

// --- Solution 1: Array ---

func swapNodes(prevA *ListNode, a *ListNode, prevB *ListNode, b *ListNode) {
	prevA.Next = b
	prevB.Next = a
	a.Next, b.Next = b.Next, a.Next
}

func array(head *ListNode, k int) *ListNode {
	k++
	prev := make([]*ListNode, k)
	dummy := &ListNode{Next: head}
	cur := dummy
	i := 0

	for cur != nil {
		if i == k {
			left := 1
			right := k - 1
			for left < right {
				swapNodes(prev[left-1], prev[left], prev[right-1], prev[right])
				prev[left], prev[right] = prev[right], prev[left]
				left++
				right--
			}
			prev[0] = prev[1]
			i = 1
		} else {
			prev[i] = cur
			cur = cur.Next
			i++
		}
	}

	if i == k {
		left := 1
		right := k - 1
		for left < right {
			swapNodes(prev[left-1], prev[left], prev[right-1], prev[right])
			prev[left], prev[right] = prev[right], prev[left]
			left++
			right--
		}
	}

	return dummy.Next
}

// --- Solution 2: Iterative ---

func iterative(head *ListNode, k int) *ListNode {
	dummy := &ListNode{Next: head}
	groupPrev := dummy

	for {
		end := groupPrev
		for i := 0; i < k; i++ {
			end = end.Next
			if end == nil {
				return dummy.Next
			}
		}

		groupNext := end.Next
		tail, node := groupNext, groupPrev.Next

		for node != groupNext {
			node.Next, tail, node = tail, node, node.Next
		}

		groupPrev.Next, groupPrev = end, groupPrev.Next
	}
}

// --- Solution 3: NoTuple ---

func noTuple(head *ListNode, k int) *ListNode {
	dummy := &ListNode{Next: head}
	groupPrev := dummy

	for {
		end := groupPrev
		for i := 0; i < k; i++ {
			end = end.Next
			if end == nil {
				return dummy.Next
			}
		}

		groupNext := end.Next
		tail := groupNext
		node := groupPrev.Next

		for node != groupNext {
			next := node.Next
			node.Next = tail
			tail = node
			node = next
		}

		tmp := groupPrev.Next
		groupPrev.Next = end
		groupPrev = tmp
	}
}

// --- Benchmarks ---

var sinkNode *ListNode

func benchmarkReverse(b *testing.B, fn func(*ListNode, int) *ListNode) {
	for _, k := range []int{5, 10, 20} {
		for _, n := range []int{100, 1000, 10000} {
			b.Run(fmt.Sprintf("k=%d/n=%d", k, n), func(b *testing.B) {
				pool := make([]ListNode, n)
				seed := uint64(k)*1_000_000 + uint64(n)
				rng := rand.New(rand.NewPCG(42, seed))

				for b.Loop() {
					head := wireList(pool, rng)
					sinkNode = fn(head, k)
				}
			})
		}
	}
}

func BenchmarkArray(b *testing.B)     { benchmarkReverse(b, array) }
func BenchmarkIterative(b *testing.B) { benchmarkReverse(b, iterative) }
func BenchmarkNoTuple(b *testing.B)   { benchmarkReverse(b, noTuple) }
