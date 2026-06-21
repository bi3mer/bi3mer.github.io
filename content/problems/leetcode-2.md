+++
date = '2026-06-21T09:06:31-05:00'
draft = false
title = 'Leetcode 2'
url = '/posts/leetcode-2/'
+++

[LeetCode 2](https://leetcode.com/problems/add-two-numbers/description/) asks the user to add two numbers represented as linked lists, where that linked list is reversed.

```
Example 1:
  Input: l1 = 2->4->3, l2 = 5->6->4
  Output: 7->0->8
```

Example one shows why the linked list being reversed is important. `2->4->3` represents `342` NOT `243`

```
Example 2:
  Input: l1 = 0, l2 = 0
  Output: 0

Example 3:
  Input: l1 = 9->9->9->9->9->9->9, l2 = 9->9->9->9
  Output: 8->9->9->9->0->0->0->1
```

This becomes important because if you look at example 3, we have two input numbers of different magnitudes, but because they are reversed, we can add from the start of the list. We'll do this a little later in the post.

# Failure Due to Overflow

```go
func listToInt(l *ListNode) int {
    magnitude := 1
    number := 0

    for l != nil {
        number += magnitude * l.Val
        magnitude *= 10
        l = l.Next
    }

    return number
}

func intToList(num int) *ListNode {
    s := strconv.Itoa(num)
    head := &ListNode{}
    dummy := head

    for i := len(s) - 1; i >= 0; i-- {
        dummy.Next = &ListNode{Val: int(s[i] - '0')}
        dummy = dummy.Next
    }

    return head.Next
}

func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
    return intToList(listToInt(l1) + listToInt(l2))
}
```

This solution is lazy in two ways. First, it doesn't implement addition of two lists. Instead, it converts both lists into an `int`. Then we get addition for free and the challenge is to turn that number back into a list again. The way it turns the integer back into a list is the second way that this implementation is lazy. It converts the number into a string and then uses that string to make the list in reverse order.

I say that string conversion is lazy because it is unnecessary. You can do a math version without any heap allocations.

```go
func intToList(num int) *ListNode {
    head := &ListNode{}
    dummy := head

    for {
        dummy.Next = &ListNode{Val: num % 10}
        dummy = dummy.Next
        num /= 10
        if num == 0 {
            break
        }
    }

    return head.Next
}
```

However, I didn't initially code this solution because I'm lazy and its easier to think about string conversion than integer division.[^strAside]

Regardless, this solution doesn't work due to the input:

```
Input:
  l1 = 1->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->1
  l2 = 5->6->4

Output:
  6->6->4->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->0->1
```

The problem is that `l1` is a number with 31 digits. The max for Go's `int` is `9,223,372,036,854,775,807` or `2^{63}-1` for a 64 bit operating system, and this number is comprised of 19 digits. So, the input is too large, and the lazy solution, even if fixed, is too lazy to work.

# Fine, I'll Do What You Wanted

```go
func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
    head := &ListNode{}
    dummy := head
    carryOver := 0
    for l1 != nil && l2 != nil {
        nextVal := l1.Val + l2.Val + carryOver
        dummy.Next = &ListNode{Val: nextVal % 10}
        carryOver = nextVal / 10

        dummy = dummy.Next
        l1 = l1.Next
        l2 = l2.Next
    }

    for l1 != nil {
        nextVal := l1.Val + carryOver
        dummy.Next = &ListNode{Val: nextVal % 10}
        carryOver = nextVal / 10

        dummy = dummy.Next
        l1 = l1.Next
    }


    for l2 != nil {
        nextVal := l2.Val + carryOver
        dummy.Next = &ListNode{Val: nextVal % 10}
        carryOver = nextVal / 10

        dummy = dummy.Next
        l2 = l2.Next
    }

    if carryOver > 0 {
        dummy.Next = &ListNode{Val: carryOver}
    }

    return head.Next
}
```

The way this works is we iterate through `l1` and `l2` together for as long as possible. This works because the reversed list guarantees that each number at index `i` shares the same digit location (e.g. `1->3` and `1->3->4` works such that both ones and both threes share the same index and adding them gives `2->6->4`).

The only other thing to consider, before getting to lists of unequal length is a carry over (e.g. `9+4=13` which gives a `carryOver` of `1` and a value of `3`.) I handled this with `%` and then integer division by `/ 10`. It may have been faster to use something like:

```go
if nextVal >= 10 {
	nextVal -= 10
	carryOver = 1
} else {
	carryOver = 0
}
```

And then I could have wrapped it into a function which returned two integers to make the code cleaner and easier to read. Oh! I forgot to say why this works. This works because there is a constraint that every number in the list is less than ten. Otherwise, this wouldn't work and the integer division approach would be necessary. Also, though, I don't know if this would be faster than integer division because you have branching. I'd have to benchmark it, but we aren't benchmarking for this blog post.

Sorry. Back to the solution.

The last thing to do is to handle unequal list lengths---see the example above. I have two `for` loops. One loops until `l1` is `nil` and the other loops until `l2` is `nil`. They are almost exact duplicates of each other. I almost made a function instead since, as you know, "Duplication may be the root of all evil in software."[^attribution] I didn't, though, because I like the guideline that you shouldn't wrap things into functions until you have three or more duplicates. Also, this is LeetCode. Code quality doesn't matter.

The way the loops work is exactly the same as the bigger loop that works with both lists. They unfortunately have to handle `carryOver` to handle the case of there being a carry over and the list having a bunch of nines.

# Conclusion

As medium problems go, this was fine. I always like but hate when input is designed specifically to prevent lazy solutions, and this problem had that. So good on whoever created this problem.

One weakness in the final solution is that the memory usage was not great. It beat only 11.53% of submissions. It turns out that there is a trick that I had missed up to this point: `debug.FreeOSMemory()`. I added this line of code to the bottom of my function, right before the return, and all of a sudden I am beating 99.52% of submissions in terms of memory usage. The tradeoff, though, is that my runtime went from beating 100% of submissions to a mere 5.12%. What the function does is force a garbage collection run, freeing as much memory as possible.

That, though, isn't the only way to reduce memory usage. The other way would be to overwrite `l1` or `l2` in place. Then, when one was overwritten, switch to overwriting the other. The worst case would be allocating one extra node, which happens when carry propagates past both lists (e.g. `999+1`). This, though, is a terrible solution. Mutating input like that in real code is borderline violence, especially without warnings in the function name or something like that.

Till next time, friends.

[^strAside]: Also, if string conversion worked, I was planning on benchmarking to show how slow string conversion would be to the integer division alternative.

[^attribution]: Martin, Robert C. Clean code: a handbook of agile software craftsmanship. Pearson Education, 2009.
