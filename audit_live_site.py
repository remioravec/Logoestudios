#!/usr/bin/env python3
"""Audit complet du site EN LIGNE logopsietudes.com.

Vérifie, sur toutes les pages publiées :
  1. Cohérence du MENU (nav) : même menu partout ?
  2. Cohérence du FOOTER : même footer partout ?
  3. Liens cassés (a href) : statut HTTP de chaque URL unique
  4. Ancres mortes (#id sans cible sur la page)
  5. Boutons onclick appelant une fonction non définie
  6. Formulaires avec action vide/invalide

Lecture seule. N'écrit jamais sur le site.
"""

import base64
import json
import os
import re
import sys
import hashlib
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

SITE = "https://logopsietudes.com"
WP_USER = os.environ["WP_USER"]
WP_PASS = os.environ["WP_PASS"]
AUTH = "Basic " + base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
UA = "Mozilla/5.0 (audit-logopsietudes)"

session = requests.Session()
session.headers.update({"User-Agent": UA})

# ---------------------------------------------------------------------------
# 1. Récupérer toutes les pages publiées via l'API REST
# ---------------------------------------------------------------------------
def list_all_page_urls():
    urls = []
    for endpoint in ("pages", "posts"):
        page = 1
        while True:
            r = session.get(
                f"{SITE}/wp-json/wp/v2/{endpoint}",
                params={"per_page": 100, "page": page, "status": "publish", "_fields": "link,id,title"},
                headers={"Authorization": AUTH},
                timeout=40,
            )
            if r.status_code != 200:
                break
            batch = r.json()
            if not batch:
                break
            for item in batch:
                urls.append(item["link"])
            total_pages = int(r.headers.get("X-WP-TotalPages", "1"))
            if page >= total_pages:
                break
            page += 1
    # dédupe en gardant l'ordre
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out

# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------
NAV_RE = re.compile(r"<nav\b[\s\S]*?</nav>", re.I)
FOOTER_RE = re.compile(r"<footer\b[\s\S]*?</footer>", re.I)
ANCHOR_RE = re.compile(r'<a\s[^>]*?href=["\']([^"\']*)["\']', re.I)
ONCLICK_RE = re.compile(r'onclick=["\']([^"\']+)["\']', re.I)
FORM_RE = re.compile(r'<form\s[^>]*?action=["\']([^"\']*)["\']', re.I)
ID_RE = re.compile(r'\bid=["\']([^"\']+)["\']', re.I)
FUNC_DEF_RE = re.compile(r'function\s+([A-Za-z_$][\w$]*)\s*\(')
FUNC_CALL_RE = re.compile(r'\b([A-Za-z_$][\w$]*)\s*\(')
RUNTIME_FUNCS = {"lucide", "createIcons", "console", "window", "document",
                 "alert", "setTimeout", "fetch", "JSON", "Math"}

def normalize_block(html):
    """Normalise un bloc HTML pour comparer la structure, en ignorant les
    variations dynamiques (classes active/current, espaces, casse des attributs)."""
    if not html:
        return ""
    s = html
    s = re.sub(r'\s+(class|aria-current|aria-expanded)="[^"]*(active|current|true|open)[^"]*"', "", s, flags=re.I)
    s = re.sub(r"<!--[\s\S]*?-->", "", s)        # commentaires
    s = re.sub(r"\s+", " ", s)                     # espaces
    return s.strip().lower()

def sig(text):
    return hashlib.md5(text.encode("utf-8", "replace")).hexdigest()[:10]

def extract_inline_funcs(html):
    funcs = set()
    for script in re.findall(r"<script[^>]*>([\s\S]*?)</script>", html, re.I):
        funcs.update(FUNC_DEF_RE.findall(script))
        for m in re.finditer(r'(?:var|let|const)?\s*([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:function\s*\(|\([^)]*\)\s*=>)', script):
            funcs.add(m.group(1))
    return funcs

def extract_called_funcs(onclick):
    skip = {"if","else","for","while","switch","return","new","typeof","delete",
            "void","in","of","function","true","false","null","undefined","this","event"}
    out = []
    for m in FUNC_CALL_RE.finditer(onclick):
        name = m.group(1)
        if name in skip:
            continue
        if m.start() > 0 and onclick[m.start()-1] == ".":
            continue
        out.append(name)
    return out

# ---------------------------------------------------------------------------
# Crawl
# ---------------------------------------------------------------------------
def fetch(url):
    try:
        r = session.get(url, timeout=40)
        return url, r.status_code, r.text
    except Exception as e:
        return url, None, str(e)

def main():
    print("Récupération de la liste des pages publiées via l'API REST...")
    page_urls = list_all_page_urls()
    print(f"  -> {len(page_urls)} URL publiées à auditer\n")

    nav_sigs = defaultdict(list)      # sig -> [urls]
    footer_sigs = defaultdict(list)
    nav_sample = {}                   # sig -> raw block
    footer_sample = {}
    nav_links = {}                    # sig -> sorted list of hrefs
    footer_links = {}

    all_links = defaultdict(set)      # href -> set(source pages)
    dangling_anchors = []             # (src, #anchor)
    missing_funcs = []                # (src, func, onclick)
    bad_forms = []                    # (src, action)
    fetch_errors = []                 # (url, status/err)

    pages = {}  # url -> html
    print("Crawl des pages...")
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(fetch, u): u for u in page_urls}
        done = 0
        for fut in as_completed(futs):
            url, status, text = fut.result()
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{len(page_urls)}")
            if status != 200:
                fetch_errors.append((url, status))
                continue
            pages[url] = text

    print(f"  -> {len(pages)} pages récupérées\n")

    print("Analyse menu / footer / liens...")
    for url, html in pages.items():
        nav = NAV_RE.search(html)
        footer = FOOTER_RE.search(html)
        nav_block = nav.group() if nav else ""
        footer_block = footer.group() if footer else ""

        ns = sig(normalize_block(nav_block)) if nav_block else "MISSING"
        fs = sig(normalize_block(footer_block)) if footer_block else "MISSING"
        nav_sigs[ns].append(url)
        footer_sigs[fs].append(url)
        if ns not in nav_sample:
            nav_sample[ns] = nav_block
            nav_links[ns] = sorted(set(ANCHOR_RE.findall(nav_block)))
        if fs not in footer_sample:
            footer_sample[fs] = footer_block
            footer_links[fs] = sorted(set(ANCHOR_RE.findall(footer_block)))

        page_ids = set(ID_RE.findall(html))
        page_funcs = extract_inline_funcs(html) | RUNTIME_FUNCS

        for href in ANCHOR_RE.findall(html):
            if not href:
                continue
            if href.startswith("#"):
                anc = href[1:]
                if anc and anc not in page_ids:
                    dangling_anchors.append((url, href))
                continue
            if href.startswith(("mailto:", "tel:", "javascript:")):
                continue
            all_links[href].add(url)

        for oc in ONCLICK_RE.findall(html):
            for fn in extract_called_funcs(oc):
                if fn not in page_funcs:
                    missing_funcs.append((url, fn, oc[:70]))

        for action in FORM_RE.findall(html):
            if not action or not action.startswith(("http://", "https://", "/")):
                bad_forms.append((url, action or "(vide)"))

    # ---- Vérifier le statut HTTP de chaque lien unique ----
    print(f"Vérification HTTP de {len(all_links)} liens uniques...")
    link_status = {}
    def check(href):
        full = href if href.startswith("http") else SITE + ("" if href.startswith("/") else "/") + href
        try:
            r = session.head(full, timeout=30, allow_redirects=True)
            if r.status_code in (403, 405) or r.status_code >= 400:
                r = session.get(full, timeout=30, allow_redirects=True, stream=True)
            return href, r.status_code, r.url
        except Exception as e:
            return href, None, str(e)
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(check, h): h for h in all_links}
        done = 0
        for fut in as_completed(futs):
            href, status, final = fut.result()
            link_status[href] = (status, final)
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{len(all_links)}")

    broken = {h: v for h, v in link_status.items()
              if v[0] is None or v[0] >= 400}

    # ===================== RAPPORT =====================
    R = []
    def p(*a):
        line = " ".join(str(x) for x in a)
        print(line)
        R.append(line)

    p("=" * 72)
    p("AUDIT SITE EN LIGNE — logopsietudes.com")
    p("=" * 72)
    p(f"Pages publiées listées : {len(page_urls)}")
    p(f"Pages récupérées (HTTP 200) : {len(pages)}")
    p(f"Erreurs de récupération : {len(fetch_errors)}")
    for u, s in fetch_errors[:20]:
        p(f"    [{s}] {u}")

    p("\n" + "-" * 72)
    p(f"1) COHÉRENCE DU MENU — {len(nav_sigs)} variante(s) distincte(s)")
    p("-" * 72)
    ordered = sorted(nav_sigs.items(), key=lambda kv: -len(kv[1]))
    for i, (s, urls) in enumerate(ordered):
        tag = "  ✅ MENU DE RÉFÉRENCE" if i == 0 and s != "MISSING" else ""
        p(f"  Variante {s} : {len(urls)} page(s){tag}")
        p(f"      liens menu : {len(nav_links.get(s, []))}")
        if i > 0 or s == "MISSING":   # montrer les pages déviantes
            for u in urls[:15]:
                p(f"        - {u}")
            if len(urls) > 15:
                p(f"        ... +{len(urls)-15} autres")
    # diff des liens entre la référence et les variantes
    if len(ordered) > 1 and ordered[0][0] != "MISSING":
        ref = set(nav_links[ordered[0][0]])
        for s, urls in ordered[1:]:
            cur = set(nav_links.get(s, []))
            p(f"  Δ variante {s} vs référence :")
            p(f"      manquants : {sorted(ref - cur)[:10]}")
            p(f"      en trop   : {sorted(cur - ref)[:10]}")

    p("\n" + "-" * 72)
    p(f"2) COHÉRENCE DU FOOTER — {len(footer_sigs)} variante(s) distincte(s)")
    p("-" * 72)
    ordered_f = sorted(footer_sigs.items(), key=lambda kv: -len(kv[1]))
    for i, (s, urls) in enumerate(ordered_f):
        tag = "  ✅ FOOTER DE RÉFÉRENCE" if i == 0 and s != "MISSING" else ""
        p(f"  Variante {s} : {len(urls)} page(s){tag}")
        if i > 0 or s == "MISSING":
            for u in urls[:15]:
                p(f"        - {u}")
            if len(urls) > 15:
                p(f"        ... +{len(urls)-15} autres")

    p("\n" + "-" * 72)
    p(f"3) LIENS CASSÉS — {len(broken)} sur {len(all_links)} liens uniques")
    p("-" * 72)
    if not broken:
        p("  ✅ Aucun lien cassé.")
    for href, (status, final) in sorted(broken.items(), key=lambda kv: str(kv[1][0])):
        srcs = list(all_links[href])
        p(f"  [{status}] {href}")
        p(f"        vu sur {len(srcs)} page(s), ex: {srcs[0]}")

    p("\n" + "-" * 72)
    p(f"4) ANCRES MORTES (#id introuvable) — {len(dangling_anchors)}")
    p("-" * 72)
    if not dangling_anchors:
        p("  ✅ Aucune ancre morte.")
    seen_anc = Counter((a) for _, a in dangling_anchors)
    for anc, n in seen_anc.most_common(20):
        p(f"  {anc}  ({n} pages)")

    p("\n" + "-" * 72)
    p(f"5) BOUTONS onclick → fonction non définie — {len(missing_funcs)}")
    p("-" * 72)
    if not missing_funcs:
        p("  ✅ Aucun bouton avec fonction manquante.")
    seen_fn = Counter(fn for _, fn, _ in missing_funcs)
    for fn, n in seen_fn.most_common(20):
        ex = next(oc for _, f, oc in missing_funcs if f == fn)
        p(f"  {fn}()  ({n} occurrences)  ex: {ex}")

    p("\n" + "-" * 72)
    p(f"6) FORMULAIRES action invalide — {len(bad_forms)}")
    p("-" * 72)
    if not bad_forms:
        p("  ✅ Aucun formulaire invalide.")
    for u, a in bad_forms[:20]:
        p(f"  {a}  <- {u}")

    p("\n" + "=" * 72)
    total_issues = (len(fetch_errors) + max(0, len(nav_sigs)-1) + max(0, len(footer_sigs)-1)
                    + len(broken) + len(dangling_anchors) + len(missing_funcs) + len(bad_forms))
    p(f"RÉSUMÉ : {total_issues} catégorie(s)/élément(s) à examiner")
    p(f"  - Variantes de menu   : {len(nav_sigs)} (idéal : 1)")
    p(f"  - Variantes de footer : {len(footer_sigs)} (idéal : 1)")
    p(f"  - Liens cassés        : {len(broken)}")
    p(f"  - Ancres mortes       : {len(set(a for _,a in dangling_anchors))} types")
    p(f"  - Boutons KO          : {len(set(fn for _,fn,_ in missing_funcs))} types")
    p(f"  - Formulaires KO      : {len(bad_forms)}")
    p("=" * 72)

    with open("/home/user/Logoestudios/audit_live_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(R))
    # Détail machine-lisible
    with open("/home/user/Logoestudios/audit_live_details.json", "w", encoding="utf-8") as f:
        json.dump({
            "pages_audited": len(pages),
            "nav_variants": {s: urls for s, urls in nav_sigs.items()},
            "footer_variants": {s: urls for s, urls in footer_sigs.items()},
            "broken_links": {h: {"status": v[0], "final": v[1], "sources": list(all_links[h])} for h, v in broken.items()},
            "dangling_anchors": dangling_anchors,
            "missing_funcs": missing_funcs,
            "bad_forms": bad_forms,
            "fetch_errors": fetch_errors,
        }, f, ensure_ascii=False, indent=2)
    print("\nRapport: audit_live_report.txt | Détails JSON: audit_live_details.json")

if __name__ == "__main__":
    main()
