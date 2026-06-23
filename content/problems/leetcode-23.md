+++
date = '2026-06-09T10:46:22-05:00'
draft = false
title = 'LeetCode 23: Merge k Sorted Lists'
url = '/posts/leetcode-23/'
+++

[LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/) is the first problem in the series that covers a <span style="color:red">HARD</span> problem. Should be challenging, right? Well, let's see.

To start, I need to define the problem. You get a list of linked lists that are sorted. You have to merge them all into one big linked list, that is also sorted. That's it.

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

And, the code above is how we can do it. Line 2 declares a slice of integers `values.` Lines 4-9 loop through each linked list, and add the values to the `values` slice. Line 11 sorts that slice. Then 13-18 take the slice and turn it into a linked list. The last line is to return the beginning of that linked list. Super simple.

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

```go {linenos=true}
func mergeKLists(lists []*ListNode) *ListNode {
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
```

This solution is very similar to solution 2. The difference is the order of operations. Solution 2 adds one linked list after another to construct one large linked list. This results in a solution that has a runtime complexity of `O(n*k)`, where `n` is the total number of nodes in the input and `k` is the number of lists. This solution merges smaller linked lists first, constructing the final linked list after several iterations. But, how many iterations? Well, whenever you see code that is reducing something by half with each iteration, that means you are probably dealing with a complexity that involves a `log`. In this case, it is `O(n*log(k))` complexity, where we iterate over `n` nodes `log(k)` times.

LeetCode gave this solution a 0ms runtime which beat 100% of other solutions. Even better, the memory usage is down, beating 85.78% of submissions.

# Solution 4: Recursion

```go {linenos=true}
func mergeKLists(lists []*ListNode) *ListNode {
    if len(lists) == 0 { return nil }
    if len(lists) == 1 { return lists[0] }
    if len(lists) == 2 { return mergeTwoLists(lists[0], lists[1]) }

    return mergeTwoLists(
        mergeKLists(lists[len(lists)/2:]),
        mergeKLists(lists[:len(lists)/2]),
    )
}
```

When you recurse, which this solution does, stack memory is allocated and used to recurse backwards. You can't avoid it. In this case, the max depth is `log(k)`. Meaning, the complexity is the same as solution 3: `O(n*log(k))`.

More interesting, this solution is the shortest and probably the most clever of the bunch. The core of the solution is to recurse with `mergeKLists` till getting to a slice of size 1 or 2, and then merge those. Note, though, that the use of slices is important. We aren't creating copies of the arrays, we are just pointing to locations within those arrays with a variable to track the size. From there, the algorithm merges the increasingly larger linked lists until arriving at the final linked list.

The results are very good. 0ms run time which beats 100% of the other submissions. Even better, the memory usage beats 96.39% of the other solutions. The best yet.

# Solution 5: Heap

```go {linenos=true}
import "container/heap"

type nodeHeap []*ListNode

func (h nodeHeap) Len() int {
	return len(h)
}
func (h nodeHeap) Less(i, j int) bool  {
	return h[i].Val < h[j].Val
}
func (h nodeHeap) Swap(i, j int) {
	h[i], h[j] = h[j], h[i]
}
func (h *nodeHeap) Push(x any) {
    *h = append(*h, x.(*ListNode))
}
func (h *nodeHeap) Pop() any {
    old := *h
    n := len(old)
    item := old[n-1]
    *h = old[:n-1]
    return item
}

func mergeKLists(lists []*ListNode) *ListNode {
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
```

This solution is similar in spirit to solution 1. The difference is that instead of pushing all the values into a slice and then sorting, this solution pushes the data into a heap. That heap keeps everything sorted during insertion.

If we were using Python for this series, I wouldn't have bothered with this solution. But I have never used Go's heap. So, here we are.

According to LeetCode, using a heap resulted in a runtime of 3ms, which beat 58.97% of the solutions. The memory usage beat 37.42% of other submissions. So, we used less memory than solution 1 but it was slower. The reason we used less memory is because we are storing pointers to the list nodes, where solution 1 stored the values and then built an entirely new list.

# Benchmarking

The full benchmark code is [on GitHub](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-23). Each benchmark runs all five solutions with `k ∈ {10, 100, 1000}` lists and `m ∈ {100…500}` nodes _per list_ (so the total node count `n` is `k × m`). Note that this `m` is the per-list size; the complexity discussion above used `n` for the total across all lists.

In the [last post](https://bi3mer.github.io/posts/leetcode-22/), I struggled with outliers while benchmarking. I've since learned about the tool [`benchstat`](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat). Running with `-count=10` and piping the output through `benchstat` is "better." (Better in quotes because even better would be to run on a server, and do a bunch of other stuff, so forgive me please.) `benchstat` reports the median rather than the mean, which is already outlier-resistant. It also shows a confidence interval so you can tell whether a difference between two solutions is real or just noise.

Now, let's see the results found on my AMD Ryzen AI 9 HX 370, with `k` fixed per chart and `n` (nodes per list) on the x-axis.

<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<script>
const LABELS = [100, 200, 300, 400, 500];
const SOLUTIONS = ['Solution 1', 'Solution 2', 'Solution 3', 'Solution 4', 'Solution 5'];
const COLORS = ['#e15759', '#4e79a7', '#f28e2b', '#76b7b2', '#59a14f'];
function makeChart(id, title, unit, solutions, colors, dataPerSolution) {
  new Chart(document.getElementById(id), {
    type: 'line',
    data: {
      labels: LABELS,
      datasets: solutions.map((name, i) => ({
        label: name,
        data: dataPerSolution[i],
        borderColor: colors[i],
        backgroundColor: colors[i],
        tension: 0.3,
        pointRadius: 4,
        fill: false,
      }))
    },
    options: {
      plugins: { title: { display: true, text: title } },
      scales: {
        x: { title: { display: true, text: 'n (nodes per list)' } },
        y: { title: { display: true, text: unit }, beginAtZero: true }
      }
    }
  });
}
</script>

<canvas id="chart-k10" style="max-height:400px"></canvas>

<script>
makeChart('chart-k10', 'k = 10', 'µs/op', SOLUTIONS, COLORS, [
  [47.6,  102.4, 167.5, 217.0, 293.8],
  [12.04, 23.86, 35.83, 47.82, 61.21],
  [12.73, 25.03, 37.32, 49.86, 63.13],
  [12.69, 25.15, 37.52, 49.98, 63.17],
  [31.96, 62.77, 94.21, 125.7, 160.9],
]);
</script>

<canvas id="chart-k100" style="max-height:400px"></canvas>

<script>
makeChart('chart-k100', 'k = 100', 'µs/op', SOLUTIONS, COLORS, [
  [633.3, 1395,  2358,  3605,  4559],
  [671.8, 1385,  2124,  2882,  5131],
  [207.3, 408.6, 617.4, 817.2, 1086],
  [210.2, 417.5, 631.1, 833.8, 1110],
  [530.3, 1048,  1580,  2106,  2718],
]);
</script>

<canvas id="chart-k1000" style="max-height:400px"></canvas>

<script>
makeChart('chart-k1000', 'k = 1000', 'ms/op',
  ['Solution 1', 'Solution 3', 'Solution 4', 'Solution 5'],
  ['#e15759', '#f28e2b', '#76b7b2', '#59a14f'],
  [
    [8.411, 14.77, 23.07, 28.76, 35.04],
    [3.280, 6.691, 10.10, 13.50, 20.35],
    [3.102, 6.480, 9.851, 13.03, 19.41],
    [8.644, 17.54, 26.13, 34.96, 45.08],
  ]
);
</script>

The first thing to notice, I think, is that solution 2 isn't in the final chart for `k=1000`. The reason is that it was so much slower that the chart couldn't show the difference between the remaining solutions. So, instead, let's look at a table of the results:

| n   | Solution 2 (ms/op) |
| --- | ------------------ |
| 100 | 168                |
| 200 | 358                |
| 300 | 554                |
| 400 | 735                |
| 500 | 1,373              |

{ .styled-table }

The y-axis in the `k=1000` chart only goes to about 50 ms for the remaining four solutions, whereas solution 2 hits `1,373 ms/op` when `m=500`.

Now with that out of the way, there are two remaining things to discuss. First, let's look at the performance of solution 1 (sorted array), solution 2 (merge one at a time), and solution 5 (heap). At `k=10`, solution 2 is extremely performant and keeps up with the best solutions. The same can not be said for solutions 1 and 5, but solution 1 is worse. So, sorting during insertion is faster in this case than sorting after. At `k=100`, solution 5 is still ahead of 1 and 2. Something interesting, though, happens with solutions 1 and 2, where solution 2 becomes slower than solution 1 at `m=500`. Lastly, at `k=1000`, solution 2 becomes so slow that it cannot be seen on the chart, but something interesting happened. The heap-based solution 5 became slower than the array.

What happened?

My answer, without having dug into it too much, is that we get to see cache locality, and the use of a very well understood algorithm (`slices.Sort` uses a [specialized quicksort](https://go.dev/src/slices/sort.go) called [Pattern-defeating Quicksort](https://arxiv.org/pdf/2106.05123)), making up for the inherent slowness of the approach. It should also be noted that the comparison isn't a completely fair one. The heap implementation uses `ListNode` and the slice one uses `int`. So, solution 1 uses one single block of memory to sort over, while solution 5 has to go through indirect pointers scattered across the computer's memory.

That said, none of these solutions beat solutions 3 and 4, which are essentially the same except 3 is imperative and 4 is recursive. Which is better? Based on the speed, I'm not inclined to say that either performed better than the other. We could do some statistical analysis to see if there were any significant differences, but I'd rather not.

What I will say is that the implementation of the recursive solution was significantly easier to implement than the imperative, and uses much less code. So, I'm inclined to say that the recursive solution is better. However, let's look at the memory usage.

## Memory

Ki is kibibytes (1,024 bytes). Mi is mebibytes (1,048,576 bytes).

| Solution   | k=10, m=100 | k=10, m=500 | k=100, m=100 | k=100, m=500 | k=1000, m=100 | k=1000, m=500 |
| ---------- | ----------- | ----------- | ------------ | ------------ | ------------- | ------------- |
| Solution 1 | 40.3 Ki     | 203 Ki      | 506 Ki       | 2.63 Mi      | 5.4 Mi        | 27.7 Mi       |
| Solution 2 | 80 B        | 80 B        | 896 B        | 896 B        | 8.0 Ki        | 8.0 Ki        |
| Solution 3 | 80 B        | 80 B        | 896 B        | 896 B        | 8.0 Ki        | 8.0 Ki        |
| Solution 4 | 80 B        | 80 B        | 896 B        | 896 B        | 8.0 Ki        | 8.0 Ki        |
| Solution 5 | 352 B       | 352 B       | 3.0 Ki       | 3.0 Ki       | 25.1 Ki       | 25.1 Ki       |

{ .styled-table }

What we see isn't that surprising. Solutions 2, 3, and 4 have the exact same number of bytes allocated for every test case. Solutions 1 and 5, though, allocate much more. I think the interesting thing to note is that you can see in the numbers how memory is allocated dynamically by each data structure. Solution 1 grows with the total node count. Solution 5 grows by doubling its backing array as it fills.

| Solution   | k=10 | k=100 | k=1000 |
| ---------- | ---- | ----- | ------ |
| Solution 1 | k×m  | k×m   | k×m    |
| Solution 2 | 1    | 1     | 1      |
| Solution 3 | 1    | 1     | 1      |
| Solution 4 | 1    | 1     | 1      |
| Solution 5 | 7    | 10    | 13     |

{ .styled-table }

Solutions 2, 3, and 4 always allocate exactly 1 (the list-of-heads slice). Solution 1 allocates `k×m` plus overhead. Solution 5 allocates `O(log(k))` times as the backing array grows through successive doublings. You can see this directly in the table: each ×10 increase in `k` adds about 3 allocations, and `log2(10) ≈ 3.3`.

# Conclusion

This problem turned out to be less hard than advertised. Solutions 1, 2, and 5 were all very easy to implement. Solution 3 took me a bit more time to think through, but made it extremely easy to implement solution 4.

As per usual, the more interesting work has been benchmarking after the fact. Solution 2 being the worst performing was a bit surprising, especially since it did so poorly at `k=1000` that it had to be cut from the graph. Otherwise, once I figured out the basic logic that it was `O(n*k)`, and that it could be reduced to `O(n*log(k))`, the problem became much simpler. Again, when you want `log`, try to divide the problem in two. That's the basic logic behind quicksort, after all. Anywho, I hope you enjoyed this post. I certainly did.

Till next time.
