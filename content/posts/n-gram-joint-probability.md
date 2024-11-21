+++
date = '2019-09-11T18:11:10-05:00'
draft = false
title = 'N-Grams: Joint Probability'
+++
Let's start by examining the simplest case of joint probability with single word probability via a uni-gram. If we want to know the probability of a word, without any context appearing before or after, then we could take a corpus of text and convert it into a dictionary with the key for the word and the count as the value: `{ "a": 1000, "an": 3, "animal": 12, ... }`. Say we want to calculate `P("a")`, meaning the likelihood of "a." We would take the count of occurrences for the word "a" and divide it by the total number of words in the corpus: `P("a") ≈ count("a") / corpus_word_count`. This is called maximum likelihood estimation (MLE) and we use the "≈" sign because our corpus is not a perfect representation of the actual likelihood of the word.

Say we wanted to calculate the probability of "an animal". In this case we would have `P("an animal") ≈ P("an")P("animal")` because the relationship between "an" and "animal" is independent for our model; this is not true for the english language which is why we use the approximately equals sign. With the independence we can now calculate the probability with the chain rule:

```
P("an animal") 
    ≈ P("an")P("animal") 
    = (count("an")/corpus_word_count) * (count("animal")/corpus_word_count)
```

Now that we understand joint probability with uni-grams, we can generalize our knowledge to work with any n-gram where n is an integer and greater than 0. To begin, let's look at the sentence, "An animal dropped from the tree." Say we have a trained bi-gram ready to calculate the likelihood of the sentence. What would it do for the first word? The bi-gram needs to have the word that occurred before "An" to work. One way to get around this problem is build n-grams with tokens at the beginning and end of a sentence, "\<s> An animal dropped from the tree \</s>." Note, if if this was a tri-gram there would be two start of sentence tokens instead of one. In our case, though, we are interested in being able to generate more than one sentence. Instead, we calculate the probability of the first word with a 1-gram, then the second word with a bi-gram, and so on for whatever n. Instead of a bi-gram here is the formulation of how a tri-gram calculates joint probability:

```
P(S) ≈ P(s1)P(s2|s1)P(s3|s1,s2)...P(sn|sn-2,sn-1)
```

If it was a bi-gram the last calculation would be `P(sn|sn-1)`. If it was a quad-gram it would be `P(sn|sn-3,sn-2,sn-1)`. There is, however, a potential problem with this formulation when we move away from theory and towards computation: [underflow](https://en.wikipedia.org/wiki/Arithmetic_underflow). Underflow occurs when the resulting calculation of an operation is a number smaller than the computer can represent. With our current method of joint probability calculation we multiply a bunch of, potentially, small decimals together and could run into underflow. To avoid some of these inaccuracies we can run the calculation in log space, and to do so we need to know the following identity:

```
log(x1*x2*...*xn) = log(x1) + log(x2) + ... + log(xn)
```

This identity tells us that we can take any multiplication and turn it into an addition problem which will reduce the likelihood of encountering extremely small numbers. In addition, [adding is a faster operation than multiplication](https://www.quora.com/Is-addition-more-efficient-than-multiplication-in-programming). With the identity, we can calculate our joint probability by first adding all the individual log probabilities and raising `e` by the result to get a probability of higher accuracy.

\[
\begin{aligned}
P(W) ≈ e ^{log(P(W1)) + log(P(W2|W1)) + ...}
\end{aligned}
\]

In addition to the formulation, I have implemented this on [github](https://github.com/bi3mer/nlp_experiments/blob/master/Models/UnsmoothedNGram.py#L103) and you'll notice that there is an extra check for the probability of zero occurring because zero is undefined for log. However, if one of the probability calculations ends up being zero then we know the resulting probability will be zero.