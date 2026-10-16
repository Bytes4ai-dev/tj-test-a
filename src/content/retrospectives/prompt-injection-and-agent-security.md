---
title: "2025: Prompt injection and agent security become real"
order: 8
year: "2025"
tag: "Governance"
description: "Prompt injection moved from a research curiosity to real vulnerabilities in shipping products once agents could read untrusted content and act on it."
service: "Govern"
heroAlt: "Original illustration: concentric rings with one ring broken open, the Governance motif."
chart:
  alt: "Diagram of the lethal trifecta: three overlapping circles labelled access to private data, exposure to untrusted content, and ability to communicate externally; the overlap is marked as the danger zone."
  caption: "Diagram of the \"lethal trifecta\" for AI agents as described by Simon Willison."
  sourceUrl: "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/"
sources:
  - title: "OWASP Gen AI Security Project, LLM01:2025 Prompt Injection"
    url: "https://genai.owasp.org/llmrisk/llm01-prompt-injection/"
  - title: "Simon Willison, The lethal trifecta for AI agents (16 June 2025)"
    url: "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/"
  - title: "CVE-2025-32711, M365 Copilot Information Disclosure Vulnerability (CVE record)"
    url: "https://www.cve.org/CVERecord?id=CVE-2025-32711"
---

A language model cannot reliably tell the difference between instructions from its user and instructions hidden in the text it reads. That is prompt injection, and the OWASP project put it at the top of its list: [LLM01 in the Top 10 for LLM Applications 2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).

While models only chatted, the damage was limited. In 2025 agents started reading email, web pages, tickets and documents, and acting on them. Simon Willison gave the risk a clear shape with ["the lethal trifecta"](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/): an agent that has access to private data, is exposed to untrusted content, and can communicate externally can be tricked into sending your data to an attacker.

Real products hit exactly that pattern. Microsoft assigned [CVE-2025-32711](https://www.cve.org/CVERecord?id=CVE-2025-32711), described as AI command injection in Microsoft 365 Copilot that allowed an unauthorized attacker to disclose information over a network, with a CVSS score of 9.3 [[3]](#source-3).

The uncomfortable lesson of the year: there is no filter that makes injection go away. The defences that work are structural. Remove one leg of the trifecta for each workflow, give the agent the narrowest credentials that do the job, require a human confirmation before sensitive actions, and log every tool call so you can see what happened.

Security moved from the model to the system around it.

## What to do about it

For each agent, write down which legs of the trifecta it has, and remove one. Then scope its credentials and log its actions. Our **Govern** service puts tested stop controls, audit trails and scoped credentials around your agents. [See Govern](/#services).
