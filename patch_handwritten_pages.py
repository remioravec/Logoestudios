"""Patch the hand-written / legacy HTML pages so they match the rest of the site:
  - title and meta description carry the 150€/48h wording
  - booking modal HTML + JS is injected so the global popup works
  - hard-coded 'Prendre rendez-vous' / 'Prendre RDV' CTAs trigger openBookingModal()

Idempotent: pages that already contain id="booking-modal" are skipped.

Run from repo root:  python3 patch_handwritten_pages.py
"""

import re
from pathlib import Path

from seo_titles import (
    HANDWRITTEN_TITLES, HANDWRITTEN_META_DESCS, SUFFIX,
    title_for_scolaire_n2, meta_desc_for_scolaire_n2,
    SUBJECT_LABELS, LEVEL_LABELS,
)
from shared_components import get_booking_modal, get_booking_js


SITE_ROOT = Path("/workspaces/Logoestudios/site")
SUBJECTS = ("mathematiques", "francais", "anglais", "espagnol", "aide-aux-devoirs", "physique-chimie")


def title_and_meta_for(rel_path):
    """Return (title, meta_desc) for a hand-written page, or (None, None) to skip retitling."""
    # 1) Explicit overrides (root + section hubs)
    handw = HANDWRITTEN_TITLES.get(rel_path)
    if handw is not None or rel_path in HANDWRITTEN_TITLES:
        return handw, HANDWRITTEN_META_DESCS.get(rel_path)

    # Path is "site/<...>" — strip the prefix for routing.
    parts = rel_path.split("/")
    if parts[0] == "site":
        parts = parts[1:]
    # 2) Subject hub:  soutien-scolaire/<subject>/index.html
    if len(parts) == 3 and parts[0] == "soutien-scolaire" and parts[2] == "index.html":
        subject = parts[1]
        if subject in SUBJECTS:
            subj_label = SUBJECT_LABELS.get(subject, subject)
            title = "Bilan " + subj_label + " en ligne — 150€, sous 48h" + SUFFIX
            meta = ("Bilan pédagogique en " + subj_label + " en ligne — 150€, sous 48h. "
                    "Enseignants qualifiés, cours particuliers 100% en visio.")
            return title, meta

    # 3) Level-only page:  soutien-scolaire/<subject>/<level>.html (no city dash)
    if (len(parts) == 3 and parts[0] == "soutien-scolaire"
            and parts[1] in SUBJECTS and parts[2].endswith(".html")
            and "-" not in parts[2][:-5]):
        subject = parts[1]
        level = parts[2][:-5]
        if level in LEVEL_LABELS:
            return (title_for_scolaire_n2(subject, level),
                    meta_desc_for_scolaire_n2(subject, level))

    return None, None


CTA_TEXTS = ("Prendre rendez-vous", "Prendre RDV", "Prendre Rendez-vous")
# Anchor hrefs that point to an in-page contact section we are replacing with the popup.
INPAGE_HREF_RE = re.compile(r'href="(#contact|#cta)"')


def patch_cta_anchors(html):
    """Replace <a href="#contact"|"#cta" ...>...Prendre rendez-vous...</a> with popup trigger."""
    pattern = re.compile(
        r'<a\s+href="(#contact|#cta)"([^>]*)>(\s*[^<]*?(?:Prendre rendez-vous|Prendre RDV|Prendre Rendez-vous)[^<]*?\s*)</a>',
        re.IGNORECASE | re.DOTALL,
    )
    return pattern.sub(
        lambda m: '<a href="#" onclick="openBookingModal(); return false;"' + m.group(2) + '>' + m.group(3) + '</a>',
        html,
    )


def patch_title_meta(html, new_title, new_meta):
    if new_title is not None:
        html = re.sub(r'<title>[^<]*</title>',
                      '<title>' + new_title + '</title>', html, count=1)
    if new_meta is not None:
        html = re.sub(r'<meta\s+name="description"\s+content="[^"]*"\s*/?>',
                      '<meta name="description" content="' + new_meta + '">',
                      html, count=1)
    return html


def inject_booking(html):
    """Inject (or refresh) booking modal HTML+JS right before </body>.

    Replaces stale modals (e.g. ones with formsubmit.co or old JS) with the current
    version. Idempotent when up-to-date.
    """
    insertion = get_booking_modal() + "<script>\n" + get_booking_js() + "\n</script>\n"

    # Strip any existing modal block — the marker comment is always at its start
    if "<!-- LOGOPSI_BOOKING_MODAL -->" in html:
        pattern = re.compile(
            r'<!-- LOGOPSI_BOOKING_MODAL -->.*?</script>\s*',
            re.DOTALL,
        )
        html = pattern.sub("", html, count=1)
    elif 'id="booking-modal"' in html:
        # Fallback: no marker but an old modal exists — remove from the div up to the script close
        pattern = re.compile(
            r'<div id="booking-modal".*?</script>\s*',
            re.DOTALL,
        )
        html = pattern.sub("", html, count=1)

    return html.replace("</body>", insertion + "</body>", 1)


def patch_file(path):
    # HANDWRITTEN_TITLES keys are "site/<rel>" — match that.
    rel = "site/" + str(path.relative_to(SITE_ROOT))
    original = path.read_text(encoding="utf-8")

    new_title, new_meta = title_and_meta_for(rel)
    patched = patch_title_meta(original, new_title, new_meta)
    patched = patch_cta_anchors(patched)
    patched = inject_booking(patched)  # itself idempotent

    if patched != original:
        path.write_text(patched, encoding="utf-8")
        return True
    return False


def main():
    files = sorted(SITE_ROOT.rglob("*.html"))
    patched = 0
    skipped = 0
    for f in files:
        if patch_file(f):
            patched += 1
        else:
            skipped += 1
    print(f"Patched: {patched}    Skipped (already current): {skipped}    Total: {len(files)}")


if __name__ == "__main__":
    main()
