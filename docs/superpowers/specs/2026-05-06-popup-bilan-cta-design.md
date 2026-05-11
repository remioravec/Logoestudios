# Popup de réservation, mise en avant du bilan 150€/48h, accès espace membre

**Date** : 2026-05-06
**Auteur** : Rémi Oravec + Claude
**Statut** : Approuvé — prêt pour planification

---

## 1. Objectif

Augmenter la conversion du site `Logo Études` en :

1. **Remplaçant** la redirection actuelle des CTAs (`href="contact.html"` ou `#contact`) par une **popup de réservation** unifiée qui met explicitement en avant l'offre **Bilan 150€ / 48h / 100% en ligne**.
2. **Reformulant** le wording des sections CTA et des hero des pages-hubs pour mettre cette offre en avant partout.
3. **Ajoutant un accès Espace membre** (`https://app.logopsiestudios.com/fr/login`) dans le navbar, le footer, et la popup, pour que les clients existants ne soient pas freinés par le tunnel de prise de RDV.
4. **Ajustant les meta titres** des pages de service pour intégrer "Bilan" et "150€" et booster la pertinence SEO sur la requête "bilan orthophonique en ligne" et variantes.

---

## 2. Contexte projet

- Site statique HTML + Tailwind CDN, français, hébergé en deux modes (statique + plugin WordPress).
- Architecture mixte :
  - **Pages générées** via `shared_components.py` : niveau 3 (troubles : `orthophonie/dyslexie.html`, `psychologie/tdah.html`...) et niveau 4 (villes : `orthophonie/villes/dyslexie-paris.html`...).
  - **Pages écrites à la main** : `site/index.html`, `site/contact.html`, `site/a-propos.html`, `site/mentions-legales.html`, et probablement les hubs N2 (`site/orthophonie/index.html`, etc.).
- CTAs existants pointent vers `contact.html` (formulaire non branché : `action="#"`) ou `#contact`.
- Section CTA verte (`get_cta_section`) affiche actuellement *"Le bilan complet est un acte professionnel payant (tarifs sur demande)"* — wording à remplacer.
- Email de contact connu : `contact@logopsistudios.com` (vu dans `site/contact.html`).

---

## 3. Spécifications fonctionnelles

### 3.1. Popup de réservation

Une popup centrée, fond opaque (backdrop), accessible (rôle `dialog`, `aria-modal`, fermeture via croix / clic sur backdrop / touche Échap).

**État 1 — Vue d'accueil (par défaut à l'ouverture)** :

```
[X]  Bilan complet en ligne

     150€  ·  Sous 48h  ·  100% en ligne

     ✓ Orthophoniste / psychologue diplômé(e) d'État
     ✓ Compte-rendu détaillé fourni
     ✓ Éligible Sécurité sociale & mutuelles

     ┌─────────────────────────────────────────┐
     │   Réserver mon bilan en ligne →         │  (CTA primary)
     └─────────────────────────────────────────┘
     ┌─────────────────────────────────────────┐
     │   Être rappelé(e) gratuitement          │  (CTA outline)
     └─────────────────────────────────────────┘

     Déjà client·e ? Se connecter →                (lien discret)
```

- **"Réserver mon bilan en ligne"** → ouvre `https://app.logopsiestudios.com/fr/login` dans un nouvel onglet (`target="_blank"`, `rel="noopener noreferrer"`).
- **"Être rappelé(e) gratuitement"** → fait basculer la popup en État 2.
- **"Se connecter"** → ouvre `https://app.logopsiestudios.com/fr/login` dans un nouvel onglet.

**État 2 — Formulaire "Être rappelé"** :

Champs :
- Nom & prénom (obligatoire)
- Téléphone (obligatoire, type `tel`)
- Email (obligatoire, type `email`)
- Créneau préférentiel (select : "Matin (9h-12h)", "Après-midi (12h-17h)", "Soir (17h-19h)", "Indifférent")
- Bouton "← Retour" + Bouton "Envoyer"

**Soumission** : POST vers `https://formsubmit.co/contact@logopsistudios.com`.
- Champs cachés : `_subject = "Demande de rappel — Logo Études"`, `_template = "table"`, `_captcha = "false"`, `_next = <URL de la page courante>?rappel=ok` pour redirection après envoi.
- À la première soumission, Formsubmit envoie un email de confirmation à `contact@logopsistudios.com` que l'admin doit valider une fois.

**État 3 — Confirmation** (côté client) :

Si l'URL contient `?rappel=ok` au chargement, afficher la popup directement en mode succès :
- Coche verte
- "Demande envoyée — vous serez rappelé(e) sous 48h ouvrées."
- Bouton "Fermer".

### 3.2. Cibles d'ouverture de la popup

La popup s'ouvre via `onclick="openBookingModal(); return false;"` sur :

- Le bouton **"Prendre rendez-vous"** du navbar desktop (sur toutes les pages).
- Le bouton **"Prendre rendez-vous"** du menu mobile.
- Le bouton **"Réserver mon bilan"** de la section CTA verte (sur toutes les pages où elle apparaît).
- Les CTAs du **hero** des pages-hubs (`site/index.html`, `orthophonie/index.html`, `psychologie/index.html`, `soutien-scolaire/index.html`).
- Tout `<a>` ou `<button>` portant la classe `js-open-booking` (mécanisme générique pour les pages futures).

**Exclusions** :
- Les CTAs de la **page `contact.html`** restent inchangés (c'est déjà la page de contact).
- Les CTAs de la **page `mentions-legales.html`** restent inchangés.
- Les liens `href="mailto:..."` restent inchangés.

### 3.3. Espace membre

**Navbar desktop** : ajout d'un lien "Connexion" (texte simple, gris foncé, `hover:text-primary`) à gauche du bouton vert "Prendre rendez-vous", `target="_blank"` vers `https://app.logopsiestudios.com/fr/login`.

**Menu mobile** : ajout d'un lien "Connexion" au-dessus du bouton vert.

**Footer** : ajout d'un lien "Espace membre" dans la rangée légale (à côté de Mentions légales / Contact / À propos), `target="_blank"`.

**Popup** : lien "Déjà client·e ? Se connecter →" en bas, discret (gris, taille `text-sm`), `target="_blank"`.

### 3.4. Reformulation de la section CTA verte

`get_cta_section()` modifié pour afficher :

```
Bilan complet — 150€
Sous 48h, 100% en ligne, par un professionnel diplômé d'État.

[ Réserver mon bilan ]   ← onclick="openBookingModal()"

✓ Compte-rendu détaillé   ✓ Éligible Sécu & mutuelles   ✓ Sous 48h
```

L'ancien texte *"Le bilan complet est un acte professionnel payant (tarifs sur demande)"* est supprimé.

### 3.5. Hero des pages-hubs

Sur `site/index.html`, `site/orthophonie/index.html`, `site/psychologie/index.html`, `site/soutien-scolaire/index.html` :

- Ajout d'un sous-titre / badge sous le H1 du hero : **"Bilan complet à 150€, sous 48h, 100% en ligne"**.
- Le bouton CTA principal du hero ouvre la popup.

### 3.6. Meta titres

Pattern : **"Bilan [sujet] en ligne — [Pro] 150€ / 48h | Logo Études"** (cible ≤ 65 caractères, dépassement toléré jusqu'à 75 pour les pages villes).

| Page | Nouveau titre |
|---|---|
| `site/index.html` | Bilan orthophonie, psychologie & soutien — 150€, 48h \| Logo Études |
| `site/orthophonie/index.html` | Bilan orthophonique en ligne — 150€, sous 48h \| Logo Études |
| `site/orthophonie/dyslexie.html` | Bilan dyslexie en ligne — Orthophoniste 150€ \| Logo Études |
| `site/orthophonie/dysorthographie.html` | Bilan dysorthographie en ligne — Orthophoniste 150€ \| Logo Études |
| `site/orthophonie/dyscalculie.html` | Bilan dyscalculie en ligne — Orthophoniste 150€ \| Logo Études |
| `site/orthophonie/dysphasie.html` | Bilan dysphasie en ligne — Orthophoniste 150€ \| Logo Études |
| `site/orthophonie/begaiement.html` | Bilan bégaiement en ligne — Orthophoniste 150€ \| Logo Études |
| `site/orthophonie/tsa.html` | Bilan TSA en ligne — Orthophoniste 150€ \| Logo Études |
| `site/orthophonie/oralite.html` | Bilan troubles de l'oralité — Orthophoniste 150€ \| Logo Études |
| `site/orthophonie/surdite.html` | Bilan surdité en ligne — Orthophoniste 150€ \| Logo Études |
| `site/orthophonie/paralysie-cerebrale.html` | Bilan paralysie cérébrale — Orthophoniste 150€ \| Logo Études |
| `site/orthophonie/fente-palatine.html` | Bilan fente palatine — Orthophoniste 150€ \| Logo Études |
| `site/orthophonie/trisomie-21.html` | Bilan trisomie 21 — Orthophoniste 150€ \| Logo Études |
| `site/orthophonie/villes/<trouble>-<ville>.html` | Bilan [trouble] à [Ville] — Orthophoniste en ligne 150€ \| Logo Études |
| `site/psychologie/index.html` | Bilan psychologique en ligne — 150€, sous 48h \| Logo Études |
| `site/psychologie/<trouble>.html` | Bilan [trouble] en ligne — Psychologue 150€ \| Logo Études |
| `site/psychologie/villes/<trouble>-<ville>.html` | Bilan [trouble] à [Ville] — Psychologue en ligne 150€ \| Logo Études |
| `site/soutien-scolaire/index.html` | Bilan pédagogique en ligne — 150€, sous 48h \| Logo Études |
| `site/soutien-scolaire/<matière>/<niveau>.html` (ex: `mathematiques/3eme.html`) | Bilan [matière] [niveau] en ligne — 150€ \| Logo Études |
| `site/soutien-scolaire/<matière>/<niveau>-<ville>.html` (ex: `mathematiques/3eme-paris.html`) | Bilan [matière] [niveau] à [Ville] — 150€ \| Logo Études |
| `site/soutien-scolaire/villes/<ville>.html` (ex: `villes/paris.html`) | Soutien scolaire à [Ville] — Bilan 150€ \| Logo Études |
| `site/contact.html`, `site/a-propos.html`, `site/mentions-legales.html` | **inchangés** |

### 3.7. Meta descriptions

Toutes les meta descriptions des pages de service sont ajustées pour intégrer **"150€"** et **"sous 48h"** quand elles ne le mentionnent pas déjà. Exemple :

- Avant : *"Séances d'orthophonie en ligne pour la dyslexie. Orthophonistes diplômés."*
- Après : *"Bilan orthophonique pour la dyslexie en ligne — 150€, rendez-vous sous 48h. Orthophonistes diplômés d'État, partout en France."*

Les meta descriptions des pages utilitaires (`contact`, `a-propos`, `mentions-legales`) sont inchangées.

---

## 4. Architecture technique

### 4.1. Modifications `shared_components.py`

| Fonction | Action |
|---|---|
| `get_head(title, meta_desc, ...)` | **Aucun changement structurel.** Les nouveaux titres sont passés via les appels existants. |
| `get_navbar(prefix)` | Ajout du lien "Connexion" desktop + mobile. Bouton "Prendre rendez-vous" passe de `href="contact.html"` à `href="#"` + `onclick="openBookingModal(); return false;"`. |
| `get_footer(prefix)` | Ajout du lien "Espace membre" dans la rangée légale. |
| `get_cta_section(title, desc)` | Réécriture complète : nouveau titre "Bilan complet — 150€", nouveaux bullets, bouton qui ouvre la popup. |
| `get_booking_modal()` | **NOUVEAU.** Retourne le HTML de la popup (États 1, 2, 3 dans le DOM, `display:none` par défaut sauf si `?rappel=ok`). |
| `get_booking_js()` | **NOUVEAU.** Retourne le bloc JS : `openBookingModal`, `closeBookingModal`, `showCallbackForm`, `showInfoView`, gestion Échap, focus trap, détection `?rappel=ok`. |
| `get_js(include_faq=False)` | Inclut désormais `get_booking_js()` dans la sortie. |

### 4.2. Nouveau script de patch : `inject_booking_modal.py`

Script Python dont le rôle est de mettre à jour les pages **non-générées** (édition manuelle) pour intégrer la popup, le lien Espace membre, et les nouveaux meta titres.

**Pages cibles** :
- `site/index.html`
- `site/contact.html` (Espace membre + meta description seulement, pas de popup ni de wording bilan)
- `site/a-propos.html` (Espace membre seulement)
- `site/mentions-legales.html` (Espace membre seulement)
- `site/orthophonie/index.html`
- `site/psychologie/index.html`
- `site/soutien-scolaire/index.html`

**Opérations par page** (via parsing HTML simple ou regex contrôlées) :

1. **Meta** : remplacer `<title>...</title>` et `<meta name="description" content="...">` selon le mapping de la section 3.6 / 3.7.
2. **Navbar** : injecter le lien "Connexion" à gauche du bouton vert + dans le menu mobile.
3. **Footer** : injecter le lien "Espace membre" dans la rangée légale.
4. **CTAs principaux** : remplacer `href="contact.html"` (et `href="#contact"`) par `href="#"` + `onclick="openBookingModal(); return false;"` sur les boutons "Prendre rendez-vous" / "Réserver mon bilan", **sauf** sur `contact.html` et `mentions-legales.html`.
5. **Hero** (pour `index.html` et hubs N2) : injecter le sous-titre/badge "Bilan complet à 150€, sous 48h, 100% en ligne" sous le H1.
6. **Popup HTML** : injecter `get_booking_modal()` juste avant `</body>`.
7. **Popup JS** : injecter `get_booking_js()` dans le `<script>` existant ou en ajouter un avant `</body>`.

Le script est **idempotent** : il détecte si la popup est déjà présente (marqueur HTML `<!-- LOGOPSI_BOOKING_MODAL -->`) et n'injecte pas en double.

### 4.3. Régénération des pages générées

Les pages N3/N4 sont régénérées via les scripts existants (`generate_level2_pages.py`, `generate_level3_4_pages.py`, `generate_physique_chimie.py`) après modification de `shared_components.py` et des mappings de titres.

**Mapping des titres N3/N4** : un fichier `seo_titles.py` (ou dictionnaire dans le générateur existant) qui mappe slug → titre/description. Lu par les scripts de génération.

### 4.4. Backend Formsubmit

- Endpoint : `https://formsubmit.co/contact@logopsistudios.com`
- Aucune dépendance backend nouvelle.
- **Action manuelle requise** : la première soumission depuis la prod déclenche un email de validation Formsubmit que `contact@logopsistudios.com` doit cliquer pour activer le service. À documenter dans le README.

---

## 5. Données / interfaces

### 5.1. Signature des nouvelles fonctions

```python
def get_booking_modal() -> str:
    """Retourne le HTML de la popup de réservation (3 états dans le DOM)."""

def get_booking_js() -> str:
    """Retourne le bloc <script> de gestion de la popup (sans balises <script>).
    À insérer dans le <script> existant des pages."""
```

### 5.2. API JS exposée globalement

- `window.openBookingModal()` — ouvre la popup en État 1.
- `window.closeBookingModal()` — ferme la popup.
- `window.showCallbackForm()` — bascule en État 2.
- `window.showInfoView()` — revient en État 1 depuis l'État 2.

Les pages futures peuvent utiliser ces fonctions ou la classe `js-open-booking` sur n'importe quel élément.

---

## 6. Tests / vérification

Pas de framework de test automatisé en place. Vérifications manuelles à exécuter avant de considérer le travail terminé :

1. **Ouvrir `site/index.html` dans un navigateur** (via un serveur local : `python -m http.server -d site`).
2. Cliquer sur "Prendre rendez-vous" du navbar → la popup s'ouvre en État 1.
3. Cliquer sur "Réserver mon bilan en ligne" → un nouvel onglet s'ouvre vers `app.logopsiestudios.com/fr/login`.
4. Cliquer sur "Être rappelé(e)" → bascule en formulaire (État 2).
5. Cliquer sur "← Retour" → revient en État 1.
6. Soumettre le formulaire → POST vers Formsubmit (vérifier dans le DevTools Network).
7. Cliquer sur le backdrop / appuyer sur Échap → la popup se ferme.
8. Vérifier `site/orthophonie/dyslexie.html` : titre = "Bilan dyslexie en ligne — Orthophoniste 150€ | Logo Études".
9. Vérifier `site/orthophonie/villes/dyslexie-paris.html` : titre = "Bilan dyslexie à Paris — Orthophoniste en ligne 150€ | Logo Études".
10. Vérifier `site/contact.html` : pas de popup, lien Espace membre présent dans navbar et footer.
11. Vérifier le navigateur **mobile** (devtools responsive) : menu mobile contient "Connexion" et la popup s'ouvre correctement.
12. Vérifier l'**accessibilité** : focus visible, navigation clavier dans la popup, fermeture Échap, lecteur d'écran annonce le rôle dialog.
13. Charger `site/index.html?rappel=ok` → la popup s'ouvre directement en État 3 (confirmation).

---

## 7. Risques et points d'attention

- **Idempotence du patch** : le script `inject_booking_modal.py` doit pouvoir être relancé sans dupliquer les éléments. Marqueur HTML `<!-- LOGOPSI_BOOKING_MODAL -->` à utiliser.
- **Activation Formsubmit** : la première soumission ne fonctionnera pas tant que l'admin n'a pas validé l'email de confirmation. Documenter dans le README.
- **Pages WordPress (`build_wp_plugin.py`)** : si le plugin WordPress republie le contenu, vérifier que les modifications sont bien embarquées par la pipeline de build du plugin. Sinon, étendre le script de build.
- **Longueur des titres villes** : dépassement potentiel jusqu'à 75 caractères. Acceptable mais à surveiller si Google tronque visuellement.
- **Z-index** : la popup doit avoir un z-index supérieur au navbar sticky (`z-50` actuel) → utiliser `z-[100]` pour le backdrop et `z-[110]` pour le contenu.
- **Conflit `contact.html`** : la page contact garde son formulaire actuel et ses CTAs internes ; ne pas casser ce flux.
- **Cache navigateur** : prévenir l'utilisateur que les visiteurs ayant la précédente version en cache verront les anciens titres jusqu'à invalidation.

---

## 8. Hors-scope (futures itérations)

- Brancher proprement le formulaire de la page `contact.html` (qui a actuellement `action="#"`).
- Tracking analytics des ouvertures de popup (GA4 / Plausible event).
- A/B test du wording de la popup.
- Internationalisation (le site est aujourd'hui mono-langue FR).
- Autodéplacement de la popup à scroll-depth (popup d'intent).

---

## 9. Critères d'acceptation

- [ ] La popup s'ouvre depuis tous les CTAs listés en 3.2 sur les pages listées en 4.2 + toutes les pages générées.
- [ ] La popup ne s'ouvre **pas** sur `contact.html` ni `mentions-legales.html`.
- [ ] Le lien "Connexion" est présent dans le navbar (desktop + mobile) de **toutes** les pages, ouvre l'app dans un nouvel onglet.
- [ ] Le lien "Espace membre" est présent dans le footer de **toutes** les pages.
- [ ] La section CTA verte affiche le nouveau wording "Bilan complet — 150€" avec les bullets mis à jour.
- [ ] Tous les meta titres listés en 3.6 sont mis à jour.
- [ ] Toutes les meta descriptions des pages de service mentionnent "150€" et/ou "sous 48h".
- [ ] Le formulaire "Être rappelé" poste correctement vers Formsubmit (vérifié dans Network).
- [ ] La popup est accessible (Échap, focus visible, role dialog).
- [ ] Le script `inject_booking_modal.py` est idempotent.
