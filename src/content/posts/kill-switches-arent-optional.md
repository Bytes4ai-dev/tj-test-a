---
title: "Kill Switches Aren't Optional Anymore: Designing Circuit Breakers for Autonomous Agents"
date: 2026-09-29
tags: [agents, safety, containment, reliability]
excerpt: "A kill switch that has never been tested is not a control. Here is how to design one that actually stops a run, and stays stopped."
draft: false
---
Kill switches sound like a solved problem: put a stop button somewhere, wire it to the process, done. In practice, most teams don't have one that works, which is exactly what ["The Governance-Containment Gap"](/posts/the-governance-containment-gap/) found — plenty of organizations watch their agents closely and still can't stop one that goes wrong. Watching and stopping are different capabilities, and only one of them is optional to skip.

## Kill switch versus circuit breaker

A kill switch is the manual version: a person, outside the agent, flips it and the run stops, quickly, and stays stopped. A circuit breaker is the automatic version of the same idea — it trips on its own when a limit is crossed, without waiting for a person to notice first. A pipeline needs both. The kill switch covers the case where a person catches something the automated checks didn't. The circuit breaker covers the far more common case: nobody is watching that exact run at that exact moment, and something still has to stop it.

## What a circuit breaker should trip on

A few limits cover most of what actually goes wrong. A token or cost budget, so a run that starts burning far more than expected stops instead of running the bill up further. A wall-clock limit, so a run that should take minutes doesn't quietly run for hours. A cap on how many plan-build-review loops a single run may take, so a run stuck failing the same check doesn't get to keep retrying past the point of being useful. Repeated failed checks, which are usually a sign the run is stuck rather than close to done. And any attempt to reach a path, a repository, or a network domain outside the allowed list — which isn't really "something went wrong" so much as "something is now actively out of bounds."

## Where it has to live

The switch has to sit outside the agent's own box and outside its own permissions. If the agent can reach the switch, it can, in principle, disable it, ignore it, or route around it — deliberately or just as one more action taken under pressure to finish the task. A kill switch the agent can touch isn't a kill switch. It's a suggestion.

Two more properties matter as much as where it lives. It has to fail closed: when something goes wrong with the switch itself — a lost connection, a crashed process, an ambiguous state — the default outcome is stop, not continue. And it has to stop gracefully wherever that's possible: no new actions once it trips, whatever the agent already produced stays where it is for a human to review, and a change in progress never gets pushed half-finished. A circuit breaker that halts mid-write, leaving a torn file or a corrupt commit behind, has just traded one failure for a messier one.

## Shapes in a real pipeline

None of this needs to be exotic. In a software pipeline, three concrete shapes cover most of it: a single go/stop switch an operator can flip, living outside the agent, that ends the run immediately; gates between steps, so a failed check halts the run before the next step starts, rather than letting a bad plan turn into a bad build; and a fixed cap on how many plan-build-review loops a run may take, so an agent stuck retrying the same failure doesn't get to retry forever.

## Record every trip

Every time the switch fires, manual or automatic, record why. A stop with no reason attached tells the next person nothing — was it a cost overrun, a repeated failed check, an attempt to touch a path outside the allowed list? The reason is what turns a stop into something the team can learn from, instead of just a run that quietly didn't finish.

## Test it like a fire drill

None of the above is worth much until it's exercised. A kill switch that has only ever existed in a design document is not a control — it's a hope. The only way to know a switch actually stops a run is to trip it, on purpose, against a real or realistic agent, and watch the run actually stop: no new action taken, no half-finished write left behind, the reason recorded where it should be. That has to happen on a schedule, the same way a fire drill happens whether or not anyone thinks the building is at risk that week — because the point of testing it is to catch the version of the switch that quietly stopped working since the last time anyone pulled it.

## Pair it with containment

A kill switch stops the agent from taking its next action. It does nothing about the actions already taken. That's why containment has to come first, not instead: credentials scoped to a single repository, default-deny network egress so there's nowhere unexpected to reach even mid-run, and changes delivered only through a branch and a pull request, so nothing lands on `main` without a person saying yes. Containment bounds how much damage is possible before anything trips. The switch bounds how much more damage happens after someone, or something, notices.

## The honest limit

Say the limit plainly, because it's the whole reason containment matters: a kill switch stops the next action, not the last one. Tripping the switch the instant an agent starts reaching outside its allowed paths does not undo the file it already wrote, the commit it already made, or the request it already sent. Whatever happened before the switch fired stays real, whatever the agent already did outside its walls stays done. A fast, well-tested kill switch is genuinely valuable — it caps how much worse a bad run gets — but it is not a substitute for making sure the run couldn't do much damage in the first place. Build the containment first. Build the switch on top of it. Test both like you mean it.
