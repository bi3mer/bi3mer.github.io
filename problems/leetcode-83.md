+++
date = '2026-07-23T09:08:02-05:00'
draft = false
title = 'LeetCode 83: Remove Duplicates from Sorted List'
url = '/posts/leetcode-83/'
+++

[LeetCode 83](https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/) is another <span style="color:green">easy</span> problem. The idea here is that we have to take a sorted linked list and remove all the duplicates. So, like the problem says, it's easy. Not as easy as removing duplicates from a slice, but still pretty easy.

```go
func deleteDuplicates(head *ListNode) *ListNode {
    if head == nil {
        return nil
    }

    cur := head
    for cur.Next != nil {
        if cur.Val == cur.Next.Val {
            cur.Next = cur.Next.Next
        } else {
            cur = cur.Next
        }

    }

    return head
}
```

Here is how it works:

1. If `head` is an empty linked list, skip it.
2. Loop over the linked list until we get to the end (i.e. `cur.Next == nil`).
   1. If the current linked list element has the same value as the next one, remove it by setting the current element's next to `cur.Next.Next`, skipping over the duplicate.
   2. If not, go one element forward in the linked list.
3. Return `head`, which is the front of the linked list.

This solution has an \(O(n)\) runtime. So, it is, as far as I know, as fast as you can get without getting into micro-optimizations around the order of operations and the data structure itself.

We can also do this recursively:

```go
func deleteDuplicates(head *ListNode) *ListNode {
    if head == nil || head.Next == nil {
        return head
    }

    head.Next = deleteDuplicates(head.Next)
    if head.Val == head.Next.Val {
        return head.Next
    }

    return head
}
```

We have two base cases which are when `head == nil` or when `head.Next == nil`. In either case, we just return `head`. Otherwise, we call `deleteDuplicates` to set the correct value of `head.Next`. Meaning, this recursive version goes all the way to the end of the linked list and then reconstructs backwards. At each step, once `head.Next` is set, we decide whether `head` itself survives: if `head.Val == head.Next.Val`, `head` is a duplicate, so we return `head.Next` instead. Otherwise, `head` is returned.

Till next time, friends.
