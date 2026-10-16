---
title: "2024: Reasoning models change how we evaluate AI"
order: 4
year: "2024"
tag: "Observability"
description: "Models that think before they answer jumped on hard maths and puzzle benchmarks, and made the cost and method of each test part of the result."
service: "Build"
heroAlt: "Original illustration: a pulse line rising over a measurement grid, the Observability motif."
chart:
  alt: "Bar chart of AIME 2024 accuracy: GPT-4o 12%, o1 single sample 74%, o1 consensus of 64 samples 83%, o1 re-ranking 1000 samples 93%."
  caption: "AIME 2024 accuracy reported by OpenAI for GPT-4o and o1 under different sampling methods."
  sourceUrl: "https://openai.com/index/learning-to-reason-with-llms/"
sources:
  - title: "OpenAI, Learning to reason with LLMs"
    url: "https://openai.com/index/learning-to-reason-with-llms/"
  - title: "OpenAI o1 System Card (arXiv 2412.16720)"
    url: "https://arxiv.org/abs/2412.16720"
  - title: "ARC Prize, OpenAI o3 breakthrough high score on ARC-AGI-Pub"
    url: "https://arcprize.org/blog/oai-o3-pub-breakthrough"
---

In September 2024 OpenAI introduced o1, a model trained to work through a problem step by step before answering, documented in its [o1 system card](https://arxiv.org/abs/2412.16720). The headline was not a better chat reply. It was a different kind of score.

On the AIME 2024 maths exam, OpenAI reported that [GPT-4o solved about 12% of problems, while o1 reached 74% with one sample, 83% with a consensus of 64 samples and 93% when re-ranking 1,000 samples](https://openai.com/index/learning-to-reason-with-llms/) [[1]](#source-1).

Read that list again and the evaluation problem is plain: the same model has four different scores depending on how much compute you spend at answer time. In December, ARC Prize reported that OpenAI's o3 scored [75.7% on the ARC-AGI-1 semi-private set within its compute limit, and 87.5% in a configuration using 172 times more compute](https://arcprize.org/blog/oai-o3-pub-breakthrough), with a retail cost per task in the thousands of dollars for the high-compute run.

So a benchmark number without its method stopped meaning much. Teams evaluating reasoning models had to record the sampling setup, the token budget, the latency and the cost per task next to the accuracy, and to check whether a gain on public puzzles carried over to their own work [[1]](#source-1) [[3]](#source-3).

It also moved evaluation from a one-off to a habit. When the model can spend more or less effort per question, quality becomes something you watch in production, not a launch checklist.

## What to do about it

Write your evaluations before you pick the model: a fixed set of your own cases, with accuracy, cost per task and latency recorded together, run on every model or setting change. Our **Build** service writes the evaluations first, then builds the AI system that passes them. [See Build](/#services).
