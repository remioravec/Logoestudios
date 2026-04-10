#!/usr/bin/env python3
"""QA script: internal link checker + structural consistency for the static site."""

import os
import re
from pathlib import Path
from urllib.parse import unquote
from collections import defaultdict

SITE_ROOT = Path("/workspaces/Logoestudios/site")

def find_html_files():
    return sorted(SITE_ROOT.rglob("*.html"))

def extract_hrefs(html_content):
    """Extract all href values from anchor tags."""
    return re.findall(r'<a\s[^>]*?href=["\']([^"\']*)["\']', html_content, re.IGNORECASE)

def is_internal_link(href):
    if not href or href.startswith(("#", "mailto:", "tel:", "http://", "https://", "javascript:")):
        return False
    return True

def resolve_link(source_file, href):
    """Resolve a relative or root-relative href to an absolute filesystem path."""
    href = href.split("#")[0].split("?")[0]  # strip fragment/query
    href = unquote(href)
    if not href:
        return None
    if href.startswith("/"):
        # Absolute from repo root -- try interpreting relative to SITE_ROOT parent
        # e.g. /site/orthophonie/foo.html
        candidate = Path("/workspaces/Logoestudios") / href.lstrip("/")
        if candidate.exists():
            return candidate
        # Also try relative to site root itself
        candidate2 = SITE_ROOT / href.lstrip("/")
        return candidate2 if candidate2.exists() else candidate
    else:
        return (source_file.parent / href).resolve()

def main():
    html_files = find_html_files()
    all_paths = {f.resolve() for f in html_files}

    total_internal_links = 0
    broken_links = []  # (source, href, resolved)
    page_link_counts = {}  # path -> count of internal links
    pages_missing_scolaire_mega = []
    pages_missing_footer_scolaire = []

    for f in html_files:
        content = f.read_text(encoding="utf-8", errors="replace")
        hrefs = extract_hrefs(content)
        internal = [h for h in hrefs if is_internal_link(h)]

        # Deduplicate per page for counting unique targets (but count total for stats)
        total_internal_links += len(internal)
        page_link_counts[f] = len(internal)

        for href in internal:
            resolved = resolve_link(f, href)
            if resolved is None:
                continue
            if not resolved.exists():
                broken_links.append((f, href, resolved))

        # Structural checks
        if "scolaire-mega" not in content:
            pages_missing_scolaire_mega.append(f)

        # Check footer contains "Soutien Scolaire" section
        footer_match = re.search(r'<footer[\s\S]*</footer>', content, re.IGNORECASE)
        if footer_match:
            if "Soutien Scolaire" not in footer_match.group():
                pages_missing_footer_scolaire.append(f)
        else:
            pages_missing_footer_scolaire.append(f)

    orphan_pages = [f for f, c in page_link_counts.items() if c == 0]

    # --- Compute incoming link counts to find pages never linked to ---
    incoming = defaultdict(int)
    for f in html_files:
        content = f.read_text(encoding="utf-8", errors="replace")
        hrefs = extract_hrefs(content)
        for href in hrefs:
            if not is_internal_link(href):
                continue
            resolved = resolve_link(f, href)
            if resolved and resolved.exists():
                incoming[resolved.resolve()] += 1

    never_linked_to = sorted(f for f in html_files if f.resolve() not in incoming)

    # ==================== REPORT ====================
    print("=" * 70)
    print("QA REPORT — Internal Linking & Structure")
    print("=" * 70)

    print(f"\nTotal HTML pages: {len(html_files)}")
    print(f"Total internal links (all <a href>): {total_internal_links}")
    print(f"Average internal links per page: {total_internal_links / len(html_files):.1f}")

    print(f"\n--- BROKEN LINKS ({len(broken_links)}) ---")
    if broken_links:
        for src, href, resolved in sorted(broken_links, key=lambda x: (str(x[0]), x[1])):
            print(f"  SOURCE: {src.relative_to(SITE_ROOT)}")
            print(f"    HREF: {href}")
            print(f"    RESOLVED TO: {resolved}")
            print()
    else:
        print("  None found. All internal links resolve correctly.")

    print(f"\n--- PAGES WITH 0 OUTGOING INTERNAL LINKS ({len(orphan_pages)}) ---")
    for p in sorted(orphan_pages):
        print(f"  {p.relative_to(SITE_ROOT)}")

    print(f"\n--- PAGES NEVER LINKED TO (no incoming links) ({len(never_linked_to)}) ---")
    for p in never_linked_to:
        print(f"  {p.relative_to(SITE_ROOT)}")

    print(f"\n--- MISSING 'scolaire-mega' MEGA MENU ({len(pages_missing_scolaire_mega)}) ---")
    if pages_missing_scolaire_mega:
        for p in sorted(pages_missing_scolaire_mega):
            print(f"  {p.relative_to(SITE_ROOT)}")
    else:
        print("  All pages contain the scolaire-mega menu.")

    print(f"\n--- MISSING 'Soutien Scolaire' IN FOOTER ({len(pages_missing_footer_scolaire)}) ---")
    if pages_missing_footer_scolaire:
        for p in sorted(pages_missing_footer_scolaire):
            print(f"  {p.relative_to(SITE_ROOT)}")
    else:
        print("  All pages have 'Soutien Scolaire' in the footer.")

    # Link coverage summary
    print("\n--- LINK COVERAGE SUMMARY ---")
    linked_to_count = len([f for f in html_files if f.resolve() in incoming])
    print(f"  Pages with at least 1 incoming link: {linked_to_count}/{len(html_files)} ({100*linked_to_count/len(html_files):.1f}%)")
    has_outgoing = len([f for f, c in page_link_counts.items() if c > 0])
    print(f"  Pages with at least 1 outgoing link: {has_outgoing}/{len(html_files)} ({100*has_outgoing/len(html_files):.1f}%)")
    print(f"  Broken links: {len(broken_links)}")
    print(f"  Pages missing mega menu: {len(pages_missing_scolaire_mega)}")
    print(f"  Pages missing footer section: {len(pages_missing_footer_scolaire)}")

if __name__ == "__main__":
    main()
