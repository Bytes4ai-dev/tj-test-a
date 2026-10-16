---
title: "2025: Vibe coding and the quality question"
order: 7
year: "2025"
tag: "Engineering"
description: "Writing software by describing it to a model went from a joke to a job description, and the question moved from how fast to how good."
service: "Build"
heroAlt: "Original illustration: stacked blocks, some slightly out of line, the Engineering motif."
chart:
  alt: "Bar chart from the METR study: developers expected a 24% speed-up, afterwards believed they were 20% faster, and were measured 19% slower."
  caption: "Expected, perceived and measured effect of AI tools on task time for 16 experienced open-source developers (METR, early 2025)."
  sourceUrl: "https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/"
sources:
  - title: "Andrej Karpathy on X, the \"vibe coding\" post (February 2025)"
    url: "https://x.com/karpathy/status/1886192184808149383"
  - title: "METR, Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity"
    url: "https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/"
  - title: "Veracode, 2025 GenAI Code Security Report"
    url: "https://www.veracode.com/blog/genai-code-security-report/"
---

In February 2025, Andrej Karpathy described ["a new kind of coding I call vibe coding"](https://x.com/karpathy/status/1886192184808149383): you describe what you want, accept what the model writes, and "forget that the code even exists". He meant it for throwaway weekend projects. The industry took it much further.

For prototypes the effect was real. People who had never shipped software built working tools in an evening. Inside companies the picture was mixed, and two studies set the tone [[2]](#source-2) [[3]](#source-3).

METR ran a randomised trial with [16 experienced developers on 246 real issues in their own repositories](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/). With AI tools allowed they took 19% longer; beforehand they expected a 24% speed-up, and afterwards they still believed they had been 20% faster [[2]](#source-2). The gap between how fast it feels and how fast it is was the real finding.

On quality, Veracode tested code from many models on security-relevant tasks and reported that [45% of the code samples failed security tests and introduced OWASP Top 10 vulnerabilities](https://www.veracode.com/blog/genai-code-security-report/). The code worked; it just was not safe.

Neither study says "do not use AI to write code". They say the review, the tests and the security checks are not optional, and that the person merging the change still owns it [[2]](#source-2) [[3]](#source-3). A team that ships more code with the same review capacity is shipping more unreviewed code.

## What to do about it

Keep the speed and add the brakes: tests that must pass before merge, an automated security scan on every AI-written change, and a named reviewer who is not the author. Our **Build** service writes the evaluations first, then builds the system that passes them. [See Build](/#services).
