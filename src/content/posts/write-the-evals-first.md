---
title: "Write the Evals First"
date: 2026-09-24
tags: [evals, engineering, ai]
excerpt: "Teams that build AI features should write their evals before they ship, not after something breaks."
draft: false
---

*This is an engineering piece. It argues for one habit.*

Here is the idea, stated plainly: if you build a feature on top of a language model, write the evals before you ship it. Not after the first complaint. Not once the feature is popular. Before.

An eval is a test for behaviour that is not fully deterministic. It asks a simple question of your system: given this input, is the output acceptable? Without that question written down, you are not engineering the feature. You are hoping about it.

## What breaks without evals

**Silent regressions.** An LLM feature depends on more moving parts than it appears to. The prompt, the model behind it, and the sources it retrieves from can each change on their own. Imagine a prompt edit that makes answers friendlier and, without anyone noticing, makes them less accurate on edge cases. Nothing crashes. No alert fires. The regression is silent, and it stays silent until a user finds it.

**Confident wrong answers.** A model can be wrong without saying so, and when it is wrong, it can be wrong fluently. A traditional bug can announce itself with an error. A wrong answer from a model looks exactly like a right one, which means you cannot rely on the output to tell you something went wrong.

**No way to tell better from worse.** Suppose you switch to a newer model because it is supposed to be stronger. Is your feature better now? Without evals, the honest answer is that you do not know. You have opinions, a few examples you tried by hand, and a feeling. That is not enough to decide whether a change helped or hurt.

## What a practical eval loop looks like

An eval loop does not need to be elaborate to be useful. It needs to exist before release, and it needs to run every time something changes.

- **A small, curated golden set.** Start with real cases: inputs your system must handle, with the outcomes you expect. Keep it small enough that someone can read every case and agree each one belongs there. Curation matters more than size.
- **Regression evals on every change.** Any change to a prompt or a model runs the golden set before it ships. If the results get worse, the change waits. This is the same discipline as running unit tests before a merge, applied to behaviour instead of functions.
- **Grounded citations for RAG.** When an answer cites a retrieved source, check that the source actually supports the answer. A citation that points at a document which says something else is worse than no citation, because it borrows trust it has not earned.
- **Routing with deterministic fallbacks.** If you route requests between models or paths, give each route a deterministic fallback for when things go wrong, and evaluate every path, including the fallback. A fallback that has never been tested is not a safety net. It is a guess.
- **Production traffic back into the set.** Sample real requests, with appropriate care for privacy, and feed the interesting ones back into the eval set. The golden set should grow toward what users actually ask, not stay frozen at what you imagined they would ask.
- **A human reads the failures.** Automated scoring tells you something failed. A person reading the failure tells you why. Keep a human in the loop for the cases that fail, and let what they learn shape the next change.

None of this depends on a particular tool. Your eval harness can be a simple script that runs the golden set and prints the failures. What matters is that it runs, and that a release depends on it.

## Why first, and not later

It is tempting to treat evals as something to add once a feature has proven itself. That order is backwards. Writing evals first forces you to say what good looks like before you build. It turns vague goals into concrete cases. It gives every future change a baseline to be measured against, instead of a memory of how things used to feel.

Evals written after launch risk describing whatever the system already does. Evals written first describe what the system should do. Only the second kind can tell you when you are wrong.

## The cornerstone

This is what we build around: evals come first. Before the prompt is tuned, before the model is chosen, before anything ships, write down the cases your system has to get right and the check that proves it does. Then ship, and keep running them. A feature without evals is a feature you cannot safely change, and every AI feature will need to change.
