# Passation — Site Logopsi Études (logopsietudes.com)

> Document destiné à un **nouveau Claude / Claude Code** qui reprend le projet.
> Lis-le en entier avant toute action. Tout ce qu'il faut pour continuer est ici.

---

## 1. Le projet en 30 secondes

- **Client** : Logopsi Études — orthophonie, psychologie et soutien scolaire **100 % en ligne**, partout en France.
- **Site en production** : **https://logopsietudes.com** (WordPress).
- **Positionnement** : bilan à **150 €**, premier rendez-vous **sous 48h**, sans liste d'attente.
- **~543 pages** organisées en cocon sémantique SEO.
- Fondatrice citée dans les avis : **Virginie**. Avis Google : **5/5 · 15 avis**.
- Téléphone : **06 85 74 71 17**.

---

## 2. ⚙️ Architecture technique — À COMPRENDRE EN PRIORITÉ

Le site n'est **pas** un WordPress classique éditable dans l'admin. Tout le contenu est servi par un **plugin maison** : **`logopsi-deployer`**.

### Comment ça marche
- Chaque page WordPress a un contenu vide (`<!-- Logopsi page: slug -->`).
- Le vrai HTML de chaque page vit dans un **fichier** : `logopsi-deployer/data/html/<slug>.html`
  (le `/` du slug devient `__` : `orthophonie/dyslexie` → `orthophonie__dyslexie.html`).
- Le plugin (`logopsi-deployer.php`) intercepte l'affichage (`template_include` + `template_redirect`)
  et **sert le fichier HTML directement**, en appliquant à la volée : correction des liens
  (`.html` → permaliens), du logo, du menu mobile, et des redirections 301.
- **PRIORITÉ AU FICHIER** : le plugin sert d'abord le fichier `data/html/*.html`.
  La méta `_logopsi_full_html` n'est qu'un repli.

### ✅ Conséquence pratique (workflow de mise à jour)
> **Éditer un fichier `data/html/*.html` → reconstruire le zip → Rémi téléverse le plugin. C'est tout.**
> **PAS besoin de cliquer « Deploy »** dans l'admin (c'était l'ancien fonctionnement, source d'oublis).

Le HTML utilise **Tailwind CSS via CDN** + **Lucide icons via CDN** (inline dans chaque page).
Couleur primaire = classe `primary` / `bg-primary` (vert). Les icônes : `<i data-lucide="...">`.

---

## 3. 🔑 Accès

- **WordPress REST/XML-RPC** : via un **mot de passe d'application** (utilisateur `administration@remi-oravec.fr`, rôle admin).
  ⚠️ **Le mot de passe n'est PAS dans ce document** (sécurité). **Demande-le à Rémi** au démarrage.
  - REST : `https://logopsietudes.com/wp-json/wp/v2/...` (auth Basic).
  - Les **leads** (demandes de contact) sont dans le type `logopsi_lead`, exposé en REST (`/wp-json/wp/v2/logopsi_lead`) et lisible en XML-RPC (`wp.getPosts`).
- **Google Search Console + Analytics** : connectés via **Composio** (toolkit `google_search_console`, `google_analytics`, `googlesheets`, `googledrive`). Property : `https://logopsietudes.com/`.
- **GitHub** : dépôt `remioravec/Logoestudios`, branche `claude/jolly-clarke-rNfIL`.
  ⚠️ Le `git push` a souvent renvoyé **403** dans l'environnement précédent (intermittent) — si ça bloque,
  **livre le zip directement à Rémi** et retente le push plus tard.

---

## 4. 🛠️ Comment faire une modification (recette)

```bash
# 1. Éditer le(s) fichier(s) source
#    wp-plugin/logopsi-deployer/data/html/<slug>.html   (contenu d'une page)
#    wp-plugin/logopsi-deployer/logopsi-deployer.php     (comportement du plugin)

# 2. (Optionnel) valider la structure : balises équilibrées, 1 seul <footer>, etc.

# 3. Reconstruire le zip
cd wp-plugin && rm -f logopsi-deployer.zip && \
  zip -rq logopsi-deployer.zip logopsi-deployer -x '*.DS_Store' '*__pycache__*' && cd ..

# 4. Livrer logopsi-deployer.zip à Rémi -> il téléverse dans WP (Extensions -> Téléverser -> Remplacer -> Activer)
```

**Règles d'or quand tu édites une page :**
- Garde le `<nav>`, le `<footer>`, la modale `booking-modal` et les `<script>` existants.
- Insère ton contenu **entre la fin du hero et le `<footer>`**.
- Vérifie l'**équilibre des balises** (`<div>`/`</div>`, `<section>`/`</section>`) et **un seul `<footer>`**.
- Les liens internes en absolu : `https://logopsietudes.com/...`.
- Rendu **impossible à styliser en local** (CDN Tailwind souvent bloqué hors-ligne) — valide la **structure** par script, le style s'applique sur le live.
- Idempotence : marque tes injections par un commentaire (`<!-- logopsi-xxx -->`) et skippe si déjà présent.

---

## 5. Types de pages (data/html/)

| Type | Exemple de fichier | Rôle |
|---|---|---|
| Accueil | `accueil.html` (servi sur `/`) | Home |
| Piliers | `orthophonie.html`, `psychologie.html`, `soutien-scolaire.html` | catégories |
| **Page mère (trouble)** | `orthophonie__dyslexie.html` | 1 trouble |
| **Hub ville** | `orthophonie__villes__nice.html` | discipline × ville |
| **Page fille (ville×trouble)** | `orthophonie__villes__dyslexie-lyon.html` | trouble × ville |
| **Soutien** | `soutien-scolaire__mathematiques__ce1.html`, `...__ce1-nice.html` | matière × niveau [× ville] |
| Divers | `contact.html`, `a-propos.html`, `tarifs.html`, `mentions-legales.html` | |

Villes = **paris, lyon, marseille, toulouse, nice**.

---

## 6. ✅ État actuel (déjà fait)

- **Menu + footer** uniformes sur toutes les pages ; liens cassés réparés ; hubs villes régénérés.
- **Toggle FR/ES** (Google Translate) dans le menu desktop + mobile ; **favicon** + **logo « Logopsi Études »**.
- **Accueil** : bouton **« Appeler 06 85 74 71 17 »** (hero + flottant mobile) ; **avis Google** (bandeau note + carrousel) + **AggregateRating (JSON-LD)** ; section **« Notre histoire / Notre équipe »**.
- **Contact** : champ **téléphone** ajouté ; formulaires envoyés à `administration@remi-oravec.fr` **+ `logopsietudes@gmail.com`** ; leads sauvegardés (type `logopsi_lead`, exposé REST) ; en-tête `From` propre.
- **Enrichissement** : **488 pages** templatisées (villes×trouble + soutien) enrichies — contenu unique, bloc local « autour de moi », FAQ, **maillage interne dense**. Marqueur `logopsi-enrich`.
- **Pages mères reworkées** (H1/H2 SEO, FAQ + schema.org FAQPage) :
  - `dyslexie`, `dysorthographie`, `hpi` (rédigées par Claude, cf. `rework_mothers.py`),
  - `dyscalculie`, `dysphasie`, `begaiement`, `tsa` (**rédactions du client** intégrées depuis un Google Sheet, cf. `integrate_redactions*.py` + `md_to_page.py`).
- **Hubs villes upgradés** (10 pages ortho+psy) : grille de tous les accompagnements de la ville (→ pages filles), réassurance, contenu local. Marqueur `logopsi-hub`.
- **Maillage ascendant** : 110/110 pages filles ville×trouble lient vers hub ville + page mère + discipline.
- **Redirection 301** `/tarifs-2/` → `/tarifs/` (dans le plugin).

---

## 7. 🔧 Scripts de tooling (tous à la racine)

| Script | Rôle |
|---|---|
| `enrich_pages.py` | Enrichit les pages templatisées (villes×trouble, soutien) — datasets CITIES/CURRIC/TROUBLE, maillage. **Idempotent.** |
| `hub_upgrade.py` | Upgrade UX des hubs villes (grille filles + réassurance + local + maillage ascendant). |
| `md_to_page.py` | **Convertisseur Markdown→HTML Tailwind** + injection dans une page mère (H1, sections, tableaux, listes, FAQ+schema, méta). Réutilisable. |
| `integrate_redactions.py` / `integrate_redactions2.py` | Intègrent les rédactions client (dyscalculie/dysphasie/begaiement/tsa) via `md_to_page`. **Modèle à suivre pour de nouvelles rédactions.** |
| `rework_mothers.py` | Reworks dyslexie/dysortho/HPI. |
| `add_call_button.py` / `add_home_sections.py` | Bouton d'appel + avis GMB + équipe (accueil). |
| `audit_live_site.py` | Crawler d'audit (menu/footer/liens) du site live via REST. |
| Historiques : `add_lang_toggle.py`, `add_mobile_toggle.py`, `fix_*`, `deploy_cocoon.py`, `build_wp_plugin.py`, `generate_*` | générations/patches passés. |

> ⚠️ Certains scripts ont un chemin `HTML="wp-plugin/logopsi-deployer/data/html"` relatif à la racine — lance-les depuis la racine du repo.

---

## 8. 🚧 Tâches EN COURS / à faire (priorité)

1. **Bouton « Connexion » CASSÉ** — pointe vers `https://app.logopsiestudios.com/fr/login` (ancien domaine, **DNS mort**) sur **542 pages**. → Attendre de Rémi la **bonne URL** de connexion, puis remplacer partout (`grep -rl 'app.logopsiestudios.com'`).
2. **Redirection de l'ancien domaine** `logopsiestudios.com` → `logopsietudes.com` : **n'existe pas** (ancien domaine sans DNS). À poser côté registrar/hébergeur de l'ancien domaine (Raiola ou Hostinger). **Rien à coder** côté site — c'est de la config DNS/301.
3. **Emails non délivrés** : **aucun plugin SMTP** n'est installé → `wp_mail()` échoue silencieusement. Les leads sont quand même **sauvegardés** (type `logopsi_lead`). Recommandation : installer/configurer **WP Mail SMTP** (nécessite des identifiants SMTP, ex. mot de passe d'application Gmail de `logopsietudes@gmail.com`).
4. **Pages à potentiel GSC** (voir `Logopsi_pages_a_enrichir_GSC.xlsx`) : continuer l'étoffe UX/contenu + maillage. Rubrique **psychologie** sous-exploitée (TDAH Paris, HPI Nice, bilan personnalité Nice).

---

## 9. 📊 SEO / données

- **Priorités d'enrichissement** : `Logopsi_pages_a_enrichir_GSC.xlsx` (58 pages classées par potentiel + requêtes cibles + action).
- **Insight clé** : l'intention **locale** (« orthophoniste … **autour de moi** / près de chez vous ») revient sur beaucoup de pages villes → à cibler partout.
- **Leads** : `Logopsi_leads_contacts.xlsx` (export des demandes). Les relire via REST/XML-RPC.
- Récupérer les données GSC via **Composio** (`GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`, `..._INSPECT_URL`).

---

## 10. Vérifs rapides (santé du repo)

```bash
# nb de pages
ls wp-plugin/logopsi-deployer/data/html/*.html | wc -l
# pages enrichies / hubs / FAQ schema
grep -rl 'logopsi-enrich' wp-plugin/logopsi-deployer/data/html/ | wc -l
grep -rl 'logopsi-hub'    wp-plugin/logopsi-deployer/data/html/ | wc -l
# structure d'une page (équilibre)
python3 -c "h=open('wp-plugin/logopsi-deployer/data/html/accueil.html').read(); print('div',h.count('<div')==h.count('</div>'),'footer',h.count('<footer'))"
```

---

*Dernière mise à jour de ce document : passation. Plugin `logopsi-deployer` v1.1.0. Bonne continuation 👋*
