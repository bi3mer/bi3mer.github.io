+++
date = '2026-06-24T09:49:20-05:00'
draft = false
title = 'LeetCode 5: Longest Palindromic Substring'
url = '/posts/leetcode-5/'
+++

And we are on [LeetCode 5](https://leetcode.com/problems/longest-palindromic-substring/description/). Based on the title, I'm sure you've figured out that we are looking for the largest substring that is a palindrome. An example palindrome is the name "Hannah." Whether you read it backwards or forwards, it is the same.

```
Example 1:
  Input: s = "babad"
  Output: "bab"

Example 2:
  Input: s = "cbbd"
  Output: "bb"

Example 3:
  Input: s = "cbbc"
  Output: "cbbc"
```

# The Basics

Before we can bother with the larger problem, we might as well do the easier part first. The easier part, in this case, is to test whether any string is a palindrome:

```go
func isPalindrome(s string) bool {
    left := 0
    right := len(s) - 1

    for left < right {
        if s[left] != s[right] {
            return false
        }

        left++
        right--
    }

    return true
}
```

The way we can do it is with two pointers: `left` and `right`. These are indexes into the array, and then we loop until `left` is not less than `right`. Inside the loop, we check that `s[left]` is not equal to `s[right]` where `s` is the string we are testing to see if it is a palindrome. If the two are not equal, then we return `false` because that means the string is not a palindrome. Otherwise, we increment `left` and decrement `right`. This loop continues until the stopping condition (`left < right`) is hit or a mismatch is found.

The stopping condition handles two cases. The first case is when `left == right`. This means the string `s` has a length that is odd. So, for example `"aba"`. In this case, the function would check that `'a'` is equal to `'a'`, and then not even check `'b'` because one character is a palindrome in itself. So it skips that check. The other case is when the string length is even and the two middle characters are equal. In this case `left` would become greater than `right` and the stopping condition still works.

# Alright, Let's be Terrible

```go
func longestPalindrome(s string) string {
    if len(s) == 1 {
        return s
    }

    longest := string(s[0])
    for i, _ := range s {
        for j := i + 1; j < len(s); j++ {
            substring := s[i:j+1]
            if isPalindrome(substring) {
                if len(longest) < len(substring) {
                    longest = substring
                }
            }
        }
    }

    return longest
}
```

Here is the simplest solution. We loop through the string starting at index 0 and going to the end. Then we loop through every possible substring starting from index `i`, and check whether it is a palindrome. If so, we update the `longest` substring.

So, we have two loops which takes us to `O(n²)`, but then we have to run `isPalindrome` and that is also `O(n)`, so the real runtime is `O(n³)`. A pretty slow solution, but it passes LeetCode. However, it only beats 7.60% of submissions in terms of runtime.

We can make a speedup for it, though, by not running a check when the substring wouldn't be longer than `longest`.

```go
if len(longest) < len(substring) && isPalindrome(substring) { ... }
```

The ordering matters here: Go short-circuits `&&` left-to-right, so the cheap length check runs first and guards the expensive `O(n)` `isPalindrome` call.

This gets our submission to beating 23.43% of submissions in terms of runtime. Still, not good enough.

# In Which I Try to Be Original

For context, I did this problem two years ago. So I am vaguely aware of the correct solution. However, I don't remember it right now. And, before looking it up, I decided to try and come up with a way to be a bit more clever.

```go
func longestPalindrome(s string) string {
    if len(s) == 1 || isPalindrome(s) {
        return s
    }

    for length := len(s) - 1; length > 1; length-- {
        for i := 0; i <= len(s) - length; i++ {
            substring := s[i:i+length]
            if isPalindrome(substring) {
                return substring
            }
        }
    }

    return string(s[0])
}
```

This function is still `O(n³)`, but it is faster than the previous ones, beating 30.15% of submissions. The way it works is it loops from the outside in. What this lets us do is create an early return condition. The second we've found a substring that is a palindrome, we know that we are done. The worst case, though, is that there are no palindromes longer than a single character inside of `s`. So, the solution is still slow.

# The Real Solution

All along I've known that the real solution is `O(n²)`. The question, though, is how?

```go
func longestPalindrome(s string) string {
    if len(s) == 1 {
        return s
    }

    longest := string(s[0])
    for i := 0; i < len(s); i++ {
        // odd length: center at i
        left, right := i - 1, i + 1
        for left >= 0 && right < len(s) && s[left] == s[right] {
            left--
            right++
        }

        if right - left - 1 > len(longest) {
            longest = s[left+1:right]
        }

        // even length: center at i and i+1
        left, right = i, i+1
        for left >= 0 && right < len(s) && s[left] == s[right] {
            left--
            right++
        }

        if right - left - 1 > len(longest) {
            longest = s[left+1:right]
        }
    }

    return longest
}
```

The way this works is that you have to change how you check the palindrome. The function above checks from the outside to the inside. What if you check from the inside to the outside? What this lets us do is drop the `isPalindrome` function. Before we get to why this is, let's spend one moment to say why this is a good thing.

Take, for example, the string "babad". We checked "ba", "ab", "ba", "bd", "bab", "aba", etc. because we had to. Yes, I made some changes which terminated the search once we found a substring of maximum length, but for every invalid palindrome, we had to search for everything, and we had to because we didn't make `isPalindrome` part of the search.

To make it part of the search, though, we have to check a palindrome from the inside out, but we still have to start from the first index and go to the end. The first index, though, is how we get to something interesting. So let's look at "babad" again:

```
babad
^

_ b a
```

We can't look to the left, so we skip forward to:

```
babad
 ^

b a b -> valid since b == b
_ b a b a -> can't expand further left
```

So we skip forward again:

```

babad
  ^

a b a -> valid since a == a
b a b a d -> invalid, b != d
```

And the loop goes to 'a' and then 'd', but what you'll notice, I hope, is that in a couple lines we traced the whole algorithm. And I point this out because the algorithm is now `O(n²)` simply by checking from the inside out. There are `O(n)` centers, and each one expands at most `O(n)` steps, so the total work is `O(n²)`. We avoid re-scanning full substrings.

The one thing we haven't taken care of in this example is a palindrome that is even length. That is the second inner `for` loop. It has the same exact logic as the first which checked for odd-length palindromes, but this one checks for even ones by changing where the search starts from. That's it.

Lastly, the runtime beats 100% of submissions. So, we're done. We did it!

# Conclusion

Well, we kind of did it. One way to make it faster is the [Rabin-Karp algorithm with binary search](https://www.geeksforgeeks.org/dsa/rabin-karp-algorithm-for-pattern-searching/) to get a solution that is `O(n log(n))`. The trade off is that it has a space complexity of `O(n)`, so it will likely be slower than the final solution here for small strings. However, Glen Manacher figured out an even faster way that is `O(n)` and it is called [Manacher's Algorithm.](https://en.wikipedia.org/wiki/Longest_palindromic_substring#Manacher's_algorithm) The speed up comes from precomputing data to say whether a palindrome exists inside another one.

This one I should have figured out without needing to do the simple solutions. So, for the next couple of posts, I'm going to consciously try to one-shot them, and by that I mean get the right solution without doing the slow solutions first. After all, this is meant for interview prep more than learning Go at this point. So, I might as well practice it as if I were in the interview rather than writing a post.

Till next time, friends.
