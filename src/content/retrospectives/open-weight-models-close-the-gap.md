---
title: "2024: Open-weight models close the gap"
order: 2
year: "2024"
tag: "Engineering"
description: "In one year the distance between the best open-weight and the best closed models shrank to a few points, and model choice became an engineering decision."
service: "Assess"
heroAlt: "Original illustration: stacked blocks of two heights converging, the Engineering motif."
chart:
  alt: "Bar chart: performance gap between top closed and top open-weight models fell from about 8% to 1.7% in one year."
  caption: "Gap between the leading closed and open-weight models on a public benchmark, early 2024 vs early 2025, as reported in the AI Index."
  sourceUrl: "https://hai.stanford.edu/ai-index/2025-ai-index-report"
sources:
  - title: "Stanford HAI, AI Index Report 2025"
    url: "https://hai.stanford.edu/ai-index/2025-ai-index-report"
  - title: "Meta, Introducing Llama 3.1: Our most capable models to date"
    url: "https://ai.meta.com/blog/meta-llama-3-1/"
  - title: "DeepSeek-AI, DeepSeek-V3 Technical Report (arXiv 2412.19437)"
    url: "https://arxiv.org/abs/2412.19437"
---

At the start of 2024 the safe assumption was simple: if you wanted the best model, you rented it from a closed provider. By the end of the year that assumption no longer held.

In July, Meta released [Llama 3.1, including a 405B-parameter model trained on more than 15 trillion tokens](https://ai.meta.com/blog/meta-llama-3-1/), and described it as competitive with leading closed models. In December, DeepSeek published [DeepSeek-V3](https://arxiv.org/abs/2412.19437), reporting performance comparable to leading closed models for 2.788M H800 GPU hours of training.

The numbers that summed up the year came later. Stanford's AI Index 2025 reported that [open-weight models cut their performance gap with closed models from 8% to 1.7% on some benchmarks in a single year](https://hai.stanford.edu/ai-index/2025-ai-index-report) [[1]](#source-1).

For engineering teams this changed the question. It was no longer "which vendor is smartest" but "where must this model run, what may it see, and what will it cost at our volume". Open weights made it possible to run a capable model inside your own network, pin a version, and test it the same way every time. They also moved work onto your team: serving, patching, licence review and safety tuning are now yours.

A small benchmark gap is not the same as no gap on your task. The only number that matters is how a model does on your own data and your own failure cases [[1]](#source-1).

## What to do about it

Pick models with evidence, not headlines: write down the constraints (data residency, cost per task, latency, licence), test two or three candidates on your own cases, and keep the test so you can re-run it when the next model ships. Our **Assess** service maps the agents and models you run and where the risk sits. [See Assess](/#services).
