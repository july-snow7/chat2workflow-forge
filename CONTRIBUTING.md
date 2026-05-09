# Contributing to Chat2Workflow Forge

Thanks for contributing. This repository handles privacy-sensitive chat export
workflows, so correctness and data hygiene matter more than speed.

## Before you open a change

1. Do not commit raw personal chat logs, screenshots, or contact names.
2. Reproduce the issue with a sanitized text fixture or a minimal synthetic
   sample.
3. Keep parser, workflow template, and reporting changes scoped so they are
   easy to review.

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests -v
```

## Pull request checklist

1. Explain what changed and why.
2. Call out any parser assumptions or template keyword changes.
3. Add or update tests for behavior changes.
4. Confirm that all sample inputs are sanitized.

## Good first contributions

- expand workflow templates for new repeatable task families
- improve parser coverage for more export edge cases
- improve report readability without leaking raw identities
- add sanitized end-to-end fixtures
