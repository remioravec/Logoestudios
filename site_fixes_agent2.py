"""Agent 2 site fixes:
  A. Inject Tarifs link into navbar + mobile menu + footer on ~531 pages.
  B. Replace old mailto domain logopsistudios.com -> logopsiestudios.com on 3 pages.
  C. Add missing meta description on site/orthophonie/index.html.
  D. Typography accents: A propos -> À propos (text only) ; Decouvr/decouvr ->
     Découvr/découvr (covers Decouvrez, Decouverte, Decouvert and lowercase).

All four fixes are idempotent. Run from repo root:
    python3 site_fixes_agent2.py
"""

import re
from pathlib import Path

SITE_ROOT = Path("/workspaces/Logoestudios/site")

# Pages that already have Tarifs - never re-inject. Also: NEVER touch tarifs.html itself.
SKIP_TARIFS = {
    "index.html",
    "contact.html",
    "a-propos.html",
    "mentions-legales.html",
    "tarifs.html",
    "orthophonie/index.html",
    "psychologie/index.html",
    "soutien-scolaire/index.html",
}


def rel(path):
    return str(path.relative_to(SITE_ROOT)).replace("\\", "/")


def depth(path):
    """Depth of file inside site/ as number of directory hops before the filename.

    site/index.html             -> 0
    site/orthophonie/dyslexie.html -> 1
    site/orthophonie/villes/paris.html -> 2
    """
    return len(path.relative_to(SITE_ROOT).parts) - 1


def prefix_for(path):
    d = depth(path)
    if d == 0:
        return "./"
    return "../" * d


# ---------------------------------------------------------------------------
# Fix A — inject Tarifs link
# ---------------------------------------------------------------------------

# Two desktop navbar variants:
#   "legacy" (contact.html / soutien-scolaire/*) -> nav links have
#       class="text-dark hover:text-primary font-medium transition-colors py-5"
#   "modern" (orthophonie/dyslexie.html, all city pages) -> nav links use
#       class="px-4 py-2 font-semibold text-[15px] text-gray-800 hover:text-primary transition-colors"
#
# We detect which by looking at the surrounding scolaire-trigger button's class string.

LEGACY_NAV_BTN_CLASS = "flex items-center space-x-1 text-dark hover:text-primary font-medium transition-colors py-5"
MODERN_NAV_BTN_CLASS = "px-4 py-2 flex items-center gap-1 font-semibold text-[15px] text-gray-800 hover:text-primary transition-colors"


def inject_navbar_tarifs(html, href):
    """Insert a Tarifs <a> right after the scolaire-trigger </div>, but before
    the parent container's closing </div>.

    Idempotent: if tarifs.html already appears in navbar block, skip.
    """
    # Find the scolaire-trigger block. The pattern is:
    #   <div ... id="scolaire-trigger" ...> ... </div>
    # followed (after optional whitespace) by </div> that closes the menu wrapper.
    # We detect that "Tarifs" is already there by looking for tarifs.html within
    # the next ~400 chars after scolaire-trigger.
    m = re.search(r'(<div[^>]*id="scolaire-trigger"[^>]*>.*?</div>)', html, re.DOTALL)
    if not m:
        return html, False

    after_idx = m.end()
    # Idempotency: tarifs already injected close by?
    if "tarifs.html" in html[after_idx:after_idx + 400]:
        return html, False

    # Decide which class variant to use by sniffing the surrounding text.
    snippet = html[m.start():m.end()]
    if 'px-4 py-2 flex items-center gap-1 font-semibold text-[15px]' in snippet:
        # modern variant
        tarifs_link = ('\n                    '
                       f'<a href="{href}" class="px-4 py-2 font-semibold text-[15px] text-gray-800 hover:text-primary transition-colors">Tarifs</a>')
    else:
        # legacy variant
        tarifs_link = ('\n                    '
                       f'<a href="{href}" class="text-dark hover:text-primary font-medium transition-colors py-5">Tarifs</a>')

    new_html = html[:after_idx] + tarifs_link + html[after_idx:]
    return new_html, True


def inject_mobile_tarifs(html, href):
    """Inject Tarifs in the mobile menu, after the Soutien Scolaire link,
    before the Prendre RDV CTA. Idempotent."""
    # Find the mobile-menu block.
    m = re.search(r'<div\s+id="mobile-menu"[^>]*>(.*?)</div>\s*</div>\s*</nav>', html, re.DOTALL)
    if not m:
        return html, False

    block = m.group(0)
    if "tarifs.html" in block:
        return html, False

    # Find the Soutien Scolaire <a> and insert Tarifs right after its closing </a>.
    # Two variants:
    #   "block text-dark hover:text-primary font-medium py-2" (legacy)
    #   "block text-gray-900 hover:text-primary font-semibold py-2" (modern)
    ss_pat = re.compile(
        r'(<a[^>]*soutien-scolaire/[^>]*>Soutien Scolaire</a>)',
        re.IGNORECASE,
    )
    sm = ss_pat.search(block)
    if not sm:
        return html, False

    # Choose className matching neighbours by inspecting Soutien Scolaire's class attribute.
    ss_link = sm.group(1)
    if 'text-gray-900' in ss_link:
        new_link = (f'\n                <a href="{href}" class="block text-gray-900 '
                    'hover:text-primary font-semibold py-2">Tarifs</a>')
    else:
        new_link = (f'\n                <a href="{href}" class="block text-dark '
                    'hover:text-primary font-medium py-2">Tarifs</a>')

    new_block = block[:sm.end()] + new_link + block[sm.end():]
    return html[:m.start()] + new_block + html[m.end():], True


def inject_footer_tarifs(html, href):
    """Insert Tarifs in the footer legal row, between A propos and Espace membre.
    If Espace membre is absent (legacy footer with only mentions-legales/Contact/
    À propos), insert Tarifs at the end of the À propos line.

    Idempotent: if any tarifs.html link already exists in the footer block we leave
    it alone."""
    # Locate the footer block. Use the legal row container.
    # The row looks like:
    #   <div class="flex ... mt-4 md:mt-0">
    #     <a href="...mentions-legales.html" ...>Mentions légales</a>
    #     <a href="...contact.html" ...>Contact</a>
    #     <a href="...a-propos.html" ...>À propos</a>
    #     [<a href="...login" ...>Espace membre</a>]
    #   </div>
    legal_pat = re.compile(
        r'(<div class="flex[^"]*mt-4 md:mt-0"[^>]*>)(.*?)(</div>)',
        re.DOTALL,
    )
    legal_match = None
    for m in legal_pat.finditer(html):
        inner = m.group(2)
        if "mentions-legales.html" in inner and "a-propos.html" in inner:
            legal_match = m
            break
    if not legal_match:
        return html, False

    inner = legal_match.group(2)
    if "tarifs.html" in inner:
        return html, False

    # Choose class style to mimic siblings — they all use:
    #   class="text-gray-500 hover:text-primary text-sm transition-colors"
    new_link = (f'\n                    <a href="{href}" class="text-gray-500 '
                'hover:text-primary text-sm transition-colors">Tarifs</a>')

    # Insert before Espace membre if present, otherwise after À propos.
    esp_pat = re.compile(r'(\s*<a[^>]*Espace membre</a>)', re.DOTALL)
    esp = esp_pat.search(inner)
    if esp:
        new_inner = inner[:esp.start()] + new_link + inner[esp.start():]
    else:
        # Append after the À propos line.
        ap_pat = re.compile(r'(<a[^>]*a-propos\.html[^>]*>À propos</a>)', re.DOTALL)
        ap = ap_pat.search(inner)
        if not ap:
            return html, False
        new_inner = inner[:ap.end()] + new_link + inner[ap.end():]

    new_html = (html[:legal_match.start()] +
                legal_match.group(1) + new_inner + legal_match.group(3) +
                html[legal_match.end():])
    return new_html, True


def fix_a_inject_tarifs():
    patched = 0
    skipped = 0
    edge = []
    files = sorted(SITE_ROOT.rglob("*.html"))
    for path in files:
        r = rel(path)
        if r in SKIP_TARIFS:
            skipped += 1
            continue

        original = path.read_text(encoding="utf-8")
        href = prefix_for(path) + "tarifs.html"

        new = original
        nav_changed = mob_changed = ftr_changed = False
        new, nav_changed = inject_navbar_tarifs(new, href)
        new, mob_changed = inject_mobile_tarifs(new, href)
        new, ftr_changed = inject_footer_tarifs(new, href)

        if new != original:
            path.write_text(new, encoding="utf-8")
            patched += 1
        else:
            skipped += 1
            # Edge: if file has none of the three blocks, flag it.
            if "scolaire-trigger" not in original and "mobile-menu" not in original:
                edge.append(r)

    print(f"[A] Tarifs injection — Patched: {patched}    Skipped: {skipped}")
    if edge:
        print(f"[A] Edge cases (no nav/mobile blocks found): {len(edge)} files; "
              f"first few: {edge[:5]}")


# ---------------------------------------------------------------------------
# Fix B — mailto domain replacement
# ---------------------------------------------------------------------------

def fix_b_mailto():
    targets = [
        SITE_ROOT / "index.html",
        SITE_ROOT / "contact.html",
        SITE_ROOT / "mentions-legales.html",
    ]
    patched = 0
    skipped = 0
    for p in targets:
        original = p.read_text(encoding="utf-8")
        # Replace exact old domain everywhere (both href and visible text).
        new = original.replace("logopsistudios.com", "logopsiestudios.com")
        if new != original:
            p.write_text(new, encoding="utf-8")
            patched += 1
        else:
            skipped += 1
    print(f"[B] Mailto domain — Patched: {patched}    Skipped: {skipped}")


# ---------------------------------------------------------------------------
# Fix C — orthophonie/index.html meta description
# ---------------------------------------------------------------------------

ORTHO_META_DESC = ("Bilan orthophonique en ligne pour enfants et adolescents — "
                   "150€, sous 48h. Orthophonistes diplômés d'État. Tous troubles "
                   "du langage et des apprentissages.")


def fix_c_meta_desc():
    p = SITE_ROOT / "orthophonie" / "index.html"
    original = p.read_text(encoding="utf-8")
    if re.search(r'<meta\s+name="description"', original):
        print("[C] orthophonie/index.html meta description — already present (skipped)")
        return

    # Insert right after the viewport meta tag.
    new = re.sub(
        r'(<meta\s+name="viewport"[^>]*>)',
        r'\1\n    <meta name="description" content="' + ORTHO_META_DESC + '">',
        original,
        count=1,
    )
    if new == original:
        print("[C] orthophonie/index.html meta description — viewport tag not found; skipped")
        return
    p.write_text(new, encoding="utf-8")
    print("[C] orthophonie/index.html meta description — Patched: 1")


# ---------------------------------------------------------------------------
# Fix D — typography
# ---------------------------------------------------------------------------

# Replacements we apply unconditionally on text (regex with HTML attr safeguards).
DECOUVR_PAIRS = [
    ("Decouvrez", "Découvrez"),
    ("decouvrez", "découvrez"),
    ("Decouverte", "Découverte"),
    ("decouverte", "découverte"),
    ("Decouvert",  "Découvert"),
    ("decouvert",  "découvert"),
]


def fix_d_typography():
    patched = 0
    skipped = 0
    files = sorted(SITE_ROOT.rglob("*.html"))
    for p in files:
        original = p.read_text(encoding="utf-8")
        new = original

        # "A propos" -> "À propos" only as visible text. The only real
        # occurrences (per grep) are inside <span>...</span> or as bare body
        # text near "A propos de". We scope the replacement to the literal
        # tokens ">A propos<" and ">A propos " (followed by text) and the
        # word boundary "A propos de" pattern. Conservative.
        new = new.replace(">A propos<", ">À propos<")
        new = new.replace("\nA propos ",   "\nÀ propos ")
        new = new.replace(" A propos de",  " À propos de")
        new = new.replace(">\n                A propos ",  ">\n                À propos ")
        new = re.sub(r'(?<=>)(\s*)A propos\b', r'\1À propos', new)

        # Decouvr* / Decouvert* — substring replacement is safe because the
        # accented form never appears as part of a URL/class/path.
        for bad, good in DECOUVR_PAIRS:
            new = new.replace(bad, good)

        if new != original:
            p.write_text(new, encoding="utf-8")
            patched += 1
        else:
            skipped += 1
    print(f"[D] Typography — Patched: {patched}    Skipped: {skipped}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    fix_a_inject_tarifs()
    fix_b_mailto()
    fix_c_meta_desc()
    fix_d_typography()


if __name__ == "__main__":
    main()
