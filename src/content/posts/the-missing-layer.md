---
title: "The Missing Layer: Why Enterprise AI Can't See Itself"
date: 2026-09-27
tags: [ai, engineering, observability]
excerpt: "Most enterprise agent pilots stall before production, and the reflex is to blame the model. That's the wrong diagnosis. What's missing is the layer that lets a system see itself: observability."
draft: false
---
The industry has an agent problem, and it isn't the models.

Gartner and IDC data this year tells a blunt story: the large majority of enterprise AI agent pilots stall before production, and a significant share of agentic projects are now at risk of being cancelled. The reflex is to blame the model — not smart enough, not reliable enough. That's the wrong diagnosis. The models are fine. What's missing is the layer that lets a system see itself: observability.

And agent observability is not application monitoring. Traditional monitoring answers *what happened* — latency, error rate, uptime. That tells you nothing about *why an agent chose what it chose*. When a multi-agent system drifts, deadlocks, or quietly burns tokens in a loop, your Prometheus dashboard stays green. The failure is invisible because you're measuring the wrong thing.

## What observability actually has to capture

Three layers, in order of how often they're missed.

**Capture every step's raw output, always.** The most common failure I've seen is the silent death — an agent exits, produces nothing, and leaves no trace, so the orchestrator carries on as if all is well. If an action leaves no record, it didn't happen, as far as the system can tell. Durable capture of every worker's output is observability rule zero. Everything else builds on it.

**Trace the decision, not just the call.** Every step should record the input it saw, the tool it picked, the arguments it passed, the result it got, and the reason. You want to replay a run and see the fork in the road — not just that the run occurred. This is where decision-chain tracing earns its keep.

**Watch behavioral signals, not just infrastructure.** Escalation rate, task completion rate, whether an output passes an evaluation, shifts in tool-call patterns. These go red before CPU does, because users feel degradation before your metrics report it.

## Feedback is a signal source, not an afterthought

Here is a pattern that worked in production. In a support-facing AI system, feedback came in from three directions — the customer, the client, and the internal support team. Rather than let it sit as anecdote, we piped that feedback into our observability stack and mapped it against the AI's own performance metrics. Escalation rates moving up or down became a first-class signal. Errors and issues surfaced as reporting, not as complaints. The feedback loop *became* part of observability.

That closes the gap between how a system thinks it's doing and how it's actually doing. But it still leaves one hard question: who watches the agents while they run?

## The observer should not be the expensive one

Here's the counterintuitive part. The natural instinct is to put your most capable, most expensive frontier model in the loop as the supervisor. That's backwards.

The supervisor's job is not creativity. It's watching. Observe the traffic between agents. Count the tokens the orchestrator is spending. Detect drift. Detect when one agent is doing something it shouldn't. And if something crosses a line — cut the loop. That is a governor and a kill switch, not a participant. It's a rule engine with eyes, and you are paying frontier prices for a job a rule engine does better.

A small, local model — LoRA-tuned for exactly this narrow watching task — can do it always-on, at a fraction of the cost, and with something the frontier model in the loop can't offer: an attributable identity. The guard must be a different thing from the thing it guards. Sovereignty isn't sitting in the loop. It's owning the lock the loop answers to.

## Coming soon: proving it

This is a claim, and claims should be tested, so we're going to test it.

We run multi-agent teams where one participant acts as the human's stand-in — the reviewer, the gate. Today that role runs on an expensive frontier model, and it is not doing what we actually need: a faithful, cheap, always-on representation of human judgment on drift and safety.

So we are going to replace it. We'll swap that participant for a local agent, build it a robust rule engine, LoRA-tune the model for the watching task, and give it one job: observe the agent-to-agent traffic, track token spend, catch drift or misbehavior, and act as the kill switch when needed. Then we'll run it apples-to-apples against the expensive version — same team, same work — and compare cost and catch-rate.

We'll publish what we find, including if it doesn't work. That's the point of observability, after all: you don't get to hide the result.

— Ravi
