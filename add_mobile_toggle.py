#!/usr/bin/env python3
"""Ajoute le bouton toggle FR/ES dans le MENU MOBILE également, et fait en sorte
que le libellé (ES/FR) se mette à jour sur les deux boutons (desktop + mobile).

Idempotent. Suppose que add_lang_toggle.py a déjà été exécuté.
"""

import glob
import os
from collections import Counter

HTML_DIR = "wp-plugin/logopsi-deployer/data/html"

# Bouton Connexion mobile exact (ancre #2)
MOBILE_LOGIN = ('<a href="https://app.logopsiestudios.com/fr/login" target="_blank" '
                'rel="noopener noreferrer" class="block text-center font-semibold py-2 '
                'text-gray-700 hover:text-primary border-b border-gray-100">Connexion</a>')

# Bouton toggle mobile (même style block que les liens du menu mobile)
MOBILE_BTN = ('<button type="button" onclick="logopsiToggleLang()" id="lang-toggle-m" '
              'class="flex items-center justify-center gap-1.5 w-full text-center font-semibold '
              'py-2 text-gray-700 hover:text-primary border-b border-gray-100">'
              '<i data-lucide="languages" class="w-4 h-4"></i>'
              '<span class="lang-toggle-label">ES</span></button>')

# Donner une classe au span desktop pour pouvoir cibler les deux libellés
DESKTOP_LABEL_OLD = '<span id="lang-toggle-label">ES</span>'
DESKTOP_LABEL_NEW = '<span id="lang-toggle-label" class="lang-toggle-label">ES</span>'

# Mettre à jour la fonction de libellé pour cibler TOUS les labels (.lang-toggle-label)
FN_OLD = ("function logopsiUpdateLangLabel(){var c=logopsiGetCookie('googtrans');"
          "var es=c&&c.indexOf('/es')>-1;var el=document.getElementById('lang-toggle-label');"
          "if(el)el.textContent=es?'FR':'ES';}")
FN_NEW = ("function logopsiUpdateLangLabel(){var c=logopsiGetCookie('googtrans');"
          "var es=c&&c.indexOf('/es')>-1;document.querySelectorAll('.lang-toggle-label')"
          ".forEach(function(el){el.textContent=es?'FR':'ES';});}")


def main():
    files = sorted(glob.glob(f"{HTML_DIR}/*.html"))
    stats = Counter()
    no_mobile_login = []

    for f in files:
        h = open(f, encoding="utf-8", errors="replace").read()
        orig = h

        # 1) classe sur le label desktop
        if DESKTOP_LABEL_OLD in h:
            h = h.replace(DESKTOP_LABEL_OLD, DESKTOP_LABEL_NEW)
            stats["desktop_label_classed"] += 1

        # 2) fonction de mise à jour des libellés
        if FN_OLD in h:
            h = h.replace(FN_OLD, FN_NEW)
            stats["fn_updated"] += 1

        # 3) bouton mobile avant le Connexion mobile
        if 'id="lang-toggle-m"' not in h:
            if MOBILE_LOGIN in h:
                h = h.replace(MOBILE_LOGIN, MOBILE_BTN + MOBILE_LOGIN, 1)
                stats["mobile_btn_added"] += 1
            else:
                no_mobile_login.append(os.path.basename(f))

        if h != orig:
            open(f, "w", encoding="utf-8").write(h)
            stats["files_changed"] += 1

    print("=== Résumé toggle mobile ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    if no_mobile_login:
        print(f"  ⚠️ sans Connexion mobile ({len(no_mobile_login)}): {no_mobile_login[:10]}")

    # Vérifs
    have_m = sum(1 for f in files if 'id="lang-toggle-m"' in open(f,encoding="utf-8",errors="replace").read())
    dup_m = sum(1 for f in files if open(f,encoding="utf-8",errors="replace").read().count('id="lang-toggle-m"')>1)
    fn_ok = sum(1 for f in files if FN_NEW in open(f,encoding="utf-8",errors="replace").read())
    print(f"\n  pages avec bouton mobile: {have_m}/{len(files)}")
    print(f"  pages avec bouton mobile dupliqué: {dup_m} (doit être 0)")
    print(f"  pages avec fonction libellé MAJ: {fn_ok}/{len(files)}")


if __name__ == "__main__":
    main()
