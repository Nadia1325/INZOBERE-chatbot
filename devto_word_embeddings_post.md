---
title: "I Gave My FAQ Chatbot Word Embeddings. It Got Smarter, but Not the Way I Expected"
published: false
description: "What word embeddings are, how GloVe works, and what happened when I added them to a TF-IDF chatbot."
tags: nlp, machinelearning, python
---

My first NLP project was a small FAQ chatbot. You type a question, and it finds the closest of 100 stored questions using TF-IDF. It worked well when I used the same words as the FAQ. Then I typed "how to check model correctness" and it gave me a wrong answer, because the FAQ says "accuracy", not "correctness".

That one failure is the reason word embeddings exist. In this post I explain what they are, how GloVe learns them, and what happened when I added them to my chatbot.

## What is a word embedding?

A computer cannot read words, only numbers. The old way is to give every word its own position in a huge list (bag of words) and count them. In that world, "accuracy" and "correctness" are two unrelated columns. The computer has no idea they are close in meaning.

A word embedding gives every word a short list of numbers, called a vector. In my project, each word has 100 numbers. The important part: words used in similar ways get similar numbers. So "good" and "great" end up close together, and "good" and "banana" end up far apart.

The idea comes from a simple sentence: *you know a word by the company it keeps.* Words that appear next to the same neighbours probably have similar meaning.

## How GloVe works, in simple words

I used GloVe (Global Vectors), made at Stanford by Pennington, Socher and Manning. Here is the high-level idea:

1. Read a huge amount of text (Wikipedia and news for the version I used).
2. Count how often each pair of words appears near each other.
3. Learn vectors so that the numbers of two words can predict how often they appear together.

Word2Vec, which came before, learns in a similar spirit but by playing a prediction game: guess a word from its neighbours (or the neighbours from a word). GloVe uses the whole count table at once. Both give vectors where meaning turns into geometry.

## What the vectors can do

I loaded the vectors with `gensim`:

```python
import gensim.downloader as api
g = api.load("glove-wiki-gigaword-100")

g.similarity("good", "great")     # 0.76
g.similarity("good", "banana")    # 0.20
g.most_similar(positive=["king", "woman"], negative=["man"], topn=1)
# [('queen', 0.77)]
g.most_similar(positive=["paris", "rwanda"], negative=["france"], topn=1)
# [('kigali', 0.80)]
```

The second analogy was my favourite: take Paris, remove France, add Rwanda, and the closest word is Kigali. Nobody told the model what a capital city is. It only read text.

I also shrank 25 words to two dimensions with PCA. Royal words, capital cities and NLP words formed their own groups. To my surprise, "sentiment" landed near the country names. My guess is that in news text, "sentiment" often appears in finance stories about markets and countries. The vectors reflect the text they learned from, including its habits.

## Adding embeddings to my chatbot

I turned every FAQ entry and every user question into one vector: the average of its word vectors, with rare words counting more. Then I compared them with cosine similarity, exactly as before, but now the numbers carry meaning.

I wrote 40 test questions that use different words from the stored ones, like "program that chats with users" for "What is a chatbot?". Then I measured three versions:

| Model | Top-1 | Top-3 | MRR |
|---|---|---|---|
| TF-IDF only | 57.5% | 70.0% | 0.676 |
| Embeddings only | 40.0% | 55.0% | 0.511 |
| Hybrid (half and half) | 60.0% | 82.5% | 0.731 |

## What surprised me

**Embeddings alone were worse.** I expected them to win. They lost to plain TF-IDF by a lot. My explanation: averaging word vectors blurs the meaning, and all my 100 questions are about NLP, so they already look alike. A word like "model" appears everywhere and pulls many questions together.

**The best result came from combining both.** TF-IDF is precise when words match. Embeddings help when they do not. They make mistakes on different questions, so together they are stronger. The biggest gain was in top-3 accuracy: the right answer was in the bot's first three suggestions 82.5% of the time, up from 70%. Top-1 improved by only one question out of 40, so I do not want to oversell it.

**"chatbot" is not in GloVe.** The vocabulary is fixed, so a word it never saw simply has no vector. That is why people use FastText, which builds vectors from pieces of words.

## What I struggled with

Testing honestly. It is tempting to tune your settings on the same questions you use to report results, which flatters the numbers. So I split the questions in half, chose my settings on one half, and measured on the other. The gain became smaller but more believable. My test set is also small, so one or two questions can change a percentage.

I also learned that a similarity score is not a confidence score. My bot still answers off-topic questions like "what is the weather" with something from the FAQ, because embedding scores do not clearly separate "in scope" from "out of scope".

## What I would do next

- Try FastText for unknown words.
- Add examples of out-of-scope questions to teach the bot when to say "I do not know".
- Try sentence embeddings, which are made for whole sentences instead of averaging words.

## Takeaway

Embeddings are not magic that replaces the old methods. They add a sense of meaning, and they work best next to methods that are precise about exact words. If you have a TF-IDF project, adding embeddings is a small change with a real lesson inside.

The full code, test set and results are in my repository: *(add your repository link here)*

## Sources

- Pennington, J., Socher, R., Manning, C. (2014). *GloVe: Global Vectors for Word Representation.* https://nlp.stanford.edu/projects/glove/
- Mikolov, T. et al. (2013). *Efficient Estimation of Word Representations in Vector Space* (Word2Vec).
- gensim library: https://radimrehurek.com/gensim/

<!-- Drag results/embedding_space_pca.png into the editor here, under the PCA paragraph -->
