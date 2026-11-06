+++
date = '2026-07-24T07:45:49-05:00'
draft = false
title = 'LeetCode 58: Length of Last Word'
url = '/posts/leetcode-58/'
+++

[LeetCode 58](https://leetcode.com/problems/length-of-last-word/description/) is another <span style="color:green">easy</span> problem.[^aside] For this problem, we get a string and we have to find the length of the last word. Here are the examples:[^onepiece]

```
Example 1:
  Input: s = "Hello World"
  Output: 5

Example 2:
  Input: s = "   fly me   to   the moon  "
  Output: 4
```

There are two main solutions that I can think of. The first solution is to loop forward through the array and track the length of each word and drop it once arriving at a space char (`' '`). That, though, will be slower than iterating backwards through the input string.

```go
func lengthOfLastWord(s string) int {
    i := len(s) - 1
    length := 0

    // ignore preceding spaces
    for ; i >= 0 && s[i] == ' '; i-- { }

    // count length of last word
    for ; i >= 0 && s[i] != ' '; i-- {
        length++
    }

    return length
}
```

This solution has a runtime complexity of \(O(n)\), but in practice it is less complicated than the forward version and should run for less time. Less importantly, it beats 100% of submissions on LeetCode, so we're done.

Till next time, friends.

[^aside]: I know. I am supposed to be doing dynamic programming problems. I'm going to get back to them. It is a very busy week for me.

[^onepiece]: I removed the third example that they provide because I see it as a spoiler for _One Piece_ and I don't approve of that.
