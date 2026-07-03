+++
date = '2026-07-03T09:16:27-05:00'
draft = false
title = 'Leetcode 13: Roman to Integer'
url = '/posts/leetcode-13/'
+++

[Today's problem](https://leetcode.com/problems/roman-to-integer/description/) is the inverse of [yesterday's.](/posts/leetcode-12/) It also shares the same constraint: the number we convert from roman to decimal must be between `1` and `3999`, inclusive.

The first thing to do is to create a quick lookup to convert a character in a roman numeral into an integer.

```go
func helper(b byte) int {
    switch b {
        case 'M': return 1000
        case 'D': return 500
        case 'C': return 100
        case 'L': return 50
        case 'X': return 10
        case 'V': return 5
        case 'I': return 1
    }

    return 0 // should return err in idiomatic Go
}
```

Notice that I didn't use [`map`.](https://go.dev/blog/maps) I didn't use them because a `switch` statement is perfectly fine for this kind of problem, and, more importantly, the `map` data structure, while convenient, [is evil.](/posts/leetcode-3/#giving-up-on-being-smart) I'm starting to think that I should write a blog post on my feelings regarding hashmaps in general. Regardless, now that we can convert a roman numeral to an `int`, we can convert the whole string:

```go
func romanToInt(s string) int {
    result := helper(s[0])
    previous := result

    for i := 1; i < len(s); i++ {
        new := helper(s[i])

        if new > previous {
            result = result - 2*previous + new
            previous = 100000
        } else {
            result += new
            previous = new
        }
    }

    return result

}
```

Unfortunately, we can't read left to right adding each roman numeral up, and this is because of numbers like `IV` being `4` instead of `6`. So, we have to keep track of the previous number we read in. If the new number is greater than the previous number, that means we ran into a case like `IV`. So, we subtract `previous` twice and add `new` to the result. We subtract it twice because the previous iteration assumed no subtractive case and already added `previous` to the result. (See the `else` condition.)

I should say that this solution is flimsy. If we wanted to add roman numerals up to `100,000,000`, for example, then we would update our `helper` and then we'd run into an error with `previous = 100000`. So, really, the function should use `previous = math.MaxInt`.

The other problem is that the function assumes a properly formatted roman numeral. If we were writing this to be used in production, we would want to create some kind of roman numeral validator before running the converter. Or, maybe we could validate as part of our converter, but it would complicate the function. If we did it the latter way, we would, without a doubt, change the return type to return an `int` and an `error`.

Regardless, that is the post for the day. Today is the third of July, and I'm not sure if I'll be solving a problem tomorrow since it is a holiday. If not and you are from the states, happy fourth.

Till next time, friends.
