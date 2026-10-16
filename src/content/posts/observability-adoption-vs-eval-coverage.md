---
title: "What 89 Percent Adoption and 52 Percent Eval Coverage Tells You About the Observability Gap"
date: 2026-09-29
tags: [agents, observability, evals, engineering]
excerpt: "LangChain's latest survey finds 89% of teams have agent observability in place, but only 52% run offline evals and 37% run online ones. Seeing what an agent did is not the same as knowing it was right."
draft: false
---
[The Missing Layer](/posts/the-missing-layer/) argued that observability is the layer enterprise AI is missing — the thing that lets a system see itself instead of running blind. LangChain's State of Agent Engineering survey, 1,340 responses collected between 18 November and 2 December 2025, suggests that argument has mostly landed. Seeing, it turns out, was only the first half of the problem.

## The good news first

Agents have moved past the pilot stage for a majority of respondents: 57% report having agents in production. That alone would have sounded ambitious two years ago. More striking is what teams built around those agents once they shipped. Observability has become table stakes: 89% report having implemented some form of it, and 62% say they have detailed tracing of individual agent steps and tool calls, not just top-level logs.

Read that second number carefully, because it is the harder one to reach. General observability — logging that an agent ran, how long it took, whether it errored — is a modest lift. Step-level tracing, where you can see which tool an agent picked, what arguments it passed, and what came back, is a different and more deliberate investment. Sixty-two percent of respondents made it. That is the industry catching up to the argument that a system needs to see its own decisions, not just its own uptime.

## The number that doesn't match

Now the harder half. LangChain's survey finds that 52.4% of respondents run offline evaluations against a test set before shipping changes. Online evaluation — checking live traffic in production, not just a curated set beforehand — is lower still, at 37.3%.

Put the two halves side by side. Eighty-nine percent of teams can tell you what their agent did. Just over half can tell you whether it did the right thing before it shipped, and just over a third can tell you whether it's still doing the right thing once it's live. That's not a small gap. It's most of the industry building the half of the system that watches, and skipping the half that judges.

## Why a trace is not a verdict

A trace records the input, the tool call, the arguments, and the result. That is genuinely useful — it is the raw material Part One asked for. But a trace answers "what happened," and it answers that question whether the outcome was good or bad. An agent can execute a flawless, fully-traced sequence of tool calls and still hand a customer the wrong answer, and the trace will not tell you that on its own. Someone, or something, still has to look at the outcome and decide if it was acceptable.

That decision is what evaluation is for. An offline eval checks a change against a curated set of cases before anyone outside the team sees it — the gate that catches a regression before it ships. An online eval checks live traffic after the fact — the check that catches drift a golden set never anticipated, because production always finds inputs nobody wrote down in advance. Observability without evaluation gives you a complete, faithful record of an agent doing something wrong. It does not stop the agent from doing it, and it does not tell you it was wrong until a person reads the trace and notices.

## What closes the gap

None of this calls for new tooling so much as it calls for finishing the build most teams already started.

- **Turn production failures into eval cases.** Every bad output a trace surfaces is a candidate for the golden set. Traces that never feed evaluation are a record nobody learns from twice.
- **Gate releases on offline evals.** A prompt or model change runs against the test set before it ships, the same way a code change runs against unit tests. If the results get worse, the change waits.
- **Run online evals against live traffic.** A golden set reflects what you imagined users would ask. Production traffic reflects what they actually ask. Only one of those catches the drift the other can't see coming.
- **Pair both with containment.** An eval that catches a bad action after the fact still needs walls around what the agent could do while it was happening: credentials scoped to the one job in front of it, default-deny egress so it can't reach anywhere it wasn't supposed to, and changes delivered only as a branch and a pull request, never a direct commit the agent makes on its own signature.

Evaluation tells you whether the agent was right. Containment limits the damage while you're finding out it wasn't.

## The honest caveat

These are self-reported answers to one vendor's public survey, not independent measurements of what any of these teams actually run. LangChain asked, and 1,340 respondents answered for themselves — nobody audited whether a team's "offline evaluation" is a disciplined golden set run on every change or a notebook someone ran once. The real gap between watching and judging is probably at least as wide as 89 versus 52, not narrower.

That caveat doesn't undercut the shape of the finding. Observability got built first because it was the easier build: point logging at the agent, ship it to a dashboard, done. Evaluation is slower and less visible — deciding what "right" even means for a given task, curating cases, and running them on every change is real, ongoing work with no obvious finish line. Most of the industry built the half that watches. The half that judges is still catching up.

— Ravi

Sources: langchain.com/state-of-agent-engineering
