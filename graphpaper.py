#!/usr/bin/env python3
"""Write a one-page vector graph paper PDF whose squares measure true when printed at 100%.

No dependencies: the PDF is written by hand (PDF units are points, 72 pt = 1 inch).

Usage:
  python3 graphpaper.py --square 0.25in --paper letter -o quarter-inch.pdf
  python3 graphpaper.py --square 5mm --paper a4 --major 5 -o 5mm-a4.pdf
"""
import argparse

PAPERS = {"letter": (612, 792), "a4": (595.276, 841.89), "legal": (612, 1008)}

def to_pt(s: str) -> float:
    s = s.strip().lower()
    for unit, k in (("mm", 72 / 25.4), ("cm", 72 / 2.54), ("in", 72.0), ("pt", 1.0)):
        if s.endswith(unit):
            return float(s[: -len(unit)]) * k
    raise ValueError(f"give a unit: in, mm, cm or pt ({s!r})")

def build(square_pt, paper, margin_pt, major_every, gray=0.6, major_gray=0.35):
    w, h = PAPERS[paper]
    cols = int((w - 2 * margin_pt) // square_pt)
    rows = int((h - 2 * margin_pt) // square_pt)
    gw, gh = cols * square_pt, rows * square_pt
    x0, y0 = (w - gw) / 2, (h - gh) / 2  # centre the grid; every square stays full size
    minor, major = [], []
    for i in range(cols + 1):
        x = x0 + i * square_pt
        (major if major_every and i % major_every == 0 else minor).append(f"{x:.3f} {y0:.3f} m {x:.3f} {y0 + gh:.3f} l")
    for j in range(rows + 1):
        y = y0 + j * square_pt
        (major if major_every and j % major_every == 0 else minor).append(f"{x0:.3f} {y:.3f} m {x0 + gw:.3f} {y:.3f} l")
    ops = [f"{gray} G 0.5 w", *minor, "S"]
    if major:
        ops += [f"{major_gray} G 0.9 w", *major, "S"]
    return w, h, "\n".join(ops).encode(), cols, rows

def write_pdf(path, w, h, content):
    objs = [
        # /PrintScaling /None asks viewers to default to 100% instead of "fit to page"
        b"<< /Type /Catalog /Pages 2 0 R /ViewerPreferences << /PrintScaling /None >> >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {w} {h}] /Contents 4 0 R >>".encode(),
        b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream",
    ]
    out, offsets = bytearray(b"%PDF-1.4\n"), []
    for n, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % n + o + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += b"".join(b"%010d 00000 n \n" % off for off in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    open(path, "wb").write(out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--square", default="0.25in", help="square size with unit, e.g. 0.25in, 5mm, 1cm")
    ap.add_argument("--paper", default="letter", choices=PAPERS)
    ap.add_argument("--margin", default="0.5in", help="minimum blank margin on every edge")
    ap.add_argument("--major", type=int, default=0, help="darker line every N squares (0 = none)")
    ap.add_argument("-o", "--output", default="graph-paper.pdf")
    a = ap.parse_args()
    w, h, content, cols, rows = build(to_pt(a.square), a.paper, to_pt(a.margin), a.major)
    write_pdf(a.output, w, h, content)
    print(f"{a.output}: {cols} x {rows} squares of {a.square} on {a.paper}")
