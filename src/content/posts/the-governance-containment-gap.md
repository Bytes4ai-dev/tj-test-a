---
title: "The Governance-Containment Gap: Why 58 Percent Monitor but Only 40 Percent Can Actually Stop an Agent"
date: 2026-09-29
tags: [agents, governance, containment, security]
excerpt: "58% of organizations now monitor their AI agents continuously, but only 40% can quickly stop one that misbehaves. A new survey puts numbers on the gap between watching and stopping."
draft: false
---
[Part Two of "The Missing Layer"](/posts/the-missing-layer-part-two/) argued that observability without containment is just a dashboard — a faithful record of damage, not a way to prevent it. Kiteworks' 2026 Data Security Forecast, published in January 2026, puts a number on exactly that gap.

## The number that looks good

Start with the encouraging figure. Kiteworks reports that 58% of organizations have continuous monitoring in place for their AI agents. That is a real investment: someone stood up dashboards, wired in logging, and can now say, credibly, that they watch what their agents do.

Read on its own, 58% sounds like progress on AI governance. Most of this site's argument about observability holds here — a watched agent is better than an unwatched one. But watching was never the hard part, and the same report shows exactly where the investment stopped short.

## The numbers that don't

Kiteworks' report finds that containment lags well behind monitoring. Three figures carry the weight:

- **60% cannot quickly terminate an agent that is misbehaving.** Flip that around and the containment number is stark: only 40% of organizations can actually pull the plug on an agent once something goes wrong. Watching a problem and stopping a problem turn out to be two different capabilities, and most organizations only built the first one.
- **63% cannot enforce purpose limitations on AI agents.** An agent built to summarize documents and an agent that can also send email or touch a database are, in practice, the same agent at most organizations, because nothing stops the first from becoming the second.
- **55% cannot isolate AI systems from broader network access.** More than half of the organizations surveyed have agents that can, in principle, reach further into the network than the task in front of them requires.

Kiteworks' own framing for this pattern is direct: watching is not stopping. A monitor that sees an agent go wrong and a team that has no tested way to intervene have, between them, produced a very detailed postmortem and nothing else.

## Why the gap exists

Monitoring is the easier build. Point logging at the agent's actions, ship it to a dashboard, and you have observability — a project with a clear scope and a clear finish line. Containment is a different kind of work. It means deciding in advance what an agent is never allowed to touch, then removing everything else from its reach, and testing that the removal actually holds under a real failure. That is slower, less visible, and easier to defer. Fifty-eight percent finished the first project. The lower numbers on termination, purpose limits, and isolation are what's left when the second project hasn't started.

## What closes the gap

None of the three weak points above require exotic tooling. Each has a concrete, buildable answer, and it is the same answer this site has been giving in different words:

- **A tested way to stop a run.** Not a kill switch that exists in a design doc, but one an on-call engineer has actually pulled, on a real agent, and watched the run actually stop.
- **Credentials scoped to one repository and one purpose.** An agent that only holds the keys to the job in front of it cannot become a different, more dangerous agent just because nobody revoked the extra access.
- **A default-deny egress proxy that only allows listed domains.** If the agent isn't supposed to reach the wider network, it shouldn't be able to dial out to it — not because it chooses not to, but because the connection fails before it starts.
- **Changes delivered only as a branch and one pull request.** The agent proposes; it never commits the organization to anything on its own signature.
- **An observer that sits outside the agent's box.** Monitoring only counts as containment-adjacent if the agent has no way to reach, edit, or switch off the thing watching it.

Every item on that list is a wall enforced from outside the agent, not a behavior the agent is asked to respect. That is the whole distinction between the 58% and the 40%: one is a policy, the other is a policy plus a wall.

## The honest caveat

Two things are worth saying plainly before anyone treats these numbers as settled fact. First, these are self-reported answers to one vendor's survey — Kiteworks asked organizations what they have in place, and organizations answered. That is a useful signal about where attention has and hasn't gone, not a direct measurement of any system's actual resilience. Self-reported monitoring coverage can be generous in the same way self-reported test coverage usually is.

Second, and more important: a kill switch that has never been tested is not a control. An organization that checks the box on "can terminate a misbehaving agent" because the capability exists somewhere in the architecture, and has never actually exercised it against a live, uncooperative run, does not know whether that box was ever true. The 40% figure almost certainly overstates how many organizations can stop an agent quickly under real conditions, because the survey has no way to tell a tested kill switch from an aspirational one.

None of that makes the gap less real. If anything, it means the gap is probably wider than 58 versus 40. Observability was always the easier half of this problem. The Kiteworks numbers are one vendor's snapshot of an industry that built the dashboard first and is still building the brake.

— Ravi

Sources: kiteworks.com/cybersecurity-risk-management/2026-data-security-forecast-ai-governance-predictions/
