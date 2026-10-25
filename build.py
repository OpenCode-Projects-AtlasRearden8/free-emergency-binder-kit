#!/usr/bin/env python3
"""Build every printable sheet and the guide to PDF with WeasyPrint."""
import argparse
import sys
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
SHEETS_DIR = ROOT / "sheets"
GUIDE_DIR = ROOT / "guide"
DIST_DIR = ROOT / "dist"


def build_page(html_path: Path, out_pdf: Path) -> None:
    html = HTML(filename=str(html_path))
    html.write_pdf(str(out_pdf))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build emergency binder PDFs")
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="Build only the named source (stem), e.g. 'pet-info-card'",
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Suppress per-file output"
    )
    args = parser.parse_args()

    sources: list[Path] = []
    if SHEETS_DIR.is_dir():
        sources += sorted(SHEETS_DIR.glob("*.html"))
    if GUIDE_DIR.is_dir():
        sources += sorted(GUIDE_DIR.glob("*.html"))

    if args.only:
        wanted = set(args.only)
        sources = [s for s in sources if s.stem in wanted]

    if not sources:
        print("No HTML sources found.", file=sys.stderr)
        return 1

    DIST_DIR.mkdir(exist_ok=True)

    failures = []
    for src in sources:
        out = DIST_DIR / f"{src.stem}.pdf"
        try:
            build_page(src, out)
            if not args.quiet:
                print(f"built {out.relative_to(ROOT)}")
        except Exception as exc:  # noqa: BLE001
            failures.append((src, exc))
            print(f"FAILED {src.name}: {exc}", file=sys.stderr)

    if failures:
        print(f"{len(failures)} build(s) failed.", file=sys.stderr)
        return 1
    if not args.quiet:
        print(f"Done: {len(sources)} PDF(s) in dist/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
