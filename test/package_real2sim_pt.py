"""DESKTOP_DRY_RUN: produce a single offline HTML without runtime dependencies."""
from pathlib import Path
import base64

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "docs/exp/2026-10-19/real2sim2real_pt"


def main():
    html = (DECK / "index.html").read_text()
    html = html.replace('<link rel="stylesheet" href="presentation.css">',
                        "<style>\n" + (DECK / "presentation.css").read_text() + "\n</style>")
    fallback = base64.b64encode((DECK / "assets/tita-fallback.png").read_bytes()).decode()
    for name in ["model-data.js", "evidence-data.js", "presentation.js"]:
        script = (DECK / name).read_text()
        if name == "presentation.js":
            script = script.replace("assets/tita-fallback.png", "data:image/png;base64," + fallback)
        assert "</script" not in script.lower()
        html = html.replace(f'<script src="{name}"></script>', "<script>\n" + script + "\n</script>")
    output = DECK / "standalone.html"
    output.write_text(html)
    assert '<script src=' not in html and 'rel="stylesheet"' not in html
    print(f"DESKTOP_DRY_RUN PASS: standalone HTML, {output.stat().st_size:,} bytes; all assets inline")


if __name__ == "__main__":
    main()
