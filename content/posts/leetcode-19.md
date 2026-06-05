+++
date = '2026-06-05T09:37:33-05:00'
draft = false
title = 'Leetcode 19'
+++

[LeetCode 19](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) asks the solver to remove a node from a linked list. It does have a trick, though. Rather than the typical "remove the nth element" it gives you an index based on the end of the list, "remove the nth element from the end of the list."

That framing is the whole problem. In a singly linked list you can only move forward, so "nth from the end" isn't something you can read off directly the way you would in an array. Every solution below is really just a different way of figuring out which node sits before the one you want to drop, since removing a node means pointing its predecessor's `Next` past it.

# Solution 1: Two Loops

The straightforward approach: walk the whole list once to learn its length, then walk again to the node just before the target.

```go
func removeNthFromEnd(head *ListNode, n int) *ListNode {
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
```

# Solution 2: One Loop via Temporary Memory

We can avoid the second loop entirely by storing the pointers in a temporary array.

```go
func removeNthFromEnd(head *ListNode, n int) *ListNode {
    var nodes []*ListNode
    for tmp := head; tmp != nil; tmp = tmp.Next {
        nodes = append(nodes, tmp)
    }

    if n == len(nodes) {
        head = head.Next
    } else {
        nodes[len(nodes) - n-1].Next =  nodes[len(nodes) - n].Next
    }

    return head
}
```

# Solution 3: The Hare and the Tortoise

```go
func removeNthFromEnd(head *ListNode, n int) *ListNode {
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
```

We can instead of using a whole array of memory, use two pointers separated by a fixed gap. First `fast` runs ahead by `n` nodes on its own. Then `fast` and `slow` move in lockstep until `fast` reaches the last node. Because the gap never changes, when `fast` is on the last node, `slow` is sitting exactly on the predecessor of the target.

The `if fast == nil` handles if the user wants to get rid of the first element of the linked list. This is the same special case from the first two solutions, just detected differently.

One thing worth noting: this leans on the problem's guarantee that `1 <= n <= length`. The first loop advances `fast` by `n` with no nil guard, so if `n` could exceed the length it would step past the end and crash. The constraints rule that out, which is also why the problem does not have to define what removing the tenth-from-end of a three-element list should even mean.

# Benchmarking

I benchmarked all three with `testing.B` and `-benchmem`. The full benchmark code is [on GitHub](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-19). If you want to see how the harness is set up — random inputs with a fixed seed, the `sink` variable, and what the columns mean — I covered that in my [LeetCode 17](https://bi3mer.github.io/posts/leetcode-17/) and [LeetCode 18](https://bi3mer.github.io/posts/leetcode-18/) posts.

|                              |   ns/op |  B/op | allocs/op |
| :--------------------------- | ------: | ----: | --------: |
| Solution 1: Two loops        |   919.1 |   803 |        50 |
| Solution 2: Temporary memory | 1,210.6 | 2,012 |        56 |
| Solution 3: Hare & tortoise  |   846.7 |   803 |        50 |
{.styled-table}

Results on an AMD Ryzen AI 9 HX 370 (averages over 5 runs, 1000 random inputs cycled per benchmark).

# Conclusion

This started out, for me, as a very dull problem. If I were working in a language I was more familiar with, I would have had the solution in under a minute, but I didn't even know how to express `None`, `null`, `NULL`, etc. in Go. (It is `nil`.) However, it was nice to see pointers, and it was much more interesting when I got to the third solution. The third solution is still basically two loops. If the list has length `L` and we remove the `n`th node from the end, solution one walks the list twice over for about `2L` pointer-follows, while solution three does `2L - n` (the `fast` pointer covers the whole list once, and `slow` trails it by `n`, so it covers `n` fewer).

Till next time.
