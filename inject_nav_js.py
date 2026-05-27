"""Inject the canonical mega-menu / mobile-menu / FAQ JS into pages that are
missing it, and patch the 22 'troubles' pages whose openMegaMenu lacks the
'scolaire' branch.

Two operations, both idempotent:

Issue A - 447 generated pages call toggleMobileMenu(), toggleFaq(), openMegaMenu(),
scheduleMegaClose(), cancelMegaClose() but never define them.  We append a
canonical <script> block (wrapped in <!-- LOGOPSI_NAV_JS --> markers) right
before </body>, after the existing booking-modal block.

Issue B - 22 troubles pages (under orthophonie/ and psychologie/) DO define
openMegaMenu, but their menus-map omits 'scolaire'.  We patch the map and
the scheduleMegaClose dispatch table so the Soutien Scolaire mega-menu opens.

Idempotency: a page is skipped for Issue A if it already contains BOTH
`function openMegaMenu` AND `scolaire: 'scolaire-mega'`.  Issue B is skipped
if the menus map already contains `scolaire`.

Run from repo root:  python3 inject_nav_js.py
"""

import re
from pathlib import Path


SITE_ROOT = Path("/workspaces/Logoestudios/site")


# Canonical nav-JS block - matches shared_components.get_js() ortho-/psycho-/scolaire-mega
# handling.  Wrapped in marker comments so we can detect+replace later.
NAV_JS_BLOCK = (
    '<!-- LOGOPSI_NAV_JS -->\n'
    '    <script>\n'
    '        if (window.lucide) { lucide.createIcons(); }\n'
    '\n'
    '        // Mega Menu (ortho / psycho / scolaire)\n'
    '        if (typeof megaCloseTimers === "undefined") {\n'
    '            var megaCloseTimers = { ortho: null, psycho: null, scolaire: null };\n'
    '        }\n'
    '        if (typeof openMegaMenu !== "function") {\n'
    '            window.openMegaMenu = function(menu) {\n'
    '                cancelMegaClose(menu);\n'
    '                var menus = { ortho: \'ortho-mega\', psycho: \'psycho-mega\', scolaire: \'scolaire-mega\' };\n'
    '                Object.keys(menus).forEach(function(key) {\n'
    '                    var el = document.getElementById(menus[key]);\n'
    '                    if (!el) return;\n'
    '                    if (key === menu) { el.classList.add(\'active\'); }\n'
    '                    else { el.classList.remove(\'active\'); clearTimeout(megaCloseTimers[key]); }\n'
    '                });\n'
    '            };\n'
    '        }\n'
    '        if (typeof scheduleMegaClose !== "function") {\n'
    '            window.scheduleMegaClose = function(menu) {\n'
    '                var menus = { ortho: \'ortho-mega\', psycho: \'psycho-mega\', scolaire: \'scolaire-mega\' };\n'
    '                megaCloseTimers[menu] = setTimeout(function() {\n'
    '                    var el = document.getElementById(menus[menu]);\n'
    '                    if (el) el.classList.remove(\'active\');\n'
    '                }, 200);\n'
    '            };\n'
    '        }\n'
    '        if (typeof cancelMegaClose !== "function") {\n'
    '            window.cancelMegaClose = function(menu) { clearTimeout(megaCloseTimers[menu]); };\n'
    '        }\n'
    '        if (typeof toggleMobileMenu !== "function") {\n'
    '            window.toggleMobileMenu = function() {\n'
    '                var m = document.getElementById(\'mobile-menu\');\n'
    '                if (m) m.classList.toggle(\'hidden\');\n'
    '            };\n'
    '        }\n'
    '\n'
    '        // FAQ accordion - handles both .faq-content/.faq-icon variant and the\n'
    '        // simpler "answer is the next sibling, toggle hidden" variant.\n'
    '        if (typeof toggleFaq !== "function") {\n'
    '            window.toggleFaq = function(btn) {\n'
    '                var answer = btn.nextElementSibling;\n'
    '                if (!answer) return;\n'
    '                if (answer.classList.contains(\'faq-content\')) {\n'
    '                    var icon = btn.querySelector(\'.faq-icon\');\n'
    '                    var isOpen = answer.classList.contains(\'open\');\n'
    '                    document.querySelectorAll(\'.faq-content\').forEach(function(c) { c.classList.remove(\'open\'); });\n'
    '                    document.querySelectorAll(\'.faq-icon\').forEach(function(i) { i.style.transform = \'\'; });\n'
    '                    if (!isOpen) {\n'
    '                        answer.classList.add(\'open\');\n'
    '                        if (icon) icon.style.transform = \'rotate(45deg)\';\n'
    '                    }\n'
    '                } else {\n'
    '                    answer.classList.toggle(\'hidden\');\n'
    '                    var icon2 = btn.querySelector(\'[data-lucide]\');\n'
    '                    if (icon2) {\n'
    '                        var isHidden = answer.classList.contains(\'hidden\');\n'
    '                        icon2.setAttribute(\'data-lucide\', isHidden ? \'plus\' : \'minus\');\n'
    '                        if (window.lucide) { window.lucide.createIcons(); }\n'
    '                    }\n'
    '                }\n'
    '            };\n'
    '        }\n'
    '    </script>\n'
    '    <!-- /LOGOPSI_NAV_JS -->\n'
)


# ------------------------------------------------------------------
# Issue A - injection
# ------------------------------------------------------------------

# Build the list of 447 generated pages that need the injection.
def issue_a_targets():
    targets = []
    targets.extend(sorted((SITE_ROOT / "orthophonie" / "villes").glob("*.html")))
    targets.extend(sorted((SITE_ROOT / "psychologie" / "villes").glob("*.html")))
    for subdir in ("anglais", "espagnol", "francais", "mathematiques",
                   "aide-aux-devoirs", "physique-chimie", "villes"):
        d = SITE_ROOT / "soutien-scolaire" / subdir
        if d.exists():
            targets.extend(sorted(d.glob("*.html")))
    return targets


def has_canonical_nav_js(html):
    """A page already has the canonical nav JS if it defines openMegaMenu AND
    its menus map mentions 'scolaire-mega'."""
    if "function openMegaMenu" not in html and "window.openMegaMenu" not in html:
        return False
    return "'scolaire-mega'" in html or '"scolaire-mega"' in html


def inject_nav_js(html):
    """Inject NAV_JS_BLOCK right before </body>.  If the block (with our marker)
    is already present, leave it alone."""
    if "<!-- LOGOPSI_NAV_JS -->" in html:
        return html  # already injected by us
    return html.replace("</body>", NAV_JS_BLOCK + "</body>", 1)


# ------------------------------------------------------------------
# Issue B - patch the 22 troubles pages
# ------------------------------------------------------------------

ORTHO_TROUBLES = [
    "dyslexie", "dysorthographie", "dyscalculie", "dysphasie",
    "begaiement", "tsa", "oralite", "surdite",
    "paralysie-cerebrale", "fente-palatine", "trisomie-21",
]
PSY_TROUBLES = [
    "tdah", "tca", "depression", "hpi", "anxiete",
    "harcelement-scolaire", "troubles-sommeil", "traumatismes-deuil",
    "addictions-ecrans", "enuresie", "phobie-scolaire",
]


def issue_b_targets():
    targets = []
    for name in ORTHO_TROUBLES:
        p = SITE_ROOT / "orthophonie" / f"{name}.html"
        if p.exists():
            targets.append(p)
    for name in PSY_TROUBLES:
        p = SITE_ROOT / "psychologie" / f"{name}.html"
        if p.exists():
            targets.append(p)
    return targets


def fix_troubles_scolaire_scope(html):
    """In the inline openMegaMenu / scheduleMegaClose defined around line 505 of
    the troubles pages, add the missing 'scolaire' branch.  Idempotent."""

    # 1) megaCloseTimers - add scolaire: null if missing
    timer_re = re.compile(
        r"(var\s+megaCloseTimers\s*=\s*\{\s*ortho\s*:\s*null\s*,\s*psycho\s*:\s*null\s*)(\})"
    )
    if timer_re.search(html) and "scolaire: null" not in html:
        html = timer_re.sub(r"\1, scolaire: null \2", html, count=1)

    # 2) Inside openMegaMenu: extend the menus map
    menus_open_re = re.compile(
        r"(function\s+openMegaMenu\s*\([^)]*\)\s*\{[\s\S]*?var\s+menus\s*=\s*\{\s*ortho\s*:\s*'ortho-mega'\s*,\s*psycho\s*:\s*'psycho-mega'\s*)(\})"
    )
    m = menus_open_re.search(html)
    if m and "scolaire: 'scolaire-mega'" not in m.group(0):
        html = menus_open_re.sub(r"\1, scolaire: 'scolaire-mega' \2", html, count=1)

    # 3) scheduleMegaClose - replace the ortho/psycho ternary with a menus map.
    sched_re = re.compile(
        r"function\s+scheduleMegaClose\s*\(menu\)\s*\{\s*"
        r"megaCloseTimers\[menu\]\s*=\s*setTimeout\(function\(\)\s*\{\s*"
        r"document\.getElementById\(\s*menu\s*===\s*'ortho'\s*\?\s*'ortho-mega'\s*:\s*'psycho-mega'\s*\)"
        r"\.classList\.remove\('active'\);\s*"
        r"\},\s*\d+\);\s*\}"
    )
    new_sched = (
        "function scheduleMegaClose(menu) {\n"
        "            var menus = { ortho: 'ortho-mega', psycho: 'psycho-mega', scolaire: 'scolaire-mega' };\n"
        "            megaCloseTimers[menu] = setTimeout(function() {\n"
        "                var el = document.getElementById(menus[menu]);\n"
        "                if (el) el.classList.remove('active');\n"
        "            }, 200);\n"
        "        }"
    )
    html = sched_re.sub(new_sched, html, count=1)

    return html


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main():
    # ---- Issue A ----
    targets_a = issue_a_targets()
    patched_a = 0
    skipped_a = 0
    skipped_files = []
    for f in targets_a:
        original = f.read_text(encoding="utf-8")
        if has_canonical_nav_js(original):
            skipped_a += 1
            skipped_files.append(str(f.relative_to(SITE_ROOT)))
            continue
        patched = inject_nav_js(original)
        if patched != original:
            f.write_text(patched, encoding="utf-8")
            patched_a += 1
        else:
            skipped_a += 1
            skipped_files.append(str(f.relative_to(SITE_ROOT)))

    print(f"[Issue A] Patched: {patched_a}    Skipped: {skipped_a}    Total: {len(targets_a)}")

    # ---- Issue B ----
    targets_b = issue_b_targets()
    patched_b = 0
    skipped_b = 0
    for f in targets_b:
        original = f.read_text(encoding="utf-8")
        # Idempotency: already has scolaire in its menus map?
        if "scolaire: 'scolaire-mega'" in original:
            skipped_b += 1
            continue
        patched = fix_troubles_scolaire_scope(original)
        if patched != original:
            f.write_text(patched, encoding="utf-8")
            patched_b += 1
        else:
            skipped_b += 1

    print(f"[Issue B] Patched: {patched_b}    Skipped: {skipped_b}    Total: {len(targets_b)}")


if __name__ == "__main__":
    main()
