+++
date = '2026-06-07T09:41:05-05:00'
draft = false
title = 'LeetCode 21: Merge Two Sorted Lists'
url = '/posts/leetcode-21/'
+++

Unfortunately, [LeetCode 21](https://leetcode.com/problems/merge-two-sorted-lists/) had no interesting wrinkles to explore.

```go
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
```

There is one way to reduce the amount of code, which is to create a dummy variable like so:

```go
func mergeTwoLists(list1 *ListNode, list2 *ListNode) *ListNode {
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
```

This removes the top-level if/else for few lines of code, but the result is identical. To verify this (mainly for fun), I benchmarked both with `testing.B` and `-benchmem`. The full benchmark code is [on GitHub](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-21). Each solution merges two randomly-generated sorted lists, varying the per-list size from 10 to 10,000 nodes. Results are averages over five runs on an AMD Ryzen AI 9 HX 370.

B/op and allocs/op were identical. Both were 0. The functions manipulated memory, but did not allocate.

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<div style="max-width: 680px; height: 350px; margin: 1.5rem auto;">
  <canvas id="lc21chart-ns"></canvas>
</div>
<script src="/js/lc21-charts.js"></script>

Looking at the chart above, solution 2 was technically slower than solution 1, but the difference boils down to noise, a common problem with benchmarking.

Anyways, I hope you enjoyed this post. Personally, I enjoyed adding charts even though a table would be clearer.
