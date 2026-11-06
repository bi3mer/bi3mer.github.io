+++
date = '2026-06-27T09:43:24-05:00'
draft = false
title = 'LeetCode 8: String to Integer (atoi)'
url = '/posts/leetcode-8/'
+++

We are doing [LeetCode 8](https://leetcode.com/problems/string-to-integer-atoi/description/) today. Unlike in most problems, they give us a set of instructions to follow. The first is to avoid any leading white space:

```go
func myAtoi(s string) int {
	if len(s) == 0 { return 0 }

	i := 0
	for ; i < len(s) && s[i] == ' '; i++ {}
	if i >= len(s) { return 0 }

	// next step...

	return -1
}
```

The line that skips the white space is the for loop. It increments `i` until a non-`' '` character is found but also does bounds checking. This takes me to one point of confusion for me, which is what are we supposed to do for an empty string? For now, I have it returning 0. In reality, I'd like to return 0 and an error.

Regardless, the next step is to check for the sign by looking for '+' or '-':

```go
// get sign
sign := 1
if s[i] == '-' {
	sign = -1
	i++

	if i >= len(s) { return 0 }
} else if s[i] == '+' {
	i++
	if i >= len(s) { return 0 }
}
```

Next up is where we get to read the number. To do so, we first have to get rid of the leading zeroes:

```go
for ; i < len(s) && s[i] == '0'; i++ {}
if i >= len(s) { return 0 }
```

It is only in this step where I saw, "If no digits were read, then the result is 0." So, returning zero was the right call. Regardless, we now, finally, get to read the number. To do that we can use the classic subtract by `'0'` to get the digit and if that digit is greater than `9` or less than `0`, then we ran into a character that isn't valid and we should stop reading. This is where I made one mistake. I initially returned `0`, but the behavior LeetCode wants is to just stop reading.

Last thing, since we are reading left to right in a base ten number system, we don't just add the digits together. We multiply by ten before adding the new digit, essentially shifting every previous digit to the left.

```go
// read in digit
var result int64
for ; i < len(s); i++ {
    c := int(s[i]) - int('0')
    if c < 0 || c > 9 { break }

    result = result*10 + int64(c)
}
```

This isn't the stopping point. What we are missing is the bounds check. If the number is less than `-2^{31}`, it should be rounded to `-2^{31}`. If the number is greater than `2^{31} - 1`, it should be rounded `2^{31} - 1`.

We could, theoretically, put the rounding code in the `for` loop or outside of it. I want to put it outside of the `for` loop so that the loop can run fast without checking bounds. However, that would be a bad choice. Go wraps integers, and we are surely going to get input that oversteps the bounds of a 64 bit `int`. So, we have to check if result is too large inside the `for` loop. That is why `result` is explicitly of type `int64`.

```go
result = result*10 + c

if sign == 1 {
	if result >= math.MaxInt32 { return math.MaxInt32 }
} else if result >= math.MaxInt32 + 1 { return math.MinInt32 }
```

Now that we have bounds handled inside the `for` loop with early returns, we have to handle the case of the sign of the number before returning it. Well, we'll also need to convert `result` to an `int`.

```go
return int(result * int64(sign))
```

And that is the solution.

As problems go, I thought that this was a bad one. It told you exactly what to do with literal steps. Those steps made it too easy to solve, and I feel like an "easy" ranking would be more appropriate. However, that kind of scaffolding is perfect for people learning how to program. So, if I context switch to someone learning programming for the first time, then this is a great problem. They can learn a bit about ASCII, and learn how to implement a function `atoi` that is fundamental to programming.

Till next time, friends.

---

```go
func myAtoi(s string) int {
	if len(s) == 0 { return 0 }

	// skip white space
	i := 0
	for ; i < len(s) && s[i] == ' '; i++ {}
	if i >= len(s) { return 0 }

	// get sign
	sign := 1
	if s[i] == '-' {
		sign = -1
		i++
		if i >= len(s) { return 0 }
	} else if s[i] == '+' {
		i++
		if i >= len(s) { return 0 }
	}

	// skip leading 0's
	for ; i < len(s) && s[i] == '0'; i++ {}
	if i >= len(s) { return 0 }

	// convert remaining string bytes to number
	var result int64
	for ; i < len(s); i++ {
		c := int(s[i]) - int('0')
		if c < 0 || c > 9 { break }

		result = result*10 + int64(c)

		// bounds checking
		if sign == 1 {
			if result >= math.MaxInt32 { return math.MaxInt32 }
		} else if result >= math.MaxInt32+1 { return math.MinInt32 }
	}

	// return signed result
	return int(result * int64(sign))
}
```
