#!/usr/bin/env python3
"""Corrige la source du plugin Logopsi pour le site logopsietudes.com :

  1. Liens cassés : href="/site/..."  ->  href="/..."
                    href="...index.html#contact"  ->  href="/contact/"
  2. Menu + footer uniformes : remplace <nav> et <footer> de chaque page par
     la version de référence (variante majoritaire, 447 pages).
  3. Régénère les 3 pages "villes" vides (hubs listant les 5 villes).

Modifie uniquement les fichiers source HTML (data/html/*.html). N'écrit pas
sur le site live (le déploiement se fait ensuite via le plugin).
"""

import re
import glob
import os
import hashlib
from collections import Counter

HTML_DIR = "wp-plugin/logopsi-deployer/data/html"
SITE = "https://logopsietudes.com"

NAV_RE = re.compile(r"<nav\b[\s\S]*?</nav>", re.I)
FOOTER_RE = re.compile(r"<footer\b[\s\S]*?</footer>", re.I)

def norm(h):
    h2 = re.sub(r'\s+(class|aria-current|aria-expanded)="[^"]*(active|current|true|open)[^"]*"', "", h, flags=re.I)
    h2 = re.sub(r"<!--[\s\S]*?-->", "", h2)
    h2 = re.sub(r"\s+", " ", h2)
    return h2.strip().lower()

def sig(t):
    return hashlib.md5(t.encode("utf-8", "replace")).hexdigest()[:8]

# ---------------------------------------------------------------------------
# Référence menu / footer = variante majoritaire
# ---------------------------------------------------------------------------
def pick_reference():
    files = glob.glob(f"{HTML_DIR}/*.html")
    nav_counter, foot_counter = Counter(), Counter()
    nav_block, foot_block = {}, {}
    for f in files:
        h = open(f, encoding="utf-8", errors="replace").read()
        n = NAV_RE.search(h)
        ft = FOOTER_RE.search(h)
        if n:
            s = sig(norm(n.group())); nav_counter[s] += 1; nav_block.setdefault(s, n.group())
        if ft:
            s = sig(norm(ft.group())); foot_counter[s] += 1; foot_block.setdefault(s, ft.group())
    nav_ref = nav_block[nav_counter.most_common(1)[0][0]]
    foot_ref = foot_block[foot_counter.most_common(1)[0][0]]
    return nav_ref, foot_ref

# ---------------------------------------------------------------------------
# Contenu des hubs "villes"
# ---------------------------------------------------------------------------
CITIES = [("Paris", "paris"), ("Marseille", "marseille"), ("Lyon", "lyon"),
          ("Toulouse", "toulouse"), ("Nice", "nice")]

DISCIPLINES = {
    "orthophonie": ("Orthophonie", "orthophonistes diplômés", "bilan orthophonique"),
    "psychologie": ("Psychologie", "psychologues cliniciens", "bilan psychologique"),
    "soutien-scolaire": ("Soutien Scolaire", "enseignants qualifiés", "soutien scolaire"),
}

def hub_sections(disc):
    label, who, service = DISCIPLINES[disc]
    cards = []
    for name, slug in CITIES:
        cards.append(f'''
        <a href="{SITE}/{disc}/villes/{slug}/" class="group block bg-white rounded-2xl shadow-sm hover:shadow-xl border border-gray-100 p-8 transition-all">
          <div class="flex items-center gap-4 mb-3">
            <div class="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-600">
              <i data-lucide="map-pin"></i>
            </div>
            <h3 class="text-xl font-bold text-gray-900 group-hover:text-indigo-600">{label} à {name}</h3>
          </div>
          <p class="text-gray-600">{service.capitalize()} en ligne à {name} avec nos {who}. Prise en charge sous 48h.</p>
          <span class="inline-flex items-center gap-1 mt-4 text-indigo-600 font-semibold">Découvrir <i data-lucide="arrow-right" class="w-4 h-4"></i></span>
        </a>''')
    grid = "\n".join(cards)
    return f'''
    <section class="bg-gradient-to-b from-indigo-50 to-white py-20">
      <div class="max-w-5xl mx-auto px-4 text-center">
        <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 mb-4">{label} en ligne dans votre ville</h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">Nos {who} accompagnent enfants et adultes partout en France. Choisissez votre ville pour découvrir notre offre de {service} à distance, avec un premier bilan sous 48h.</p>
      </div>
    </section>
    <section class="py-16">
      <div class="max-w-6xl mx-auto px-4">
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">{grid}
        </div>
        <div class="text-center mt-12">
          <a href="{SITE}/{disc}/" class="inline-flex items-center gap-2 text-indigo-600 font-semibold hover:underline">Voir toute l'offre {label} <i data-lucide="arrow-right" class="w-4 h-4"></i></a>
        </div>
      </div>
    </section>'''

def build_villes_page(disc, nav_ref, foot_ref):
    """Construit une page hub villes en clonant le squelette de la page discipline."""
    skeleton = open(f"{HTML_DIR}/{disc}.html", encoding="utf-8", errors="replace").read()
    # prefix = tout jusqu'à la fin du premier </nav> ; suffix = à partir de <footer>
    m_nav = NAV_RE.search(skeleton)
    m_foot = FOOTER_RE.search(skeleton)
    prefix = skeleton[:m_nav.end()]
    suffix = skeleton[m_foot.start():]
    label = DISCIPLINES[disc][0]
    title = f"{label} en ligne par ville — Bilan sous 48h | Logopsi Études"
    desc = f"{label} à distance à Paris, Marseille, Lyon, Toulouse et Nice. Premier bilan sous 48h avec nos professionnels diplômés. Logopsi Études."
    prefix = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", prefix, flags=re.S)
    prefix = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', rf'\g<1>{desc}\g<2>', prefix, flags=re.I)
    return prefix + hub_sections(disc) + "\n" + suffix

# ---------------------------------------------------------------------------
def main():
    nav_ref, foot_ref = pick_reference()
    print(f"Référence : nav={len(nav_ref)} car / footer={len(foot_ref)} car")

    files = sorted(glob.glob(f"{HTML_DIR}/*.html"))

    villes_files = {
        "orthophonie__villes.html": "orthophonie",
        "psychologie__villes.html": "psychologie",
        "soutien-scolaire__villes.html": "soutien-scolaire",
    }

    stats = Counter()
    for f in files:
        base = os.path.basename(f)
        h = open(f, encoding="utf-8", errors="replace").read()
        orig = h

        # --- Régénérer les hubs villes vides ---
        if base in villes_files:
            h = build_villes_page(villes_files[base], nav_ref, foot_ref)
            stats["villes_regen"] += 1

        # --- 1. Corriger les liens cassés ---
        n_site = h.count('href="/site/')
        if n_site:
            h = h.replace('href="/site/', 'href="/')
            stats["fix_site"] += n_site
        # variante domaine absolu éventuelle
        h2 = h.replace(f'href="{SITE}/site/', f'href="{SITE}/')
        if h2 != h:
            stats["fix_site_abs"] += 1; h = h2
        # contact cassé : ...index.html#contact  ->  /contact/
        h2 = re.sub(r'href="[^"]*index\.html#contact"', f'href="{SITE}/contact/"', h)
        if h2 != h:
            stats["fix_contact"] += len(re.findall(r'index\.html#contact', h))
            h = h2

        # --- 2. Uniformiser nav + footer ---
        if NAV_RE.search(h):
            new = NAV_RE.sub(lambda m: nav_ref, h, count=1)
            if new != h:
                stats["nav_unified"] += 1
            h = new
        if FOOTER_RE.search(h):
            new = FOOTER_RE.sub(lambda m: foot_ref, h, count=1)
            if new != h:
                stats["footer_unified"] += 1
            h = new

        if h != orig:
            open(f, "w", encoding="utf-8").write(h)
            stats["files_changed"] += 1

    print("\n=== Résumé des corrections (source) ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    # Vérif : combien de variantes restent ?
    nav_c, foot_c = Counter(), Counter()
    nonav = 0
    for f in glob.glob(f"{HTML_DIR}/*.html"):
        h = open(f, encoding="utf-8", errors="replace").read()
        n = NAV_RE.search(h); ft = FOOTER_RE.search(h)
        nav_c[sig(norm(n.group())) if n else "NONAV"] += 1
        foot_c[sig(norm(ft.group())) if ft else "NOFOOT"] += 1
    print("\n=== Après correction ===")
    print("  variantes nav :", dict(nav_c))
    print("  variantes footer :", dict(foot_c))
    # liens résiduels
    resid_site = sum(open(f,encoding="utf-8",errors="replace").read().count('/site/') for f in glob.glob(f"{HTML_DIR}/*.html"))
    resid_contact = sum(open(f,encoding="utf-8",errors="replace").read().count('index.html#contact') for f in glob.glob(f"{HTML_DIR}/*.html"))
    print(f"  occurrences '/site/' restantes : {resid_site}")
    print(f"  occurrences 'index.html#contact' restantes : {resid_contact}")

if __name__ == "__main__":
    main()
