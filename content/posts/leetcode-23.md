+++
date = '2026-06-09T10:46:22-05:00'
draft = true
title = 'LeetCode 23'
+++

[LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/) is the first post in the series that covers a <span style="color:red">HARD</span> problem. Should be challenging, right? Well, let's see.

# Solution 1: Screw Linked Lists

I don't have anything against linked lists. They're cool. However, sorting an array is a solved problem. So, if everything was in just one big slice, then we'd be done.

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

And, the code above is how we can do it. Line 2 declares a slice of integers `values.` Lines 4-9 loop through each linked list, and adds the values to the `values` slice. Line 11 sorts that slice. Then 13-18 take the slice and turn it into a linked list. The last line is to return the beginning of that linked list. Super simple.

And here is what is crazy. Not only does this solution pass all the test cases and the submission cases, it also had a runtime of 0ms and, according to LeetCode, beats 100.00% of submissions. Personally, I don't find this satisfactory at all. In fact, it makes me suspicious of how LeetCode is measuring runtime, but we've run into this problem before. So, we'll get to benchmarking the solution later on in the post to get a more accurate understanding of what is going on.

On the worse side, though, the solution does poorly on the memory front, beating just 11.53% of submissions. So, let's try and come up with something a bit more clever.

# Solution 2: Merging Lists One at a Time

```go {linenos=true}
func mergeKLists(lists []*ListNode) *ListNode {
    var head *ListNode
    for _, l := range lists {
        head = mergeTwoLists(head, l)
    }

    return head
}
```

Looking at this solution, you may be wondering where the function `mergeTwoLists` came from. Well, it is the solution to [problem 21](https://bi3mer.github.io/posts/leetcode-21/). So if you want to see that code, go check that post out.

Now, let's look at the solution itself. We declare a `head` list node and then use it to merge the lists together, one at a time. This can work because we know that each sublist is already sorted, but it is also slow. On LeetCode, the runtime was 72ms, beating only 26.78% of submissions. The memory, though, improved to beating 70.69% of the submissions.

Obviously, this isn't good enough. So, let's come up with something better.

# Solution 3: Divide & Conquer

...

# Complexity Analysis

# Benchmarking

# Conclusion
