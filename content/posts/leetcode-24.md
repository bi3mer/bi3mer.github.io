+++
date = '2026-06-10T09:25:33-05:00'
draft = false
title = 'LeetCode 24'
+++

[LeetCode 24](https://leetcode.com/problems/swap-nodes-in-pairs/) is a problem where you have to swap pairs of nodes in a linked list. I think the examples are more informative than the text, so here are the examples but I did modify them to use linked list notation:

```
Example 1:
  Input:  1 -> 2 -> 3 -> 4
  Output: 2 -> 1 -> 4 -> 3

Example 2:
  Input:  nil
  Output: nil

Example 3:
  Input:  1
  Output: 1

Example 4:
  Input:  1 -> 2 -> 3
  Output: 2 -> 1 -> 3
```

This post will be shorter than the others in the series. Despite being listed as <span style="color:orange">medium</span> difficulty, there wasn't anything that I found interesting.

# Solution 1: Value Swapping

```go
func swapPairs(head *ListNode) *ListNode {
    temp := head
    for temp != nil && temp.Next != nil {
        temp.Val, temp.Next.Val = temp.Next.Val, temp.Val
        temp = temp.Next.Next
    }

    return head
}
```

This solution swaps the values, not the pointers with `Next`. As a result, this really isn't in the spirit of what the problem was after. It also would be tremendously slow if the values were larger structs. Go copies structs by value on assignment, so swapping two large structs would copy both in full every time. With integers, though, this operation is very fast. So fast that LeetCode gives it a 0ms runtime and beats 100% of the solutions.

# Solution 2: Pointer Swapping

```go {linenos=true}
func swapPairs(head *ListNode) *ListNode {
    dummy := &ListNode{Next: head}
    prev := dummy

    for prev.Next != nil && prev.Next.Next != nil {
        left := prev.Next
        right := prev.Next.Next

        left.Next = right.Next // left points to rest of the list
        right.Next = left      // right points back to left
        prev.Next = right      // previous now points to right

        prev = left            // left is now the predecessor of the next pair
    }

    return dummy.Next
}
```

This solution is a bit more complicated than the first. The complication is because we aren't swapping two values. Instead, we have to move the pointers for each pair, which requires three operations, lines 9-12. The only "trick" is to figure out that this can't be done for the first value without either a special case before the for loop or a dummy node to track the node before the pair being swapped. Otherwise, the main difficulty is in thinking about the order of operations.

This solution also beats 100% of the submissions with a runtime of 0ms. It also uses less memory than solution 1, according to LeetCode. Treat, this, though, with a grain of salt. For integers, it really shouldn't matter, and I'm 90% sure that benchmarking would show this. Larger structs would show a difference, though.

That brings me to one note on the whole "beating 100%" thing. It's not like this code snippet is beating all the other submissions. The benchmarking is coarse. You know this if you've read any of the other posts. However, the claim is even less valid for this problem, since the submissions that are worse, from what I can tell, are worse because they include a print statement for debugging. Meaning, this submission is not particularly good. It is basically the only solution.

# Conclusion

If you have read the previous posts, you may be disappointed by the lack of a benchmark. I really just wasn't interested in the results. I found this problem to be dull. On the plus side, it made it very easy to write this post. The [last one](https://bi3mer.github.io/posts/leetcode-23/) took hours; so I may be just a bit burned out as well.

Regardless, I hope you enjoyed this one, and I'm sure the next one will be more exciting since it is a <span style="color:red">HARD</span> problem!
