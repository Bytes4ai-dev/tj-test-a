---
title: "2024: MCP arrives"
order: 5
year: "2024"
tag: "Agents"
description: "The Model Context Protocol gave AI applications one standard way to reach tools and data, and quietly widened what an agent can touch."
service: "Build"
heroAlt: "Original illustration: connected nodes around a hub, the Agents motif."
chart:
  alt: "Diagram: without a shared protocol, every AI app needs its own connector to every tool (many crossing lines); with MCP, each app and each tool implements the protocol once (lines meet at one hub)."
  caption: "Diagram of the integration problem MCP was introduced to solve, drawn from Anthropic's announcement."
  sourceUrl: "https://www.anthropic.com/news/model-context-protocol"
sources:
  - title: "Anthropic, Introducing the Model Context Protocol"
    url: "https://www.anthropic.com/news/model-context-protocol"
  - title: "Anthropic, Donating the Model Context Protocol and establishing the Agentic AI Foundation"
    url: "https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation"
  - title: "Model Context Protocol, official site and specification"
    url: "https://modelcontextprotocol.io/"
---

Before late 2024, connecting a model to a tool meant writing a custom integration for each pair: this assistant to that ticket system, that agent to this database. In November, Anthropic [introduced the Model Context Protocol (MCP)](https://www.anthropic.com/news/model-context-protocol) as an open standard for connecting AI applications to data sources and tools.

The idea is ordinary in the best way. A tool exposes an MCP server once; any MCP-capable client can use it. The diagram below shows why that matters: one shared protocol in place of a web of one-off connectors. The [specification and SDKs](https://modelcontextprotocol.io/) are public.

Adoption came fast. By December 2025, Anthropic reported [more than 10,000 active public MCP servers and 97M+ monthly SDK downloads](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation), and donated the protocol to the Agentic AI Foundation under the Linux Foundation, co-founded with Block and OpenAI [[2]](#source-2).

For anyone building agents, MCP made the hard part easy: an agent could now reach a calendar, a code host, a database and a file store in an afternoon. That is also the governance problem. Each server is a new set of permissions, often running with a person's own tokens, and an agent that can call ten tools can be talked into misusing any of them.

The protocol is a plug, not a policy. Who may connect which server, with which scopes, and how calls are logged, are still decisions you have to make.

## What to do about it

Before connecting MCP servers to anything real, list them, give each one its own narrowly scoped credential, and log every tool call. Our **Build** service designs AI and agent systems with evaluations and these controls in from the start. [See Build](/#services).
