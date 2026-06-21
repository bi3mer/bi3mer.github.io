+++
date = '2026-06-16T09:24:41-05:00'
draft = false
title = 'Leetcode 30'
url = '/posts/leetcode-30/'
+++

We are finally back to a <span style="color:red">HARD</span> problem with [LeetCode 30.](https://leetcode.com/problems/substring-with-concatenation-of-all-words/description/) As input, we get one string and one array of strings. The expected output is an array of indices.

```
Example 1:
  Input: s = "barfoothefoobarman", words = ["foo","bar"]
  Output: [0,9]

Example 2:
  Input: s = "wordgoodgoodgoodbestword", words = ["word","good","best","word"]
  Output: []

Example 3:
  Input: s = "barfoofoobarthefoobarman", words = ["bar","foo","the"]
  Output: [6,9,12]
```

The output array is expected to have indices into `s`. Looking at Example 1, there are two indices: 0 and 9:

```
barfoothefoobarman
|        |
0        9
```

Index 0 points to the start of the string "barfoo" and index 9 points to the start of "foobar". I know this because of the words for Example 1: `["foo", "bar"]`. So, what the problem wants us to do is find indexes into `s` where it contains a permutation of the concatenation of all the strings in `words`. So looking at Example 3, we can see that `words` has three different strings, which gives us more than two permutations like in Example 1:

- "barfoothe"
- "barthefoo"
- "foobarthe"
- "foothebar"
- "thebarfoo"
- "thefoobar"

And we also get these constraints:

- All the strings of `words` are of the same length.
- `1 <= s.length <= 10^4`
- `1 <= words.length <= 5000`
- `1 <= words[i].length <= 30`
- `s` and `words[i]` consist of lowercase English letters.

# Solution 1: Permutation Finder

```go
func generatePermutations(words []string, current string, output *[]string) {
    if len(words) == 0 {
        *output = append(*output, current)
        return
    }

    n := len(words) - 1
    for i, w := range words {
        words[i], words[n] = words[n], words[i]
        generatePermutations(words[:n], current + w, output)
        words[i], words[n] = words[n], words[i]
    }
}

func findSubstring(s string, words []string) []int {
    var permutations []string
    generatePermutations(words, "", &permutations)

    var output []int
    if len(permutations) == 0 {
        return output
    }

    len_p := len(permutations[0])
    n := len(s) - len_p

    for i := 0; i <= n; i++ {
        for _, p := range permutations {
            if s[i:i+len_p] == p {
                output = append(output, i)
                break
            }
        }
    }

    return output
}
```

This was my idea of what I thought a lazy solution would look like. `generatePermutations` generates every possible permutation of the `words` slice, and then we can do lazy loop through `s` and check at every index whether a permutation exists for the given substring. The problem, though, is that the complexity blows up when we are generating permutations for:

```
words = ["a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a"]
```

`words` has 20 elements, meaning 20! (factorial) permutations. That means that `generatePermutations` is trying to generate an array of 2.432902e+18 strings.

So, this doesn't work.

# Solution 2: In-Place Permutations

```go
func checkSubString(s string, words []string) bool {
    if len(words) == 0 {
        return true
    }

    n := len(words) - 1
    for i, w := range words {
        if s[:len(w)] == w {
            words[i], words[n] = words[n], words[i]
            validSubstring := checkSubString(s[len(w):], words[:n])
            words[i], words[n] = words[n], words[i]

            if validSubstring {
                return true
            }
        }
    }

    return false
}

func findSubstring(s string, words []string) []int {
    var output []int
    if len(words) == 0 {
        return output
    }

    minLength := 0
    for _, w := range words {
        minLength += len(w)
    }

    for i := 0; i <= len(s) - minLength; i++ {
        if checkSubString(s[i:i+minLength], words) {
            output = append(output, i)
        }
    }

    return output
}
```

This Solution is very similar to Solution 1. However, it doesn't try to create all the valid permutations at once. Instead, it does a kind of recursive tree-search through the valid permutations when it checks substrings with `checkSubstring`.

This also fails.

```
s="ababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababab"
words=["ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba","ab","ba"]
```

The failure is due to this solution taking too long on the input above. The reason why is that this input was designed to ensure that any permutation approach will fail. So, good on whoever created this problem.

# Solution 3: Frequency Map

```go
func findSubstring(s string, words []string) []int {
    var output []int
    if len(words) == 0 {
        return output
    }

    wordFrequency := make(map[string]int)
    for _, w := range words {
        wordFrequency[w]++
    }

    freq := make(map[string]int)
    wordLength := len(words[0])
    subStrLength := wordLength * len(words)

    for i := 0; i <= len(s) - subStrLength; i++ {
        for j := i; j < i + subStrLength; j += wordLength{
            freq[s[j:j+wordLength]]++
        }

        // check if freq and wordFrequency are the same
        equal := true
        for _, w := range words {
            if freq[w] != wordFrequency[w] {
                equal = false
            }
        }

        if equal {
            output = append(output, i)
        }

        clear(freq) // empty for future use
    }
    return output
}
```

This solution takes advantage of the constraint, "All the strings of `words` are of the same length." What this allows us to do is build a frequency map, which is to say, "How often does substring X occur?" We can build that for the `words` array as well as for every substring in `s`, and then we compare said frequency maps. If the maps are the same, awesome. We found a valid index. If not, we move on. This lets us avoid all the permutation nonsense, and, instead, build a map and compare. Way faster.

Even better, this solution passes. Unfortunately, though, this solution is not the fastest, beating only 23% of submissions in terms of run time. This despite me going out of my way to avoid extra allocations by only allocating two `map` data structures.

So, one more solution and we're done.

# Solution 4: Sliding Window

```go { linenos=true }
func findSubstring(s string, words []string) []int {
    var output []int
    if len(words) == 0 {
        return output
    }

    wordLength := len(words[0])
    wordCount := len(words)
    wordFrequency := make(map[string]int)

    for _, w := range words {
        wordFrequency[w]++
    }

    freq := make(map[string]int)
    for offset := 0; offset < wordLength; offset++ {
        count := 0
        left := offset

        for right := offset; right+wordLength <= len(s); right += wordLength {
            word := s[right : right+wordLength]
            if _, exists := wordFrequency[word]; !exists {
                clear(freq)
                count = 0
                left = right + wordLength
                continue
            }

            freq[word]++
            count++

            for freq[word] > wordFrequency[word] {
                freq[s[left:left+wordLength]]--
                count--
                left += wordLength
            }

            if count == wordCount {
                output = append(output, left)
                freq[s[left:left+wordLength]]--
                count--
                left += wordLength
            }
        }

        clear(freq)
    }

    return output
}
```

This solution is, unfortunately, much more complicated than the prior ones, and, as a result, is not an easy read. Before getting into the exact details, I think a higher level picture may be helpful.

The core idea is to avoid as much computation as possible. The previous Solution looped through almost every character in `s`, and for each one it generated a whole frequency map. So, when we are talking about making an algorithm go faster, look for the pain points.

Can we skip characters in `s`? I don't think so.

Can we skip scanning the whole substring at index `i` when we build a new frequency map? We can. If we come across a word not in the frequency map built from `words`, we can just stop. That is the first optimization, and it occurs on line 22-27.

Can we avoid rebuilding the frequency map? This is more difficult, but the answer is also, mostly, yes. I say mostly because we do clear the frequency map on lines 23 and 46. But, we can still avoid the majority of clears when we slide the frequency map around `s`. Meaning, we are going to use a sliding window.

When `right` (line 20) advances by one word, we add that word to `freq`. When a word appears too many times, we shrink from the `left`, removing words one at a time until the counts are valid again. This means each word is added at most once and removed at most once per offset, rather than being reprocessed from scratch at every position.

The final piece is the outer offset loop, which runs `wordLength` times. Once for each distinct alignment. Since all words have the same length, every valid starting index is congruent to one of the `wordLength` offsets mod `wordLength`. So instead of restricting which positions we look at, the offset loop partitions all positions into `wordLength` alignment classes, and each class gets swept by a single sliding window. We still examine every position in `s`, but we group them so that one window can slide across an entire class without ever rebuilding from scratch.

The runtime for this beats somwhere between 95% and 100% of submissions, depending on the run. The memory seems to be consistently near beating 95% and 98% of submissions. So, this is about as good as it gets.

# Conclusion

No benchmarks this time. Getting to the final sliding window solution from permutations took long for me to think about, code, and then write up. However, despite that, I really enjoyed working on this problem. There was a lot of meat to it, and it felt like the beginnings of an unadorned [Advent of Code](https://adventofcode.com/) problem.

Still, I'm not in love with this solution. I think that I'll come back to it at some point. The `clear(freq)` on line 46 feels off to me. I think I can avoid it, but I'd have to spend more time with how to work around it. But, I'll do that another day, maybe. I also think that the explanation for the final solution is a bit weak, so apologies if it wasn't helpful. I'll try again on another day, maybe.

Till next time, friend.
