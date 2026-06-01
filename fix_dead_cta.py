#!/usr/bin/env python3
"""Répare les CTA morts des pages soutien scolaire (et autres) :
  - <a href="#"> SANS onclick dont le texte est
    "Réserver un cours d'essai" / "Évaluer le niveau" (+ variantes)
    => ajoute onclick="openBookingModal(); return false;"

Ne touche PAS les boutons qui ont déjà un onclick (ex: "Prendre rendez-vous").
openBookingModal() est défini sur les 542 pages. Idempotent.
"""

import re
import glob
from collections import Counter

HTML_DIR = "wp-plugin/logopsi-deployer/data/html"

# textes ciblés (sans accents normalisés pour la comparaison)
TARGETS = [
    "reserver un cours d'essai",
    "evaluer le niveau de mon enfant",
    "evaluer le niveau",
]

def norm(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = (t.replace("é", "e").replace("è", "e").replace("ê", "e").replace("É", "e")
           .replace("’", "'"))
    return re.sub(r"\s+", " ", t).strip().lower()

ANCHOR_RE = re.compile(r'<a\b([^>]*)>(\s*[^<]*?\s*)</a>', re.I)

def main():
    files = sorted(glob.glob(f"{HTML_DIR}/*.html"))
    stats = Counter()
    pages_changed = 0

    for f in files:
        h = open(f, encoding="utf-8", errors="replace").read()
        has_booking = "function openBookingModal" in h
        if not has_booking:
            continue

        changed = False
        def repl(m):
            nonlocal changed
            attrs, inner = m.group(1), m.group(2)
            if "onclick" in attrs.lower():
                return m.group(0)
            if 'href="#"' not in attrs.replace(" ", "").replace("'", '"') and 'href="#"' not in attrs:
                return m.group(0)
            t = norm(inner)
            if t in TARGETS:
                changed = True
                stats[t] += 1
                new_attrs = attrs + ' onclick="openBookingModal(); return false;"'
                return f'<a{new_attrs}>{inner}</a>'
            return m.group(0)

        new = ANCHOR_RE.sub(repl, h)
        if changed and new != h:
            open(f, "w", encoding="utf-8").write(new)
            pages_changed += 1

    print("=== CTA réparés (par texte) ===")
    for t, n in stats.most_common():
        print(f"  {n:4d}  {t!r}")
    print(f"\nPages modifiées: {pages_changed}")

    # Vérif : reste-t-il des CTA morts de ce type ?
    remaining = 0
    for f in files:
        h = open(f, encoding="utf-8", errors="replace").read()
        for m in ANCHOR_RE.finditer(h):
            if "onclick" in m.group(1).lower():
                continue
            if 'href="#"' not in m.group(1):
                continue
            if norm(m.group(2)) in TARGETS:
                remaining += 1
    print(f"CTA morts restants de ce type: {remaining} (doit être 0)")


if __name__ == "__main__":
    main()
