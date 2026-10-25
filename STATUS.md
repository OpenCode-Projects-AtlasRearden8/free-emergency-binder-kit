# STATUS

Last updated: 2026-10-25

## What was built

**Free Emergency Binder Kit** — eight fill-in-by-hand printable sheets plus a
printable quick guide, for a home emergency binder. Published by
Asdale Dynamics, LLC (Dylan Asdale, dylanasdale.github.io).

| Sheet (source in `sheets/`) | Purpose |
|---|---|
| `contacts-checkin.html` | Everyday contacts + out-of-town check-in contact and plan |
| `insurance-one-pager.html` | One page per policy: numbers, claims contact, where originals live |
| `utility-shutoff-map.html` | Gas/water/electric shutoff instructions + hand-drawn house map |
| `pet-info-card.html` | One page per pet: health, meds, feeding, temperament, evacuation |
| `household-info.html` | Household members, medical basics, document locker locations |
| `grab-and-go.html` | 5 / 30 / 60-minute checklists + where things are in the home |
| `ice-letter.html` | In-case-of-emergency letter template (handwritten, signed) |
| `yearly-review.html` | 20-minute annual review checklist + review log |
| `guide/guide.html` | Printable short guide on where to store copies (3-2-1 family style) |

- All content is fill-in-by-hand: print, write, done. No accounts, no network,
  no data collection of any kind. Sensitive details are deliberately kept on
  paper, out of any file.
- Shared print stylesheet: `assets/style.css` (US Letter, print-safe colors).
- Build script: `build.py` (renders HTML → PDF with WeasyPrint; supports
  `--only <stem>` for a single sheet).
- Tests: `tests/test_build.py` (pytest + pypdf validation).
- `GUIDE.md` (in `guide/`) is the plain-text version of the storage guide.
- MIT licensed; see `LICENSE`.

## How to run it

```bash
pip install weasyprint pypdf pytest
python3 build.py            # builds dist/*.pdf from sheets/ and guide/
python3 build.py --only pet-info-card   # rebuild one sheet
python3 -m pytest tests/    # validate every PDF
```

## Verification results

- `python3 build.py` → all 9 pages build (8 sheets + guide) with no errors.
- `python3 -m pytest tests/ -v` → **5/5 tests pass**:
  - every sheet source exists and matches the expected list
  - every sheet + the guide builds a valid PDF with extractable text
  - every sheet/guide links the shared stylesheet
  - full kit build runs clean; every PDF parses and has ≥1 page
- Page-fitting: each PDF verified to render as exactly **1 printable page**
  (checked with pypdf page counts and visual pixel renders of sample sheets).
- During development I caught and fixed a real bug: `build.py` originally set
  `base_url` to the repo root, which silently made the stylesheet link resolve
  one directory too high — the PDFs looked unstyled while still building
  "successfully". The test suite plus visual renders caught it; `base_url` was
  removed so relative links resolve correctly.

## Known gaps

- Printing is fixed to US Letter in CSS; A4 prints fine with automatic
  margin adaptation but is not pixel-tuned.
- The house map is a hand-drawn box, by design; a labeled vector-map variant
  could be a future addition.
- No fillable-form (interactive PDF) fields — intentional for privacy, but
  a typed-fill variant could be offered later from the same sources.
- Sheets are generic (US emergency numbers on the contacts footer); other
  regions would want localized emergency numbers.
- Legal/medical content is educational only; a disclaimer is printed on the
  ICE letter, and the same caveat belongs in any commercial distribution.
