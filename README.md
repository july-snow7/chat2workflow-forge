# Chat2Workflow Forge

Turn long chat exports into reusable agent workflow cards.

This project starts from a plain-text WeChat export and turns it into:

- an anonymized corpus summary
- a set of recurring workflow templates
- JSON or Markdown artifacts that can be fed into any agent stack

It is intentionally provider-agnostic, so the same outputs can be used with DeepSeek, Kimi, OpenAI, Anthropic, or a local model runner.

## Why this repo exists

Raw chat logs are messy, but they contain repeatable work patterns:

- internship and interview prep
- homework, papers, and exams
- project planning and meeting follow-ups
- content ops for short video and social platforms
- finance and research questions
- coordination, handoff, and status updates

The goal is not to summarize a chat. The goal is to mine stable workflows and compile them into an agent harness.

## Design goals

- Local first: the raw export never needs to leave your machine
- Privacy safe: sender names are anonymized in reports by default
- Model neutral: no vendor lock-in in the output format
- Demo friendly: the repo produces clear artifacts that are easy to show on GitHub or X

## What it does

1. Parse a WeChat text export into dated messages.
2. Redact sender identities in reports.
3. Match messages against workflow templates.
4. Emit a ranked workflow bundle with tools, inputs, outputs, steps, and evaluation notes.
5. Export either Markdown for humans or JSON for downstream agents.

## Example corpus profile

From a large personal export like the one used to shape this project:

- 92,895 message lines
- 1,320 active dates
- 1,575 unique senders
- strong clusters around career, projects, content, academic work, and finance

That is enough structure to justify a real workflow miner, not just a toy summarizer.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

chat2workflow analyze /path/to/wechat_export.txt --out report.md
chat2workflow export-workflows /path/to/wechat_export.txt --out workflows.json
```

## Output shape

Each workflow card contains:

- title
- summary
- matched message count
- confidence
- signals
- tools
- inputs
- outputs
- steps
- evaluation
- privacy notes

That makes it easy to plug the same artifact into different model providers or evaluation harnesses.

## Suggested launch angle

Position this as:

> A local-first compiler that turns conversation history into agent workflows.

That framing is stronger than "chat summary" and much easier to reuse in a public demo, blog post, or launch thread.

## Status

This repository currently ships with:

- a parser
- a workflow miner
- a report renderer
- CLI entry points
- unit tests
- CI for GitHub Actions
