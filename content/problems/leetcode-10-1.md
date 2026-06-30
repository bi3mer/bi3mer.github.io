+++
date = '2026-06-29T08:44:13-05:00'
draft = false
title = 'LeetCode 10: Regular Expression Matching -> Recursion'
url = '/posts/leetcode-10-1/'
+++

[LeetCode 10](https://leetcode.com/problems/regular-expression-matching/) asks us to implement regular expression matching for two characters: `'.'` and `'*'`. `s` is a string and we're testing whether the pattern string `p` matches the contents of `s`. `'.'` matches any single character. `'*'` matches with zero or more of the preceding character (e.g. `"a*"` could match with "" or "a" or "aaa" or "aaaaaaa" etc.). Fun fact: this is referred to as a [Kleene star.](https://en.wikipedia.org/wiki/Kleene_star)

```
Example 1:
  Input: s = "aa", p = "a"
  Output: false

Example 2:
  Input: s = "aa", p = "a*"
  Output: true

Example 3:
  Input: s = "ab", p = ".*"
  Output: true
```

There are two solid ways to solve this. I know because I did it a few years ago. The first way is recursive and the second way is with [dynamic programming.](https://en.wikipedia.org/wiki/Dynamic_programming) Up to this point, we haven't done any problems that required dynamic programming, and it is not a strong point of mine. As a result, I know that solving the problem the dynamic programming way will take me more than thirty minutes and I don't want to spend my whole morning on this problem. That is why I'm breaking this problem into two blog posts. In the first post, this one, I'll solve the problem with recursion. It is slower than the dynamic programming way, but I could use the practice writing a recursive solution. In [the second post,](/posts/leetcode-10-2/) I'll solve this problem with dynamic programming and explain what dynamic programming even is.

Now, let's talk about how to solve this problem recursively.

Before that, though, it occurs to me that it isn't self apparent that we need to use something complicated like recursion. Why not loop through `s` based on the pattern? The reason is inputs like `s="aaaaaba", p="a*ab"` where it isn't clear how far along `s` we should stop matching with `'a'`. This means we need some kind of backtracking method, hence recursion.

The first thing to do when writing recursion is to figure out your base cases. At least, that's what I think. Who am I to sound all authoritative? Sentences like that are one of the many plagues that have come from AI. So, let's try that again. When I'm doing recursion, the first thing I like to do is figure out my base cases. In this case, I know that I'm going to have two strings (`s` and `p`) and I'm going to recurse through them. I could either pass along indexes or I could slice the strings up. I'm going to opt for the latter in this case. So, my base cases are when either string or both have a length of zero.

```go
func isMatch(s string, p string) bool {
	if len(s) == 0 {
		return len(p) == 0
	}

	if len(p) == 0 { return false }

	// more code below
}
```

Imagine we run the code so far with `isMatch("", "a")`. It will see that the length of `s` is zero and then see that the length of the pattern is one, so it will return `false`. So far so good. What if we tried `isMatch("", "a*")`? Now we have a problem because `'*'` can match with zero or more of the preceding character. So, we need to update the code to handle this case.

```go
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
```

Now we have our base cases handled. I should say that I put in an iterative solution to checking `p`. I could have made it recursive. It would have made the code prettier but needlessly dogmatic in its commitment to recursion.

Now that we have our base cases handled, we can implement checking `s` based on `p`. There are three cases:

1. Regular character (e.g. `'a'`)
2. Wild card (i.e. `'.'`)
3. Kleene star (i.e. `'*'`)
   - Kleene star with regular character
   - Kleene star with wild card

Let's start with imagining we only had to handle regular characters. If this were the case, we would do something like:

```go
if s[0] == p[0] { return isMatch(s[1:], p[1:]) }

return false
```

Then we could add a case for the wild card:

```go
if s[0] == p[0] || p[0] == '.' { return isMatch(s[1:], p[1:]) }

return false
```

However, none of this works if there is a Kleene star after the first character in `p`. So what we actually need to do is handle separately when there is a Kleene star and when there isn't a Kleene star:

```go
if len(p) > 1 && p[1] == '*' {
	if s[0] == p[0] || p[0] == '.' {
		return isMatch(s[1:], p) || isMatch(s, p[2:])
	}

	return isMatch(s, p[2:])
} else {
	if s[0] == p[0] || p[0] == '.' {
		return isMatch(s[1:], p[1:])
	}
}

return false
```

In the Kleene star case, we have two cases to handle. The first is when we have a character match either via the character or via a wildcard. In that case, we return the result of `isMatch(s[1:], p) || isMatch(s, p[2:])`. The first call removes the first character from `s` and keeps `p` unchanged, matching one occurrence. The second skips the "x\*" pair in `p` without consuming `s`, matching zero occurrences. This is the backtracking: if one path fails, the `||` tries the other.

And like that, we have a fully working solution to the problem. Unfortunately, it is slow. It beats only 15.53% of submissions. The way to fix this is with dynamic programming, and that'll be in the [next post.](/posts/leetcode-10-2/) Below is the complete solution based on the code we wrote. I have also included a second version that is much more compact, but is (1) slower and (2) harder to read.

**Our Solution**

```go
func isMatch(s string, p string) bool {
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
	if len(p) > 1 && p[1] == '*' {
		if s[0] == p[0] || p[0] == '.' {
			return isMatch(s[1:], p) || isMatch(s, p[2:])
		}

		return isMatch(s, p[2:])
	} else {
		if s[0] == p[0] || p[0] == '.' {
			return isMatch(s[1:], p[1:])
		}
	}

	return false
}
```

**Compact Solution**

```go
func matchChar(s, p byte) bool {
	return p == '.' || s == p
}

func isMatch(s, p string) bool {
	if s == "" && p == "" { return true }
	if p == "" { return false }

	if len(p) >= 2 && p[1] == '*' {
		if isMatch(s, p[2:]) { return true } // skip star
		return len(s) > 0 && matchChar(s[0], p[0]) && isMatch(s[1:], p)
	}

	return len(s) > 0 && matchChar(s[0], p[0]) && isMatch(s[1:], p[1:])
}
```
