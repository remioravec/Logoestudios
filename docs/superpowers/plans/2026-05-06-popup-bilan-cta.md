# Popup de réservation, bilan 150€/48h et espace membre — Plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ajouter une popup de réservation unifiée sur tous les CTAs du site, mettre en avant l'offre "Bilan 150€ / sous 48h / 100% en ligne" partout, ajouter un accès Espace membre dans le navbar/footer/popup, et ajuster les meta titres pour booster le SEO.

**Architecture:** Le site est statique (HTML + Tailwind CDN). On centralise les nouveaux composants dans `shared_components.py` (modal HTML, JS, mises à jour navbar/footer/CTA) — utilisé par les générateurs N3/N4. On wire `seo_titles.py` dans les générateurs (N2, N3/N4) pour les nouveaux titres. Les pages hand-written (`site/index.html`, `site/contact.html`, `site/a-propos.html`, `site/mentions-legales.html`, hubs N2 `orthophonie/psychologie/soutien-scolaire/index.html`) sont mises à jour par un script `patch_handwritten_pages.py` idempotent.

**Tech Stack:** Python 3 (générateurs), HTML/CSS/JS (Tailwind CDN), Formsubmit (endpoint de soumission, pas de backend custom).

**Référence du spec :** `docs/superpowers/specs/2026-05-06-popup-bilan-cta-design.md`

---

## File Structure

**Created:**
- `seo_titles.py` — mapping centralisé des nouveaux titres et meta descriptions par slug.
- `patch_handwritten_pages.py` — script idempotent qui patche les pages hand-written.
- `tests/test_components.py` — assertions sur `shared_components` (smoke tests, runnable en `python3 tests/test_components.py`).
- `tests/test_seo_titles.py` — assertions sur le mapping.
- `tests/test_patch_handwritten_pages.py` — assertions sur les opérations du script (idempotence + cas limites).
- `tests/fixtures/` — petits HTML d'exemple pour tester le patch.

**Modified:**
- `shared_components.py` — ajout `get_booking_modal()`, `get_booking_js()`, mise à jour `get_navbar()`, `get_footer()`, `get_cta_section()`, `get_js()`.
- `generate_level2_pages.py` — utilise `seo_titles` pour les titres ; injecte popup HTML+JS dans la sortie ; met à jour la navbar/footer/CTA inlinés.
- `generate_level3_4_pages.py` — utilise `seo_titles` pour les titres N3/N4 (récupère via `shared_components`).
- `generate_physique_chimie.py` — utilise `seo_titles` pour les titres physique-chimie.
- `site/**/*.html` — sortie des générateurs et pages hand-written, après patch.

---

## Test Convention

Comme `pytest` n'est pas installé en local et qu'il n'existe pas de framework de test, on utilise des **scripts d'assertion runnable** :

```python
# tests/test_components.py
from shared_components import get_booking_modal

def test_modal_contains_price():
    assert "150€" in get_booking_modal()

if __name__ == "__main__":
    test_modal_contains_price()
    print("OK")
```

On lance via `python3 tests/test_components.py`. Chaque test print "OK" en succès, lève `AssertionError` en échec.

---

## Phase 1 — Composants Python centralisés (`shared_components.py`)

### Task 1 : `get_booking_modal()` — HTML de la popup

**Files:**
- Create: `tests/test_components.py`
- Modify: `shared_components.py` (ajout d'une nouvelle fonction)

- [ ] **Step 1.1 : Écrire le test (qui doit échouer)**

Créer `tests/test_components.py` :

```python
"""Smoke tests for shared_components. Run via `python3 tests/test_components.py`."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_components import get_booking_modal


def test_modal_has_marker():
    assert "<!-- LOGOPSI_BOOKING_MODAL -->" in get_booking_modal()


def test_modal_has_price_and_delay():
    html = get_booking_modal()
    assert "150" in html
    assert "48h" in html or "48 h" in html


def test_modal_has_two_primary_ctas():
    html = get_booking_modal()
    assert "app.logopsiestudios.com/fr/login" in html
    assert "showCallbackForm" in html


def test_modal_has_callback_form():
    html = get_booking_modal()
    assert 'action="https://formsubmit.co/contact@logopsistudios.com"' in html
    assert 'name="phone"' in html or 'type="tel"' in html
    assert 'name="email"' in html
    assert 'name="name"' in html


def test_modal_has_aria_attributes():
    html = get_booking_modal()
    assert 'role="dialog"' in html
    assert 'aria-modal="true"' in html


def test_modal_has_member_login_link():
    html = get_booking_modal()
    assert "Se connecter" in html or "Déjà client" in html


if __name__ == "__main__":
    test_modal_has_marker()
    test_modal_has_price_and_delay()
    test_modal_has_two_primary_ctas()
    test_modal_has_callback_form()
    test_modal_has_aria_attributes()
    test_modal_has_member_login_link()
    print("test_components: OK")
```

- [ ] **Step 1.2 : Lancer le test pour vérifier qu'il échoue**

Run: `python3 tests/test_components.py`
Expected: `ImportError: cannot import name 'get_booking_modal' from 'shared_components'`

- [ ] **Step 1.3 : Implémenter `get_booking_modal()` dans `shared_components.py`**

Ajouter à la fin de `shared_components.py` (juste avant la dernière fonction utilitaire ou en fin de fichier) :

```python
# ------------------------------------------------------------------
# 8. BOOKING MODAL (popup de réservation)
# ------------------------------------------------------------------

def get_booking_modal():
    """Return the booking modal HTML (3 states in DOM, hidden by default).

    Visible state controlled by classes 'modal-open' on body and data-view
    attribute on #booking-modal: 'info' | 'callback' | 'success'.
    """
    return (
        '    <!-- LOGOPSI_BOOKING_MODAL -->\n'
        '    <div id="booking-modal" class="fixed inset-0 z-[100] hidden items-center justify-center p-4" role="dialog" aria-modal="true" aria-labelledby="booking-modal-title" data-view="info">\n'
        '        <div class="absolute inset-0 bg-black/60" onclick="closeBookingModal()"></div>\n'
        '        <div class="relative bg-white rounded-3xl shadow-2xl max-w-lg w-full p-8 z-[110] modal-enter">\n'
        '            <button onclick="closeBookingModal()" aria-label="Fermer" class="absolute top-4 right-4 w-9 h-9 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-colors">\n'
        '                <i data-lucide="x" class="w-5 h-5 text-gray-700"></i>\n'
        '            </button>\n'
        '\n'
        '            <!-- VIEW: INFO -->\n'
        '            <div data-view-info>\n'
        '                <h2 id="booking-modal-title" class="text-2xl font-bold text-gray-900 mb-2">Bilan complet en ligne</h2>\n'
        '                <p class="text-primary font-semibold mb-6">150€ &middot; Sous 48h &middot; 100% en ligne</p>\n'
        '                <ul class="space-y-3 mb-8">\n'
        '                    <li class="flex items-start gap-3 text-gray-700"><i data-lucide="check" class="w-5 h-5 text-primary flex-shrink-0 mt-0.5"></i><span>Orthophoniste / psychologue diplômé(e) d’État</span></li>\n'
        '                    <li class="flex items-start gap-3 text-gray-700"><i data-lucide="check" class="w-5 h-5 text-primary flex-shrink-0 mt-0.5"></i><span>Compte-rendu détaillé fourni</span></li>\n'
        '                    <li class="flex items-start gap-3 text-gray-700"><i data-lucide="check" class="w-5 h-5 text-primary flex-shrink-0 mt-0.5"></i><span>Éligible Sécurité sociale &amp; mutuelles</span></li>\n'
        '                </ul>\n'
        '                <a href="https://app.logopsiestudios.com/fr/login" target="_blank" rel="noopener noreferrer" class="block w-full bg-primary hover:bg-primaryHover text-white font-semibold text-center py-3.5 rounded-full transition-colors mb-3">Réserver mon bilan en ligne &rarr;</a>\n'
        '                <button onclick="showCallbackForm()" class="block w-full border-2 border-primary text-primary hover:bg-primary hover:text-white font-semibold py-3 rounded-full transition-colors">Être rappelé(e) gratuitement</button>\n'
        '                <p class="text-center text-sm text-gray-500 mt-6">Déjà client&middot;e ? <a href="https://app.logopsiestudios.com/fr/login" target="_blank" rel="noopener noreferrer" class="text-primary hover:underline font-medium">Se connecter &rarr;</a></p>\n'
        '            </div>\n'
        '\n'
        '            <!-- VIEW: CALLBACK -->\n'
        '            <div data-view-callback class="hidden">\n'
        '                <button onclick="showInfoView()" class="text-sm text-gray-500 hover:text-primary mb-4 inline-flex items-center gap-1"><i data-lucide="arrow-left" class="w-4 h-4"></i> Retour</button>\n'
        '                <h2 class="text-2xl font-bold text-gray-900 mb-2">Être rappelé(e) gratuitement</h2>\n'
        '                <p class="text-gray-600 mb-6">Renseignez vos coordonnées, nous vous rappelons sous 48h ouvrées.</p>\n'
        '                <form action="https://formsubmit.co/contact@logopsistudios.com" method="POST" class="space-y-4">\n'
        '                    <input type="hidden" name="_subject" value="Demande de rappel — Logo Études">\n'
        '                    <input type="hidden" name="_template" value="table">\n'
        '                    <input type="hidden" name="_captcha" value="false">\n'
        '                    <input type="hidden" name="_next" value="">\n'
        '                    <input type="text" name="name" required placeholder="Nom et prénom" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:border-primary">\n'
        '                    <input type="tel" name="phone" required placeholder="Téléphone" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:border-primary">\n'
        '                    <input type="email" name="email" required placeholder="Email" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:border-primary">\n'
        '                    <select name="creneau" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:border-primary bg-white">\n'
        '                        <option value="indifferent">Créneau préférentiel — indifférent</option>\n'
        '                        <option value="matin">Matin (9h-12h)</option>\n'
        '                        <option value="apres-midi">Après-midi (12h-17h)</option>\n'
        '                        <option value="soir">Soir (17h-19h)</option>\n'
        '                    </select>\n'
        '                    <button type="submit" class="w-full bg-primary hover:bg-primaryHover text-white font-semibold py-3.5 rounded-full transition-colors">Envoyer ma demande</button>\n'
        '                </form>\n'
        '            </div>\n'
        '\n'
        '            <!-- VIEW: SUCCESS -->\n'
        '            <div data-view-success class="hidden text-center py-6">\n'
        '                <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-5">\n'
        '                    <i data-lucide="check" class="w-8 h-8 text-primary"></i>\n'
        '                </div>\n'
        '                <h2 class="text-2xl font-bold text-gray-900 mb-2">Demande envoyée</h2>\n'
        '                <p class="text-gray-600 mb-6">Nous vous rappelons sous 48h ouvrées.</p>\n'
        '                <button onclick="closeBookingModal()" class="bg-primary hover:bg-primaryHover text-white font-semibold px-8 py-3 rounded-full transition-colors">Fermer</button>\n'
        '            </div>\n'
        '        </div>\n'
        '    </div>\n'
    )
```

- [ ] **Step 1.4 : Lancer le test pour vérifier qu'il passe**

Run: `python3 tests/test_components.py`
Expected: `test_components: OK`

- [ ] **Step 1.5 : Commit**

```bash
git add shared_components.py tests/test_components.py
git commit -m "feat(modal): add get_booking_modal() with info/callback/success views"
```

---

### Task 2 : `get_booking_js()` + intégration dans `get_js()`

**Files:**
- Modify: `shared_components.py` (ajout `get_booking_js()`, modif `get_js()`)
- Modify: `tests/test_components.py` (ajout des tests)

- [ ] **Step 2.1 : Ajouter les tests d'abord**

Ajouter à la fin de `tests/test_components.py` (avant le bloc `if __name__`) :

```python
from shared_components import get_booking_js, get_js


def test_booking_js_exposes_open_close():
    js = get_booking_js()
    assert "function openBookingModal" in js
    assert "function closeBookingModal" in js
    assert "function showCallbackForm" in js
    assert "function showInfoView" in js


def test_booking_js_handles_escape():
    js = get_booking_js()
    assert "Escape" in js or "27" in js


def test_booking_js_handles_rappel_ok():
    js = get_booking_js()
    assert "rappel=ok" in js or "rappel" in js


def test_get_js_includes_booking_js():
    js = get_js()
    assert "openBookingModal" in js
    assert "closeBookingModal" in js
```

Et ajouter les appels correspondants au bloc `if __name__`:

```python
    test_booking_js_exposes_open_close()
    test_booking_js_handles_escape()
    test_booking_js_handles_rappel_ok()
    test_get_js_includes_booking_js()
```

- [ ] **Step 2.2 : Lancer le test pour vérifier qu'il échoue**

Run: `python3 tests/test_components.py`
Expected: `ImportError: cannot import name 'get_booking_js'`

- [ ] **Step 2.3 : Implémenter `get_booking_js()` et modifier `get_js()`**

Ajouter dans `shared_components.py`, juste après `get_booking_modal()` :

```python
def get_booking_js():
    """Return the booking-modal JS block (without surrounding <script> tags).

    Exposes window.openBookingModal, closeBookingModal, showCallbackForm,
    showInfoView. Auto-opens success view on URL ?rappel=ok.
    """
    return (
        '\n'
        '        // ---- Booking modal ----\n'
        '        function setBookingView(view) {\n'
        '            var modal = document.getElementById("booking-modal");\n'
        '            if (!modal) return;\n'
        '            modal.setAttribute("data-view", view);\n'
        '            modal.querySelector("[data-view-info]").classList.toggle("hidden", view !== "info");\n'
        '            modal.querySelector("[data-view-callback]").classList.toggle("hidden", view !== "callback");\n'
        '            modal.querySelector("[data-view-success]").classList.toggle("hidden", view !== "success");\n'
        '        }\n'
        '        function openBookingModal() {\n'
        '            var modal = document.getElementById("booking-modal");\n'
        '            if (!modal) return;\n'
        '            modal.classList.remove("hidden");\n'
        '            modal.classList.add("flex");\n'
        '            document.body.style.overflow = "hidden";\n'
        '            var nextInput = modal.querySelector(\'input[name="_next"]\');\n'
        '            if (nextInput) {\n'
        '                var url = new URL(window.location.href);\n'
        '                url.searchParams.set("rappel", "ok");\n'
        '                nextInput.value = url.toString();\n'
        '            }\n'
        '            setBookingView("info");\n'
        '            if (window.lucide) { window.lucide.createIcons(); }\n'
        '        }\n'
        '        function closeBookingModal() {\n'
        '            var modal = document.getElementById("booking-modal");\n'
        '            if (!modal) return;\n'
        '            modal.classList.add("hidden");\n'
        '            modal.classList.remove("flex");\n'
        '            document.body.style.overflow = "";\n'
        '        }\n'
        '        function showCallbackForm() { setBookingView("callback"); if (window.lucide) { window.lucide.createIcons(); } }\n'
        '        function showInfoView() { setBookingView("info"); if (window.lucide) { window.lucide.createIcons(); } }\n'
        '        document.addEventListener("keydown", function(e) {\n'
        '            if (e.key === "Escape") { closeBookingModal(); }\n'
        '        });\n'
        '        // Generic class hook\n'
        '        document.addEventListener("click", function(e) {\n'
        '            var t = e.target.closest(".js-open-booking");\n'
        '            if (t) { e.preventDefault(); openBookingModal(); }\n'
        '        });\n'
        '        // Auto-open success view if ?rappel=ok\n'
        '        (function() {\n'
        '            try {\n'
        '                var p = new URLSearchParams(window.location.search);\n'
        '                if (p.get("rappel") === "ok") {\n'
        '                    openBookingModal();\n'
        '                    setBookingView("success");\n'
        '                    if (window.lucide) { window.lucide.createIcons(); }\n'
        '                }\n'
        '            } catch (err) {}\n'
        '        })();\n'
    )
```

Modifier `get_js()` pour inclure le booking JS. Repérer la ligne actuelle :

```python
        '        function toggleMobileMenu() { document.getElementById(\'mobile-menu\').classList.toggle(\'hidden\'); }\n'
        + faq_js +
        '    </script>\n'
```

Remplacer par :

```python
        '        function toggleMobileMenu() { document.getElementById(\'mobile-menu\').classList.toggle(\'hidden\'); }\n'
        + faq_js
        + get_booking_js() +
        '    </script>\n'
```

- [ ] **Step 2.4 : Lancer le test pour vérifier qu'il passe**

Run: `python3 tests/test_components.py`
Expected: `test_components: OK`

- [ ] **Step 2.5 : Commit**

```bash
git add shared_components.py tests/test_components.py
git commit -m "feat(modal): add get_booking_js() and wire into get_js()"
```

---

### Task 3 : Mise à jour `get_navbar()` — lien Connexion + hook popup

**Files:**
- Modify: `shared_components.py` (fonction `get_navbar()`)
- Modify: `tests/test_components.py`

- [ ] **Step 3.1 : Ajouter les tests**

Ajouter à `tests/test_components.py` (avant le bloc `if __name__`) :

```python
from shared_components import get_navbar


def test_navbar_has_connexion_link_desktop():
    html = get_navbar("./")
    assert "Connexion" in html
    assert "app.logopsiestudios.com/fr/login" in html
    # The desktop link should be in the gap-4 container alongside the green CTA
    assert html.count("app.logopsiestudios.com/fr/login") >= 2  # desktop + mobile


def test_navbar_cta_opens_popup():
    html = get_navbar("./")
    # The "Prendre rendez-vous" green button should NOT link to contact.html anymore
    # It should call openBookingModal()
    assert "openBookingModal()" in html


def test_navbar_keeps_prefix_for_other_links():
    html = get_navbar("../")
    assert "../orthophonie/" in html
```

Et ajouter les appels au bloc `if __name__` :

```python
    test_navbar_has_connexion_link_desktop()
    test_navbar_cta_opens_popup()
    test_navbar_keeps_prefix_for_other_links()
```

- [ ] **Step 3.2 : Lancer le test pour vérifier qu'il échoue**

Run: `python3 tests/test_components.py`
Expected: `AssertionError` sur `Connexion` ou `openBookingModal()`.

- [ ] **Step 3.3 : Modifier `get_navbar()`**

Dans `shared_components.py`, fonction `get_navbar()`, repérer le bloc desktop CTA :

```python
        '                <div class="hidden lg:flex items-center gap-4">\n'
        '                    <a href="' + prefix + 'contact.html" class="bg-primary text-white font-semibold px-6 py-2.5 rounded-full hover:bg-primaryHover transition-colors shadow-md text-[15px]">\n'
        '                        Prendre rendez-vous\n'
        '                    </a>\n'
        '                </div>\n'
```

Remplacer par :

```python
        '                <div class="hidden lg:flex items-center gap-4">\n'
        '                    <a href="https://app.logopsiestudios.com/fr/login" target="_blank" rel="noopener noreferrer" class="text-[15px] font-semibold text-gray-700 hover:text-primary transition-colors">\n'
        '                        Connexion\n'
        '                    </a>\n'
        '                    <a href="#" onclick="openBookingModal(); return false;" class="bg-primary text-white font-semibold px-6 py-2.5 rounded-full hover:bg-primaryHover transition-colors shadow-md text-[15px]">\n'
        '                        Prendre rendez-vous\n'
        '                    </a>\n'
        '                </div>\n'
```

Repérer le bloc mobile CTA :

```python
        '                <a href="' + prefix + 'contact.html" class="w-full bg-primary text-white font-semibold py-3 rounded-full shadow-md mt-4 block text-center">Prendre rendez-vous</a>\n'
```

Remplacer par :

```python
        '                <a href="https://app.logopsiestudios.com/fr/login" target="_blank" rel="noopener noreferrer" class="block text-center font-semibold py-2 text-gray-700 hover:text-primary border-b border-gray-100">Connexion</a>\n'
        '                <a href="#" onclick="openBookingModal(); return false;" class="w-full bg-primary text-white font-semibold py-3 rounded-full shadow-md mt-4 block text-center">Prendre rendez-vous</a>\n'
```

- [ ] **Step 3.4 : Lancer le test pour vérifier qu'il passe**

Run: `python3 tests/test_components.py`
Expected: `test_components: OK`

- [ ] **Step 3.5 : Commit**

```bash
git add shared_components.py tests/test_components.py
git commit -m "feat(navbar): add Connexion link, hook CTA to booking popup"
```

---

### Task 4 : Mise à jour `get_footer()` — lien Espace membre

**Files:**
- Modify: `shared_components.py` (fonction `get_footer()`)
- Modify: `tests/test_components.py`

- [ ] **Step 4.1 : Ajouter les tests**

Ajouter à `tests/test_components.py` :

```python
from shared_components import get_footer


def test_footer_has_espace_membre_link():
    html = get_footer("./")
    assert "Espace membre" in html
    assert "app.logopsiestudios.com/fr/login" in html
```

Et l'appel dans le bloc `if __name__`:

```python
    test_footer_has_espace_membre_link()
```

- [ ] **Step 4.2 : Lancer le test (échoue)**

Run: `python3 tests/test_components.py`
Expected: `AssertionError` sur "Espace membre".

- [ ] **Step 4.3 : Modifier `get_footer()`**

Dans `shared_components.py`, fonction `get_footer()`, repérer la rangée de liens légaux :

```python
        '                <div class="flex space-x-6 mt-4 md:mt-0">\n'
        '                    <a href="' + prefix + 'mentions-legales.html" class="text-gray-500 hover:text-primary text-sm transition-colors">Mentions légales</a>\n'
        '                    <a href="' + prefix + 'contact.html" class="text-gray-500 hover:text-primary text-sm transition-colors">Contact</a>\n'
        '                    <a href="' + prefix + 'a-propos.html" class="text-gray-500 hover:text-primary text-sm transition-colors">À propos</a>\n'
        '                </div>\n'
```

Remplacer par :

```python
        '                <div class="flex flex-wrap gap-x-6 gap-y-2 mt-4 md:mt-0">\n'
        '                    <a href="' + prefix + 'mentions-legales.html" class="text-gray-500 hover:text-primary text-sm transition-colors">Mentions légales</a>\n'
        '                    <a href="' + prefix + 'contact.html" class="text-gray-500 hover:text-primary text-sm transition-colors">Contact</a>\n'
        '                    <a href="' + prefix + 'a-propos.html" class="text-gray-500 hover:text-primary text-sm transition-colors">À propos</a>\n'
        '                    <a href="https://app.logopsiestudios.com/fr/login" target="_blank" rel="noopener noreferrer" class="text-gray-500 hover:text-primary text-sm transition-colors">Espace membre</a>\n'
        '                </div>\n'
```

- [ ] **Step 4.4 : Lancer le test**

Run: `python3 tests/test_components.py`
Expected: `test_components: OK`

- [ ] **Step 4.5 : Commit**

```bash
git add shared_components.py tests/test_components.py
git commit -m "feat(footer): add Espace membre link"
```

---

### Task 5 : Réécriture `get_cta_section()` — wording 150€/48h

**Files:**
- Modify: `shared_components.py` (fonction `get_cta_section()`)
- Modify: `tests/test_components.py`

- [ ] **Step 5.1 : Ajouter les tests**

Ajouter à `tests/test_components.py` :

```python
from shared_components import get_cta_section


def test_cta_section_uses_new_wording():
    html = get_cta_section("Prêt à commencer ?", "Réservez votre bilan en quelques clics.")
    assert "150" in html
    assert "48h" in html or "48 h" in html
    assert "openBookingModal()" in html
    # Old wording must be gone
    assert "tarifs sur demande" not in html
```

Et l'appel :

```python
    test_cta_section_uses_new_wording()
```

- [ ] **Step 5.2 : Lancer le test (échoue)**

Run: `python3 tests/test_components.py`
Expected: `AssertionError` sur "150" ou "openBookingModal".

- [ ] **Step 5.3 : Réécrire `get_cta_section()`**

Remplacer entièrement la fonction `get_cta_section` dans `shared_components.py` par :

```python
def get_cta_section(title, desc):
    """Return the green CTA banner section, highlighting the 150€/48h offer."""

    return (
        '    <!-- CTA -->\n'
        '    <section class="py-20">\n'
        '        <div class="max-w-4xl mx-auto px-6">\n'
        '            <div class="bg-primary rounded-3xl p-12 text-center text-white relative overflow-hidden">\n'
        '                <div class="absolute inset-0 opacity-10">\n'
        '                    <svg viewBox="0 0 100 100" preserveAspectRatio="none" class="w-full h-full">\n'
        '                        <path d="M0,20 Q25,0 50,20 T100,20 V100 H0 Z" fill="white"/>\n'
        '                    </svg>\n'
        '                </div>\n'
        '                <div class="relative z-10">\n'
        '                    <p class="uppercase tracking-widest text-sm text-green-50 mb-2">Bilan complet en ligne</p>\n'
        '                    <h2 class="text-4xl md:text-5xl font-bold mb-3">150&euro; &middot; sous 48h</h2>\n'
        '                    <p class="text-lg mb-8 text-green-50 max-w-xl mx-auto">' + desc + '</p>\n'
        '                    <button type="button" onclick="openBookingModal()" class="bg-white text-primary px-8 py-4 rounded-full font-bold hover:bg-green-50 transition text-lg inline-block shadow-lg">\n'
        '                        Réserver mon bilan\n'
        '                    </button>\n'
        '                    <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-3 max-w-2xl mx-auto">\n'
        '                        <p class="text-sm text-green-50"><i data-lucide="check-circle" class="w-4 h-4 inline mr-1"></i>Compte-rendu détaillé</p>\n'
        '                        <p class="text-sm text-green-50"><i data-lucide="check-circle" class="w-4 h-4 inline mr-1"></i>Sécu &amp; mutuelles</p>\n'
        '                        <p class="text-sm text-green-50"><i data-lucide="check-circle" class="w-4 h-4 inline mr-1"></i>Sous 48h</p>\n'
        '                    </div>\n'
        '                </div>\n'
        '            </div>\n'
        '        </div>\n'
        '    </section>\n'
    )
```

Note : on ignore désormais le paramètre `title` (gardé pour compat avec les générateurs existants qui le passent). Le titre est fixé à "150€ · sous 48h". Si une page veut un titre custom, c'est une régression mineure acceptable (le wording uniforme est l'objectif).

- [ ] **Step 5.4 : Lancer le test**

Run: `python3 tests/test_components.py`
Expected: `test_components: OK`

- [ ] **Step 5.5 : Commit**

```bash
git add shared_components.py tests/test_components.py
git commit -m "feat(cta): rewrite get_cta_section with 150€/48h wording + popup hook"
```

---

## Phase 2 — Infrastructure SEO titles

### Task 6 : Création de `seo_titles.py`

**Files:**
- Create: `seo_titles.py`
- Create: `tests/test_seo_titles.py`

- [ ] **Step 6.1 : Écrire les tests**

Créer `tests/test_seo_titles.py` :

```python
"""Tests for seo_titles mappings. Run via `python3 tests/test_seo_titles.py`."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seo_titles import (
    title_for_ortho_n2, title_for_ortho_n3, title_for_ortho_n4,
    title_for_psycho_n2, title_for_psycho_n3, title_for_psycho_n4,
    title_for_scolaire_n2, title_for_scolaire_n3, title_for_scolaire_n4,
    title_for_handwritten,
    meta_desc_for_ortho_n2, meta_desc_for_psycho_n2,
)


def test_ortho_n2_dyslexie():
    assert title_for_ortho_n2("dyslexie") == "Bilan dyslexie en ligne — Orthophoniste 150€ | Logo Études"


def test_ortho_n2_oralite():
    assert title_for_ortho_n2("oralite") == "Bilan troubles de l'oralité — Orthophoniste 150€ | Logo Études"


def test_ortho_n3_paris():
    assert title_for_ortho_n3("paris") == "Bilan orthophonique à Paris — 150€, sous 48h | Logo Études"


def test_ortho_n4_dyslexie_paris():
    assert title_for_ortho_n4("dyslexie", "paris") == "Bilan dyslexie à Paris — Orthophoniste en ligne 150€ | Logo Études"


def test_psycho_n2_tdah():
    assert title_for_psycho_n2("tdah") == "Bilan TDAH en ligne — Psychologue 150€ | Logo Études"


def test_scolaire_n4():
    assert title_for_scolaire_n4("mathematiques", "3eme", "paris") == "Bilan mathématiques 3ème à Paris — 150€ | Logo Études"


def test_handwritten_index():
    assert title_for_handwritten("site/index.html") == "Bilan orthophonie, psychologie & soutien — 150€, 48h | Logo Études"


def test_handwritten_contact_unchanged():
    assert title_for_handwritten("site/contact.html") is None  # None means: do not modify


def test_meta_desc_ortho_n2():
    desc = meta_desc_for_ortho_n2("dyslexie")
    assert "150" in desc
    assert "48h" in desc or "48 h" in desc


if __name__ == "__main__":
    test_ortho_n2_dyslexie()
    test_ortho_n2_oralite()
    test_ortho_n3_paris()
    test_ortho_n4_dyslexie_paris()
    test_psycho_n2_tdah()
    test_scolaire_n4()
    test_handwritten_index()
    test_handwritten_contact_unchanged()
    test_meta_desc_ortho_n2()
    print("test_seo_titles: OK")
```

- [ ] **Step 6.2 : Lancer le test (échoue)**

Run: `python3 tests/test_seo_titles.py`
Expected: `ModuleNotFoundError: No module named 'seo_titles'`

- [ ] **Step 6.3 : Créer `seo_titles.py`**

Créer `/workspaces/Logoestudios/seo_titles.py` :

```python
"""Centralised SEO titles and meta descriptions for the Logo Études site.

Used by:
  - generate_level2_pages.py  (trouble pages)
  - generate_level3_4_pages.py (city hubs + trouble+city)
  - generate_physique_chimie.py
  - patch_handwritten_pages.py (index, hubs N2, etc.)
"""

from generate_level3_4_pages import display_name as _display_name


SUFFIX = " | Logo Études"


CITY_NAMES = {
    "paris": "Paris",
    "marseille": "Marseille",
    "lyon": "Lyon",
    "toulouse": "Toulouse",
    "nice": "Nice",
}


SUBJECT_LABELS = {
    "mathematiques": "mathématiques",
    "francais": "français",
    "anglais": "anglais",
    "espagnol": "espagnol",
    "physique-chimie": "physique-chimie",
    "aide-aux-devoirs": "aide aux devoirs",
}


LEVEL_LABELS = {
    "cp": "CP", "ce1": "CE1", "ce2": "CE2", "cm1": "CM1", "cm2": "CM2",
    "6eme": "6ème", "5eme": "5ème", "4eme": "4ème", "3eme": "3ème",
    "seconde": "seconde", "premiere": "première", "terminale": "terminale",
}


# ---- ORTHOPHONIE ----

def title_for_ortho_n2(slug):
    return "Bilan " + _display_name(slug).lower() + " en ligne — Orthophoniste 150€" + SUFFIX


def title_for_ortho_n3(city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return "Bilan orthophonique à " + city + " — 150€, sous 48h" + SUFFIX


def title_for_ortho_n4(trouble_slug, city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return "Bilan " + _display_name(trouble_slug).lower() + " à " + city + " — Orthophoniste en ligne 150€" + SUFFIX


def meta_desc_for_ortho_n2(slug):
    name = _display_name(slug).lower()
    return ("Bilan orthophonique pour la " + name + " en ligne — 150€, rendez-vous sous 48h. "
            "Orthophonistes diplômés d'État, partout en France.")


def meta_desc_for_ortho_n3(city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return ("Bilan orthophonique en ligne pour les habitants de " + city + ". 150€, rendez-vous sous 48h. "
            "Orthophonistes diplômés d'État, 100% en visio.")


def meta_desc_for_ortho_n4(trouble_slug, city_slug):
    name = _display_name(trouble_slug).lower()
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return ("Bilan orthophonique pour la " + name + " à " + city + " en ligne — 150€, sous 48h. "
            "Orthophonistes diplômés d'État, séances 100% en visio depuis " + city + ".")


# ---- PSYCHOLOGIE ----

def title_for_psycho_n2(slug):
    return "Bilan " + _display_name(slug) + " en ligne — Psychologue 150€" + SUFFIX


def title_for_psycho_n3(city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return "Bilan psychologique à " + city + " — 150€, sous 48h" + SUFFIX


def title_for_psycho_n4(trouble_slug, city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return "Bilan " + _display_name(trouble_slug) + " à " + city + " — Psychologue en ligne 150€" + SUFFIX


def meta_desc_for_psycho_n2(slug):
    name = _display_name(slug)
    return ("Bilan psychologique pour " + name + " en ligne — 150€, rendez-vous sous 48h. "
            "Psychologues diplômés d'État, partout en France.")


def meta_desc_for_psycho_n3(city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return ("Bilan psychologique en ligne pour les habitants de " + city + ". 150€, rendez-vous sous 48h. "
            "Psychologues diplômés d'État, 100% en visio.")


def meta_desc_for_psycho_n4(trouble_slug, city_slug):
    name = _display_name(trouble_slug)
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return ("Bilan psychologique pour " + name + " à " + city + " en ligne — 150€, sous 48h. "
            "Psychologues diplômés d'État, séances 100% en visio depuis " + city + ".")


# ---- SOUTIEN SCOLAIRE ----

def title_for_scolaire_n2(subject_slug, level_slug):
    subj = SUBJECT_LABELS.get(subject_slug, subject_slug)
    lvl = LEVEL_LABELS.get(level_slug, level_slug)
    return "Bilan " + subj + " " + lvl + " en ligne — 150€" + SUFFIX


def title_for_scolaire_n3(city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return "Soutien scolaire à " + city + " — Bilan 150€" + SUFFIX


def title_for_scolaire_n4(subject_slug, level_slug, city_slug):
    subj = SUBJECT_LABELS.get(subject_slug, subject_slug)
    lvl = LEVEL_LABELS.get(level_slug, level_slug)
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return "Bilan " + subj + " " + lvl + " à " + city + " — 150€" + SUFFIX


def meta_desc_for_scolaire_n2(subject_slug, level_slug):
    subj = SUBJECT_LABELS.get(subject_slug, subject_slug)
    lvl = LEVEL_LABELS.get(level_slug, level_slug)
    return ("Bilan pédagogique de " + subj + " niveau " + lvl + " en ligne — 150€, sous 48h. "
            "Enseignants qualifiés, cours particuliers 100% en visio.")


def meta_desc_for_scolaire_n3(city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return ("Soutien scolaire en ligne pour les élèves de " + city + ". Bilan pédagogique à 150€, sous 48h. "
            "Enseignants qualifiés du primaire au lycée.")


def meta_desc_for_scolaire_n4(subject_slug, level_slug, city_slug):
    subj = SUBJECT_LABELS.get(subject_slug, subject_slug)
    lvl = LEVEL_LABELS.get(level_slug, level_slug)
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return ("Bilan pédagogique de " + subj + " " + lvl + " à " + city + " — 150€, sous 48h. "
            "Cours particuliers 100% en visio depuis " + city + ".")


# ---- HAND-WRITTEN PAGES ----

# None means: do not modify the title.
HANDWRITTEN_TITLES = {
    "site/index.html": "Bilan orthophonie, psychologie & soutien — 150€, 48h | Logo Études",
    "site/orthophonie/index.html": "Bilan orthophonique en ligne — 150€, sous 48h | Logo Études",
    "site/psychologie/index.html": "Bilan psychologique en ligne — 150€, sous 48h | Logo Études",
    "site/soutien-scolaire/index.html": "Bilan pédagogique en ligne — 150€, sous 48h | Logo Études",
    "site/contact.html": None,
    "site/a-propos.html": None,
    "site/mentions-legales.html": None,
}


HANDWRITTEN_META_DESCS = {
    "site/index.html": "Orthophonie, psychologie et soutien scolaire en ligne. Bilan complet à 150€, rendez-vous sous 48h, 100% en visio. Professionnels diplômés d'État, partout en France.",
    "site/orthophonie/index.html": "Bilan orthophonique en ligne pour enfants et adolescents — 150€, sous 48h. Orthophonistes diplômés d'État. Tous troubles du langage et des apprentissages.",
    "site/psychologie/index.html": "Bilan psychologique en ligne pour enfants et adolescents — 150€, sous 48h. Psychologues diplômés d'État, accompagnement personnalisé.",
    "site/soutien-scolaire/index.html": "Soutien scolaire en ligne du primaire au lycée. Bilan pédagogique à 150€, sous 48h. Enseignants qualifiés, cours particuliers 100% en visio.",
}


def title_for_handwritten(rel_path):
    """Return the new title for a hand-written page, or None to leave unchanged."""
    return HANDWRITTEN_TITLES.get(rel_path)


def meta_desc_for_handwritten(rel_path):
    return HANDWRITTEN_META_DESCS.get(rel_path)
```

- [ ] **Step 6.4 : Lancer le test**

Run: `python3 tests/test_seo_titles.py`
Expected: `test_seo_titles: OK`

- [ ] **Step 6.5 : Commit**

```bash
git add seo_titles.py tests/test_seo_titles.py
git commit -m "feat(seo): add seo_titles.py with centralized title/meta mappings"
```

---

### Task 7 : Wire `seo_titles` dans `generate_level3_4_pages.py`

**Files:**
- Modify: `generate_level3_4_pages.py`

- [ ] **Step 7.1 : Importer `seo_titles`**

En haut de `generate_level3_4_pages.py`, après les imports existants (vers la ligne 24), ajouter :

```python
from seo_titles import (
    title_for_ortho_n3, title_for_ortho_n4,
    title_for_psycho_n3, title_for_psycho_n4,
    title_for_scolaire_n3, title_for_scolaire_n4,
    meta_desc_for_ortho_n3, meta_desc_for_ortho_n4,
    meta_desc_for_psycho_n3, meta_desc_for_psycho_n4,
    meta_desc_for_scolaire_n3, meta_desc_for_scolaire_n4,
)
```

- [ ] **Step 7.2 : Remplacer les title/meta_desc dans `generate_ortho_psycho_n3`**

Repérer (vers la ligne 1083) :

```python
    title = practitioner_label + " enfant à " + city + " en ligne"
    meta_desc = (
        practitioner_label + " pour enfant à " + city + " en ligne. "
        "Consultation sous 48h avec un " + practitioner + " diplômé. "
        "Prise en charge rapide, 100% en visio depuis " + city + "."
    )
```

Remplacer par :

```python
    if category == "orthophonie":
        title = title_for_ortho_n3(cslug)
        meta_desc = meta_desc_for_ortho_n3(cslug)
    else:
        title = title_for_psycho_n3(cslug)
        meta_desc = meta_desc_for_psycho_n3(cslug)
```

- [ ] **Step 7.3 : Remplacer les title/meta_desc dans `generate_ortho_psycho_n4`**

Repérer (vers la ligne 1222) :

```python
    title = practitioner_label + " " + dname + " à " + city + " en ligne"
    meta_desc = (
        practitioner_label + " spécialisé en " + dname.lower() + " pour enfant à " + city
        + ". Consultation en ligne sous 48h avec un " + practitioner
        + " diplômé. Accompagnement personnalisé depuis " + city + "."
    )
```

Remplacer par :

```python
    if category == "orthophonie":
        title = title_for_ortho_n4(slug, cslug)
        meta_desc = meta_desc_for_ortho_n4(slug, cslug)
    else:
        title = title_for_psycho_n4(slug, cslug)
        meta_desc = meta_desc_for_psycho_n4(slug, cslug)
```

- [ ] **Step 7.4 : Remplacer le title dans `generate_scolaire_n3`**

Repérer (vers la ligne 1440) :

```python
    title = "Soutien scolaire à " + city + " en ligne"
    meta_desc = (
        ...
    )
```

Remplacer par :

```python
    title = title_for_scolaire_n3(cslug)
    meta_desc = meta_desc_for_scolaire_n3(cslug)
```

(Garder l'appel mais retirer le bloc multi-lignes du `meta_desc` initial.)

- [ ] **Step 7.5 : Remplacer le title dans `generate_scolaire_n4`**

Repérer (vers la ligne 1573) :

```python
    title = subj_label + " " + level_label + " à " + city + " - Cours en ligne"
    meta_desc = (
        ...
    )
```

Remplacer par :

```python
    title = title_for_scolaire_n4(subject_slug, level_slug, cslug)
    meta_desc = meta_desc_for_scolaire_n4(subject_slug, level_slug, cslug)
```

- [ ] **Step 7.6 : Smoke test rapide via une dry-run**

Run :
```bash
python3 -c "
import generate_level3_4_pages as g
# Just verify imports + a function builds title correctly
from seo_titles import title_for_ortho_n3
assert 'Bilan orthophonique à Paris' in title_for_ortho_n3('paris')
print('imports OK')
"
```
Expected: `imports OK`

- [ ] **Step 7.7 : Commit**

```bash
git add generate_level3_4_pages.py
git commit -m "feat(seo): wire seo_titles in generate_level3_4_pages.py"
```

---

### Task 8 : Wire `seo_titles` dans `generate_level2_pages.py` + injection booking modal

**Files:**
- Modify: `generate_level2_pages.py`

- [ ] **Step 8.1 : Importer `seo_titles`, `get_booking_modal`, `get_booking_js`**

En haut de `generate_level2_pages.py`, après les imports `os, json` (ligne 5), ajouter :

```python
from shared_components import get_booking_modal, get_booking_js
from seo_titles import title_for_ortho_n2, title_for_psycho_n2
```

- [ ] **Step 8.2 : Remplacer le title et meta description dans `generate_page`**

Repérer (vers la ligne 864) dans le f-string HTML :

```python
    <title>{data["title"]} - Logo Études</title>
    <meta name="description" content="{data["meta_desc"]}">
```

Modifier en amont du f-string (juste avant `html = f"""<!DOCTYPE html>`) pour calculer le bon titre :

```python
    if is_ortho:
        page_title = title_for_ortho_n2(slug)
    elif is_psycho:
        page_title = title_for_psycho_n2(slug)
    else:
        page_title = data["title"] + " - Logo Études"
```

Et dans le f-string remplacer les deux lignes ci-dessus par :

```python
    <title>{page_title}</title>
    <meta name="description" content="{data["meta_desc"]}">
```

(On garde `data["meta_desc"]` car les meta descriptions des pages troubles N2 sont déjà rédigées avec soin dans le data ; si vous voulez forcer "150€/48h", c'est un travail séparé.)

- [ ] **Step 8.3 : Injecter le booking modal HTML+JS dans la sortie**

À la fin de `generate_page`, repérer la fin de la fonction (avant `return html`). Vérifier que `</body>` est dans le f-string. Si oui, modifier la dernière partie pour injecter le modal et le JS avant `</body>`.

Repérer dans le f-string la fin (cherche `</body>` ou `</script>` final). Selon ce qu'on trouve, deux cas :

**Cas A** — la fonction retourne le HTML directement avec `</body>` à l'intérieur du f-string :
Trouver `</body>` dans le f-string et insérer juste avant :
```
{get_booking_modal()}
<script>{get_booking_js()}</script>
```

**Cas B** — sinon, après le f-string et avant `return html`, ajouter :
```python
    # Inject booking modal & JS just before </body>
    if "</body>" in html:
        injection = get_booking_modal() + "\n    <script>" + get_booking_js() + "    </script>\n"
        html = html.replace("</body>", injection + "</body>", 1)
```

(Cas B est plus robuste — préférer cette approche.)

- [ ] **Step 8.4 : Mettre à jour la navbar et les CTAs inlinés dans `generate_level2_pages.py`**

Comme `generate_level2_pages.py` inline sa propre navbar (ne réutilise pas `get_navbar`), il faut modifier le f-string de la navbar pour :
- Ajouter le lien "Connexion" (texte + lien externe) à gauche du bouton vert
- Remplacer le `href="contact.html"` du bouton vert par `href="#"` + `onclick="openBookingModal(); return false;"`
- Idem pour la version mobile
- Ajouter "Espace membre" dans le footer inliné

Repérer dans le f-string les blocs équivalents et appliquer les mêmes substitutions que la Task 3 et la Task 4.

**Conseil** : faire un `grep -n "contact.html\|Prendre rendez-vous" generate_level2_pages.py` pour localiser tous les endroits.

```bash
grep -n "contact.html\|Prendre rendez-vous\|Espace membre\|Connexion" /workspaces/Logoestudios/generate_level2_pages.py
```

Pour chaque occurrence du bouton "Prendre rendez-vous" (desktop + mobile), appliquer la substitution. Pour le footer, ajouter `<a href="https://app.logopsiestudios.com/fr/login" target="_blank" rel="noopener noreferrer" ...>Espace membre</a>` à côté de Mentions légales / Contact / À propos.

- [ ] **Step 8.5 : Smoke test — générer une page et vérifier qu'elle contient les nouveaux éléments**

Run :
```bash
cd /workspaces/Logoestudios && python3 -c "
from generate_level2_pages import ORTHO_PAGES, generate_page
html = generate_page('dyslexie', ORTHO_PAGES['dyslexie'], 'orthophonie')
assert 'Bilan dyslexie en ligne' in html, 'title missing'
assert 'LOGOPSI_BOOKING_MODAL' in html, 'modal missing'
assert 'openBookingModal' in html, 'JS missing'
assert 'Connexion' in html, 'Connexion link missing'
assert 'Espace membre' in html, 'Espace membre missing'
print('generate_level2 OK')
"
```
Expected: `generate_level2 OK`

- [ ] **Step 8.6 : Commit**

```bash
git add generate_level2_pages.py
git commit -m "feat(level2): wire seo_titles, inject booking modal, add Connexion + Espace membre"
```

---

### Task 9 : Wire `seo_titles` dans `generate_physique_chimie.py`

**Files:**
- Modify: `generate_physique_chimie.py`

- [ ] **Step 9.1 : Localiser la construction du titre**

Run :
```bash
grep -n "title = \|<title>" /workspaces/Logoestudios/generate_physique_chimie.py
```

- [ ] **Step 9.2 : Importer et brancher**

En haut, ajouter :
```python
from seo_titles import (
    title_for_scolaire_n2, title_for_scolaire_n4,
    meta_desc_for_scolaire_n2, meta_desc_for_scolaire_n4,
)
```

Pour chaque construction de `title = ...`, remplacer par l'appel approprié :
- Page niveau (ex: `physique-chimie/3eme.html`) → `title_for_scolaire_n2("physique-chimie", level_slug)`
- Page niveau+ville → `title_for_scolaire_n4("physique-chimie", level_slug, cslug)`

- [ ] **Step 9.3 : Smoke test**

Run :
```bash
cd /workspaces/Logoestudios && python3 -c "
import generate_physique_chimie  # import only triggers no errors
from seo_titles import title_for_scolaire_n2
assert 'Bilan physique-chimie 3ème' in title_for_scolaire_n2('physique-chimie', '3eme')
print('OK')
"
```
Expected: `OK`

- [ ] **Step 9.4 : Commit**

```bash
git add generate_physique_chimie.py
git commit -m "feat(seo): wire seo_titles in generate_physique_chimie.py"
```

---

## Phase 3 — Régénération

### Task 10 : Régénérer toutes les pages générées

**Files:**
- Modify: `site/**/*.html` (sortie des générateurs)

- [ ] **Step 10.1 : Régénérer level 2 (pages troubles)**

Run :
```bash
cd /workspaces/Logoestudios && python3 generate_level2_pages.py
```
Expected: pas d'erreur, plein de fichiers réécrits sous `site/orthophonie/*.html` et `site/psychologie/*.html`.

- [ ] **Step 10.2 : Régénérer level 3/4**

Run :
```bash
cd /workspaces/Logoestudios && python3 generate_level3_4_pages.py
```
Expected: pas d'erreur.

- [ ] **Step 10.3 : Régénérer physique-chimie**

Run :
```bash
cd /workspaces/Logoestudios && python3 generate_physique_chimie.py
```
Expected: pas d'erreur.

- [ ] **Step 10.4 : Vérifier les nouveaux titres dans 4 fichiers échantillons**

Run :
```bash
grep -H "<title>" /workspaces/Logoestudios/site/orthophonie/dyslexie.html /workspaces/Logoestudios/site/orthophonie/villes/dyslexie-paris.html /workspaces/Logoestudios/site/psychologie/tdah.html /workspaces/Logoestudios/site/soutien-scolaire/mathematiques/3eme.html
```
Expected:
```
.../orthophonie/dyslexie.html:    <title>Bilan dyslexie en ligne — Orthophoniste 150€ | Logo Études</title>
.../orthophonie/villes/dyslexie-paris.html:    <title>Bilan dyslexie à Paris — Orthophoniste en ligne 150€ | Logo Études</title>
.../psychologie/tdah.html:    <title>Bilan TDAH en ligne — Psychologue 150€ | Logo Études</title>
.../soutien-scolaire/mathematiques/3eme.html:    <title>Bilan mathématiques 3ème en ligne — 150€ | Logo Études</title>
```

- [ ] **Step 10.5 : Vérifier que la popup est bien injectée**

Run :
```bash
grep -l "LOGOPSI_BOOKING_MODAL" /workspaces/Logoestudios/site/orthophonie/*.html /workspaces/Logoestudios/site/orthophonie/villes/*.html | wc -l
```
Expected: ≥ 60 (toutes les pages générées orthophonie + villes).

- [ ] **Step 10.6 : Commit**

```bash
git add site/
git commit -m "build: regenerate all pages with new SEO titles + booking modal"
```

---

## Phase 4 — Patch des pages hand-written

### Task 11 : Création de `patch_handwritten_pages.py` — squelette + idempotence

**Files:**
- Create: `patch_handwritten_pages.py`
- Create: `tests/test_patch_handwritten_pages.py`
- Create: `tests/fixtures/sample_handwritten.html`

- [ ] **Step 11.1 : Créer une fixture HTML d'exemple**

Créer `tests/fixtures/sample_handwritten.html` :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Sample - Logo Études</title>
    <meta name="description" content="Sample meta">
</head>
<body class="bg-light">
    <nav class="bg-white">
        <a href="./contact.html" class="bg-primary">Prendre rendez-vous</a>
    </nav>
    <main><h1>Title</h1></main>
    <footer>
        <a href="./mentions-legales.html">Mentions légales</a>
        <a href="./contact.html">Contact</a>
        <a href="./a-propos.html">À propos</a>
    </footer>
</body>
</html>
```

- [ ] **Step 11.2 : Écrire le test d'idempotence**

Créer `tests/test_patch_handwritten_pages.py` :

```python
"""Tests for patch_handwritten_pages. Run via `python3 tests/test_patch_handwritten_pages.py`."""

import sys
import os
import shutil
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patch_handwritten_pages import patch_file, MARKER

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "sample_handwritten.html")


def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _setup_tempfile():
    tmpdir = tempfile.mkdtemp()
    dest = os.path.join(tmpdir, "site", "test-page.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy(FIXTURE, dest)
    return tmpdir, dest


def test_patch_inserts_marker():
    tmpdir, dest = _setup_tempfile()
    try:
        patch_file(dest, rel_path="site/test-page.html")
        content = _read(dest)
        assert MARKER in content
    finally:
        shutil.rmtree(tmpdir)


def test_patch_is_idempotent():
    tmpdir, dest = _setup_tempfile()
    try:
        patch_file(dest, rel_path="site/test-page.html")
        first = _read(dest)
        patch_file(dest, rel_path="site/test-page.html")
        second = _read(dest)
        assert first == second
        # Marker should appear exactly once
        assert second.count(MARKER) == 1
    finally:
        shutil.rmtree(tmpdir)


if __name__ == "__main__":
    test_patch_inserts_marker()
    test_patch_is_idempotent()
    print("test_patch_handwritten_pages: OK")
```

- [ ] **Step 11.3 : Lancer le test (échoue)**

Run: `python3 tests/test_patch_handwritten_pages.py`
Expected: `ModuleNotFoundError: No module named 'patch_handwritten_pages'`

- [ ] **Step 11.4 : Créer le squelette `patch_handwritten_pages.py`**

Créer `/workspaces/Logoestudios/patch_handwritten_pages.py` :

```python
#!/usr/bin/env python3
"""Patch hand-written HTML pages to inject booking modal, Espace membre links,
and updated SEO titles.

Idempotent: detects MARKER and skips re-injection of the modal HTML.

Targeted pages:
  - site/index.html
  - site/contact.html  (Espace membre + meta only — no popup, no CTA changes)
  - site/a-propos.html (Espace membre only)
  - site/mentions-legales.html (Espace membre only)
  - site/orthophonie/index.html
  - site/psychologie/index.html
  - site/soutien-scolaire/index.html
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shared_components import get_booking_modal, get_booking_js
from seo_titles import title_for_handwritten, meta_desc_for_handwritten


MARKER = "<!-- LOGOPSI_BOOKING_MODAL -->"
CONNEXION_MARKER = "<!-- LOGOPSI_CONNEXION_LINK -->"
ESPACE_MARKER = "<!-- LOGOPSI_ESPACE_MEMBRE -->"
HERO_MARKER = "<!-- LOGOPSI_HERO_BILAN -->"


PAGES_FULL_PATCH = [
    "site/index.html",
    "site/orthophonie/index.html",
    "site/psychologie/index.html",
    "site/soutien-scolaire/index.html",
]

PAGES_LINKS_ONLY = [
    "site/contact.html",
    "site/a-propos.html",
    "site/mentions-legales.html",
]


def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def update_title_and_meta(html, rel_path):
    """Update <title> and <meta name=description> using seo_titles mappings."""
    new_title = title_for_handwritten(rel_path)
    new_desc = meta_desc_for_handwritten(rel_path)
    if new_title:
        html = re.sub(
            r"<title>[^<]*</title>",
            "<title>" + new_title + "</title>",
            html,
            count=1,
        )
    if new_desc:
        html = re.sub(
            r'<meta\s+name="description"\s+content="[^"]*"\s*/?>',
            '<meta name="description" content="' + new_desc + '">',
            html,
            count=1,
        )
    return html


def inject_booking_modal(html):
    """Inject booking modal HTML and JS just before </body>. Idempotent."""
    if MARKER in html:
        return html
    injection = (
        get_booking_modal()
        + "\n    <script>"
        + get_booking_js()
        + "    </script>\n"
    )
    return html.replace("</body>", injection + "</body>", 1)


def patch_file(filepath, rel_path):
    """Apply all patches to a single file according to its rel_path."""
    html = _read(filepath)
    html = update_title_and_meta(html, rel_path)
    if rel_path not in PAGES_LINKS_ONLY:
        html = inject_booking_modal(html)
    # Other patches added in subsequent tasks (Connexion, Espace membre, CTAs, hero).
    _write(filepath, html)


def main():
    repo_root = os.path.dirname(os.path.abspath(__file__))
    for rel in PAGES_FULL_PATCH + PAGES_LINKS_ONLY:
        path = os.path.join(repo_root, rel)
        if os.path.exists(path):
            patch_file(path, rel)
            print("patched: " + rel)
        else:
            print("skipped (not found): " + rel)


if __name__ == "__main__":
    main()
```

- [ ] **Step 11.5 : Lancer le test (passe)**

Run: `python3 tests/test_patch_handwritten_pages.py`
Expected: `test_patch_handwritten_pages: OK`

- [ ] **Step 11.6 : Commit**

```bash
git add patch_handwritten_pages.py tests/test_patch_handwritten_pages.py tests/fixtures/sample_handwritten.html
git commit -m "feat(patch): scaffold patch_handwritten_pages.py with idempotent marker"
```

---

### Task 12 : Patch — injection Connexion (navbar) + Espace membre (footer)

**Files:**
- Modify: `patch_handwritten_pages.py` (ajout 2 fonctions)
- Modify: `tests/test_patch_handwritten_pages.py`

- [ ] **Step 12.1 : Ajouter les tests**

Ajouter à `tests/test_patch_handwritten_pages.py` (avant `if __name__`) :

```python
def test_patch_inserts_connexion_link():
    tmpdir, dest = _setup_tempfile()
    try:
        patch_file(dest, rel_path="site/test-page.html")
        content = _read(dest)
        assert "Connexion" in content
        assert "app.logopsiestudios.com/fr/login" in content
    finally:
        shutil.rmtree(tmpdir)


def test_patch_inserts_espace_membre_in_footer():
    tmpdir, dest = _setup_tempfile()
    try:
        patch_file(dest, rel_path="site/test-page.html")
        content = _read(dest)
        # Espace membre should appear after the À propos link in the footer
        idx_a_propos = content.find("À propos")
        idx_espace = content.find("Espace membre")
        assert idx_espace > idx_a_propos > 0
    finally:
        shutil.rmtree(tmpdir)
```

Et l'appel au bloc `if __name__`:
```python
    test_patch_inserts_connexion_link()
    test_patch_inserts_espace_membre_in_footer()
```

- [ ] **Step 12.2 : Lancer le test (échoue)**

Run: `python3 tests/test_patch_handwritten_pages.py`
Expected: `AssertionError` sur "Connexion".

- [ ] **Step 12.3 : Implémenter `inject_connexion_link()` et `inject_espace_membre_link()`**

Dans `patch_handwritten_pages.py`, juste avant `def patch_file(...)`, ajouter :

```python
CONNEXION_HTML = (
    '\n                    ' + CONNEXION_MARKER + '\n'
    '                    <a href="https://app.logopsiestudios.com/fr/login" target="_blank" rel="noopener noreferrer" class="text-[15px] font-semibold text-gray-700 hover:text-primary transition-colors">Connexion</a>\n'
)


def inject_connexion_link(html):
    """Insert a Connexion link before the green CTA in the navbar. Idempotent."""
    if CONNEXION_MARKER in html:
        return html
    # Find the first <a ...> with class containing both "bg-primary" and "Prendre rendez-vous" content.
    pattern = re.compile(
        r'(<a\s[^>]*class="[^"]*bg-primary[^"]*"[^>]*>\s*Prendre rendez-vous)',
        re.MULTILINE,
    )
    return pattern.sub(CONNEXION_HTML + r'                    \1', html, count=1)


ESPACE_HTML = (
    '\n            ' + ESPACE_MARKER + '\n'
    '            <a href="https://app.logopsiestudios.com/fr/login" target="_blank" rel="noopener noreferrer" class="text-gray-500 hover:text-primary text-sm transition-colors">Espace membre</a>\n'
)


def inject_espace_membre_link(html):
    """Insert an Espace membre link after the À propos link in the footer. Idempotent."""
    if ESPACE_MARKER in html:
        return html
    # Insert after the first occurrence of an <a> linking to a-propos.html
    pattern = re.compile(
        r'(<a\s+href="[^"]*a-propos\.html"[^>]*>[^<]*</a>)',
        re.MULTILINE,
    )
    return pattern.sub(r'\1' + ESPACE_HTML, html, count=1)
```

Modifier `patch_file` pour les appeler :

```python
def patch_file(filepath, rel_path):
    html = _read(filepath)
    html = update_title_and_meta(html, rel_path)
    html = inject_connexion_link(html)
    html = inject_espace_membre_link(html)
    if rel_path not in PAGES_LINKS_ONLY:
        html = inject_booking_modal(html)
    _write(filepath, html)
```

- [ ] **Step 12.4 : Lancer le test (passe)**

Run: `python3 tests/test_patch_handwritten_pages.py`
Expected: `test_patch_handwritten_pages: OK`

- [ ] **Step 12.5 : Commit**

```bash
git add patch_handwritten_pages.py tests/test_patch_handwritten_pages.py
git commit -m "feat(patch): inject Connexion + Espace membre links idempotently"
```

---

### Task 13 : Patch — remplacement des CTAs `contact.html` → `openBookingModal()`

**Files:**
- Modify: `patch_handwritten_pages.py`
- Modify: `tests/test_patch_handwritten_pages.py`

- [ ] **Step 13.1 : Ajouter les tests**

Ajouter à `tests/test_patch_handwritten_pages.py` :

```python
def test_patch_replaces_cta_with_popup_hook():
    tmpdir, dest = _setup_tempfile()
    try:
        patch_file(dest, rel_path="site/test-page.html")
        content = _read(dest)
        assert "openBookingModal()" in content
    finally:
        shutil.rmtree(tmpdir)


def test_patch_skips_cta_replacement_on_contact_page():
    """contact.html should NOT have CTAs rewritten."""
    tmpdir, dest = _setup_tempfile()
    try:
        # Use rel_path that's in PAGES_LINKS_ONLY
        patch_file(dest, rel_path="site/contact.html")
        content = _read(dest)
        # Espace membre still added
        assert "Espace membre" in content
        # But popup CTA NOT injected
        assert "LOGOPSI_BOOKING_MODAL" not in content
        # The original contact.html link in nav stays
    finally:
        shutil.rmtree(tmpdir)
```

Et appels :
```python
    test_patch_replaces_cta_with_popup_hook()
    test_patch_skips_cta_replacement_on_contact_page()
```

- [ ] **Step 13.2 : Lancer le test (échoue)**

Run: `python3 tests/test_patch_handwritten_pages.py`
Expected: `AssertionError` sur "openBookingModal()".

- [ ] **Step 13.3 : Implémenter `replace_cta_with_popup_hook()`**

Dans `patch_handwritten_pages.py`, ajouter avant `patch_file` :

```python
CTA_LABELS = ["Prendre rendez-vous", "Prendre RDV", "Réserver mon bilan", "Réserver", "Prendre rendez vous"]


def replace_cta_with_popup_hook(html):
    """Convert <a href="...contact.html"> ... CTA label ... </a> into popup-opening anchors.

    Only replaces anchors where:
      - href ends with contact.html or is #contact
      - inner text contains one of CTA_LABELS
    """
    def _repl(m):
        full = m.group(0)
        href = m.group(1)
        # Skip mailto, external, etc.
        if not (href.endswith("contact.html") or href == "#contact"):
            return full
        # Replace href with #, add onclick
        modified = re.sub(
            r'href="[^"]*"',
            'href="#" onclick="openBookingModal(); return false;"',
            full,
            count=1,
        )
        return modified

    pattern = re.compile(
        r'<a\s+[^>]*href="([^"]+)"[^>]*>([^<]*(?:' + "|".join(re.escape(lbl) for lbl in CTA_LABELS) + r')[^<]*)</a>',
        re.IGNORECASE | re.DOTALL,
    )
    return pattern.sub(_repl, html)
```

Modifier `patch_file` :

```python
def patch_file(filepath, rel_path):
    html = _read(filepath)
    html = update_title_and_meta(html, rel_path)
    html = inject_connexion_link(html)
    html = inject_espace_membre_link(html)
    if rel_path not in PAGES_LINKS_ONLY:
        html = replace_cta_with_popup_hook(html)
        html = inject_booking_modal(html)
    _write(filepath, html)
```

- [ ] **Step 13.4 : Lancer le test (passe)**

Run: `python3 tests/test_patch_handwritten_pages.py`
Expected: `test_patch_handwritten_pages: OK`

- [ ] **Step 13.5 : Commit**

```bash
git add patch_handwritten_pages.py tests/test_patch_handwritten_pages.py
git commit -m "feat(patch): replace contact.html CTAs with openBookingModal() hook"
```

---

### Task 14 : Patch — injection sous-titre hero "Bilan 150€/48h" sur les hubs

**Files:**
- Modify: `patch_handwritten_pages.py`
- Modify: `tests/test_patch_handwritten_pages.py`

- [ ] **Step 14.1 : Ajouter une fixture pour page hub**

Créer `tests/fixtures/sample_hub.html` :

```html
<!DOCTYPE html>
<html lang="fr">
<head><title>Hub - Logo Études</title></head>
<body>
    <section class="hero">
        <h1 class="text-5xl">Orthophonie en ligne</h1>
        <p>Welcome.</p>
    </section>
</body>
</html>
```

- [ ] **Step 14.2 : Ajouter le test**

Ajouter à `tests/test_patch_handwritten_pages.py` :

```python
HUB_FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "sample_hub.html")


def _setup_hub_tempfile():
    tmpdir = tempfile.mkdtemp()
    dest = os.path.join(tmpdir, "site", "orthophonie", "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy(HUB_FIXTURE, dest)
    return tmpdir, dest


def test_patch_inserts_hero_subtitle_on_hub():
    tmpdir, dest = _setup_hub_tempfile()
    try:
        patch_file(dest, rel_path="site/orthophonie/index.html")
        content = _read(dest)
        assert "Bilan complet à 150" in content or "150€" in content and "48h" in content
        assert "LOGOPSI_HERO_BILAN" in content
    finally:
        shutil.rmtree(tmpdir)


def test_hero_subtitle_idempotent():
    tmpdir, dest = _setup_hub_tempfile()
    try:
        patch_file(dest, rel_path="site/orthophonie/index.html")
        first = _read(dest)
        patch_file(dest, rel_path="site/orthophonie/index.html")
        second = _read(dest)
        assert first == second
        assert second.count("LOGOPSI_HERO_BILAN") == 1
    finally:
        shutil.rmtree(tmpdir)
```

Appels :
```python
    test_patch_inserts_hero_subtitle_on_hub()
    test_hero_subtitle_idempotent()
```

- [ ] **Step 14.3 : Lancer le test (échoue)**

Run: `python3 tests/test_patch_handwritten_pages.py`
Expected: `AssertionError`.

- [ ] **Step 14.4 : Implémenter `inject_hero_subtitle()`**

Dans `patch_handwritten_pages.py`, ajouter :

```python
HERO_HTML = (
    '\n        ' + HERO_MARKER + '\n'
    '        <p class="mt-4 inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold">\n'
    '            <span class="w-2 h-2 rounded-full bg-primary"></span> Bilan complet à 150€, sous 48h, 100% en ligne\n'
    '        </p>\n'
)


def inject_hero_subtitle(html):
    """Insert the bilan subtitle right after the first <h1> in the document. Idempotent."""
    if HERO_MARKER in html:
        return html
    pattern = re.compile(r'(<h1[^>]*>[^<]*</h1>)', re.MULTILINE | re.DOTALL)
    return pattern.sub(r'\1' + HERO_HTML, html, count=1)
```

Modifier `patch_file` pour appeler `inject_hero_subtitle` **uniquement** sur les pages hub (PAGES_FULL_PATCH minus `site/index.html`) :

```python
HUB_PAGES = [
    "site/orthophonie/index.html",
    "site/psychologie/index.html",
    "site/soutien-scolaire/index.html",
    "site/index.html",  # also gets the subtitle
]


def patch_file(filepath, rel_path):
    html = _read(filepath)
    html = update_title_and_meta(html, rel_path)
    html = inject_connexion_link(html)
    html = inject_espace_membre_link(html)
    if rel_path in HUB_PAGES:
        html = inject_hero_subtitle(html)
    if rel_path not in PAGES_LINKS_ONLY:
        html = replace_cta_with_popup_hook(html)
        html = inject_booking_modal(html)
    _write(filepath, html)
```

- [ ] **Step 14.5 : Lancer le test (passe)**

Run: `python3 tests/test_patch_handwritten_pages.py`
Expected: `test_patch_handwritten_pages: OK`

- [ ] **Step 14.6 : Commit**

```bash
git add patch_handwritten_pages.py tests/test_patch_handwritten_pages.py tests/fixtures/sample_hub.html
git commit -m "feat(patch): inject 150€/48h hero subtitle on hub pages"
```

---

### Task 15 : Lancer le patch sur les pages hand-written réelles

**Files:**
- Modify: `site/index.html`, `site/contact.html`, `site/a-propos.html`, `site/mentions-legales.html`, `site/orthophonie/index.html`, `site/psychologie/index.html`, `site/soutien-scolaire/index.html`

- [ ] **Step 15.1 : Faire un backup git du dossier `site/`**

```bash
cd /workspaces/Logoestudios && git status site/ | head -10
```
Expected : pas d'unstaged changes (déjà commit après régénération à la Task 10).

- [ ] **Step 15.2 : Lancer le script**

Run :
```bash
cd /workspaces/Logoestudios && python3 patch_handwritten_pages.py
```
Expected output :
```
patched: site/index.html
patched: site/orthophonie/index.html
patched: site/psychologie/index.html
patched: site/soutien-scolaire/index.html
patched: site/contact.html
patched: site/a-propos.html
patched: site/mentions-legales.html
```

- [ ] **Step 15.3 : Vérifier les nouveaux titres**

Run :
```bash
grep -H "<title>" /workspaces/Logoestudios/site/index.html /workspaces/Logoestudios/site/orthophonie/index.html /workspaces/Logoestudios/site/psychologie/index.html /workspaces/Logoestudios/site/soutien-scolaire/index.html
```
Expected: les 4 lignes contiennent "Bilan ... 150€" et "| Logo Études".

- [ ] **Step 15.4 : Vérifier que `contact.html` n'a PAS de modal mais a Espace membre**

Run :
```bash
grep -c "LOGOPSI_BOOKING_MODAL" /workspaces/Logoestudios/site/contact.html
grep -c "Espace membre" /workspaces/Logoestudios/site/contact.html
```
Expected:
```
0
1
```

- [ ] **Step 15.5 : Idempotence — re-lancer le script et vérifier qu'aucun fichier ne change**

Run :
```bash
cd /workspaces/Logoestudios && git status -s site/ | head; python3 patch_handwritten_pages.py; git status -s site/ | head
```
Expected: même output `git status` avant et après le 2ème run.

- [ ] **Step 15.6 : Commit**

```bash
git add site/
git commit -m "build: apply booking modal patch to hand-written pages"
```

---

## Phase 5 — Vérification finale

### Task 16 : Smoke test navigateur — popup, formulaire, espace membre

**Files:** none (verification only).

- [ ] **Step 16.1 : Lancer un serveur local**

Run :
```bash
cd /workspaces/Logoestudios && python3 -m http.server -d site 8765
```
Le port 8765 est arbitraire. Laisser tourner dans un terminal.

- [ ] **Step 16.2 : Vérifier les 13 points de contrôle du spec §6**

Ouvrir `http://localhost:8765/index.html` dans un navigateur (ou via le forwardé du codespace) et vérifier :

1. **Click sur "Prendre rendez-vous"** (navbar) → popup s'ouvre, vue info.
2. **Click sur "Réserver mon bilan en ligne"** dans la popup → nouvel onglet vers `app.logopsiestudios.com/fr/login`.
3. **Click sur "Être rappelé(e)"** → bascule en formulaire (vue callback).
4. **Click sur "← Retour"** → revient en vue info.
5. **Click sur backdrop** → popup se ferme.
6. **Touche Échap** → popup se ferme.
7. Naviguer vers `/orthophonie/dyslexie.html` et vérifier le `<title>` (DevTools → Elements → `<head>`).
8. Naviguer vers `/orthophonie/villes/dyslexie-paris.html` → vérifier `<title>`.
9. Naviguer vers `/contact.html` → pas de popup au clic CTA, lien Espace membre visible dans navbar et footer.
10. Vérifier le navbar mobile (DevTools responsive 375px) : "Connexion" présent + popup OK.
11. Vérifier `?rappel=ok` dans l'URL : ouvre `http://localhost:8765/index.html?rappel=ok` → popup s'ouvre directement en mode succès.
12. Vérifier que la popup a `role="dialog"` et `aria-modal="true"` (DevTools → Elements).
13. Tab keyboard navigation à l'intérieur de la popup (focus visible).

**À chaque point** : noter dans une check-list rapide. En cas d'échec, créer une mini-tâche correctrice.

- [ ] **Step 16.3 : Soumettre le formulaire de test (sandbox Formsubmit)**

- Ouvrir la popup → Être rappelé.
- Remplir avec des fausses valeurs.
- Soumettre. Le navigateur sera redirigé vers Formsubmit (page de confirmation).
- **Note importante** : la première soumission **réelle** depuis le domaine `logopsistudios.com` déclenchera l'email de validation Formsubmit à valider par l'admin. Documenter ce point dans le README ou un fichier OPS.

- [ ] **Step 16.4 : Tuer le serveur local**

```bash
# Si lancé avec `python3 -m http.server -d site 8765`, juste Ctrl+C dans son terminal.
```

- [ ] **Step 16.5 : Si tout passe, pas de commit nécessaire (vérification only)**

---

### Task 17 : Documentation OPS — activation Formsubmit

**Files:**
- Create: `OPS.md` (ou ajout au `README.md` existant)

- [ ] **Step 17.1 : Documenter l'étape d'activation Formsubmit**

Créer `/workspaces/Logoestudios/OPS.md` :

```markdown
# Logo Études — Notes opérationnelles

## Activation Formsubmit (formulaire "Être rappelé")

Le formulaire de la popup "Être rappelé" poste vers
`https://formsubmit.co/contact@logopsistudios.com`.

**Lors de la première soumission depuis la prod**, Formsubmit envoie un
email de validation à `contact@logopsistudios.com`. L'admin doit cliquer
sur le lien de confirmation dans cet email pour activer le service.

Tant que l'activation n'a pas eu lieu, les soumissions n'arrivent pas
dans la boîte mail.

Documentation Formsubmit : https://formsubmit.co/

## Lancer un serveur local pour tester

    python3 -m http.server -d site 8765

Puis ouvrir http://localhost:8765/index.html.

## Régénérer toutes les pages

    python3 generate_level2_pages.py
    python3 generate_level3_4_pages.py
    python3 generate_physique_chimie.py
    python3 patch_handwritten_pages.py

L'ordre est important : d'abord les générateurs, puis le patch sur les
pages hand-written. Le patch est idempotent.
```

- [ ] **Step 17.2 : Commit**

```bash
git add OPS.md
git commit -m "docs: ops note for Formsubmit activation + regen workflow"
```

---

## Critères d'acceptation finaux (récap du spec §9)

- [ ] Popup s'ouvre depuis tous les CTAs listés.
- [ ] Popup ne s'ouvre PAS sur `contact.html` ni `mentions-legales.html`.
- [ ] Lien "Connexion" dans navbar (desktop + mobile) sur toutes les pages.
- [ ] Lien "Espace membre" dans footer sur toutes les pages.
- [ ] Section CTA verte affiche "150€ · sous 48h" + bullets mis à jour.
- [ ] Tous les meta titres listés au spec §3.6 sont mis à jour.
- [ ] Meta descriptions des pages de service mentionnent "150€" et/ou "sous 48h".
- [ ] Formulaire "Être rappelé" poste vers Formsubmit.
- [ ] Popup accessible (Échap, focus, role dialog).
- [ ] `patch_handwritten_pages.py` est idempotent.
- [ ] OPS.md documente l'activation Formsubmit.

---

## Self-review

**Spec coverage :**
- §3.1 popup 3 états → Tasks 1, 2 ✅
- §3.2 cibles d'ouverture → Tasks 3, 13 ✅
- §3.3 espace membre → Tasks 3, 4, 12 ✅
- §3.4 CTA section → Task 5 ✅
- §3.5 hero hubs → Task 14 ✅
- §3.6 meta titres → Tasks 6, 7, 8, 9, 11 ✅
- §3.7 meta descriptions → Tasks 6, 7, 8, 9, 11 ✅
- §4.1 modifs shared_components → Tasks 1-5 ✅
- §4.2 patch script → Tasks 11-15 ✅
- §4.3 régénération → Task 10 ✅
- §4.4 backend Formsubmit → Tasks 1, 17 ✅
- §6 verification → Task 16 ✅
- §7 risques → couverts (idempotence Tasks 11/14, activation OPS Task 17, z-index Task 1)

**Type/method consistency :**
- `MARKER` constant used consistently across `patch_handwritten_pages.py` and tests.
- `openBookingModal` / `closeBookingModal` / `showCallbackForm` / `showInfoView` — same names in modal HTML (Task 1), JS (Task 2), navbar onclick (Task 3), CTA section (Task 5), patch script (Task 13).
- `title_for_*` / `meta_desc_for_*` naming consistent across `seo_titles.py` (Task 6) and consumers (Tasks 7, 8, 9, 11).

**Placeholder scan :** clean.
