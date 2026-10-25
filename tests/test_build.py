"""Tests: every sheet must build successfully into a valid PDF."""
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SHEETS = sorted((ROOT / "sheets").glob("*.html"))
GUIDES = sorted((ROOT / "guide").glob("*.html"))


def build(stem: str) -> Path:
    out = ROOT / "dist" / f"{stem}.pdf"
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "--only", stem, "--quiet"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"build.py failed for {stem}: {result.stderr}"
    assert out.exists(), f"dist/{stem}.pdf was not produced"
    return out


def is_valid_pdf(path: Path) -> PdfReader:
    reader = PdfReader(str(path))
    assert len(reader.pages) >= 1, f"{path.name} has no pages"
    first_page = reader.pages[0]
    extracted = first_page.extract_text() or ""
    assert extracted.strip(), f"{path.name} page 1 has no extractable text"
    assert path.stat().st_size > 1000, f"{path.name} looks empty"
    return reader


def test_sheets_exist():
    stems = sorted(p.stem for p in SHEETS)
    expected = [
        "contacts-checkin",
        "grab-and-go",
        "household-info",
        "ice-letter",
        "insurance-one-pager",
        "pet-info-card",
        "utility-shutoff-map",
        "yearly-review",
    ]
    assert stems == expected


def test_each_sheet_builds_valid_pdf():
    for sheet in SHEETS:
        pdf_path = build(sheet.stem)
        reader = is_valid_pdf(pdf_path)
        assert len(reader.pages) == 1, (
            f"{sheet.stem}: expected a single-page printable, "
            f"got {len(reader.pages)} pages"
        )
        pdf_path.unlink()


def test_guide_builds_valid_pdf():
    for guide in GUIDES:
        pdf_path = build(guide.stem)
        is_valid_pdf(pdf_path)
        pdf_path.unlink()


def test_every_html_links_shared_stylesheet():
    for html_path in SHEETS + GUIDES:
        text = html_path.read_text(encoding="utf-8")
        assert "../assets/style.css" in text, (
            f"{html_path.name} does not link the shared stylesheet"
        )


def test_kit_builds_clean():
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "--quiet"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"full build failed: {result.stderr}"
    pdfs = sorted((ROOT / "dist").glob("*.pdf"))
    assert len(pdfs) == len(SHEETS) + len(GUIDES)
    for pdf in pdfs:
        is_valid_pdf(pdf)
