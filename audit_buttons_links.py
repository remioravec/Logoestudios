#!/usr/bin/env python3
"""Audit every button (onclick), anchor (href) and form on the static site.

Reports:
  - broken <a href="..."> (file-system links that don't resolve)
  - dangling <a href="#anchor"> with no matching id on the same page
  - onclick="funcName(...)" or onclick="...funcName(...)..." where funcName
    is not defined in the page's inline JS and is not a known runtime helper
  - <form action="..."> with non-http(s) targets or empty action

Exit code 1 if any issue is found.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote
from collections import defaultdict

SITE_ROOT = Path("/workspaces/Logoestudios/site")

# Runtime-provided callables that are not defined in the page itself. Anything
# in here is considered safe even if we can't find its definition.
RUNTIME_FUNCS = {
    # Lucide icons
    "lucide", "createIcons",
    # Browser/DOM
    "console", "window", "document",
    # Common third-party (none currently, kept for future)
}

ANCHOR_RE = re.compile(r'<a\s[^>]*?href=["\']([^"\']*)["\'][^>]*>', re.IGNORECASE)
ONCLICK_RE = re.compile(r'onclick=["\']([^"\']+)["\']', re.IGNORECASE)
FORM_RE = re.compile(r'<form\s[^>]*?action=["\']([^"\']*)["\']', re.IGNORECASE)
ID_RE = re.compile(r'\bid=["\']([^"\']+)["\']', re.IGNORECASE)
FUNC_DEF_RE = re.compile(r'function\s+([A-Za-z_$][\w$]*)\s*\(')
FUNC_CALL_RE = re.compile(r'\b([A-Za-z_$][\w$]*)\s*\(')


def is_external(href):
    return href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:"))


def resolve_local(source_file, href):
    href = href.split("#")[0].split("?")[0]
    href = unquote(href)
    if not href:
        return None
    if href.startswith("/"):
        candidate = Path("/workspaces/Logoestudios") / href.lstrip("/")
        if not candidate.exists():
            candidate = SITE_ROOT / href.lstrip("/")
    else:
        candidate = (source_file.parent / href).resolve()
    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate


def extract_inline_funcs(html):
    """Return the set of function names defined in inline <script> blocks."""
    funcs = set()
    for script in re.findall(r"<script[^>]*>([\s\S]*?)</script>", html, re.IGNORECASE):
        for name in FUNC_DEF_RE.findall(script):
            funcs.add(name)
        # var/let/const f = function() {...}  or  f = () => {...}
        for m in re.finditer(r'(?:var|let|const)?\s*([A-Za-z_$][\w$]*)\s*=\s*(?:function\s*\(|\([^)]*\)\s*=>)', script):
            funcs.add(m.group(1))
    return funcs


def extract_called_funcs(onclick_value):
    """Return *global* function names invoked by an onclick value.

    Skip method calls (anything preceded by '.') because those resolve at
    runtime against the receiver (e.g. classList.toggle(), array.forEach()).
    """
    skip_keywords = {"if", "else", "for", "while", "switch", "return", "new",
                     "typeof", "delete", "void", "in", "of", "function",
                     "true", "false", "null", "undefined", "this"}
    calls = []
    for m in FUNC_CALL_RE.finditer(onclick_value):
        name = m.group(1)
        if name in skip_keywords:
            continue
        # Is this a method call (preceded by '.')? Skip.
        if m.start() > 0 and onclick_value[m.start() - 1] == ".":
            continue
        calls.append(name)
    return calls


def audit():
    files = sorted(SITE_ROOT.rglob("*.html"))

    broken_links = []         # (source, href, resolved)
    dangling_anchors = []     # (source, "#anchor")
    missing_funcs = []        # (source, onclick, missing_func)
    bad_form_actions = []     # (source, action)

    for f in files:
        content = f.read_text(encoding="utf-8", errors="replace")
        page_ids = set(ID_RE.findall(content))
        page_funcs = extract_inline_funcs(content) | RUNTIME_FUNCS

        # ---- anchors ----
        for href in ANCHOR_RE.findall(content):
            if not href:
                continue
            if is_external(href):
                continue
            if href.startswith("#"):
                anchor = href[1:]
                if anchor and anchor not in page_ids:
                    dangling_anchors.append((f, href))
                continue
            resolved = resolve_local(f, href)
            if resolved and not resolved.exists():
                broken_links.append((f, href, resolved))

        # ---- onclick handlers ----
        for onclick in ONCLICK_RE.findall(content):
            for fname in extract_called_funcs(onclick):
                if fname not in page_funcs:
                    missing_funcs.append((f, onclick, fname))

        # ---- forms ----
        for action in FORM_RE.findall(content):
            if not action:
                bad_form_actions.append((f, "(empty)"))
            elif not action.startswith(("http://", "https://", "/")):
                bad_form_actions.append((f, action))

    # ---- Report ----
    print("=" * 70)
    print("BUTTON & LINK AUDIT — Logopsi Études")
    print("=" * 70)

    def section(title, items, fmt):
        print(f"\n--- {title} ({len(items)}) ---")
        if items:
            for it in items[:30]:
                print(" ", fmt(it))
            if len(items) > 30:
                print(f"  ... and {len(items) - 30} more")
        else:
            print("  OK")
        return len(items)

    n1 = section("BROKEN <a href> (file not found)", broken_links,
                 lambda x: f"{x[0].relative_to(SITE_ROOT)}  ->  {x[1]}")
    n2 = section("DANGLING <a href=\"#anchor\"> (no matching id)", dangling_anchors,
                 lambda x: f"{x[0].relative_to(SITE_ROOT)}  ->  {x[1]}")
    n3 = section("onclick CALLS UNDEFINED FUNCTION", missing_funcs,
                 lambda x: f"{x[0].relative_to(SITE_ROOT)}  ->  {x[2]}()   from: {x[1][:60]}")
    n4 = section("FORMS WITH BAD action=", bad_form_actions,
                 lambda x: f"{x[0].relative_to(SITE_ROOT)}  ->  {x[1]}")

    issues = n1 + n2 + n3 + n4
    print("\n" + "=" * 70)
    print(f"Pages audited: {len(files)}    Issues: {issues}")
    print("=" * 70)
    return 0 if issues == 0 else 1


if __name__ == "__main__":
    sys.exit(audit())
