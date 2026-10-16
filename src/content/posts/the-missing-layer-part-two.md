---
title: "The Missing Layer, Part Two: Why Observability Without Containment Is Just a Dashboard"
date: 2026-09-29
tags: [agents, observability, containment, security]
excerpt: "Watching an agent is not the same as stopping it. Observability tells you what happened; containment decides what can happen at all — and the two only work as a pair."
draft: false
---
[Part One](/posts/the-missing-layer/) made the case that agents need a layer that lets the system see itself, and that the watcher has to be a different thing from what it watches. That argument stands. But it leaves a gap open, and the gap is the one that matters most in practice: seeing is not stopping.

## A dashboard is not a brake

Observability tells you what an agent did. Containment decides what it can do. Those are different jobs, and confusing them is the failure mode we keep seeing.

Picture the trace. Every step logged, every tool call recorded, the decision chain intact end to end. The dashboard lights up the moment the agent deletes a branch it shouldn't have touched. You can replay the run, see the input, see the tool it picked, see the exact instant things went wrong. That is a complete, faithful record of the damage. It is not prevention. A camera pointed at a door being kicked in has recorded the break-in, not stopped it.

## The failure mode we keep running into

Here's the pattern: a team adds traces, logs, and evals. They see the problem clearly — clearly enough to write a postmortem with a timestamp and a root cause. And they still can't stop it, because nothing about the observability layer changed what the agent was able to reach. It held the same credentials and the same network access before the incident as after. Seeing the fork in the road doesn't move the fork. Only something enforced outside the agent does that.

This is where Part One's instinct — the watcher must be a different thing from what it watches — turns out to be only half the design. The other half is that the watcher's authority has to sit outside the agent's own box, not just its own model weights.

## What containment actually looks like

Containment means limits enforced from outside the agent, not limits the agent agrees to respect. Concretely, that means things like:

- **Scoped credentials.** The agent gets access to one repository, not the whole org. If it wanted to touch anything else, the API call fails before it starts, not after someone notices.
- **A sandbox with no headroom.** Runs as a non-root user, no new privileges, a read-only root filesystem. There should be nothing left in the box for a compromised or confused agent to escalate into.
- **Default-deny egress.** A proxy that only allows a fixed, listed set of domains. An agent that isn't supposed to talk to the wider internet simply can't dial out to it, credentials or no credentials.
- **Changes as a branch and a pull request, never a direct push to main.** The agent can propose; it cannot commit the org to anything on its own signature. A human, or a gate, sits between the change and the branch that ships.

None of these depend on the agent behaving well. They hold even when it doesn't.

## The two layers need each other

Containment without observability is a black box. The walls hold, but nobody can tell you what the agent tried to do, how often it hit a boundary, or whether the boundary is even the right one. You get safety with no visibility into whether that safety is being tested.

Observability without containment is a dashboard. You get a beautifully detailed record of an agent doing something it should never have been able to do.

Put them together and something better than either happens: the observer sits outside the agent's box, watching from a position the agent can't reach. It can't switch off its own monitor or edit what got recorded, because the monitor was never inside its perimeter to begin with. That is the same principle Part One argued for the watcher model, applied one level down to infrastructure.

And once observation happens from outside the box, it stops being a story the agent tells about itself and starts being evidence. An audit that compares what the agent claims it did against what actually changed — which remote branches moved, which files landed where — closes the loop. The agent's self-report is a claim. The diff against reality is the check.

## The honest limit

We should be plain about where this stops working. Software walls are not perfect. A sandbox is still software, running on a kernel, and a kernel exploit can escape a container regardless of how tightly the rest of the box is configured. Non-root, read-only, default-deny egress — all of it narrows the blast radius. None of it makes an agent safe on its own.

That's not a reason to skip containment. It's a reason not to oversell it. The goal isn't an agent that cannot possibly cause harm — nothing offers that guarantee. The goal is an agent whose worst plausible action is small, visible, and reversible: scoped enough that the damage stays local, watched closely enough that the damage gets seen immediately, and gated enough that the damage never reaches main without a human saying yes.

Part One asked for a system that can see itself. Part Two's answer is that seeing has to come with the power to stop — enforced from outside, not requested from within.

— Ravi
