# Free Emergency Binder Kit

Free printables for a home emergency binder, by **Asdale Dynamics, LLC**
(Dylan Asdale — plain-English AI guides and practical life-admin tools at
[dylanasdale.github.io](https://dylanasdale.github.io)).

Eight fill-in-by-hand sheets that cover the basics when life goes sideways:

| Sheet | What it does |
|---|---|
| Contacts & Out-of-Town Check-In | Who to call, plus a form to give an out-of-town contact |
| Insurance Policy One-Pager | Key details for each policy on a single page |
| Utility Shutoff Map & Instructions | Label the shutoffs and tape the map to the wall |
| Pet Info Card | Vets, meds, feeding notes for each pet |
| Household Info Card | Addresses, accounts, medical basics in one spot |
| Grab-and-Go Checklist | What to take if you have 5, 30, or 60 minutes |
| In-Case-of-Emergency Letter | A short letter template for the people who step in |
| Yearly Review Reminder Card | One page, once a year, keep it fresh |

Everything is local-first and private by design:

- **Nothing leaves your home.** No servers, no accounts, no tracking.
- **Fill in by hand.** The PDFs print with blank lines — you never type
  sensitive info into a file.
- **Free.** MIT licensed; print as many copies as you like.

## Quick start

Requirements: Python 3.9+ with WeasyPrint and pypdf.

```bash
pip install weasyprint pypdf pytest
python3 build.py          # builds every sheet to dist/*.pdf
python3 -m pytest tests/  # verifies every PDF exists and is valid
```

Each built PDF prints on US Letter or A4 (the layouts adapt automatically).
Print one copy for the binder, plus the extra copies noted in
[guide/GUIDE.md](guide/GUIDE.md).

## Project layout

```
build.py            renders sheets/*.html -> dist/*.pdf via WeasyPrint
sheets/*.html       printable sheet sources (HTML/CSS, no JS)
assets/style.css    shared print stylesheet
guide/GUIDE.html    printable quick guide (also built to dist/)
tests/test_build.py Pytest suite: every sheet must build a valid PDF
dist/               built PDFs land here (gitignored)
```

## Customize

Edit any sheet in `sheets/`, then re-run `python3 build.py`. The stylesheet
handles page size, margins, and print-safe colors, so you only touch content.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
Provided as an educational and organizational aid only; not legal, medical,
or insurance advice.
