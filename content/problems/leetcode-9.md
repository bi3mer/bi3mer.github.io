+++
date = '2026-06-28T10:08:11-05:00'
draft = false
math = true
title = 'Leetcode 9: Palindrome Number'
url = '/posts/leetcode-9/'

+++

[LeetCode 9](https://leetcode.com/problems/palindrome-number/description/) asks us to implement a function that says whether an `int` is a palindrome or not. As a reminder, a palindrome is, in this context, a sequence of digits that can be read backwards or forwards exactly the same, like `121`.

The easy solution is to convert the number into a string, and then use the `isPalindrome` function we wrote for [LeetCode 5:](/posts/leetcode-5/)

```go
func isPalindrome(x int) bool {
    if x < 0 {
        return false // any negative number cannot be a palindrome
    }

    s := strconv.Itoa(x)
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

There is a follow up for this problem: "Follow up: Could you solve it without converting the integer to a string?" And the answer is: yes. The way we can do it is to reverse the input number and then do an integer comparison. That leaves the question, how do we reverse an integer? Lucky for us, we already did that when we solved [LeetCode 7.](/posts/leetcode-7/)

```go
// LeetCode 7
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

// LeetCode 9
func isPalindrome(x int) bool {
    if x < 0 {
        return false
    }

    return x == reverse(x)
}
```

This isn't the only solution. There is one other that I want to code up.

```go
func palindromeHelper(x, digits int) bool {
    if digits <= 1 {
        return true
    }

    divisor := int(math.Pow(10, float64(digits-1)))
    first := x / divisor
    end := x % 10

    return end == first && palindromeHelper((x%divisor)/10, digits-2)
}

func isPalindrome(x int) bool {
    if x < 0 {
        return false
    }

    if x < 10 {
        return true
    }

    digits := int(math.Floor(math.Log10(float64(x)))) + 1
    return palindromeHelper(x, digits)
}
```

Let's start with `isPalindrome`. This function is the entry point and has two case checks: (1) negative numbers can't be palindromes and (2) single digit numbers are palindromes. Then, it uses log base ten to calculate the number of digits. The only "trick" here is to take the floor of the result and then add one. As an example, \(\log*{10}(100) = 2.0\) and \(\log*{10}(9999) = 3.99999\). This is proof by example which is inherently not a proof. However, I have neither the skills nor the time to write an actual proof for it. So please either take my examples as proof, find a proof online, or make the proof yourself as an exercise.

Right, now we can look at `palindromeHelper`. It takes as an argument `x` which was the input and `digits` which is the number of digits that `x` has---we calculated this just before with the \(\log\_{10}\) trick. The function first checks how many digits are left. If less than or equal to 1, then return true. Because this solution is recursive (it doesn't have to be), this less than or equal to check acts as our base case.

After the base case, we calculate `divisor`. This number is calculated with \(10^{digits - 1}\). So, it starts large and gets small, mimicking the palindrome check from the outside of the number to the inside. The divisor is then used to get the first digit in the check via division and to get the last digit via a modulus operation. As an example, imagine we are working with the number `1221`:

```
palindromeHelper(1221, 4):
  divisor := 10^3 = 1000
  first := 1221 / 1000 = 1
  end := 1221 % 10 = 1

  return 1 == 1 && palindromeHelper((1221 % 1000)/10, 4 - 2)
  return true && palindromeHelper(221 / 10, 2)
  return true && palindromeHelper(22, 2)
  return true && true
  return true

palindromeHelper(22, 2):
  divisor := 10^1 = 10
  first := 22 / 10 = 2
  end := 22 % 10 = 2

  return 2 == 2 && palindromeHelper(_, 0) // base case of <= 1 evaluates to true
  return true && true
  return true
```

Anyways, this is where I'm going to call it. I hope this post was helpful.

Till next time, friends.
