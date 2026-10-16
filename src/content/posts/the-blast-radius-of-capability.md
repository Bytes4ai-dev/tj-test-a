---
title: "The Blast Radius of Capability"
date: 2026-09-24
tags: [opinion, critical, ai, privacy]
excerpt: "The more capable an AI model is, the larger the blast radius when it is wrong, misused, or pointed at the wrong data."
draft: false
---

*This is an opinion piece. It is deliberately critical.*

The latest AI models are impressive. They write, reason, summarise, plan, and act with a fluency that is hard not to admire. Bytes4AI admires it too. But admiration is not the same as trust, and impressive is not the same as safe.

Here is the argument of this piece, stated plainly: the more capable the model, the larger the blast radius. Capability and risk are not separate dials. They are the same dial. A tool that can do more can also do more damage when it is wrong, when it is misused, or when it is pointed at the wrong data.

That is not a reason to fear these models. It is a reason to take them seriously.

## Why capability widens the blast radius

Think of the blast radius as the area a mistake can reach. A narrow tool has a small one. A general model has a much larger one. The mechanisms below push it outward.

**Generality.** A narrow tool does one job, so it has a short list of ways to fail. A general model does many jobs, and every job it can do is another way it can go wrong. One model, many uses, many failure modes. The flexibility that makes it valuable is the same flexibility that makes its failures hard to predict.

**Autonomy.** A model that only produces text leaves a human between its output and the world. A model that takes actions removes that buffer. When a model can send the message, move the file, make the payment, or change the setting, its errors stop being suggestions and start being actions. An agent that is wrong is not just wrong; it is wrong on your behalf.

**Access.** Capability invites access. The more a model can do, the more tempting it is to give it people's data, inboxes, files, calendars, and accounts, because that is where its usefulness lives. But access is exactly what turns a mistake into a breach. A model with no access can embarrass you. A model with access to everything can expose you.

**Scale.** A person who makes an error makes it in one place. A model that carries a flaw carries it everywhere it is deployed, at the same moment. There is no gradual spread and no early warning. One flaw, copied to everyone at once.

**Persuasion.** Fluent output sounds confident, and confident output invites belief. A capable model can be wrong in beautifully written paragraphs. The better the prose, the easier it is for a reader to skip checking it. If trust follows fluency, it follows whether or not the fluency has earned it.

Each of these widens the radius on its own. Together they compound. Imagine an agent that is general enough to handle any request, trusted to act without asking, connected to a person's email and bank account, deployed identically for everyone, and articulate enough that its mistakes read as sound advice. That hypothetical agent is the shape of risk that capability invites, and it is worth designing against before it is built.

## Why Bytes4AI is still pro-progress

None of this makes Bytes4AI anti-AI. The same capability that widens the blast radius is genuinely useful. A model that can read a long document can help someone understand a contract they would otherwise sign blind. A model that can act can take tedious work off a person's plate. Those benefits are real, and pretending otherwise is not honesty; it is just a different kind of bias.

Refusing capability is not protection. Protection that blocks all progress invites its own bypass. If the only safe option is the useless one, the useful option gets taken anyway, and it gets taken with no protection at all. The useful question is not whether to use capable models. It is how to use them without handing them a radius nobody can recover from.

## What pro-protection means in practice

Pro-protection is not a mood. It is a set of principles that shrink the blast radius without shrinking the benefit.

- **Data minimisation.** Give a model the data a task needs, and nothing more. Data that is never shared cannot leak.
- **Consent people can understand.** If a person cannot explain what they agreed to, they did not really agree. Consent should be plain, specific, and easy to withdraw.
- **Least privilege for AI agents.** An agent should hold the narrowest permissions that let it do its job. Read access where read is enough. No standing access to everything, just in case.
- **A human confirms irreversible actions.** Anything that cannot be undone, such as sending money, deleting records, or sharing private data, waits for a person to say yes.
- **Audit trails.** Every action an agent takes should leave a record a person can read. If nobody can see what happened, nobody can fix it.
- **Safe defaults that can be reversed.** The default setting should be the cautious one, and changing it should be a deliberate, reversible choice rather than a trap.
- **The burden of proof sits with whoever widens the radius.** If a product gives a model more autonomy, more access, or more reach, the job of showing that it is safe belongs to the builder, not to the people whose data is on the line.

None of these principles stops a model from being capable. They decide where that capability is allowed to land.

## Judge a model by what it can break

It is natural to judge a model by what it can do. That is only half of the picture. The other half is what it can break: whose data it touches, which actions it can take, how far a single error can travel, and who pays when it goes wrong. A more capable model deserves more scrutiny, not less, because it has more to break.

Bytes4AI is about bytes: the data that AI is built on, and the data that describes real people. We will stay vocal about progress and give credit to what is genuinely good. We will also insist that the people inside the data are protected. Pro-progress, pro-protection. The more a model can do, the more carefully we should ask what it can undo.
