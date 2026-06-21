+++
date = '2026-06-11T09:15:19-05:00'
draft = false
title = 'LeetCode 25'
url = '/posts/leetcode-25/'
+++

Welcome back. We are going to be solving a dreaded <span style="color:red">HARD</span> problem. Specifically, we are going to do [problem 25](https://leetcode.com/problems/reverse-nodes-in-k-group/description/). What I like about it is that it directly builds on [problem 24, the problem I solved yesterday.](../leetcode-24/) As a reminder, [problem 24](https://leetcode.com/problems/swap-nodes-in-pairs/) asked you to swap nodes in pairs. This problem is the same idea, except instead of pairs, we have to swap `k` nodes. Meaning, problem 24 was a specific instance of this problem where `k=2`. To help, here are two examples:

```
Example 1:
  Input: head = 1->2->3->4->5, k = 2
  Output: 2->1->4->3->5

Example 2:
  Input: head = 1->2->3->4->5, k = 3
  Output: 3->2->1->4->5
```

# Solution 1: Array Tracking

```go
func swapNodes(prevA *ListNode, a *ListNode, prevB *ListNode, b *ListNode) {
	prevA.Next = b
	prevB.Next = a
	a.Next, b.Next = b.Next, a.Next
}

func reverseKGroup(head *ListNode, k int) *ListNode {
    k++ // we need one extra to track the node before
    prev := make([]*ListNode, k)
    dummy := &ListNode{Next: head}
    cur := dummy
    i := 0

    for cur != nil {
        if i == k {
            left := 1
            right := k - 1
            for left < right {
                swapNodes(prev[left - 1], prev[left], prev[right-1], prev[right])
                prev[left], prev[right] = prev[right], prev[left]

                left++
                right --
            }

            prev[0] = prev[1]
            i = 1
        } else {
            prev[i] = cur
            cur = cur.Next
            i++
        }
    }

    if i == k {
        left := 1
        right := k - 1
        for left < right {
            swapNodes(prev[left - 1], prev[left], prev[right-1], prev[right])
            prev[left], prev[right] = prev[right], prev[left]

            left++
            right --
        }
    }

    return dummy.Next
}
```

This solution tracks `k` nodes with an array. Well, it tracks `k+1` nodes. It does so because it needs to track the node that is previous to the group we are swapping for. This also makes it easier to handle the first case.

Once `k+1` nodes have been collected, we swap them from the outside to the inside. `1->2->3->4`, for example, will first swap `1` and `4`: `4->2->3->1`. Then it will swap the interior of `2` and `3`. But, for this to work, we can't just swap the linked list, we have to swap the array. If we don't, the array no longer reflects the structure of the linked list, and we would get the wrong nodes. In our example, it would say that `1` was previous to `2` instead of `4`, causing a bug.

The results for this solution are pretty good. We beat 100% of the submissions with a runtime of 0ms. The memory was slightly worse, beating only 74.62% of submissions.

You'll also notice some duplicate code that starts with `if i == k`. I can hear the critics screaming, "No duplicate code!" Grow up. It doesn't matter.

# Solution 2: Iterative Swap

```go {linenos=true}
func reverseKGroup(head *ListNode, k int) *ListNode {
    dummy := &ListNode{Next: head}
    groupPrev := dummy

    for {
        // find kth element for group
        end := groupPrev
        for i := 0; i < k; i++ {
            end = end.Next

            if end == nil {
                return dummy.Next // out of elements, we're done
            }
        }

        // swap k elements for the group
        groupNext := end.Next
        tail, node := groupNext, groupPrev.Next

        for node != groupNext {
            node.Next, tail, node = tail, node, node.Next
        }

        groupPrev.Next, groupPrev = end, groupPrev.Next
    }
}
```

This solution has an advantage over the other one in that it doesn't have an extra data structure tracking the underlying one. What it does instead is first find the end element with lines 7-14. Lines 17-27 are dedicated to reversing the elements in that group. Before talking about reversing, though, I want to point out that after it, the program loops back to finding k elements again. Eventually, it will run out of elements in the list and return.

Now we can look at the next phase which swaps the nodes in the group. Line 17 grabs `groupNext`, the element just after the kth node. Line 18 sets `tail` to `groupNext` and `node` to `groupPrev.Next`, the first element of the group. The idea is that `node` walks through the group flipping each link backward, while `tail` is what the group's first node will end up pointing at: the node just past the group.

The actual flipping happens on line 21: `node.Next, tail, node = tail, node, node.Next.` Go evaluates tuple assignment on the entire right-hand side before assigning anything, so all three reads (tail, node, and node.Next) happen against the current state, and only then are the three assignments made.

Lastly, line 24 again uses tuple assignment to move the tracking elements along the list so we can swap the next `k` elements.

The runtime was 0ms, beating 100% of submissions. The memory usage beat only 38.97% of submissions.

# Benchmark

I was genuinely surprised that the memory usage for solution 2 was worse than solution 1, given that solution 1 uses an array to track everything. So, for this benchmark, we are going to add an extra solution. Before that, though, let's stop calling things "solution X" and instead say that solution 1 will now be referred to as "Array" and solution 2 as "Iterative." The next solution will be called "NoTuple." NoTuple is going to be the exact same code as Iterative, but it will have zero tuple assignments in it. If you want to see the benchmarking code with this solution you can find it on [GitHub](https://github.com/bi3mer/bi3mer.github.io/tree/master/example-code/leetcode-25).

Each benchmark runs with `k ∈ {5, 10, 20}` and list length `n ∈ {100, 1000, 10000}` using `-count=10`, analyzed with `benchstat`.

<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<script>
const LABELS = [100, 1000, 10000];
const SOLUTIONS = ['Array', 'Iterative', 'NoTuple'];
const COLORS = ['#e15759', '#4e79a7', '#f28e2b'];
function makeChart(id, title, solutions, colors, dataPerSolution) {
  new Chart(document.getElementById(id), {
    type: 'bar',
    data: {
      labels: LABELS,
      datasets: solutions.map((name, i) => ({
        label: name,
        data: dataPerSolution[i],
        backgroundColor: colors[i],
      }))
    },
    options: {
      plugins: { title: { display: true, text: title } },
      scales: {
        x: { title: { display: true, text: 'n (list length)' } },
        y: { title: { display: true, text: 'µs/op' }, beginAtZero: true }
      }
    }
  });
}
</script>

<canvas id="chart-k5" style="max-height:400px"></canvas>

<script>
makeChart('chart-k5', 'k = 5', SOLUTIONS, COLORS, [
  [0.4555, 3.901, 38.96],
  [0.4527, 4.245, 42.07],
  [0.4521, 4.248, 42.19],
]);
</script>

<canvas id="chart-k10" style="max-height:400px"></canvas>

<script>
makeChart('chart-k10', 'k = 10', SOLUTIONS, COLORS, [
  [0.4858, 4.133, 40.90],
  [0.4213, 3.870, 38.74],
  [0.4170, 3.868, 38.39],
]);
</script>

<canvas id="chart-k20" style="max-height:400px"></canvas>

<script>
makeChart('chart-k20', 'k = 20', SOLUTIONS, COLORS, [
  [0.5073, 4.193, 41.32],
  [0.3967, 3.663, 36.43],
  [0.3976, 3.658, 36.43],
]);
</script>

At `k=5`, Array is actually faster than Iterative for larger lists — 3.901µs vs 4.245µs at `n=1000`, about an 8% win. The crossover happens between `k=5` and `k=10`. By `k=10`, Iterative pulls ahead by ~7%, and by `k=20` it leads by ~13%.

Iterative and NoTuple are indistinguishable at every configuration (with some variation due to noise). Without looking at the assembly, it doesn't seem to matter whether you use tuple assignment or not.

On memory, Array allocates a `prev` slice that grows with `k`: 64 B at `k=5`, 112 B at `k=10`, 192 B at `k=20`. Additionally, Array always has 2 allocs per call. Iterative and NoTuple are flat at 16 B and 1 alloc regardless of `k`. That leaves open the question of why LeetCode said that Iterative used more memory than Array. The answer is that LeetCode is an imperfect platform. I ran it again to see if there was any determinism, and there wasn't. This time, the same exact solution had a memory usage that beat 98.79% of other submissions.

# Conclusion

Programming the solution to this problem was a bit tricky and cumbersome, but that was it. The main takeaway, for me, is that tuple assignment doesn't appear to have any performance cost, so might as well use it.

Till next time, friends.
