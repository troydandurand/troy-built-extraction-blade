# TROY-BUILT™ v0.3 — Public engineering preview

## What you can test
- Process **user-supplied** chat export ZIPs containing compatible conversation-tree JSON and flattened JSON.
- Preserve original JSON bytes in output ZIP.
- Produce active-branch JSON and reversible Markdown text representation.
- Generate source SHA-256 hashes and per-export QA metadata.

## Evidence to date
The engineering build was exercised against 12 tree exports and 12 flattened JSON exports. The reported 24/24 Markdown text round-trip results are **source-relative**. Two earlier unit tests passed. Independent live ChatGPT conversation acquisition, UI-completeness, non-text Markdown fidelity, and commercial readiness remain unproven.

## Download
Use GitHub **Code → Download ZIP**, or the versioned source archive linked in the main README. The source ZIP is not a notarized Mac app or installable product.

## Restrictions and privacy
Never publish user conversations or credentials in Issues or examples. This public code is provided for evaluation; **no commercial software license has been granted**. Do not assume that a repo being public means the software is open source.

## Feedback
Open an Issue with an anonymized reproduction using `TEST_FEEDBACK_TEMPLATE.md`.
