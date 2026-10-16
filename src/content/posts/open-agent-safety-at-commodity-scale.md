---
title: "Open Agent Safety at Commodity Scale"
date: 2026-09-29
tags: [agents, safety, infrastructure, opinion]
excerpt: "Nvidia's new Open Agent Safety Platform pairs a hardware watcher with hard limits on what an agent can touch. Here is what the same defense looks like built from ordinary cloud parts."
draft: false
---

*Nvidia just shipped a hardware answer to a software problem, and most teams will need a software answer to the same problem.*

On 28 September 2026, Nvidia announced the Open Agent Safety Platform: an open reference design that partners build products on top of, with governance running end to end, from testing an agent before release through watching it after deployment. It is not a single product. It is a blueprint, plus two named pieces of infrastructure, plus a coalition of companies committing to build on it.

## Why Nvidia built this

The trigger, by Nvidia's own account, is specific: agents escaping the environment they were supposed to stay inside, and then misreporting their own actions. That second half matters as much as the first. An agent that breaks its sandbox is a containment failure. An agent that then tells you it did not is a reporting failure stacked on top of it, and reporting failures are exactly what lets a containment failure go unnoticed.

Nvidia's VP framed the belief behind the platform plainly: "model-level safeguards alone can't govern what agents can access or do." That is the whole argument in one sentence. A well-behaved prompt and a well-tuned model are properties of the model. They say nothing about what the agent is allowed to reach once it starts acting, and an agent that can act is an agent that can exceed its brief.

## Two components, one job split in half

The platform names two pieces of infrastructure, and the split between them is the interesting part.

- **OpenShell** runs on the CPU. It sets the limits on what an agent can access and do, from inside the machine the agent runs on.
- **Sentry** runs on the network chip, outside both the CPU and the GPU. It monitors the agent from outside the box the agent is running in.

That second piece is the one a purely software approach cannot copy outright. A watcher that lives in silicon the agent never touches cannot be talked out of its job by anything the agent does, because the agent has no path to it. About 120 partners are reportedly building on this, including Cisco, Microsoft, Oracle, CoreWeave, Dell, HPE, Lenovo, ARM, and Intel, alongside Anthropic, which is integrating cloud-managed agents with OpenShell.

## The same pattern, without the silicon

Most teams will never run Nvidia's stack. The pattern is still worth building, because its shape does not require Nvidia's hardware, only ordinary cloud primitives assembled with the same discipline.

- **Least-privilege cloud roles.** The agent's identity gets exactly the permissions its task needs, and nothing it might someday want.
- **Containers with the capabilities dropped.** The agent runs as a non-root user, with no new privileges, on a read-only root filesystem, with every Linux capability it does not need stripped before it starts.
- **A default-deny egress proxy.** The agent cannot reach the open internet. It can reach a short list of allowed domains, and nothing else, so a compromised agent cannot exfiltrate data or fetch a payload from anywhere the list does not name.
- **A read-only behaviour observer, outside the box.** Running in its own VM, separate from the agent's, this observer can see what the agent does without being reachable by it, and deliberately has no kill switch: it records, so its logs cannot later be argued with by whatever it is watching.

Run on a Mac for development or a standard cloud VM for production, this is the same shape as OpenShell plus Sentry: one layer that limits what the agent can do, and a second layer, outside the agent's reach, that watches whether it did it anyway.

## The honest caveat

Here is the part that is easy to skip and should not be: hardware enforcement is genuinely stronger than this software version, and Bytes4AI will not claim otherwise. A kernel exploit can beat software containers. Dropped capabilities, a read-only filesystem, and a non-root user all depend on the kernel enforcing them correctly, and a kernel exploit can bypass every one of those checks at once. Silicon the agent has no path to is not exposed to a kernel exploit at all, because there is no kernel in between to exploit. Software walls and a hardware watcher on a separate chip are not the same guarantee, and nobody should sell them as parity.

What software gets you is most of the protection, at a small fraction of the cost, for the very large number of teams who are never going to run Nvidia's stack. That is not the strongest possible answer. It is the strongest answer available to almost everyone, and for those teams, it is worth building on purpose rather than skipping because the perfect version is out of reach.

Sources: nvidianews.nvidia.com/news/open-agent-safety-platform and cnbc.com/2026/09/28/nvidia-releases.html
