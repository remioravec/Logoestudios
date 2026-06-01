#!/usr/bin/env python3
"""Deux correctifs UI sur les pages source du plugin Logopsi :

  A. Bouton "Découvrir le déroulement d'une séance" (22 pages) : actuellement
     mort (aucun onclick). On le branche sur une nouvelle modale #seance-modal
     décrivant les étapes d'une séance, injectée avant </body>.

  B. Toggle de langue FR/ES (desktop + mobile, 542 pages) : redesign en "pill"
     plus soignée (icône globe, fond/bordure arrondis, hover primary).

Idempotent.
"""

import re
import glob
import os
from collections import Counter

HTML_DIR = "wp-plugin/logopsi-deployer/data/html"
SITE = "https://logopsietudes.com"

# ---------------------------------------------------------------------------
# A. Modale "déroulement d'une séance"
# ---------------------------------------------------------------------------
STEPS = [
    ("calendar-check", "Réservation en ligne", "Choisissez un créneau qui vous convient. Premier rendez-vous sous 48h."),
    ("clipboard-list", "Premier bilan", "Un échange avec le professionnel pour comprendre les besoins et fixer des objectifs."),
    ("route", "Plan personnalisé", "Un programme d'accompagnement adapté à votre situation et à votre rythme."),
    ("video", "Séances en visio", "Des séances régulières en ligne, avec des supports numériques interactifs."),
    ("trending-up", "Suivi & bilans d'étape", "Des points réguliers pour mesurer les progrès et ajuster le programme."),
]

def steps_html():
    out = []
    for i, (icon, title, desc) in enumerate(STEPS, 1):
        out.append(f'''
          <li class="flex gap-4">
            <div class="shrink-0 w-10 h-10 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold"><i data-lucide="{icon}" class="w-5 h-5"></i></div>
            <div>
              <p class="font-semibold text-gray-900">{i}. {title}</p>
              <p class="text-sm text-gray-600 leading-relaxed">{desc}</p>
            </div>
          </li>''')
    return "".join(out)

SEANCE_MODAL = f'''
<!-- logopsi-seance-modal -->
<div id="seance-modal" class="hidden fixed inset-0 z-[110] flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
  <div class="bg-white rounded-3xl w-full max-w-lg shadow-2xl relative max-h-[90vh] overflow-y-auto">
    <button type="button" onclick="closeSeanceModal()" aria-label="Fermer" class="absolute top-4 right-4 p-2 text-gray-400 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-colors"><i data-lucide="x" class="w-6 h-6"></i></button>
    <div class="p-8">
      <h3 class="text-2xl font-bold text-gray-900 mb-2">Le déroulement d'une séance</h3>
      <p class="text-gray-600 mb-6 text-sm">Un accompagnement simple, humain et 100% en ligne, en 5 étapes.</p>
      <ol class="space-y-5">{steps_html()}
      </ol>
      <a href="{SITE}/contact/" class="mt-8 block w-full bg-primary text-white text-center font-bold py-3 rounded-full hover:opacity-90 transition-opacity">Prendre rendez-vous</a>
    </div>
  </div>
</div>
<script>
function openSeanceModal(){{var m=document.getElementById('seance-modal');if(m){{m.classList.remove('hidden');document.body.style.overflow='hidden';if(window.lucide)lucide.createIcons();}}}}
function closeSeanceModal(){{var m=document.getElementById('seance-modal');if(m){{m.classList.add('hidden');document.body.style.overflow='';}}}}
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeSeanceModal();}});
document.addEventListener('click',function(e){{var m=document.getElementById('seance-modal');if(m&&e.target===m)closeSeanceModal();}});
</script>
<!-- /logopsi-seance-modal -->
'''

# bouton "déroulement" : ajoute type+onclick à la balise ouvrante
SEANCE_BTN_RE = re.compile(
    r'(<button\b)((?:(?!onclick)[^>])*?)(>\s*Découvrir le déroulement d\'une séance\s*</button>)',
    re.I,
)

# ---------------------------------------------------------------------------
# B. Redesign du toggle de langue (pill)
# ---------------------------------------------------------------------------
DESKTOP_PILL = ('inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border '
                'border-gray-200 bg-white text-gray-700 text-sm font-semibold '
                'hover:bg-primary hover:text-white hover:border-primary shadow-sm '
                'transition-all mr-2')
MOBILE_PILL = ('flex items-center justify-center gap-2 mx-auto my-2 px-5 py-2 rounded-full '
               'border border-gray-200 bg-gray-50 text-gray-700 font-semibold '
               'hover:bg-primary hover:text-white hover:border-primary transition-all')

def redesign_toggle(h):
    changed = False
    # Desktop
    new = re.sub(
        r'(<button\b[^>]*id="lang-toggle"[^>]*class=")[^"]*("[^>]*>)\s*<i data-lucide="[^"]*"([^>]*)></i>',
        lambda m: f'{m.group(1)}{DESKTOP_PILL}{m.group(2)}<i data-lucide="globe"{m.group(3)}></i>',
        h)
    if new != h:
        changed = True; h = new
    # Mobile
    new = re.sub(
        r'(<button\b[^>]*id="lang-toggle-m"[^>]*class=")[^"]*("[^>]*>)\s*<i data-lucide="[^"]*"([^>]*)></i>',
        lambda m: f'{m.group(1)}{MOBILE_PILL}{m.group(2)}<i data-lucide="globe"{m.group(3)}></i>',
        h)
    if new != h:
        changed = True; h = new
    return h, changed


def main():
    files = sorted(glob.glob(f"{HTML_DIR}/*.html"))
    stats = Counter()
    for f in files:
        h = open(f, encoding="utf-8", errors="replace").read()
        orig = h

        # A. brancher le bouton séance + injecter la modale
        if "Découvrir le déroulement d'une séance" in h:
            new, n = SEANCE_BTN_RE.subn(r'\1 type="button" onclick="openSeanceModal()"\2\3', h)
            if n:
                stats["seance_btn_wired"] += n
                h = new
            if "logopsi-seance-modal" not in h:
                idx = h.lower().rfind("</body>")
                if idx != -1:
                    h = h[:idx] + SEANCE_MODAL + h[idx:]
                else:
                    h = h + SEANCE_MODAL
                stats["seance_modal_added"] += 1

        # B. redesign toggle
        h, changed = redesign_toggle(h)
        if changed:
            stats["toggle_redesigned"] += 1

        if h != orig:
            open(f, "w", encoding="utf-8").write(h)
            stats["files_changed"] += 1

    print("=== Résumé ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    # Vérifs
    wired = sum(1 for f in files if 'onclick="openSeanceModal()"' in open(f,encoding="utf-8",errors="replace").read())
    modal = sum(1 for f in files if 'logopsi-seance-modal' in open(f,encoding="utf-8",errors="replace").read())
    dead = sum(1 for f in files if re.search(r'<button\b(?:(?!onclick)[^>])*?>\s*Découvrir le déroulement', open(f,encoding="utf-8",errors="replace").read()))
    pill = sum(1 for f in files if DESKTOP_PILL in open(f,encoding="utf-8",errors="replace").read())
    print(f"\n  boutons séance branchés (pages): {wired}")
    print(f"  modales séance présentes: {modal}")
    print(f"  boutons séance encore morts: {dead} (doit être 0)")
    print(f"  toggles desktop redesignés: {pill}/{len(files)}")


if __name__ == "__main__":
    main()
