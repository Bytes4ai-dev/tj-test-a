---
title: "Nested Conductor: Pros and Cons"
date: 2026-09-25
tags: [agents, engineering, ai]
excerpt: "A LangGraph Conductor running inside my existing launcher: what the graph takes over, what stays outside it, and what the lab runs showed. An in-house lab build, not production."
draft: false
---

*This is about an in-house lab build, not production. Every fact below was measured in my lab.*

My agents already run through a launcher of my own. It has a lock, it has caps, and it wraps every run in git walls. Inside it sits a Conductor that routes work between an Architect and an Engineer. I wanted to see what changes when that Conductor becomes a graph. So I built one, and I nested it inside the launcher instead of letting it replace the launcher. This post argues both sides, from what my lab runs showed and nothing else.

## What I built

The stack is LangGraph 1.2.12 on Python 3.14.7, with a SQLite checkpointer. The workers are Claude command-line sessions: one plays the Architect, one plays the Engineer.

The graph replaces only the Conductor's orchestration. It runs the sequence architect, gate, engineer, gate, commit, and then loops, with a hard cap of five loops.

Everything else stays where it was. The launcher, its lock, its caps and its three git walls remain separate scripts around the graph. The three walls are a branch preflight, bound hooks, and a post-run audit.

That is the nesting. The graph runs inside the launcher, not instead of it. The graph is the brain. The launcher and its walls are the body the brain lives in, and the brain does not get to rearrange the body.

It was not a perfectly clean fit. In the lab, the launcher copy differed from the real one in one block: 4 lines removed, 1 added.

## The pros

**The brain and the walls are separate.** Because the walls live outside the graph, a confused graph still meets the same walls. The graph has no say over a branch preflight or a post-run audit that runs as its own script. I did not have to take that on trust; the first milestone attempt, below, put it to the test.

**Gates are code.** Each gate is a check a program runs, not a reading of prose. One gate checks that the task file has its seven required headings. One reads a small JSON status written next to the human-readable result. One requires exactly one pull request into main, with the pushed branch equal to the local branch. A gate like that either passes or it does not, and I can see exactly why.

**Silence is not success.** A worker counts as finished only when its exit line reads `exit=0`. Quiet output never counts, and neither does empty output. In my view that is the right default: a worker that stops without saying anything has not proved it did the work, so it has not finished.

**The run can be stopped without being lost.** Kill-and-resume from the checkpoint was tested in the lab: the run was killed and picked up again from where the checkpoint left it. A human pause at the gates was tested too. That changes how I think about a run. Stopping it is a choice I can make, not a loss I have to absorb.

**It reached the milestone.** A full Architect-Engineer run behind the real walls ended "feature complete" at loop 2, with exactly one pull request to a throwaway repository. All 7 checks passed.

**The walls held when the brain was wrong.** The first attempt at that milestone failed, and it failed usefully. The walls, the cap and the one-pull-request rule all held across the five loops. That is the case for nesting in one line: the brain was wrong, and the body around it still held its shape.

## The cons

**Two layers to keep in step.** Nesting means two layers: the graph, and the launcher around it. They have to agree. Even in the lab, the launcher copy already had to differ from the real one, by 4 lines removed and 1 added. That is a small difference, but it is a place where the two layers can drift apart, and someone has to own keeping them together.

**A gate that reads text can stop complete work.** A real run stopped at a text-format gate because of one harmless prose line that began "Warnings:". The work itself was complete. The gate did what it was written to do, and what it was written to do was too blunt. That is why the JSON status exists: a gate should read a field, not guess at a sentence.

**The graph does not make a worker read its prompt correctly.** In the first milestone attempt, a loop note was glued onto the end of the request. The Architect read it as part of the required text, and it kept asking for a rewrite until the five-loop cap stopped the run. The graph routed exactly as designed. It just routed a misunderstanding for all five loops. The fix was in the prompt, not in the graph: the request now sits between explicit markers. Orchestration cannot correct what a worker misreads.

**More stack to own.** LangGraph, Python and a SQLite checkpointer are now part of the system, alongside the launcher and its scripts. Each one is something I have to understand and keep working. The graph buys structure, and the price is more moving parts.

**The evidence is thin.** What I have is one lab milestone on a throwaway repository. It passed all 7 checks, and I am glad it did, but one run is one run. It shows the design can work. It does not yet show that it keeps working.

## What is not in the graph yet

Two pieces still live outside the graph: the run heartbeat and the scheduled queue. Until they move in, or I decide they should stay out, the graph owns the loop and nothing around it. I would rather say that plainly than let the diagram suggest the graph runs everything.

## Where that leaves it

My verdict, and it is an opinion: nesting is the right shape for this build. The strongest argument for it is the failed attempt, not the successful one. When the brain misread its request, the cap, the walls and the one-pull-request rule held anyway, because none of them lived in the brain. That is what I wanted from the split.

The costs are real. There are two layers to keep in step, and the lab copy of the launcher already differs from the real one. A text gate has already stopped complete work, and the JSON status is the answer to that. The graph cannot make a worker read well. And the good result rests on one milestone run on a throwaway repository.

So I would not call this finished. It is an in-house lab build, not production, and everything above comes from my lab runs. The next evidence I want is more runs behind the same walls, including ones where the brain goes wrong again.

*— Ravi*
