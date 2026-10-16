---
title: "2026: Shadow AI, agents with your credentials"
order: 10
year: "2026"
tag: "Data and people"
description: "Shadow IT became shadow AI: staff brought their own tools, then their own agents, and those agents act with the person's own access."
service: "Govern"
heroAlt: "Original illustration: a grid of dots with a few unlit dots outside the grid, the Data and people motif."
chart:
  alt: "Bar chart from IBM's 2025 breach report: 13% of organizations reported breaches of AI models or applications; of those, 97% lacked proper AI access controls; 63% of breached organizations had no AI governance policy or were still developing one; 20% reported a breach due to shadow AI."
  caption: "AI-related findings from IBM's Cost of a Data Breach Report 2025 (each bar has its own base, as labelled)."
  sourceUrl: "https://newsroom.ibm.com/2025-07-30-ibm-report-13-of-organizations-reported-breaches-of-ai-models-or-applications,-97-of-which-reported-lacking-proper-ai-access-controls"
sources:
  - title: "IBM Newsroom, IBM Report: 13% of organizations reported breaches of AI models or applications, 97% of which reported lacking proper AI access controls (30 July 2025)"
    url: "https://newsroom.ibm.com/2025-07-30-ibm-report-13-of-organizations-reported-breaches-of-ai-models-or-applications,-97-of-which-reported-lacking-proper-ai-access-controls"
  - title: "Microsoft WorkLab, 2024 Work Trend Index: AI at work is here. Now comes the hard part"
    url: "https://www.microsoft.com/en-us/worklab/work-trend-index/ai-at-work-is-here-now-comes-the-hard-part"
  - title: "IBM, Cost of a Data Breach Report"
    url: "https://www.ibm.com/reports/data-breach"
---

Every wave of new technology arrives first through the side door. With AI it arrived fast. Microsoft's 2024 Work Trend Index found that [75% of knowledge workers used AI at work and 78% of AI users brought their own AI tools](https://www.microsoft.com/en-us/worklab/work-trend-index/ai-at-work-is-here-now-comes-the-hard-part) [[2]](#source-2).

Bring-your-own chat was a data-leak risk. Bring-your-own agent is different in kind. An agent connected to someone's mailbox, drive or code host acts with that person's own tokens. To every system it touches, it looks exactly like them. It does not show up in an inventory, and nobody reviewed its permissions because, technically, nobody granted any new ones.

The cost is now measured. IBM's 2025 breach research found that [one in five organizations reported a breach due to shadow AI, and those with high levels of shadow AI saw an average of $670,000 in higher breach costs](https://newsroom.ibm.com/2025-07-30-ibm-report-13-of-organizations-reported-breaches-of-ai-models-or-applications,-97-of-which-reported-lacking-proper-ai-access-controls). The same report found that [13% of organizations reported breaches of AI models or applications, 97% of those lacked proper AI access controls, and 63% of breached organizations had no AI governance policy or were still writing one](https://newsroom.ibm.com/2025-07-30-ibm-report-13-of-organizations-reported-breaches-of-ai-models-or-applications,-97-of-which-reported-lacking-proper-ai-access-controls) [[1]](#source-1).

Banning the tools rarely works; people route around bans when the tools save them hours. What works is giving them a sanctioned path that is easier than the shadow one, and making agent access visible.

## What to do about it

Find the agents first: review OAuth grants and API tokens issued to AI tools, then move the useful ones onto their own scoped service identities with logging. Our **Govern** service puts scoped credentials, audit trails and stop controls around your agents. [See Govern](/#services).
