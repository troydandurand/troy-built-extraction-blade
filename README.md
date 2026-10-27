# TROY-BUILT™ Conversation Preservation Blade — v0.3 Engineering Preview

**ProfitFuel™ AiOS — LEVITY. LETHALITY. LEGACY. ALL SIGNAL. NO NOISE.**

**Not a live-history downloader. Not production-certified.**

This is a source-relative command-line tool. It processes user-supplied conversation export ZIP files containing supported tree or flattened JSON formats, preserves the source JSON bytes, and writes machine-reversible Markdown and JSON with a SHA-256 manifest.

## Requirements
Python 3 (standard library only).

## Run
```bash
python3 -m unittest -v test_blade_v03.py
python3 blade_v03.py '/path/to/exports.zip' '/path/to/output.zip'
```

## What is verified
12 tree and 12 flattened JSON exports processed; 24/24 text round-trip checks and 2/2 unit tests passed on supplied sources. **This does not establish completeness against live original chats**. Non-text content and alternative branches remain preserved in source JSON, not fully represented in Markdown.

## Privacy
Use only data you own or are authorized to process. Never post private conversation files in public issues. Public examples use synthetic content.

## License
**No software license granted.** Source is publicly visible for controlled evaluation, but this preview is not an open-source license grant. Commercial terms remain pending.

## Feedback
See TEST_FEEDBACK_TEMPLATE.md and SECURITY.md.
