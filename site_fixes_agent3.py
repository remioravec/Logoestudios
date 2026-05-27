#!/usr/bin/env python3
"""
Agent 3 — CTA button normalization for Logo Etudes static site.

Fix A: rounded-lg -> rounded-full ONLY inside <a>/<button> tags whose class
       contains bg-primary OR border-2 border-primary. Decorative
       <div class="... bg-primary rounded-lg ...">  blocks are left alone.

Fix B: Canonicalize CTA wording (inside text content of <a>/<button>/<span>):
         "Reserver un cours" / "Reserver un cours d'essai gratuit" -> "Reserver un cours d'essai"
         "Reserver un bilan" -> "Reserver mon bilan"
         "Prendre rendez-vous avec un expert" -> "Prendre rendez-vous"
       (handles both accented "Réserver" and bare "Reserver").
       Keeps "Prendre RDV" and "Contactez-nous" as-is.

Fix C: For any <a href="#contact"> or <a href="#cta"> CTA (has bg-primary or
       border-2 border-primary) whose anchor target does NOT exist in the
       same page, rewrite to:
         href="#" onclick="openBookingModal(); return false;"
       Idempotent: skips links that already include openBookingModal.

Constraints:
- Skips tarifs.html.
- Will not modify text inside the LOGOPSI_BOOKING_MODAL block or LOGOPSI_NAV_JS block.
- Only edits static HTML under /workspaces/Logoestudios/site/.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/workspaces/Logoestudios/site")
SKIP_FILENAMES = {"tarifs.html"}

# Regions of the file we should never touch.
GUARD_BLOCKS = [
    (re.compile(r"<!--\s*LOGOPSI_BOOKING_MODAL\s*-->.*?<!--\s*/LOGOPSI_BOOKING_MODAL\s*-->",
                re.DOTALL),),
    (re.compile(r"<!--\s*LOGOPSI_NAV_JS\s*-->.*?<!--\s*/LOGOPSI_NAV_JS\s*-->",
                re.DOTALL),),
]

# Tag with class attribute (single line).
TAG_WITH_CLASS_RE = re.compile(
    r'<(a|button)\b([^>]*?)\bclass="([^"]*)"([^>]*)>',
    re.IGNORECASE,
)


def iter_html_files() -> list[Path]:
    files = []
    for p in ROOT.rglob("*.html"):
        if p.name in SKIP_FILENAMES:
            continue
        files.append(p)
    return sorted(files)


def mask_guarded(content: str) -> tuple[str, list[tuple[int, int, str]]]:
    """Replace guarded blocks with placeholders so regex won't touch them.
    Returns (masked_content, slots) where slots is a list of (start, end, original).
    """
    slots: list[tuple[int, int, str]] = []
    masked = content
    # Apply each guard pattern; we accumulate replacements.
    # Strategy: collect spans first, then rebuild.
    spans: list[tuple[int, int]] = []
    for (pat,) in GUARD_BLOCKS:
        for m in pat.finditer(content):
            spans.append(m.span())
    if not spans:
        return content, []
    # Merge overlapping spans
    spans.sort()
    merged: list[tuple[int, int]] = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    # Build masked content with placeholders
    out = []
    prev = 0
    for i, (s, e) in enumerate(merged):
        out.append(content[prev:s])
        token = f"\0GUARDED_BLOCK_{i}\0"
        out.append(token)
        slots.append((s, e, content[s:e]))
        prev = e
    out.append(content[prev:])
    return "".join(out), slots


def unmask_guarded(content: str, slots: list[tuple[int, int, str]]) -> str:
    for i, (_s, _e, orig) in enumerate(slots):
        token = f"\0GUARDED_BLOCK_{i}\0"
        content = content.replace(token, orig)
    return content


# ----- Fix A: rounded-lg -> rounded-full on CTA <a>/<button> tags -----

def fix_a_rounded_full(content: str) -> tuple[str, int]:
    """Walk every <a>/<button> tag with a class attr; if the class contains
    bg-primary OR (border-2 border-primary), replace rounded-lg -> rounded-full.
    Returns (new_content, patched_count)."""
    patched = 0

    def repl(m: re.Match) -> str:
        nonlocal patched
        tag = m.group(1)
        pre = m.group(2)
        cls = m.group(3)
        post = m.group(4)
        is_cta = (
            "bg-primary" in cls
            or "border-2 border-primary" in cls
        )
        if not is_cta:
            return m.group(0)
        if "rounded-lg" not in cls:
            return m.group(0)
        new_cls = cls.replace("rounded-lg", "rounded-full")
        if new_cls == cls:
            return m.group(0)
        patched += 1
        return f'<{tag}{pre}class="{new_cls}"{post}>'

    new_content = TAG_WITH_CLASS_RE.sub(repl, content)
    return new_content, patched


# ----- Fix B: Wording normalization -----

# We replace strictly inside text content of <a>, <button>, <span>. To stay safe
# we craft replacements that anchor on the next characters following the wording
# (typically whitespace + < or end of tag, or specific suffix like " gratuit").

def fix_b_wording(content: str) -> tuple[str, int]:
    """Normalize CTA wording. Returns (new_content, patched_count)."""
    patched = 0

    # Mapping is order-sensitive: do longer/more-specific strings first
    # so we don't double-rewrite.
    replacements: list[tuple[str, str]] = [
        # Long form first
        ("Réserver un cours d'essai gratuit", "Réserver un cours d'essai"),
        ("Reserver un cours d'essai gratuit",  "Reserver un cours d'essai"),
        ("Prendre rendez-vous avec un expert", "Prendre rendez-vous"),
        # bare "Réserver un cours" / "Réserver un bilan" — only when NOT followed
        # by " d'essai" / " orthophonique" / etc. We use a lookahead.
    ]

    for old, new in replacements:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            patched += count

    # Now the trickier ones with negative lookaheads:
    # "Réserver un cours" not already followed by " d'essai"
    pat_cours = re.compile(r"R[ée]server un cours(?! d'essai)")
    def repl_cours(m: re.Match) -> str:
        nonlocal patched
        patched += 1
        # Preserve the leading capitalization style of the match
        head = m.group(0)
        if head.startswith("Réserver"):
            return "Réserver un cours d'essai"
        return "Reserver un cours d'essai"
    content = pat_cours.sub(repl_cours, content)

    # "Réserver un bilan" -> "Réserver mon bilan"
    # but DO NOT touch "Reserver un bilan orthophonique" (ortho/index hero — but
    # actually that wording also wants to be canonical "Réserver mon bilan").
    # The audit only lists 4 variants; for safety we limit to plain ones.
    pat_bilan = re.compile(r"R[ée]server un bilan(?! orthophonique)")
    def repl_bilan(m: re.Match) -> str:
        nonlocal patched
        patched += 1
        head = m.group(0)
        if head.startswith("Réserver"):
            return "Réserver mon bilan"
        return "Reserver mon bilan"
    content = pat_bilan.sub(repl_bilan, content)

    return content, patched


# ----- Fix C: Dead anchors -> openBookingModal -----

DEAD_ANCHOR_RE = re.compile(
    r'<a\b([^>]*?)\bhref="(#contact|#cta)"([^>]*?)\bclass="([^"]*)"([^>]*)>',
    re.IGNORECASE,
)

# Same content but with class= before href= ordering
DEAD_ANCHOR_RE_2 = re.compile(
    r'<a\b([^>]*?)\bclass="([^"]*)"([^>]*?)\bhref="(#contact|#cta)"([^>]*)>',
    re.IGNORECASE,
)


def fix_c_dead_anchors(content: str) -> tuple[str, int]:
    """For each <a href="#contact"|"#cta"> with bg-primary or border-2 border-primary,
    if the same anchor id does NOT exist on the page, rewrite the link to call
    openBookingModal(). Skip if already has openBookingModal."""
    patched = 0

    # Detect existing ids in the page.
    id_pat = re.compile(r'\bid="([^"]+)"')
    page_ids = set(id_pat.findall(content))

    def is_cta_class(cls: str) -> bool:
        return ("bg-primary" in cls) or ("border-2 border-primary" in cls)

    def rewrite_attrs(full_match: str, target: str, cls: str) -> str | None:
        """Return rewritten <a ...> string if dead+CTA+not-already-modal, else None."""
        if not is_cta_class(cls):
            return None
        anchor_id = target.lstrip("#")
        if anchor_id in page_ids:
            return None  # alive anchor; leave alone
        if "openBookingModal" in full_match:
            return None  # already wired

        # Strip href and replace with href="#" onclick="openBookingModal(); return false;"
        # Strategy: regex-replace within full_match.
        new = re.sub(
            r'href="(?:#contact|#cta)"',
            'href="#" onclick="openBookingModal(); return false;"',
            full_match,
            count=1,
        )
        return new

    def repl1(m: re.Match) -> str:
        nonlocal patched
        target = m.group(2)
        cls = m.group(4)
        new = rewrite_attrs(m.group(0), target, cls)
        if new is None:
            return m.group(0)
        patched += 1
        return new

    def repl2(m: re.Match) -> str:
        nonlocal patched
        target = m.group(4)
        cls = m.group(2)
        new = rewrite_attrs(m.group(0), target, cls)
        if new is None:
            return m.group(0)
        patched += 1
        return new

    content = DEAD_ANCHOR_RE.sub(repl1, content)
    content = DEAD_ANCHOR_RE_2.sub(repl2, content)
    return content, patched


# ----- Driver -----

def run() -> None:
    files = iter_html_files()
    print(f"Scanning {len(files)} HTML files under {ROOT}\n")

    totals = {"A_patched": 0, "A_skipped": 0,
              "B_patched": 0, "B_skipped": 0,
              "C_patched": 0, "C_skipped": 0,
              "files_changed": 0}

    for f in files:
        original = f.read_text(encoding="utf-8")
        masked, slots = mask_guarded(original)

        new_a, a_n = fix_a_rounded_full(masked)
        new_b, b_n = fix_b_wording(new_a)
        new_c, c_n = fix_c_dead_anchors(new_b)

        result = unmask_guarded(new_c, slots)

        if a_n: totals["A_patched"] += a_n
        else:   totals["A_skipped"] += 1
        if b_n: totals["B_patched"] += b_n
        else:   totals["B_skipped"] += 1
        if c_n: totals["C_patched"] += c_n
        else:   totals["C_skipped"] += 1

        if result != original:
            f.write_text(result, encoding="utf-8")
            totals["files_changed"] += 1

    print("=== AGENT 3 SUMMARY ===")
    print(f"Files scanned     : {len(files)}")
    print(f"Files changed     : {totals['files_changed']}")
    print(f"A rounded-full    : {totals['A_patched']} replacements "
          f"({totals['A_skipped']} files w/ no A change)")
    print(f"B wording fixes   : {totals['B_patched']} replacements "
          f"({totals['B_skipped']} files w/ no B change)")
    print(f"C anchor rewrites : {totals['C_patched']} replacements "
          f"({totals['C_skipped']} files w/ no C change)")


if __name__ == "__main__":
    run()
