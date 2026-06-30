+++
date = '2026-06-29T08:50:27-05:00'
draft = false
title = 'Leetcode 10: Regular Expression Matching -> Dynamic Programming'
url = '/posts/leetcode-10-2/'
+++

We're back for part 2. In [the previous post,](/posts/leetcode-10-1/) we solved [LeetCode 10](https://leetcode.com/problems/regular-expression-matching/) with recursion. In this post, we are going to solve it with dynamic programming.

Dynamic programming breaks a problem into subproblems, solves them, and stores their results. Once stored, those results can be reused for a massive speedup when the same subproblems come up again. Two conditions need to hold for this to work:

1. Overlapping subproblems - subproblems recur across branches
2. Optimal substructure - an optimal solution can be built from optimal solutions to its parts

Given those requirements, we have an obvious question to ask: Does this regex problem meet the requirements for dynamic programming? Yes, yes it does. Looking back at the [recursive solution](/posts/leetcode-10-1/), we can see both:

1. Overlapping subproblems - different paths through the recursion tree end up evaluating the same `(s, p)` suffix pairs.
2. Optimal substructure - whether `s[0..i]` matches `p[0..j]` depends only on whether smaller substrings match, so we can build the full answer from smaller answers.

That, though, is the easy part of dynamic programming. At least for me. Now, we have to implement it. There are two approaches: top-down and bottom-up. Top-down dynamic programming uses recursion with memoization (storing past results and using them). Bottom-up dynamic programming builds a table and fills it in while using that table when possible to speed up finding results.

In this post, we are going to implement both. Because we implemented a recursive solution, we might as well start with top-down.

## Top-Down Dynamic Programming Solution

```go
type key struct { s, p string }

func isMatchTopDown(s string, p string, memo map[key]bool) bool {
	// Base Case 1: Empty s
	if len(s) == 0 {
		if len(p) % 2 == 0 {
			// check if Kleene star make empty string match
			for i := 1; i < len(p); i+=2 {
				if p[i] != '*' { return false }
			}

			return true
		}

		// if not mod 2, then Kleene stars do not matter
		return false
	}

	// Base Case 2: Empty p
	if len(p) == 0 {
		return false
	}

	// Recursive Case
    k := key{s, p}
    if res, ok := memo[k]; ok {
        return res
    }

    res := false
	if len(p) > 1 && p[1] == '*' {
		if s[0] == p[0] || p[0] == '.' {
			res = isMatchTopDown(s[1:], p, memo) || isMatchTopDown(s, p[2:], memo)
		} else {
            res = isMatchTopDown(s, p[2:], memo)
        }
	} else {
		if s[0] == p[0] || p[0] == '.' {
			res = isMatchTopDown(s[1:], p[1:], memo)
		}
	}

    memo[k] = res
	return res
}

func isMatch(s string, p string) bool {
    memo := map[key]bool{}
    return isMatchTopDown(s, p, memo)
}
```

If this code makes no sense, please go back to the [previous post](/posts/leetcode-10-1/) where it is properly described because this section won't discuss how it works. Instead, it will only discuss the changes.

The first change is at the very bottom with `isMatch`. The previous solution had `isMatch` be recursive. Now, it makes a map `memo` and then calls a new function `isMatchTopDown` with `s`, `p`, and the new `memo`. Before going into the changes for `isMatchTopDown`, it is worth looking at the type of `memo`. It has this mystery type `key` and the value that the `key` links to is a `bool`.

```go
type key struct { s, p string }
```

This is the type definition for `key`. It is a struct with two strings. `memo` then reflects the signature of `isMatch`. You give it two strings, and it outputs a `bool`. The difference, of course, is that `memo` is a `map` that is unpopulated when `isMatch` is called. The job of populating and using `memo` is handled by `isMatchTopDown`.

`isMatchTopDown` is almost exactly the same as the previous solution. Four things changed: the function takes a `memo` parameter, a cache lookup happens before the recursive case, all `return` statements in the recursive case are replaced with assignments to `res`, and `memo[k] = res` is stored before returning. That's it. Really not hard at all once you have the recursion figured out.

## Bottom-Up Dynamic Programming Solution

```go
func isMatch(s string, p string) bool {
    m, n := len(s), len(p)
    dp := make([][]bool, m+1)
    for i := range dp {
        dp[i] = make([]bool, n+1)
    }
    // ...
}
```

Bottom up dynamic programming is where we build a table. The code above is how we can make said table for this problem. The table is based on the length of `s` and `p`. Notice, then, that instead of passing around strings that have been cut up, we are going to be working with indexes into `s` and `p`. All the values in `dp` (short for dynamic programming) are by default initialized to `false`, which is ideal in this case since we want the default to be `false`. (However, it makes the code a bit less clear, I think.)

```go
dp[0][0] = true
```

We do want some values in the table to be `true`. Above, we can see the first one. `true` means a match. The problem, though, is that it isn't clear what exactly the indexes `0` and `0` mean. `dp[i][j]` means "`s[:i]` matches `p[:j]`". So `dp[0][0]` means an empty string matches an empty pattern, which is true. (See recursive solution above.)

```go
for j := 2; j <= n; j++ {
	if p[j-1] == '*' {
		dp[0][j] = dp[0][j-2]
	}
}
```

That, though, isn't our only base case. Another base case is when `s` is empty but `p` is not. A Kleene star can match zero characters, so patterns like `"a*"` or `"a*b*"` can match an empty string. The loop sets `dp[0][j] = dp[0][j-2]` when it sees a `'*'`, meaning it inherits from two spots back.

```go
for i := 1; i <= m; i++ {
	for j := 1; j <= n; j++ {
		if p[j-1] == '*' {
			// handled below
		} else if p[j-1] == s[i-1] || p[j-1] == '.' {
			dp[i][j] = dp[i-1][j-1]
		}
	}
}

return dp[m][n]
```

Now we have some code that is truly unreadable, and this is why I really dislike bottom-up dynamic programming. I'm sure there is a better way to write it, though. I need more practice. Right now all the indexing is just too much.

Regardless, we have two for loops. The first loops through `m`, which is the length of `s`, with `i` and the second loops through `n`, which is the length of `p`, with `j`. So, there is an example of bad naming, but let's not dwell on that.

The indexes are based on `s[:i]` and `p[:j]`. So, by starting at small values we are building `dp` from the bottom-up. Hence the name.

We start inside the inner `for` loop by checking if we are in the case of a Kleene star. We'll come back to the if `true` case and start with what happens when it evaluates to `false`. The condition for the `else if` is: `else if p[j-1] == s[i-1] || p[j-1] == '.'`. This code is extremely similar to the recursive solution and all we are doing is checking for two characters matching. What isn't as clear is: `dp[i][j] = dp[i-1][j-1]`. `dp[i][j]` is what we are currently evaluating, and we are setting it to the value previously evaluated for `dp[i-1][j-1]`. What this means is that if the previous regex was valid, then this, slightly larger one, is also valid.

Now, let's go back and handle the case when `p[j-1] == '*'` evaluates to `true`:

```go
if p[j-2] == s[i-1] || p[j-2] == '.' {
    dp[i][j] = dp[i][j-2] || dp[i-1][j]
} else {
    dp[i][j] = dp[i][j-2]
}
```

We start with a familiar looking `if` condition: `p[j-2] == s[i-1] || p[j-2] == '.'`. All this is doing is checking if the characters match or we have a wildcard. If so, we get the confusing looking code: `dp[i][j] = dp[i][j-2] || dp[i-1][j]`. This right hand side is equivalent to the recursive solution: `isMatch(s, p[2:]) || isMatch(s[1:], p)`. So, all we are doing is looking backwards to see what we found for the smaller results. It is easy, but not necessarily intuitive. Hopefully future posts on dynamic programming make this clearer.

That code won't evaluate, though, when we don't get a character match. So, instead, we evaluate `dp[i][j] = dp[i][j-2]`. This code is using the result two pattern characters before, and the reason why that works is because Kleene star can evaluate an empty string to `true`.

From there, the algorithm runs until it has completely filled in the graph, and it does it in `O(mn)` time. It is, according to LeetCode's faulty measurements, faster than the top-down approach. The full solution is at the bottom of this post.

## Conclusion

I've learned that top-down dynamic programming is easy. Make the recursive solution, then add memoization. Easy. Bottom-up dynamic programming is brutal. I'll need a ton more practice before I ever try it outside of a LeetCode problem. That said, I don't know if I have ever come across a problem where dynamic program was required except for pathfinding. Pathfinding, though, is somehow different for me. Probably because I've implemented all the variants so many times.

Regardless, I hope you enjoyed this post. I'm definitely going to look to restructure this series of posts once I finish problem 16. I need to practice dynamic programming with more intent. I don't think it will suffice to wait till they randomly pop up.

Till next time, friends.

### Code for Bottom-Up Solution

```go
func isMatch(s string, p string) bool {
    m, n := len(s), len(p)
    dp := make([][]bool, m+1)
    for i := range dp {
        dp[i] = make([]bool, n+1)
    }

    dp[0][0] = true

    for j := 2; j <= n; j++ {
        if p[j-1] == '*' {
            dp[0][j] = dp[0][j-2]
        }
    }

    for i := 1; i <= m; i++ {
        for j := 1; j <= n; j++ {
            if p[j-1] == '*' {
                if p[j-2] == s[i-1] || p[j-2] == '.' {
                    dp[i][j] = dp[i][j-2] || dp[i-1][j]
                } else {
                    dp[i][j] = dp[i][j-2]
                }
            } else if p[j-1] == s[i-1] || p[j-1] == '.' {
                dp[i][j] = dp[i-1][j-1]
            }
        }
    }

    return dp[m][n]
}
```
