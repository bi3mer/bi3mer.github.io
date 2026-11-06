+++
date = '2026-07-12T10:07:42-05:00'
draft = false
title = 'LeetCode 121: Best Time to Buy and Sell'
url = '/posts/leetcode-121/'
+++

Welcome back. I missed a post yesterday, but I'm back to solve [LeetCode 121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/?envType=problem-list-v2&envId=dynamic-programming). The idea is that given an input slice of integers, which represents the prices of a stock, we want to choose one day to buy and one day to sell such that we get the maximum profit. The return value is the max profit found.

```
Example 1:
  Input: prices = [7,1,5,3,6,4]
  Output: 5
  Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.

Example 2:
  Input: prices = [7,6,4,3,1]
  Output: 0
  Explanation: No transactions possible without losing money, so 0
```

The solution isn't difficult if we are being lazy:

```go
func maxProfit(prices []int) int {
    profit := 0

    for i := 0; i < len(prices); i++ {
        for j := i + 1; j < len(prices); j++ {
            profit = max(profit, prices[j] - prices[i])
        }
    }

    return profit
}
```

We loop through the slice twice, giving an algorithm that is \(O(n^2)\). Unsurprisingly, this solution fails for a slice with a ton of elements. Specifically, the problem has the following constraint: \(0 <= len(prices) <= 10^5\). If \(n=10^5\), I think you can figure out how squaring that would be a problem. The way to speed it up is to avoid the second loop.

```go
func maxProfit(prices []int) int {
    minPrice := math.MaxInt
    maxProfit := 0

    for _, p := range prices {
        if p < minPrice {
            minPrice = p
        } else  {
            maxProfit = max(maxProfit, p - minPrice)
        }
    }

    return maxProfit
}
```

We do one of two things while looping through `prices`. In the first case, the current element in the loop is less than the minimum price that we have found. If that is the case, profit is impossible. However, it is the best possible point so far to buy. So we store it for future use and continue the loop. In the second case, `p < minPrice` evaluates to false, and then we test if `p` minus the minimum price found is greater than the profit found so far. If so, we update the max profit found. And that's it. Because the whole problem is linear, we don't need to test every possible profit like we did in the first version. We just need to test the best possible linear profits, bringing us down to an algorithm with a runtime complexity of \(O(n)\).

Till next time, friends.
