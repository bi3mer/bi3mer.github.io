package lc19bench

import (
	"math/rand/v2"
	"testing"
)

type ListNode struct {
	Val  int
	Next *ListNode
}

func removeNthFromEndTwoLoops(head *ListNode, n int) *ListNode {
	tmp := head
	size := 0
	for tmp != nil {
		tmp = tmp.Next
		size++
	}
	if n == size {
		head = head.Next
	} else {
		tmp = head
		size -= n + 1
		for size > 0 {
			tmp = tmp.Next
			size--
		}
		tmp.Next = tmp.Next.Next
	}
	return head
}

func removeNthFromEndTempMemory(head *ListNode, n int) *ListNode {
	var nodes []*ListNode
	for tmp := head; tmp != nil; tmp = tmp.Next {
		nodes = append(nodes, tmp)
	}
	if n == len(nodes) {
		head = head.Next
	} else {
		nodes[len(nodes)-n-1].Next = nodes[len(nodes)-n].Next
	}
	return head
}

func removeNthFromEndHareTortoise(head *ListNode, n int) *ListNode {
	slow := head
	fast := head
	for i := 0; i < n; i++ {
		fast = fast.Next
	}
	if fast == nil {
		return head.Next
	}
	for fast.Next != nil {
		fast = fast.Next
		slow = slow.Next
	}
	slow.Next = slow.Next.Next
	return head
}

func buildList(vals []int) *ListNode {
	dummy := &ListNode{}
	cur := dummy
	for _, v := range vals {
		cur.Next = &ListNode{Val: v}
		cur = cur.Next
	}
	return dummy.Next
}

type input struct {
	vals []int
	n    int
}

func randomInputs(count int) []input {
	rng := rand.New(rand.NewPCG(42, 0))
	inputs := make([]input, count)
	for i := range inputs {
		length := int(rng.IntN(99)) + 2 // 2..100
		vals := make([]int, length)
		for j := range vals {
			vals[j] = int(rng.IntN(100))
		}
		n := int(rng.IntN(length)) + 1 // 1..length
		inputs[i] = input{vals: vals, n: n}
	}
	return inputs
}

var sink *ListNode

func BenchmarkTwoLoops(b *testing.B) {
	inputs := randomInputs(1000)
	idx := 0
	b.ResetTimer()
	for b.Loop() {
		sink = removeNthFromEndTwoLoops(buildList(inputs[idx].vals), inputs[idx].n)
		idx = (idx + 1) % 1000
	}
}

func BenchmarkTempMemory(b *testing.B) {
	inputs := randomInputs(1000)
	idx := 0
	b.ResetTimer()
	for b.Loop() {
		sink = removeNthFromEndTempMemory(buildList(inputs[idx].vals), inputs[idx].n)
		idx = (idx + 1) % 1000
	}
}

func BenchmarkHareTortoise(b *testing.B) {
	inputs := randomInputs(1000)
	idx := 0
	b.ResetTimer()
	for b.Loop() {
		sink = removeNthFromEndHareTortoise(buildList(inputs[idx].vals), inputs[idx].n)
		idx = (idx + 1) % 1000
	}
}
