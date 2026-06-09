+++
date = '2026-06-09T10:46:22-05:00'
draft = true
title = 'LeetCode 23'
+++

[LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/) is the first post in the series that covers a <span style="color:red">HARD</span> problem. Should be challenging, right? Well, let's see.

# Solution 1: Screw Linked Lists

I don't have anything against linked lists. They're cool. However, sorting an array is a solved problem. So, if everything was in just one big array, then we'd be done.

```go {linenos=true}
func mergeKLists(lists []*ListNode) *ListNode {
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
        cur.Next = &ListNode {Val: v, Next: nil}
        cur = cur.Next
    }

    return head.Next
}
```

And, the code above is how we can do it. Line 2 declares the array of integers `values.` Lines 4-9 loops through each linked list, and adds the values to the `values` array. Line 11 sorts that array. Then 13-18 take the array and turn it into a linked list. The last line is to return the beginning of that linked list. Super simple.

And here is what is crazy. Not only does this solution pass all the test cases and the submission cases, it also had a runtime of 0ms and, according to LeetCode, beats 100.00% of submissions. Personally, I don't find this satisfactory at all. In fact, it makes me suspicious of how LeetCode is measuring runtime. But, oh well.

On the worse side, though, the solution does poorly on the memory front, beating just 11.53% of submissions. So, let's try and come up with something a bit more clever.

# Solution 2:
