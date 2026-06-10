package lc23bench

import (
	"container/heap"
	"fmt"
	"math/rand/v2"
	"slices"
	"testing"
)

type ListNode struct {
	Val  int
	Next *ListNode
}

func mergeTwoLists(list1 *ListNode, list2 *ListNode) *ListNode {
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

// wireList wires pool into a sorted linked list in-place, no allocation.
// It fully resets every node's Val and Next, so a pool can be reused across
// benchmark iterations even after a previous merge has cross-linked its nodes.
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

// --- Solution 1: flatten + sort ---
func flattenSort(lists []*ListNode) *ListNode {
	var values []int
	for _, l := range lists {
		for l != nil {
			values = append(values, l.Val)
			l = l.Next
		}
	}
	slices.Sort(values)
	head := &ListNode{}
	cur := head
	for _, v := range values {
		cur.Next = &ListNode{Val: v}
		cur = cur.Next
	}
	return head.Next
}

// --- Solution 2: sequential merge ---
func sequential(lists []*ListNode) *ListNode {
	var head *ListNode
	for _, l := range lists {
		head = mergeTwoLists(head, l)
	}
	return head
}

// --- Solution 3: divide and conquer (iterative, in-place) ---
// NOTE: mutates the contents of the lists slice it is given. The benchmark
// rebuilds that slice every iteration, so this is safe here. Do not hoist the
// slice construction out of the loop or this will read corrupted input.
func dcIterative(lists []*ListNode) *ListNode {
	if len(lists) == 0 {
		return nil
	}
	for len(lists) > 1 {
		n := len(lists)
		w := 0
		if n%2 != 0 {
			lists[n-2] = mergeTwoLists(lists[n-2], lists[n-1])
			n--
		}
		for i := 0; i < n; i += 2 {
			lists[w] = mergeTwoLists(lists[i], lists[i+1])
			w++
		}
		lists = lists[:w]
	}
	return lists[0]
}

// --- Solution 4: divide and conquer (recursive) ---
func dcRecursive(lists []*ListNode) *ListNode {
	if len(lists) == 0 {
		return nil
	}
	if len(lists) == 1 {
		return lists[0]
	}
	if len(lists) == 2 {
		return mergeTwoLists(lists[0], lists[1])
	}
	return mergeTwoLists(
		dcRecursive(lists[len(lists)/2:]),
		dcRecursive(lists[:len(lists)/2]),
	)
}

// --- Solution 5: heap ---
type nodeHeap []*ListNode

func (h nodeHeap) Len() int           { return len(h) }
func (h nodeHeap) Less(i, j int) bool { return h[i].Val < h[j].Val }
func (h nodeHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *nodeHeap) Push(x any)        { *h = append(*h, x.(*ListNode)) }
func (h *nodeHeap) Pop() any {
	old := *h
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	*h = old[:n-1]
	return item
}

func heapMerge(lists []*ListNode) *ListNode {
	h := &nodeHeap{}
	for _, l := range lists {
		if l != nil {
			heap.Push(h, l)
		}
	}
	dummy := &ListNode{}
	cur := dummy
	for h.Len() > 0 {
		smallest := heap.Pop(h).(*ListNode)
		cur.Next = smallest
		cur = cur.Next
		if smallest.Next != nil {
			heap.Push(h, smallest.Next)
		}
	}
	return dummy.Next
}

// --- Benchmarks ---
var sinkNode *ListNode

// makeKLists rewires each pool into a fresh sorted list and returns a new
// slice of heads. Both the per-node values and the lists slice are rebuilt
// every call so every solution sees identical, uncorrupted input.
func makeKLists(pools [][]ListNode, rng *rand.Rand) []*ListNode {
	lists := make([]*ListNode, len(pools))
	for i, pool := range pools {
		lists[i] = wireList(pool, rng)
	}
	return lists
}

func benchmarkMerge(b *testing.B, fn func([]*ListNode) *ListNode) {
	for _, k := range []int{10, 100, 1000} {
		for n := 100; n <= 500; n += 100 {
			b.Run(fmt.Sprintf("k=%d/n=%d", k, n), func(b *testing.B) {
				pools := make([][]ListNode, k)
				for i := range pools {
					pools[i] = make([]ListNode, n)
				}

				// Reseed deterministically per (k, n) so that every solution
				// is benchmarked against the exact same sequence of inputs.
				seed := uint64(k)*1_000_000 + uint64(n)
				rng := rand.New(rand.NewPCG(42, seed))

				for b.Loop() {
					lists := makeKLists(pools, rng)
					sinkNode = fn(lists)
				}
			})
		}
	}
}

func BenchmarkFlattenSort(b *testing.B) { benchmarkMerge(b, flattenSort) }
func BenchmarkSequential(b *testing.B)  { benchmarkMerge(b, sequential) }
func BenchmarkDCIterative(b *testing.B) { benchmarkMerge(b, dcIterative) }
func BenchmarkDCRecursive(b *testing.B) { benchmarkMerge(b, dcRecursive) }
func BenchmarkHeap(b *testing.B)        { benchmarkMerge(b, heapMerge) }
