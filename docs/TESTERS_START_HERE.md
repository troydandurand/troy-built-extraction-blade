# Testers — start here

1. Download the repository source ZIP and unzip locally.
2. Run `python3 -m unittest -v test_blade_v03.py`.
3. Test only **synthetic or your own authorized** JSON export ZIP.
4. Run `python3 blade_v03.py input.zip output.zip`.
5. Inspect `QA_MANIFEST.json` and preserved `*.source.json`.
6. Record format, Python version, output status, and any parse/round-trip failures.
7. Open an Issue **without attaching private chats**.

The processor does **not** independently fetch all your live ChatGPT conversations.
