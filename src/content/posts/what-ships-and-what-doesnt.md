---
title: "What Ships and What Doesn't: Why Our Deploy Machinery Never Reaches the Customer"
date: 2026-09-26
tags: [ai, engineering, governance]
excerpt: "Our build tooling can merge and deploy for us. It never ships. So in the product, every change still waits for a person: not because a setting says so, but because the thing that skips the wait isn't there."
draft: false
---

*A short note on one design choice.*

When we build, we want speed. So we use a developer-mode accelerator: tooling that speeds up the person building the system. It can merge an approved change and start a deploy without anyone typing each command by hand.

It never ships.

## Two different machines

There is the machine we build with, and there is the product. The accelerator belongs to the first. It is gitignored, and it is not part of anything a customer receives.

That split is the point. Speed-up tools are for the builder. The customer gets the product, and only the product.

## The gate comes back by absence

In the product, every customer pull request waits for a human. Not because someone turned on a setting that says "require approval." Settings can be switched off, misconfigured, or overridden on a bad day.

The gate is there because the thing that would auto-merge is not there. There is no switch to flip, because the machinery that skips the wait was never shipped. The human step comes back by absence.

## Removing the wait is not removing the approval

The accelerator removes waiting, not judgment. When we use it, a person has already decided; the tool carries out that decision. It does not make one.

That is the line we hold: tools can remove the wait. They do not remove the approval.

## Why it matters

It is tempting to ship the fast path to everyone. It looks like a feature. But a fast path that skips people is a risk that someone else ends up carrying. Keeping it on the builder's side means the speed stays with the people who chose it, and the safety stays with the people who rely on it.

What ships, and what doesn't, is a decision too. We make it on purpose.
