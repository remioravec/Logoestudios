#!/usr/bin/env python3
"""Ajoute un bouton toggle de langue Français / Español dans le menu (desktop)
et la machinerie de traduction automatique (Google Translate) avant </body>,
sur toutes les pages source du plugin Logopsi.

- Bouton inséré juste avant le bouton "Connexion" desktop dans le <nav>.
- Traduction client-side à la volée (FR <-> ES), via cookie googtrans + reload.
- Idempotent : ré-exécutable sans doublonner.
"""

import re
import glob
import os
from collections import Counter

HTML_DIR = "wp-plugin/logopsi-deployer/data/html"

# Bouton toggle (desktop). Icône Lucide "languages" + label dynamique ES/FR.
TOGGLE_BTN = (
    '<button type="button" onclick="logopsiToggleLang()" id="lang-toggle" '
    'aria-label="Changer de langue (Français / Español)" '
    'class="inline-flex items-center gap-1.5 text-[15px] font-semibold '
    'text-gray-700 hover:text-primary transition-colors mr-2">'
    '<i data-lucide="languages" class="w-4 h-4"></i>'
    '<span id="lang-toggle-label">ES</span></button>\n                    '
)

# Machinerie de traduction (insérée avant </body>)
MACHINERY = """
<!-- logopsi-lang-toggle -->
<div id="google_translate_element" style="display:none"></div>
<style>
.goog-te-banner-frame,.skiptranslate{display:none!important}
body{top:0!important}
#goog-gt-tt,.goog-te-balloon-frame{display:none!important}
.goog-text-highlight{background:none!important;box-shadow:none!important}
</style>
<script>
function logopsiGoogleInit(){new google.translate.TranslateElement({pageLanguage:'fr',includedLanguages:'es',autoDisplay:false},'google_translate_element');}
function logopsiGetCookie(n){var m=document.cookie.match('(^|; )'+n+'=([^;]*)');return m?m[2]:'';}
function logopsiSetLang(lang){var v=(lang==='es')?'/fr/es':'/fr/fr';var h=location.hostname;document.cookie='googtrans='+v+';path=/';document.cookie='googtrans='+v+';path=/;domain=.'+h;location.reload();}
function logopsiToggleLang(){var c=logopsiGetCookie('googtrans');if(c&&c.indexOf('/es')>-1){logopsiSetLang('fr');}else{logopsiSetLang('es');}}
function logopsiUpdateLangLabel(){var c=logopsiGetCookie('googtrans');var es=c&&c.indexOf('/es')>-1;var el=document.getElementById('lang-toggle-label');if(el)el.textContent=es?'FR':'ES';}
document.addEventListener('DOMContentLoaded',logopsiUpdateLangLabel);
</script>
<script src="//translate.google.com/translate_a/element.js?cb=logopsiGoogleInit"></script>
<!-- /logopsi-lang-toggle -->
"""

NAV_RE = re.compile(r"<nav\b[\s\S]*?</nav>", re.I)
# bouton Connexion desktop = celui dont la classe contient text-[15px]
DESKTOP_LOGIN_RE = re.compile(
    r'<a\b[^>]*app\.logopsiestudios\.com/fr/login[^>]*class="[^"]*text-\[15px\][^"]*"[^>]*>[\s\S]*?</a>',
    re.I,
)


def main():
    files = sorted(glob.glob(f"{HTML_DIR}/*.html"))
    stats = Counter()
    skipped_no_login = []
    skipped_no_body = []

    for f in files:
        h = open(f, encoding="utf-8", errors="replace").read()
        orig = h

        # 1) Insérer le bouton toggle avant le Connexion desktop (1ère occurrence)
        if "id=\"lang-toggle\"" not in h:
            m = DESKTOP_LOGIN_RE.search(h)
            if m:
                h = h[:m.start()] + TOGGLE_BTN + h[m.start():]
                stats["btn_added"] += 1
            else:
                skipped_no_login.append(os.path.basename(f))

        # 2) Insérer la machinerie avant </body>
        if "logopsi-lang-toggle" not in h:
            idx = h.lower().rfind("</body>")
            if idx != -1:
                h = h[:idx] + MACHINERY + h[idx:]
                stats["machinery_added"] += 1
            else:
                h = h + MACHINERY
                stats["machinery_appended"] += 1
                skipped_no_body.append(os.path.basename(f))

        if h != orig:
            open(f, "w", encoding="utf-8").write(h)
            stats["files_changed"] += 1

    print("=== Résumé toggle langue ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    if skipped_no_login:
        print(f"  ⚠️ sans bouton Connexion desktop ({len(skipped_no_login)}): {skipped_no_login[:10]}")
    if skipped_no_body:
        print(f"  ⚠️ sans </body> ({len(skipped_no_body)}): {skipped_no_body[:10]}")

    # Vérif idempotence / présence
    have_btn = sum(1 for f in files if 'id="lang-toggle"' in open(f,encoding="utf-8",errors="replace").read())
    have_mac = sum(1 for f in files if 'logopsi-lang-toggle' in open(f,encoding="utf-8",errors="replace").read())
    dup_btn = sum(1 for f in files if open(f,encoding="utf-8",errors="replace").read().count('id="lang-toggle"')>1)
    print(f"\n  pages avec bouton: {have_btn}/{len(files)}")
    print(f"  pages avec machinerie: {have_mac}/{len(files)}")
    print(f"  pages avec bouton dupliqué: {dup_btn} (doit être 0)")


if __name__ == "__main__":
    main()
