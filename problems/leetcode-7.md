+++
date = '2026-06-26T09:04:39-05:00'
draft = false
title = 'LeetCode 7: Reverse Integer'
url = '/posts/leetcode-7/'
+++

[LeetCode 7](https://leetcode.com/problems/reverse-integer/description/) asks us to reverse an integer, and we have to assume that the environment doesn't allow us to store a 64-bit integer. Thus, we can't do a simple string conversion solution like:

```python
def lazy_python_reverse(val: int) -> int:
    new_val = int(str(abs(val))[::-1])
    if val < 0:
        new_val = -new_val

    return new_val
```

This solution gets the absolute value of `val` and turns it into a string that is then reversed with `[::-1]` and then the reversed string is turned back into an integer. We need to take the absolute value to get rid of the negative sign since reversing would cause the negative sign to appear on the other side of the string, and then integer conversion would probably fail. (I haven't checked; I assume.) After that, we have the if statement to change new_val to negative if necessary.

Additionally, this lazy python solution is missing one other constraint to work: "If reversing `x` causes the value to go outside the signed 32-bit integer range `[-2^{31}, 2^{31} - 1]`, then return 0." We could add that:

```python
if new_val < -2**31 or new_val > 2**31 - 1:
    return 0
```

But, I don't have much interest in it. The actual solution is to use modulus and division to extract numbers one at a time. Before getting to that, though, how do we handle the constraint of not being able to use a 64-bit number but having to detect overflow? Go's default behavior for this is wrapping, so the language isn't going to help us much.

What we can do is ignore the negative until the very end, and use a `uint32` (unsigned integer). This will be helpful because the max of a `uint32` is `2^{32}`, 2x larger than `2^{31}`. So, we can do the reverse, and if it is too large, then we can `return 0`. Otherwise, we can safely turn the `uint32` into an `int` and then make it negative if necessary before returning it.

```go
func reverse(x int) int {
    var result uint32

    // reverse x into result...

    if x < 0 {
        if result > uint32(math.MaxInt32) + 1 {
            return 0
        }

        return -int(result)
    } else {
        if result > math.MaxInt32 {
            return 0
        }

        return int(result)
    }
}
```

The thresholds differ because the int32 range is asymmetric: `[-2^{31}, 2^{31} - 1]`, so the negative side allows one extra value (`-2,147,483,648`).

That's the memory constraint handled. Now, how do we do the reversing?

```go
result := uint32(0)

var x32 uint32
if x > 0 {
    x32 = uint32(x)
} else {
    x32 = uint32(-x)
}
```

First, we have to turn `x`, an `int`, into a `uint32`. Unfortunately, Go has no `abs` function for integers to do this, so we have to do it ourselves. A bit silly, in my opinion, but I'm sure they have a well thought out reason.

```go
for x32 != 0 {
    result = result * 10 + x32 % 10
    x32 /= 10
}
```

Second, we have to reverse `x32`. We do this with the aforementioned division and modulo. The loop works by removing the lowest digit until `x32` is equal to `0`. The removal happens with `x32 /= 10` (e.g. `132 / 10` removes `2`). The way we get the digit is with the line above. The first part of the equation `result *= 10`, shifts the digits to the left and leaves a `0` in the tens place. That space is filled with `x32 % 10`, which is the last digit of `x32`. Remember, we are reversing the integer.

The problem is that this doesn't have a guard. So if we are reversing `1,534,236,469`, we run into a problem because it turns into `9,646,324,351` which exceeds `uint32`'s max of `4,294,967,295`. The value wraps around, so the overflow check never sees the real number. We need a guard while we convert.

```go
for x32 != 0 {
	digit := x32 % 10
	x32 /= 10

	if result > uint32(math.MaxInt32)/10 {
	    return 0
	}

	result = result * 10 + digit
}

```

Since we bail out in the loop if result would overflow, we no longer need the separate checks at the end:

```go
if x < 0 {
    return -int(result)
}

return int(result)
```

And that is the solution. I kind of broke my rule from [the previous post](/posts/leetcode-5/) where I said that I wouldn't solve the problem the dumb way. However, I did it in a different language so I would have it done quickly, and I did it in a way that ignored the problem's constraints on purpose. So, I think I can slide by with a technicality on this.

My big takeaway from solving this was that I didn't like that Go has no `math.Abs` for integers. I did some googling to see if there was a reason, and it seems that the early version of the language had no generics. Thus, you couldn't have a generic function. However, there is one other problem which is that the absolute value of an integer is trivial, but there is, apparently, a lot of work that goes in to making an efficient float version. However, since there is the `max` operator in Go, we could simplify the initialization of `x32` to `x32 := uint32(max(-x, x))`

Also, this solution beats 100% of submissions in terms of runtime. Granted, never trust LeetCode's reporting on speed, but it still feels good. It occurs to me that the lack of granular reporting may be on purpose. We get a nice little dopamine boost when we solve a problem, and our solution does better than everyone else's.

Till next time, friends.

---

```go
func reverse(x int) int {
    result := uint32(0)
    x32 := uint32(max(-x, x))

    for x32 != 0 {
        digit := x32 % 10
        x32 /= 10

        if result > uint32(math.MaxInt32)/10 {
            return 0
        }

        result = result * 10 + digit
    }

    if x < 0 {
        return -int(result)
    }

    return int(result)
}
```
