---
title: "2024: RAG goes mainstream"
order: 1
year: "2024"
tag: "Data and people"
description: "Retrieval-augmented generation became the default way enterprises put their own data in front of a model, and retrieval quality became the real work."
service: "Modernize"
heroAlt: "Original illustration: a grid of dots, a few of them highlighted and drawn into a single column, the Data and people motif."
chart:
  alt: "Bar chart: RAG used in 31% of enterprise AI implementations in 2023 and 51% in 2024."
  caption: "Share of enterprise generative AI implementations using retrieval-augmented generation, 2023 vs 2024 (vendor survey)."
  sourceUrl: "https://menlovc.com/2024-the-state-of-generative-ai-in-the-enterprise/"
sources:
  - title: "Menlo Ventures, 2024: The State of Generative AI in the Enterprise"
    url: "https://menlovc.com/2024-the-state-of-generative-ai-in-the-enterprise/"
  - title: "Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (arXiv 2005.11401)"
    url: "https://arxiv.org/abs/2005.11401"
  - title: "Microsoft Research, GraphRAG: Unlocking LLM discovery on narrative private data"
    url: "https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/"
  - title: "Anthropic, Introducing Contextual Retrieval"
    url: "https://www.anthropic.com/news/contextual-retrieval"
---

By 2024 most teams had learned the same lesson the hard way: a general model does not know your contracts, your runbooks or last quarter's numbers. The fix that won was not training a new model. It was retrieval: find the right passages in your own data, put them in the prompt, and ask the model to answer from them.

The idea was not new. The term comes from a [2020 research paper by Lewis and colleagues](https://arxiv.org/abs/2005.11401) that paired a retriever with a generator. What changed in 2024 was scale of adoption. Menlo Ventures' enterprise survey found RAG in [51% of enterprise AI implementations, up from 31% the year before](https://menlovc.com/2024-the-state-of-generative-ai-in-the-enterprise/), while fine-tuning stayed rare [[1]](#source-1).

The year also showed that "add a vector database" was the start, not the end. Microsoft Research published [GraphRAG](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/), which builds a knowledge graph from the documents so the model can answer questions about whole collections, not just single passages. Anthropic's [Contextual Retrieval write-up](https://www.anthropic.com/news/contextual-retrieval) reported that adding context to each chunk before indexing cut failed retrievals by 49%, and by 67% with reranking, on its own tests.

The common thread: answer quality was mostly decided before the model saw anything. Chunking, metadata, access rules and freshness of the source data mattered more than the choice of model. RAG turned AI projects back into data projects, with all the old questions about ownership, quality and who may see what.

That last question is the one that bites later. A retrieval layer that ignores document permissions will happily hand a model text the user was never allowed to read.

## What to do about it

Treat your retrieval layer as a data platform, not a demo: measure retrieval quality on your own questions, carry document permissions into the index, and keep sources fresh. Our **Modernize** service rebuilds data platforms so analytics and AI share one trusted base. [See Modernize](/#services).
