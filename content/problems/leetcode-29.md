+++
date = '2026-06-15T09:22:12-05:00'
draft = false
title = 'LeetCode 29'
url = '/posts/leetcode-29/'
+++

[LeetCode 29](https://leetcode.com/problems/divide-two-integers/description/) asks for you to implement integer division without using division, mod, or multiplication. Naturally, the first thing I did was use division.

```go
func divide(dividend int, divisor int) int {
    return dividend / divisor
}
```

This, though, failed!

```
input: -2147483648 / -1
Output: 2147483648
Expected Output: 2147483647
```

That led me to the conclusion that this is silly and a waste of time.[^1] So I didn't bother with the bit manipulation solutions I know are out there. Instead, I made a quick fix for division to make Go's division of integers fit what LeetCode wanted.

```go
func divide(dividend int, divisor int) int {
    if dividend == int(-math.Pow(2, 31)) && divisor == -1 {
        return int(math.Pow(2, 31)) - 1
    }

    return dividend / divisor
}
```

I am starting to think that doing one LeetCode problem a day and making an accompanying blog post may not be the best idea. If I had more time, I'd probably give this problem more time. I say "probably," because it isn't necessarily easy to motivate oneself to do something that they are uninterested in, and integer division like this does not catch my fancy. The next one will be better, hopefully.

Till next time, friends.

[^1]: The reason why the output can't be `2^31` and instead should be `2^31 - 1` can be seen in the instructions: "Note: Assume we are dealing with an environment that could only store integers within the 32-bit signed integer range: `[−2^31, 2^31 − 1]`. For this problem, **if the quotient is strictly greater than `2^31 - 1`, then return `2^31 - 1`**, and if the quotient is strictly less than -2^31, then return -2^31."
