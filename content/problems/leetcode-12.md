+++
date = '2026-07-02T08:00:56-05:00'
draft = false
title = 'LeetCode 12: Integer to Roman'
url = '/posts/leetcode-12/'
+++

[LeetCode 12](https://leetcode.com/problems/integer-to-roman/description/) asks us to take an integer and convert it to a roman numeral representation. Here are some examples:

```
Example 1:
  Input: num = 3749
  Output: "MMMDCCXLIX"

Example 2:
  Input: num = 58
  Output: "LVIII"

Example 3:
  Input: num = 1994
  Output: "MCMXCIV"
```

They also provide a table, which is helpful:

| Symbol | Value |
| ------ | ----- |
| I      | 1     |
| V      | 5     |
| X      | 10    |
| L      | 50    |
| C      | 100   |
| D      | 500   |
| M      | 1000  |

So, how can we do this?

The first thing to do is to check if we'll have to handle giant numbers, but the one and only constraint is: `1 <= num <= 3999`. So no input number will be `>= 4000`. Given that, things are already simpler, but we do have to worry about how to handle numbers like `4` and `9`. These numbers are represented in roman numerals with `IV` and `IX` instead of the more intuitive `IIII` and `VIIII`. This same pattern will repeat itself for every one of the symbols above.

Now, we could handle this with some if statements, but hear me out. Today is my birthday, and I don't feel like doing anything that intense. (It actually isn't my birthday, I wrote this the day before.) So, instead of figuring out the algorithm way, we can do the "data" way which takes advantage of the constraint: `1 <= num <= 3999`.

```go
var (
    M = []string{"", "M", "MM", "MMM"}
    C = []string{"", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"}
    X = []string{"", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"}
    I = []string{"", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"}
)

func intToRoman(num int) string {
    return M[num/1000] + C[(num%1000) / 100] + X[(num%100)/10] + I[num%10]
}
```

Each index pulls out one digit of `num`, then looks up the roman symbol for that digit at that place value. `num/1000` gets the thousands digit (0-3, since `num <= 3999`), indexing into `M`. `(num%1000)/100` strips the thousands with `%1000`, then divides by `100` to get the hundreds digit (0-9), indexing into `C`. `(num%100)/10` strips everything above the tens with `%100`, then divides by 10 to get the tens digit, indexing into `X`. `num%10` just grabs the ones digit directly, indexing into `I`. Concatenating the four together gives the full roman numeral.

And that's problem 12 done. It beat 100% of submissions in terms of runtime, and the code is nice and simple. Can't not be happy about that. If it's anybody's birthday today as well, happy birthday!

Till next time, friends.
