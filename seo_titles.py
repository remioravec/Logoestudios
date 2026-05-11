"""Centralised SEO titles and meta descriptions for the Logopsi Studios site.

Used by:
  - generate_level2_pages.py  (trouble pages)
  - generate_level3_4_pages.py (city hubs + trouble+city)
  - generate_physique_chimie.py
  - patch_handwritten_pages.py (index, hubs N2, etc.)
"""

SUFFIX = " | Logopsi Studios"


def _display_name(slug):
    # Lazy import to avoid circular dependency: generate_level3_4_pages
    # itself imports from seo_titles.
    from generate_level3_4_pages import display_name
    return display_name(slug)


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

# Overrides for slugs whose display name is long enough that adding "en ligne"
# would push the title past ~65 chars.
_ORTHO_N2_TITLE_OVERRIDES = {
    "oralite": "Bilan troubles de l'oralité — Orthophoniste 150€/48h" + SUFFIX,
    "paralysie-cerebrale": "Bilan paralysie cérébrale — Orthophoniste 150€/48h" + SUFFIX,
}


def title_for_ortho_n2(slug):
    if slug in _ORTHO_N2_TITLE_OVERRIDES:
        return _ORTHO_N2_TITLE_OVERRIDES[slug]
    return "Bilan " + _display_name(slug).lower() + " en ligne — Orthophoniste 150€/48h" + SUFFIX


def title_for_ortho_n3(city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return "Bilan orthophonique à " + city + " — 150€, sous 48h" + SUFFIX


def title_for_ortho_n4(trouble_slug, city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return "Bilan " + _display_name(trouble_slug).lower() + " à " + city + " — Orthophoniste 150€/48h" + SUFFIX


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
    return "Bilan " + _display_name(slug) + " en ligne — Psychologue 150€/48h" + SUFFIX


def title_for_psycho_n3(city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return "Bilan psychologique à " + city + " — 150€, sous 48h" + SUFFIX


def title_for_psycho_n4(trouble_slug, city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return "Bilan " + _display_name(trouble_slug) + " à " + city + " — Psychologue 150€/48h" + SUFFIX


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
    return "Bilan " + subj + " " + lvl + " en ligne — 150€/48h" + SUFFIX


def title_for_scolaire_n3(city_slug):
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return "Soutien scolaire à " + city + " — Bilan 150€/48h" + SUFFIX


def title_for_scolaire_n4(subject_slug, level_slug, city_slug):
    subj = SUBJECT_LABELS.get(subject_slug, subject_slug)
    lvl = LEVEL_LABELS.get(level_slug, level_slug)
    city = CITY_NAMES.get(city_slug, city_slug.title())
    return "Bilan " + subj + " " + lvl + " à " + city + " — 150€/48h" + SUFFIX


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
    "site/index.html": "Bilan orthophonie, psychologie & soutien — 150€, 48h | Logopsi Studios",
    "site/orthophonie/index.html": "Bilan orthophonique en ligne — 150€, sous 48h | Logopsi Studios",
    "site/psychologie/index.html": "Bilan psychologique en ligne — 150€, sous 48h | Logopsi Studios",
    "site/soutien-scolaire/index.html": "Bilan pédagogique en ligne — 150€, sous 48h | Logopsi Studios",
    "site/contact.html": "Contact — Bilan 150€/48h | Logopsi Studios",
    "site/a-propos.html": "À propos — Bilan 150€/48h | Logopsi Studios",
    "site/mentions-legales.html": "Mentions légales — Bilan 150€/48h | Logopsi Studios",
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
