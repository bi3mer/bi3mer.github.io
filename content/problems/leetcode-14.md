+++
date = '2026-07-04T07:48:05-05:00'
draft = false
math = true
title = 'LeetCode 14: Longest Common Prefix'
url = '/posts/leetcode-14/'
+++

[LeetCode 14](https://leetcode.com/problems/longest-common-prefix/description/) asks us to find the longest common prefix for a slice of strings. We are guaranteed that the input slice has at least one string.

```
Example 1:
  Input: strs = ["flower","flow","flight"]
  Output: "fl"

  All three words start with "fl"

Example 2:
  Input: strs = ["dog","racecar","car"]
  Output: ""

  No prefix shared by any of these strings.
```

I think that this problem is fairly clear in terms of what it wants, so let's get to the solution. There are two ways I can see someone trying to solve it. The first way is to a brute force way, where they find the longest common substring for one word given every other element in the slice. Then they do it again for the next, and afterwards you have the take the minimum length common substring and you return it. This, though, is \(O(n^2 \times m)\), where `n` is the number of strings and `m` is the average word length.

We could make that pseudo-algorithm real code, and then try to optimize it. We aren't going to, though. Instead, the big gain will be if we can knock an `n` off the runtime, and we can. We don't have to check every pair every time. We can store what we've done, in a sense. Even better, we don't need some dynamic programming style solution:

```go
func longestCommonPrefix(strs []string) string {
    longest := strs[0]

    for i := 1; i < len(strs); i++ {
        l := min(len(longest), len(strs[i]))

        for l > 0 {
            if longest[:l] == strs[i][:l] {
                break
            }

            l--
        }

        longest = strs[i][:l]
    }

    return longest
}
```

This works for calculating the longest common prefix (LCP) for the first two words. (If there is one word, then it just returns that word because the longest common prefix for one one word is itself.) After it has calculated the first LCP, it calculates the LCP between the previous LCP and the next word in the slice `strs`. So, we store the result and use it to calculate the next LCP, and that is it. Just a loop and a string equality check.

Till next time, friends.
