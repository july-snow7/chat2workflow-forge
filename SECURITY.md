# Security Policy

## Supported versions

This project is currently in early alpha. Security and privacy fixes should
target the latest commit on `main`.

## Reporting a vulnerability

If you discover a security or privacy issue:

1. Do not open a public GitHub issue with raw chat content or personal data.
2. Describe the impact, reproduction steps, and affected component at a high
   level.
3. Send the report privately to the maintainer before public disclosure.

Examples of security-sensitive issues for this project include:

- sender identity leakage in reports or exports
- accidental retention of raw chat content outside the local working directory
- unsafe file handling that could overwrite unrelated files
- parser behavior that exposes hidden metadata unexpectedly
