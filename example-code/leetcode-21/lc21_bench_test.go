package lc21bench

import (
	"fmt"
	"math/rand/v2"
	"testing"
)

type ListNode struct {
	Val  int
	Next *ListNode
}

func mergeTwoListsManual(list1 *ListNode, list2 *ListNode) *ListNode {
	if list1 == nil {
		return list2
	} else if list2 == nil {
		return list1
	}

	var head *ListNode
	if list1.Val <= list2.Val {
		head = list1
		list1 = list1.Next
	} else {
		head = list2
		list2 = list2.Next
	}

	cur := head

	for list1 != nil && list2 != nil {
		if list1.Val <= list2.Val {
			cur.Next = list1
			list1 = list1.Next
		} else {
			cur.Next = list2
			list2 = list2.Next
		}

		cur = cur.Next
	}

	if list1 == nil {
		cur.Next = list2
	} else if list2 == nil {
		cur.Next = list1
	}

	return head
}

func mergeTwoListsDummy(list1 *ListNode, list2 *ListNode) *ListNode {
	dummy := &ListNode{}
	cur := dummy

	for list1 != nil && list2 != nil {
		if list1.Val <= list2.Val {
			cur.Next = list1
			list1 = list1.Next
		} else {
			cur.Next = list2
			list2 = list2.Next
		}

		cur = cur.Next
	}

	if list1 != nil {
		cur.Next = list1
	} else {
		cur.Next = list2
	}

	return dummy.Next
}

// wireList links pool into a sorted linked list in-place, no allocation.
func wireList(pool []ListNode, rng *rand.Rand) *ListNode {
	v := rng.IntN(10) + 1
	for i := range pool {
		v += rng.IntN(10) + 1
		pool[i].Val = v
		if i < len(pool)-1 {
			pool[i].Next = &pool[i+1]
		} else {
			pool[i].Next = nil
		}
	}
	return &pool[0]
}

var sinkNode *ListNode

func benchmarkMerge(b *testing.B, mergeFn func(*ListNode, *ListNode) *ListNode) {
	rng := rand.New(rand.NewPCG(42, 0))
	for _, size := range []int{10, 100, 1000, 10000} {
		b.Run(fmt.Sprintf("size=%d", size), func(b *testing.B) {
			pool1 := make([]ListNode, size)
			pool2 := make([]ListNode, size)
			for b.Loop() {
				l1 := wireList(pool1, rng)
				l2 := wireList(pool2, rng)
				sinkNode = mergeFn(l1, l2)
			}
		})
	}
}

func BenchmarkManualHead(b *testing.B) {
	benchmarkMerge(b, mergeTwoListsManual)
}

func BenchmarkDummyNode(b *testing.B) {
	benchmarkMerge(b, mergeTwoListsDummy)
}
