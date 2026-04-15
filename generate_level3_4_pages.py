#!/usr/bin/env python3
"""Generate all Niveau 3 (city hub) and Niveau 4 (trouble+city / level+city) pages.

Generates approximately 380 pages:
  - Ortho N3: 5 city hubs
  - Ortho N4: 55 trouble+city pages
  - Psycho N3: 5 city hubs
  - Psycho N4: 55 trouble+city pages
  - Scolaire N3: 5 city hubs
  - Scolaire N4: ~255 level+city pages
"""

import os

from shared_components import (
    get_head, get_navbar, get_footer, get_cta_section,
    get_about_section, get_js, get_breadcrumb,
)
from generate_level2_pages import ORTHO_PAGES, PSYCHO_PAGES, VILLES

try:
    from generate_physique_chimie import LEVELS as PC_LEVELS
except ImportError:
    PC_LEVELS = {}

# ============================================================
# DATA
# ============================================================

CITY_DATA = {
    "Paris": {
        "region": "Île-de-France",
        "gentile": "parisiens et franciliens",
        "wait_text": "Les délais pour consulter un {practitioner} spécialisé à Paris peuvent atteindre plusieurs mois. En ligne, nous proposons un premier rendez-vous sous 48 heures.",
        "transport_text": "Plus besoin de traverser Paris en transport. Votre enfant consulte depuis le confort de votre domicile, dans un environnement familier et rassurant.",
    },
    "Marseille": {
        "region": "Bouches-du-Rhône",
        "gentile": "marseillais",
        "wait_text": "À Marseille, les listes d'attente chez les spécialistes sont souvent longues. Notre plateforme vous connecte avec un professionnel sous 48 heures.",
        "transport_text": "Évitez les déplacements dans Marseille. Les séances se font en visio depuis chez vous, avec la même qualité qu'en cabinet.",
    },
    "Lyon": {
        "region": "Rhône",
        "gentile": "lyonnais",
        "wait_text": "Les familles lyonnaises connaissent les difficultés d'accès aux soins spécialisés. En ligne, votre enfant est pris en charge sous 48 heures.",
        "transport_text": "Plus besoin de traverser Lyon pour un rendez-vous. Consultez depuis chez vous, dans un cadre familier pour votre enfant.",
    },
    "Toulouse": {
        "region": "Haute-Garonne",
        "gentile": "toulousains",
        "wait_text": "À Toulouse, trouver un spécialiste rapidement peut être un défi. Notre plateforme propose un premier rendez-vous sous 48 heures.",
        "transport_text": "Pas besoin de se déplacer à Toulouse. Les séances en ligne offrent confort et flexibilité pour toute la famille.",
    },
    "Nice": {
        "region": "Alpes-Maritimes",
        "gentile": "niçois",
        "wait_text": "Sur la Côte d'Azur, les délais de prise en charge sont souvent longs. En ligne, nous garantissons un premier rendez-vous sous 48 heures.",
        "transport_text": "Consultez depuis chez vous à Nice ou ses environs. Plus besoin de se déplacer pour accéder à des spécialistes qualifiés.",
    },
}

# Display names for slugs that differ from title-cased slug
DISPLAY_NAMES = {
    "tsa": "TSA",
    "hpi": "HPI",
    "tca": "TCA",
    "tdah": "TDAH",
    "trisomie-21": "Trisomie 21",
    "paralysie-cerebrale": "Paralysie cérébrale",
    "fente-palatine": "Fente palatine",
    "phobie-scolaire": "Phobie scolaire",
    "harcelement-scolaire": "Harcèlement scolaire",
    "addictions-ecrans": "Addictions aux écrans",
    "troubles-sommeil": "Troubles du sommeil",
    "traumatismes-deuil": "Traumatismes et deuil",
    "oralite": "Troubles de l'oralité",
    "surdite": "Surdité",
    "enuresie": "Énurésie",
    "dyslexie": "Dyslexie",
    "dysorthographie": "Dysorthographie",
    "dyscalculie": "Dyscalculie",
    "dysphasie": "Dysphasie",
    "begaiement": "Bégaiement",
    "anxiete": "Anxiété",
    "depression": "Dépression",
}


def display_name(slug):
    """Return the pretty French display name for a trouble slug."""
    if slug in DISPLAY_NAMES:
        return DISPLAY_NAMES[slug]
    return slug.replace("-", " ").capitalize()


def city_slug(city):
    """Return a URL-safe slug for a city name."""
    return city.lower().replace("é", "e").replace("è", "e").replace("ê", "e")


# ------------------------------------------------------------------
# Soutien-scolaire subjects & level data
# ------------------------------------------------------------------

SCOLAIRE_SUBJECTS = {
    "mathematiques": {
        "label": "Mathématiques",
        "icon": "calculator",
        "desc": "Cours de mathématiques en ligne",
        "levels": {
            "cp": {"label": "CP", "cycle": "Primaire"},
            "ce1": {"label": "CE1", "cycle": "Primaire"},
            "ce2": {"label": "CE2", "cycle": "Primaire"},
            "cm1": {"label": "CM1", "cycle": "Primaire"},
            "cm2": {"label": "CM2", "cycle": "Primaire"},
            "6eme": {"label": "6ème", "cycle": "Collège"},
            "5eme": {"label": "5ème", "cycle": "Collège"},
            "4eme": {"label": "4ème", "cycle": "Collège"},
            "3eme": {"label": "3ème", "cycle": "Collège"},
            "seconde": {"label": "Seconde", "cycle": "Lycée"},
            "premiere": {"label": "Première", "cycle": "Lycée"},
            "terminale": {"label": "Terminale", "cycle": "Lycée"},
        },
    },
    "francais": {
        "label": "Français",
        "icon": "book-open",
        "desc": "Cours de français en ligne",
        "levels": {
            "cp": {"label": "CP", "cycle": "Primaire"},
            "ce1": {"label": "CE1", "cycle": "Primaire"},
            "ce2": {"label": "CE2", "cycle": "Primaire"},
            "cm1": {"label": "CM1", "cycle": "Primaire"},
            "cm2": {"label": "CM2", "cycle": "Primaire"},
            "6eme": {"label": "6ème", "cycle": "Collège"},
            "5eme": {"label": "5ème", "cycle": "Collège"},
            "4eme": {"label": "4ème", "cycle": "Collège"},
            "3eme": {"label": "3ème", "cycle": "Collège"},
            "seconde": {"label": "Seconde", "cycle": "Lycée"},
            "premiere": {"label": "Première", "cycle": "Lycée"},
            "terminale": {"label": "Terminale", "cycle": "Lycée"},
        },
    },
    "anglais": {
        "label": "Anglais",
        "icon": "globe",
        "desc": "Cours d'anglais en ligne",
        "levels": {
            "cp": {"label": "CP", "cycle": "Primaire"},
            "ce1": {"label": "CE1", "cycle": "Primaire"},
            "ce2": {"label": "CE2", "cycle": "Primaire"},
            "cm1": {"label": "CM1", "cycle": "Primaire"},
            "cm2": {"label": "CM2", "cycle": "Primaire"},
            "6eme": {"label": "6ème", "cycle": "Collège"},
            "5eme": {"label": "5ème", "cycle": "Collège"},
            "4eme": {"label": "4ème", "cycle": "Collège"},
            "3eme": {"label": "3ème", "cycle": "Collège"},
            "seconde": {"label": "Seconde", "cycle": "Lycée"},
            "premiere": {"label": "Première", "cycle": "Lycée"},
            "terminale": {"label": "Terminale", "cycle": "Lycée"},
        },
    },
    "physique-chimie": {
        "label": "Physique-Chimie",
        "icon": "flask-conical",
        "desc": "Cours de physique-chimie en ligne",
        "levels": {
            "5eme": {"label": "5ème", "cycle": "Collège"},
            "4eme": {"label": "4ème", "cycle": "Collège"},
            "3eme": {"label": "3ème", "cycle": "Collège"},
            "seconde": {"label": "Seconde", "cycle": "Lycée"},
            "premiere": {"label": "Première", "cycle": "Lycée"},
            "terminale": {"label": "Terminale", "cycle": "Lycée"},
        },
    },
    "aide-aux-devoirs": {
        "label": "Aide aux devoirs",
        "icon": "book-open",
        "desc": "Aide aux devoirs en ligne",
        "levels": {
            "cp": {"label": "CP", "cycle": "Primaire"},
            "ce1": {"label": "CE1", "cycle": "Primaire"},
            "ce2": {"label": "CE2", "cycle": "Primaire"},
            "cm1": {"label": "CM1", "cycle": "Primaire"},
            "cm2": {"label": "CM2", "cycle": "Primaire"},
            "6eme": {"label": "6ème", "cycle": "Collège"},
            "5eme": {"label": "5ème", "cycle": "Collège"},
            "4eme": {"label": "4ème", "cycle": "Collège"},
            "3eme": {"label": "3ème", "cycle": "Collège"},
        },
    },
}

# ------------------------------------------------------------------
# Educational content for each subject (used in N4 scolaire pages)
# physique-chimie uses PC_LEVELS imported from generate_physique_chimie.py
# ------------------------------------------------------------------

MATHS_LEVELS = {
    "cp": {
        "hero": "Le CP est l'année où votre enfant découvre les nombres jusqu'à 100, apprend à compter, à additionner et à soustraire. C'est aussi l'entrée dans la géométrie avec les premières formes. Une base solide en CP est essentielle pour toute la suite de la scolarité en mathématiques.",
        "topics": [
            ("Les nombres jusqu'à 100", "hash", "Lire, écrire et comparer les nombres. Comprendre la dizaine et les unités."),
            ("Addition et soustraction", "plus", "Calculer des additions et soustractions simples, résoudre des petits problèmes."),
            ("Les formes géométriques", "shapes", "Reconnaître et nommer les formes de base : carré, rectangle, triangle, cercle."),
            ("Mesures et grandeurs", "ruler", "Comparer des longueurs, utiliser une règle, découvrir les heures et la monnaie."),
        ],
        "method": "En CP, nous rendons les mathématiques concrètes et ludiques. Manipulation d'objets virtuels, jeux de calcul, défis amusants : votre enfant apprend en s'amusant. Nous veillons à consolider le sens du nombre, fondation de tout le parcours mathématique.",
        "faq": [
            ("Mon enfant a du mal avec les nombres, est-ce normal en CP ?", "C'est fréquent et tout à fait rattrapable. Nos enseignants utilisent des supports visuels et manipulatoires pour aider votre enfant à construire le sens du nombre à son rythme."),
            ("Comment savoir si mon enfant a besoin de soutien en maths dès le CP ?", "Si votre enfant confond les chiffres, a du mal à compter au-delà de 20 ou ne comprend pas les additions simples après quelques mois de CP, un accompagnement peut l'aider à rattraper sereinement."),
        ],
    },
    "ce1": {
        "hero": "Le CE1 approfondit les acquis du CP : les nombres vont jusqu'à 1 000, la multiplication fait son apparition et la géométrie se précise. C'est une année de consolidation où les automatismes de calcul se mettent en place.",
        "topics": [
            ("Les nombres jusqu'à 1 000", "hash", "Lire, écrire, décomposer et comparer les nombres jusqu'à 1 000."),
            ("La multiplication", "x", "Découvrir le sens de la multiplication, apprendre les premières tables (2, 3, 4, 5)."),
            ("Géométrie du plan", "shapes", "Reconnaître et tracer des figures, utiliser la règle et l'équerre, notions de symétrie."),
            ("Résolution de problèmes", "lightbulb", "Comprendre un énoncé, choisir l'opération, formuler une réponse."),
        ],
        "method": "En CE1, nous alternons entre exercices de calcul mental pour développer les automatismes et résolution de problèmes pour donner du sens aux opérations. Chaque séance est structurée avec un temps de jeu et un temps de travail.",
        "faq": [
            ("Mon enfant ne retient pas les tables de multiplication, que faire ?", "C'est très courant en CE1. Nos enseignants utilisent des jeux de mémorisation, des chansons et des exercices répétés sur plusieurs séances pour ancrer les tables progressivement."),
            ("Le CE1 est-il une année difficile en maths ?", "Le CE1 marque un saut quantitatif important (nombres plus grands, nouvelles opérations). Un accompagnement régulier permet d'éviter l'accumulation de lacunes qui pèseraient ensuite."),
        ],
    },
    "ce2": {
        "hero": "Le CE2 consolide les fondamentaux : les quatre opérations sont travaillées, les nombres dépassent 10 000 et la géométrie s'enrichit avec les premières notions d'angle et de périmètre. C'est la fin du cycle 2 et un socle crucial pour le CM1.",
        "topics": [
            ("Nombres et calcul", "hash", "Nombres jusqu'à 10 000, addition, soustraction, multiplication posée, initiation à la division."),
            ("Calcul mental", "brain", "Automatiser les tables, calculer rapidement des sommes et des différences."),
            ("Périmètre et mesures", "ruler", "Calculer le périmètre d'un polygone, convertir des unités simples."),
            ("Résolution de problèmes", "lightbulb", "Problèmes à une ou deux étapes avec les quatre opérations."),
        ],
        "method": "En CE2, nous insistons sur le calcul mental quotidien et la méthodologie de résolution de problèmes. L'enfant apprend à repérer les mots-clés d'un énoncé et à choisir la bonne opération. Nous préparons aussi le passage au cycle 3.",
        "faq": [
            ("Mon enfant a du mal avec la division, est-ce grave ?", "La division est introduite progressivement en CE2. Nos enseignants reprennent les bases de la multiplication (qui est l'opération inverse) et utilisent des partages concrets pour donner du sens à la division."),
            ("Comment préparer le passage en CM1 ?", "Le CM1 suppose une bonne maîtrise des quatre opérations et du calcul mental. Nos séances consolident ces acquis et comblent les éventuelles lacunes pour un passage serein."),
        ],
    },
    "cm1": {
        "hero": "Le CM1 marque l'entrée dans le cycle 3 avec de nouvelles exigences : les fractions font leur apparition, les nombres décimaux sont introduits et la géométrie se complexifie avec les droites parallèles et perpendiculaires. C'est une année charnière.",
        "topics": [
            ("Fractions simples", "pie-chart", "Comprendre la notion de fraction, comparer et encadrer des fractions simples."),
            ("Nombres décimaux", "hash", "Découvrir les dixièmes et centièmes, placer des décimaux sur une droite graduée."),
            ("Géométrie : droites et angles", "ruler", "Droites parallèles, perpendiculaires, mesurer et construire des angles."),
            ("Proportionnalité", "scale", "Premières situations de proportionnalité, tableaux et schémas."),
        ],
        "method": "En CM1, nous accompagnons le passage de l'arithmétique entière aux fractions et décimaux, un virage conceptuel majeur. Nos enseignants utilisent des représentations visuelles (parts de pizza, droites graduées) pour rendre ces notions intuitives.",
        "faq": [
            ("Les fractions sont trop abstraites pour mon enfant, comment l'aider ?", "Nous partons de situations concrètes (partager un gâteau, mesurer des quantités) pour construire le sens de la fraction. Les manipulations visuelles rendent la notion accessible à tous les élèves."),
            ("Mon enfant était bon en maths avant le CM1, pourquoi ça baisse ?", "Le CM1 introduit des concepts plus abstraits (fractions, décimaux). C'est normal que le rythme change. Un accompagnement ciblé permet de surmonter ce cap et de retrouver confiance."),
        ],
    },
    "cm2": {
        "hero": "Le CM2 prépare l'entrée au collège : les fractions, les décimaux et la géométrie sont approfondis. L'enfant apprend aussi les premières notions de proportionnalité et perfectionne sa résolution de problèmes complexes. Une année décisive pour aborder la 6ème sereinement.",
        "topics": [
            ("Opérations sur les décimaux", "calculator", "Additionner, soustraire, multiplier et diviser des nombres décimaux."),
            ("Fractions et pourcentages", "pie-chart", "Additionner des fractions de même dénominateur, découvrir les pourcentages."),
            ("Aires et volumes", "box", "Calculer l'aire d'un rectangle, d'un triangle, découvrir les unités de volume."),
            ("Préparation à la 6ème", "graduation-cap", "Consolider les acquis, développer l'autonomie, s'adapter aux exigences du collège."),
        ],
        "method": "En CM2, nous préparons votre enfant aux méthodes de travail du collège : prise de notes, organisation, raisonnement autonome. Les séances combinent consolidation des fondamentaux et introduction progressive des attendus de 6ème.",
        "faq": [
            ("Comment préparer mon enfant à la 6ème en maths ?", "Nous vérifions que les bases sont solides (calcul, fractions, géométrie) et nous familiarisons votre enfant avec le format des cours au collège : exercices plus longs, raisonnement à rédiger, autonomie accrue."),
            ("Mon enfant angoisse à l'idée d'aller au collège, est-ce fréquent ?", "Très fréquent. Au-delà du soutien scolaire, nos enseignants rassurent et donnent confiance. Un enfant bien préparé en maths aborde la 6ème plus sereinement."),
        ],
    },
    "6eme": {
        "hero": "La 6ème est la première année du collège et la fin du cycle 3. En mathématiques, votre enfant approfondit les nombres décimaux, découvre les fractions avancées, entre dans le calcul littéral et explore la géométrie dans l'espace. C'est un cap d'adaptation majeur.",
        "topics": [
            ("Nombres et calculs", "calculator", "Opérations sur les décimaux, priorités opératoires, initiation au calcul littéral."),
            ("Fractions", "pie-chart", "Comparer, simplifier et additionner des fractions de dénominateurs différents."),
            ("Géométrie dans l'espace", "box", "Patrons de solides, volumes de pavés droits, perspective cavalière."),
            ("Proportionnalité", "scale", "Tableaux de proportionnalité, coefficient, pourcentages."),
        ],
        "method": "En 6ème, nous aidons votre enfant à s'adapter au rythme du collège. Nos séances comblent les lacunes du primaire si nécessaire et construisent les nouvelles compétences attendues : rédaction mathématique, raisonnement, autonomie.",
        "faq": [
            ("Mon enfant a du mal à s'adapter au collège en maths, que faire ?", "L'adaptation prend souvent quelques mois. Nos enseignants identifient les lacunes éventuelles du primaire et aident votre enfant à prendre ses repères avec la méthode de travail du collège."),
            ("Le calcul littéral est nouveau et difficile, comment l'aborder ?", "Nous introduisons le calcul littéral progressivement, en partant de situations concrètes. L'objectif est que l'élève comprenne le sens des lettres en mathématiques avant de manipuler les expressions."),
        ],
    },
    "5eme": {
        "hero": "La 5ème approfondit les mathématiques du collège : les nombres relatifs, le calcul littéral, les statistiques et la géométrie dynamique. C'est une année où l'abstraction augmente et où les lacunes du passé peuvent se faire sentir.",
        "topics": [
            ("Nombres relatifs", "plus-minus", "Additionner et soustraire des nombres relatifs, repérage dans un plan."),
            ("Calcul littéral", "variable", "Développer, factoriser des expressions simples, résoudre des équations du premier degré."),
            ("Statistiques", "bar-chart", "Moyenne, médiane, diagrammes, effectifs et fréquences."),
            ("Symétrie et angles", "rotate-cw", "Symétrie centrale, angles alternes-internes, somme des angles d'un triangle."),
        ],
        "method": "En 5ème, nous aidons l'élève à passer de l'arithmétique concrète au raisonnement abstrait. Chaque notion est ancrée dans des exemples concrets avant d'être formalisée. Nous développons aussi les compétences de rédaction mathématique.",
        "faq": [
            ("Mon enfant ne comprend pas les nombres relatifs, comment l'aider ?", "Les nombres négatifs sont un concept difficile. Nos enseignants utilisent des repères concrets (températures, ascenseur, argent de poche) pour donner du sens avant de passer aux règles de calcul."),
            ("La 5ème est-elle importante pour la suite ?", "Oui, la 5ème pose les bases du calcul littéral et de la géométrie qui seront approfondis en 4ème et 3ème. Combler les lacunes maintenant évite l'effet boule de neige."),
        ],
    },
    "4eme": {
        "hero": "La 4ème est une année exigeante en mathématiques : le théorème de Pythagore, les équations, les puissances et la géométrie dans l'espace sont au programme. Le niveau d'abstraction augmente significativement et la rigueur de rédaction devient essentielle.",
        "topics": [
            ("Théorème de Pythagore", "triangle", "Calculer une longueur dans un triangle rectangle, réciproque du théorème."),
            ("Équations", "equal", "Résoudre des équations du premier degré, mettre en équation un problème."),
            ("Puissances", "superscript", "Notation puissance, règles de calcul, écriture scientifique."),
            ("Transformations", "move", "Translation, rotation, homothétie, propriétés de conservation."),
        ],
        "method": "En 4ème, nous combinons rigueur et méthode. Chaque séance travaille la compréhension du cours puis l'application sur des exercices de difficulté croissante. Nous insistons sur la rédaction des démonstrations, compétence clé pour le Brevet.",
        "faq": [
            ("Le théorème de Pythagore est difficile pour mon enfant, que faire ?", "Nous décomposons le théorème en étapes claires : identifier le triangle rectangle, repérer l'hypoténuse, appliquer la formule. Avec de la pratique et de la méthode, tous les élèves peuvent le maîtriser."),
            ("Comment préparer le Brevet dès la 4ème ?", "Les notions de 4ème constituent une part importante du programme de 3ème et donc du Brevet. Nous veillons à ce que chaque chapitre soit solidement acquis pour aborder la 3ème en confiance."),
        ],
    },
    "3eme": {
        "hero": "La 3ème est l'année du Brevet. En mathématiques, votre enfant aborde le théorème de Thalès, les fonctions, la trigonométrie et les probabilités. L'épreuve du Brevet évalue la maîtrise du programme de tout le cycle 4 et la capacité à raisonner de manière autonome.",
        "topics": [
            ("Théorème de Thalès", "triangle", "Calculer des longueurs, vérifier un parallélisme, résoudre des problèmes géométriques."),
            ("Fonctions", "trending-up", "Notion de fonction, lecture graphique, fonctions linéaires et affines."),
            ("Trigonométrie", "compass", "Cosinus, sinus, tangente dans un triangle rectangle."),
            ("Probabilités", "dice", "Expériences aléatoires, calcul de probabilités, arbres de probabilités."),
        ],
        "method": "En 3ème, notre priorité est la préparation au Brevet. Nous combinons révision du programme, entraînement sur des sujets de Brevet chronométrés et perfectionnement de la méthodologie (rédaction, démonstrations, gestion du temps).",
        "faq": [
            ("Comment bien préparer l'épreuve de maths du Brevet ?", "Nous proposons un plan de révision structuré couvrant tout le cycle 4. Les séances incluent des exercices type Brevet, des annales corrigées et des conseils de méthode pour gagner des points le jour J."),
            ("Mon enfant a des lacunes depuis la 4ème, est-il trop tard ?", "Non. Nos enseignants identifient les lacunes prioritaires et construisent un parcours de remise à niveau ciblé. Avec un travail régulier, il est tout à fait possible de se remettre à niveau pour le Brevet."),
        ],
    },
    "seconde": {
        "hero": "La Seconde générale est un tournant en mathématiques : le programme est dense et exigeant avec les fonctions, les équations, les statistiques avancées et la géométrie analytique. C'est aussi l'année du choix de spécialité : un bon niveau en maths ouvre de nombreuses portes.",
        "topics": [
            ("Fonctions", "trending-up", "Notion de fonction, variations, extremums, fonctions de référence (carré, inverse, racine)."),
            ("Équations et inéquations", "equal", "Résolution algébrique, factorisation, signe d'un produit/quotient."),
            ("Statistiques et probabilités", "bar-chart", "Écart-type, variance, probabilités conditionnelles, arbres pondérés."),
            ("Géométrie dans le plan", "compass", "Vecteurs, coordonnées, équation de droite, colinéarité."),
        ],
        "method": "En Seconde, nous préparons votre enfant aux exigences du lycée : abstraction accrue, raisonnement rigoureux, démonstrations. Nos séances combinent compréhension du cours et entraînement intensif pour développer les réflexes mathématiques.",
        "faq": [
            ("Le niveau de maths monte beaucoup en Seconde, comment s'adapter ?", "Le saut entre la 3ème et la Seconde est réel. Nos enseignants accompagnent cette transition en consolidant les acquis du collège et en installant progressivement les nouvelles méthodes de travail."),
            ("Faut-il prendre la spécialité maths en Première ?", "La spécialité maths est indispensable pour les filières scientifiques, économiques et certaines formations sélectives. Nos enseignants peuvent évaluer le niveau de votre enfant et le conseiller."),
        ],
    },
    "premiere": {
        "hero": "La Première spécialité mathématiques approfondit considérablement le programme : suites, dérivation, fonctions exponentielles, produit scalaire et probabilités conditionnelles. Le coefficient au bac est élevé et le rythme de travail s'intensifie.",
        "topics": [
            ("Suites numériques", "list", "Suites arithmétiques et géométriques, sens de variation, formules explicites et par récurrence."),
            ("Dérivation", "trending-up", "Nombre dérivé, fonction dérivée, tangente, variations d'une fonction."),
            ("Fonction exponentielle", "zap", "Propriétés algébriques, dérivée, résolution d'équations et d'inéquations."),
            ("Produit scalaire", "move", "Définition, propriétés, applications à la géométrie plane."),
        ],
        "method": "En Première spécialité, nous insistons sur la rigueur du raisonnement et la maîtrise technique. Chaque séance combine explication de cours, exercices d'application et problèmes de synthèse. Nous préparons les évaluations communes et anticipons le programme de Terminale.",
        "faq": [
            ("La dérivation est difficile, comment aider mon enfant ?", "La dérivation est un concept fondamental mais qui demande du temps. Nos enseignants partent de l'interprétation graphique (tangente) avant de passer au calcul formel, avec de nombreux exercices progressifs."),
            ("Mon enfant hésite à garder la spécialité maths en Terminale, que faire ?", "Nos enseignants évaluent le niveau et la motivation de votre enfant. Si la spécialité est nécessaire pour son projet d'études, un accompagnement régulier peut combler les difficultés."),
        ],
    },
    "terminale": {
        "hero": "La Terminale spécialité mathématiques est l'aboutissement du parcours au lycée. Le programme couvre les limites, la continuité, les primitives, la fonction logarithme, la géométrie dans l'espace et les probabilités avancées. L'épreuve du bac, coefficient 16, exige une préparation rigoureuse.",
        "topics": [
            ("Limites et continuité", "infinity", "Limites de fonctions, asymptotes, théorème des valeurs intermédiaires."),
            ("Primitives et intégrales", "sigma", "Calculer des primitives, intégrale d'une fonction, calcul d'aires."),
            ("Fonction logarithme", "trending-up", "Logarithme népérien, propriétés, équations et inéquations."),
            ("Géométrie dans l'espace", "box", "Droites et plans, orthogonalité, représentations paramétriques."),
        ],
        "method": "En Terminale, notre priorité est la préparation au bac (coefficient 16). Nous combinons révision approfondie du programme, entraînement intensif sur des sujets de bac et perfectionnement de la méthodologie. Nous préparons aussi le Grand Oral.",
        "faq": [
            ("Comment bien préparer l'épreuve de maths au bac ?", "Notre méthode combine révision systématique du cours, entraînement sur des sujets de bac chronométrés et travail sur les erreurs les plus courantes. Nous ciblons les chapitres les plus fréquents aux examens."),
            ("Mon enfant vise une prépa ou une école d'ingénieurs, comment le préparer ?", "Au-delà du programme de Terminale, nous proposons des exercices de niveau supérieur et développons la rapidité et l'autonomie dans la résolution de problèmes."),
        ],
    },
}

FRANCAIS_LEVELS = {
    "cp": {
        "hero": "Le CP est l'année fondamentale de l'apprentissage de la lecture et de l'écriture. Votre enfant découvre les correspondances entre les lettres et les sons, commence à lire des mots puis des phrases, et apprend à écrire les premières syllabes. Un accompagnement dès le CP pose les bases de toute la réussite scolaire.",
        "topics": [
            ("Lecture et déchiffrage", "book-open", "Reconnaissance des lettres, correspondance sons-lettres, lecture syllabique puis fluide."),
            ("Écriture et copie", "pencil", "Formation des lettres, copie de mots et de phrases courtes, premiers écrits autonomes."),
            ("Compréhension orale et écrite", "ear", "Écouter et comprendre des histoires, répondre à des questions sur un texte lu."),
            ("Vocabulaire", "list", "Enrichir le lexique quotidien, catégoriser des mots, découvrir les familles de mots."),
        ],
        "method": "En CP, nous utilisons des méthodes de lecture éprouvées, combinant approche syllabique et compréhension de texte. Chaque séance est ludique et interactive, avec des jeux de lecture, des dictées de syllabes et des lectures partagées.",
        "faq": [
            ("Mon enfant a du mal à lire en CP, dois-je m'inquiéter ?", "L'apprentissage de la lecture prend du temps et chaque enfant avance à son rythme. Si les difficultés persistent après quelques mois, un accompagnement individualisé peut l'aider à consolider les bases."),
            ("Comment motiver mon enfant à lire ?", "Nos enseignants choisissent des textes adaptés aux centres d'intérêt de votre enfant. La lecture doit rester un plaisir : nous évitons la pression et valorisons chaque progrès."),
        ],
    },
    "ce1": {
        "hero": "Le CE1 consolide la lecture et développe la production écrite. Votre enfant améliore sa fluence de lecture, commence à rédiger des textes courts et entre dans l'étude de la grammaire et de la conjugaison. C'est l'année où la lecture devient un outil au service de tous les apprentissages.",
        "topics": [
            ("Lecture fluide", "book-open", "Améliorer la vitesse et l'expressivité de lecture, comprendre des textes variés."),
            ("Grammaire", "list", "La phrase, le verbe, le nom, le déterminant, l'adjectif, le sujet."),
            ("Conjugaison", "clock", "Présent des verbes du 1er groupe, être et avoir, passé composé et futur."),
            ("Production d'écrits", "pencil", "Écrire des phrases puis des petits textes : récits, descriptions, lettres."),
        ],
        "method": "En CE1, nous développons la fluence de lecture par des exercices quotidiens et travaillons la grammaire et la conjugaison en lien avec la production écrite. L'enfant apprend à construire des phrases correctes et à enrichir son expression.",
        "faq": [
            ("Mon enfant lit mais ne comprend pas ce qu'il lit, que faire ?", "La compréhension est une compétence qui se travaille. Nos enseignants utilisent des stratégies de questionnement, des inférences guidées et des résumés pour développer la compréhension fine."),
            ("La grammaire est difficile pour mon enfant, comment l'aider ?", "Nous rendons la grammaire concrète en manipulant des phrases : trier, classer, transformer. L'enfant comprend les règles en les expérimentant plutôt qu'en les récitant."),
        ],
    },
    "ce2": {
        "hero": "Le CE2 approfondit la maîtrise de la langue : l'orthographe devient un enjeu central, la grammaire se complexifie et la conjugaison s'étend à de nouveaux temps. C'est aussi l'année où l'enfant développe sa capacité à rédiger des textes plus longs et structurés.",
        "topics": [
            ("Orthographe", "check-circle", "Orthographe lexicale (mots courants) et grammaticale (accords, homophones)."),
            ("Conjugaison", "clock", "Imparfait, futur simple, passé composé, passé simple pour les verbes fréquents."),
            ("Lecture et compréhension", "book-open", "Lire des textes variés (récits, documentaires, poésie), stratégies de compréhension."),
            ("Rédaction", "pencil", "Écrire des textes de 5 à 10 lignes, organiser ses idées, respecter les consignes."),
        ],
        "method": "En CE2, nous insistons sur l'orthographe par des dictées progressives et des exercices de mémorisation visuelle. La rédaction est travaillée en lien avec la lecture : chaque texte lu inspire une production écrite.",
        "faq": [
            ("Mon enfant fait beaucoup de fautes d'orthographe, est-ce normal en CE2 ?", "L'orthographe s'acquiert progressivement. Nos enseignants identifient les erreurs récurrentes et proposent des stratégies ciblées : règles mnémotechniques, dictées préparées, exercices de discrimination."),
            ("Comment donner le goût de la lecture à mon enfant ?", "Nous proposons des textes variés et adaptés aux goûts de votre enfant. L'important est de trouver le type de livre qui l'accroche, qu'il s'agisse de BD, de romans d'aventure ou de documentaires."),
        ],
    },
    "cm1": {
        "hero": "Le CM1 marque l'entrée dans le cycle 3 en français : les textes se complexifient, l'analyse grammaticale s'approfondit et la rédaction exige plus de structure et de richesse. L'enfant apprend aussi à argumenter et à exprimer son avis sur une lecture.",
        "topics": [
            ("Grammaire avancée", "list", "Compléments du verbe et de phrase, types et formes de phrases, propositions."),
            ("Conjugaison", "clock", "Plus-que-parfait, conditionnel présent, verbes irréguliers fréquents."),
            ("Vocabulaire et lexique", "book-open", "Synonymes, antonymes, homonymes, familles de mots, sens propre et figuré."),
            ("Rédaction structurée", "pencil", "Écrire des textes de 15-20 lignes avec introduction, développement et conclusion."),
        ],
        "method": "En CM1, nous développons l'analyse grammaticale et la richesse du vocabulaire au service de la rédaction. Les séances alternent entre exercices de grammaire ciblés et ateliers d'écriture créative.",
        "faq": [
            ("La grammaire devient trop complexe pour mon enfant, que faire ?", "Nous reprenons les bases si nécessaire et construisons progressivement les nouvelles notions. Des exercices de manipulation de phrases rendent la grammaire concrète et logique."),
            ("Comment améliorer la rédaction de mon enfant ?", "Nous travaillons la planification (organiser ses idées avant d'écrire), l'enrichissement (vocabulaire, connecteurs) et la relecture (corrections autonomes). L'écriture régulière est la clé du progrès."),
        ],
    },
    "cm2": {
        "hero": "Le CM2 prépare l'entrée au collège en français : la maîtrise de la langue doit être solide pour aborder les exigences de la 6ème. L'enfant perfectionne sa grammaire, enrichit son vocabulaire et apprend à rédiger des textes variés et structurés.",
        "topics": [
            ("Analyse grammaticale complète", "list", "Nature et fonction des mots, propositions subordonnées, voix active et passive."),
            ("Orthographe grammaticale", "check-circle", "Accords complexes (participe passé, adjectifs), homophones grammaticaux."),
            ("Lecture littéraire", "book-open", "Lire des œuvres complètes, analyser des personnages, comprendre les intentions de l'auteur."),
            ("Préparation à la 6ème", "graduation-cap", "Rédaction argumentée, prise de notes, méthodes de travail du collège."),
        ],
        "method": "En CM2, nous préparons votre enfant au français du collège : lectures plus longues, rédactions plus exigeantes, analyse grammaticale complète. Nos séances développent l'autonomie et la confiance en soi.",
        "faq": [
            ("Mon enfant est-il prêt pour le français en 6ème ?", "Nous évaluons les compétences essentielles (lecture, écriture, grammaire) et comblons les lacunes éventuelles. Un enfant qui maîtrise les bases du CM2 est bien armé pour le collège."),
            ("La dictée est un cauchemar pour mon enfant, que faire ?", "Nous préparons les dictées en amont : étude des mots difficiles, rappel des règles, stratégies de relecture. Progressivement, l'enfant gagne en confiance et en autonomie."),
        ],
    },
    "6eme": {
        "hero": "La 6ème est la première année du collège en français : l'étude de la grammaire se formalise, la conjugaison s'approfondit et l'enfant découvre l'analyse de textes littéraires. La rédaction devient un exercice central avec des attendus plus élevés.",
        "topics": [
            ("Grammaire et analyse", "list", "Classes grammaticales, fonctions, phrases complexes, propositions."),
            ("Conjugaison", "clock", "Tous les temps de l'indicatif, subjonctif présent, impératif."),
            ("Lecture et analyse littéraire", "book-open", "Récits d'aventure, contes et mythes, poésie, initiation au théâtre."),
            ("Expression écrite", "pencil", "Raconter, décrire, dialoguer, répondre à des questions de compréhension."),
        ],
        "method": "En 6ème, nous aidons votre enfant à s'adapter aux exigences du collège en français. Les séances combinent étude de la langue (grammaire, conjugaison) et travail sur les textes (compréhension, rédaction).",
        "faq": [
            ("Mon enfant a du mal avec l'analyse grammaticale, comment l'aider ?", "L'analyse grammaticale demande méthode et entraînement. Nos enseignants enseignent une démarche systématique pour identifier la nature et la fonction des mots dans une phrase."),
            ("Comment améliorer les notes de rédaction de mon enfant ?", "Nous travaillons les critères d'évaluation du collège : respect du sujet, organisation du texte, richesse du vocabulaire, correction de la langue. Chaque rédaction est un entraînement ciblé."),
        ],
    },
    "5eme": {
        "hero": "La 5ème approfondit l'étude de la littérature et de la langue. Votre enfant découvre de nouveaux genres littéraires (récit de voyage, littérature médiévale), perfectionne sa grammaire et développe ses compétences argumentatives à l'écrit.",
        "topics": [
            ("Littérature", "book-open", "Récits de voyage, héros et héroïsme, littérature du Moyen Âge, poésie."),
            ("Grammaire avancée", "list", "Subordonnées relatives et conjonctives, voix active/passive, discours direct/indirect."),
            ("Vocabulaire thématique", "list", "Champs lexicaux, figures de style, étymologie, registres de langue."),
            ("Argumentation", "message-square", "Exprimer son avis, justifier, convaincre à l'oral et à l'écrit."),
        ],
        "method": "En 5ème, nous développons la sensibilité littéraire et les compétences d'analyse. Les séances alternent entre étude de textes, exercices de langue et ateliers d'écriture pour former un élève autonome et cultivé.",
        "faq": [
            ("Mon enfant ne comprend pas les textes littéraires, que faire ?", "La compréhension littéraire s'apprend. Nos enseignants guident votre enfant dans l'analyse : identifier les personnages, comprendre les enjeux, repérer les procédés d'écriture."),
            ("Comment améliorer l'expression écrite de mon enfant ?", "L'écriture régulière est la clé. Nos séances proposent des exercices variés (rédactions, réécritures, ateliers créatifs) avec des retours détaillés pour progresser."),
        ],
    },
    "4eme": {
        "hero": "La 4ème est une année clé en français : le programme littéraire s'enrichit (romantisme, fantastique, presse), l'argumentation prend de l'importance et la maîtrise de la langue doit être plus fine. C'est aussi une année de préparation au Brevet.",
        "topics": [
            ("Littérature", "book-open", "Le fantastique, la presse, l'amour en littérature, le réalisme."),
            ("Grammaire et orthographe", "check-circle", "Propositions subordonnées, accords complexes, concordance des temps."),
            ("Argumentation écrite", "message-square", "Rédiger une argumentation structurée, thèse, arguments, exemples."),
            ("Oral", "mic", "Exposés, débats, lecture expressive, prise de parole argumentée."),
        ],
        "method": "En 4ème, nous préparons le Brevet en travaillant les compétences clés : compréhension fine de textes, maîtrise de la langue, rédaction argumentée. Chaque séance développe à la fois les connaissances et la méthodologie.",
        "faq": [
            ("L'argumentation est difficile pour mon enfant, comment l'aider ?", "Nous enseignons une méthode claire : formuler une thèse, trouver des arguments, les illustrer par des exemples, conclure. Des exercices progressifs rendent ce type d'écriture accessible."),
            ("Comment préparer le Brevet de français dès la 4ème ?", "Les compétences travaillées en 4ème sont directement évaluées au Brevet. Nous anticipons la préparation en familiarisant l'élève avec les exercices types : compréhension, grammaire, rédaction."),
        ],
    },
    "3eme": {
        "hero": "La 3ème est l'année du Brevet de français. L'épreuve évalue la compréhension et les compétences linguistiques, la dictée, la grammaire et la rédaction. Notre accompagnement prépare votre enfant à chaque composante de l'épreuve.",
        "topics": [
            ("Compréhension de texte", "book-open", "Analyser un texte littéraire, identifier les procédés d'écriture, interpréter."),
            ("Grammaire et dictée", "check-circle", "Maîtrise des accords, syntaxe, ponctuation, dictée préparée."),
            ("Rédaction", "pencil", "Rédaction d'invention ou d'argumentation selon le sujet, méthodologie."),
            ("Préparation au Brevet", "award", "Annales corrigées, gestion du temps, méthodologie de l'épreuve."),
        ],
        "method": "En 3ème, chaque séance cible une compétence du Brevet. Nous proposons des entraînements sur annales, des dictées préparées, des exercices de grammaire ciblés et des ateliers de rédaction. L'objectif est la réussite sereine de l'épreuve.",
        "faq": [
            ("Comment bien préparer l'épreuve de français du Brevet ?", "Nous travaillons chaque partie de l'épreuve : compréhension de texte, questions de grammaire, dictée et rédaction. Des annales corrigées et chronométrées préparent votre enfant dans les conditions de l'examen."),
            ("La dictée du Brevet me fait peur, comment se préparer ?", "La dictée du Brevet évalue des règles de base bien identifiées. Nos enseignants proposent des dictées d'entraînement ciblant les pièges les plus fréquents, avec des méthodes de relecture efficaces."),
        ],
    },
    "seconde": {
        "hero": "La Seconde générale en français est une année de transition vers le lycée. Le programme est centré sur la littérature (roman, théâtre, poésie) et l'analyse de texte. L'écriture argumentative et le commentaire littéraire sont introduits.",
        "topics": [
            ("Le roman et le récit", "book-open", "Étude d'œuvres intégrales, analyse narratologique, personnages et point de vue."),
            ("Le théâtre", "drama", "Lire et analyser une pièce, mise en scène, double énonciation."),
            ("La poésie", "feather", "Versification, figures de style, analyse de poèmes."),
            ("Méthodologie", "list", "Introduction au commentaire composé, dissertation, contraction et essai."),
        ],
        "method": "En Seconde, nous aidons votre enfant à développer une lecture analytique des textes littéraires et à structurer ses rédactions selon les attendus du lycée. La méthodologie du commentaire est un axe central de notre accompagnement.",
        "faq": [
            ("Le commentaire de texte est nouveau et difficile, comment l'aborder ?", "Nous enseignons une méthode pas à pas : lire attentivement, repérer les procédés, construire un plan, rédiger. Avec de la pratique guidée, le commentaire devient un exercice maîtrisé."),
            ("Comment améliorer la culture littéraire de mon enfant ?", "Nous recommandons des lectures complémentaires adaptées à ses goûts et travaillons la contextualisation des œuvres. La culture littéraire se construit séance après séance."),
        ],
    },
    "premiere": {
        "hero": "La Première est l'année de l'épreuve anticipée de français au bac (EAF). L'épreuve écrite (commentaire ou dissertation) et l'oral (explication de texte et entretien) exigent une préparation rigoureuse. Notre accompagnement couvre les deux volets de l'épreuve.",
        "topics": [
            ("Commentaire composé", "book-open", "Méthodologie complète, analyse de textes littéraires, rédaction structurée."),
            ("Dissertation littéraire", "pencil", "Analyser un sujet, construire un plan, argumenter avec des références."),
            ("Oral de français", "mic", "Explication linéaire de texte, question de grammaire, entretien sur l'œuvre."),
            ("Œuvres au programme", "list", "Étude approfondie des 4 œuvres et parcours associés."),
        ],
        "method": "En Première, nous préparons intensivement les deux épreuves du bac de français. L'écrit est travaillé par des exercices de commentaire et de dissertation corrigés. L'oral est préparé par des entraînements réguliers avec simulation d'entretien.",
        "faq": [
            ("Comment bien préparer l'oral de français ?", "Nous préparons chaque texte du descriptif avec une explication linéaire structurée, la question de grammaire et l'entretien sur l'œuvre. Des simulations d'oral dans les conditions de l'examen complètent la préparation."),
            ("Mon enfant ne sait pas faire un commentaire de texte, que faire ?", "Le commentaire s'apprend avec méthode. Nous enseignons les étapes (observation, analyse, plan, rédaction) et les entraînons sur des textes variés jusqu'à ce que la méthode soit automatisée."),
        ],
    },
    "terminale": {
        "hero": "La Terminale en français n'a pas d'épreuve dédiée, mais les compétences rédactionnelles et analytiques restent essentielles pour la philosophie, le Grand Oral et les études supérieures. Nous accompagnons votre enfant pour perfectionner son expression écrite et orale.",
        "topics": [
            ("Expression écrite avancée", "pencil", "Dissertation, synthèse, argumentation pour la philosophie et les autres matières."),
            ("Grand Oral", "mic", "Préparation du sujet, structuration de l'exposé, entraînement à la prise de parole."),
            ("Compétences rédactionnelles", "file-text", "Style, clarté, rigueur : perfectionner l'écriture pour le supérieur."),
            ("Culture générale", "book-open", "Enrichir sa culture littéraire et philosophique, développer l'esprit critique."),
        ],
        "method": "En Terminale, nous perfectionnons les compétences écrites et orales de votre enfant. L'accompagnement est personnalisé selon les besoins : préparation du Grand Oral, renforcement pour la philosophie, préparation aux concours ou au supérieur.",
        "faq": [
            ("Le français est-il encore important en Terminale ?", "Absolument. La qualité de l'expression écrite et orale est évaluée dans toutes les matières et au Grand Oral. C'est aussi un atout déterminant pour les études supérieures et les concours."),
            ("Comment préparer le Grand Oral ?", "Nous aidons votre enfant à choisir et structurer son sujet, à développer son argumentation et à s'entraîner à la prise de parole. Des simulations d'oral dans les conditions de l'examen sont proposées."),
        ],
    },
}

ANGLAIS_LEVELS = {
    "cp": {
        "hero": "L'anglais au CP, c'est la découverte d'une nouvelle langue à travers le jeu, les chansons et les activités orales. Votre enfant se familiarise avec les sonorités de l'anglais, apprend ses premiers mots et développe une oreille attentive. Un contact précoce favorise un apprentissage naturel.",
        "topics": [
            ("Vocabulaire de base", "list", "Les couleurs, les nombres, les animaux, la famille, le corps humain."),
            ("Chansons et comptines", "music", "Apprendre par la musique, mémoriser du vocabulaire en chantant."),
            ("Compréhension orale", "ear", "Écouter et comprendre des consignes simples, des histoires courtes en anglais."),
            ("Premières interactions", "message-circle", "Se présenter, saluer, dire son âge, exprimer ses goûts."),
        ],
        "method": "Au CP, nous rendons l'anglais amusant et naturel. Les séances sont 100% orales avec des jeux, des chansons, des histoires et des interactions en anglais. L'enfant apprend sans s'en rendre compte.",
        "faq": [
            ("Mon enfant est-il trop jeune pour apprendre l'anglais ?", "Au contraire, le CP est un âge idéal. Le cerveau de l'enfant est particulièrement réceptif aux langues étrangères. Un contact régulier permet de développer une oreille et une prononciation excellentes."),
            ("Les séances sont-elles en anglais ou en français ?", "Nos enseignants alternent progressivement. Les consignes de base sont données en anglais avec un support visuel, et le français est utilisé pour les explications quand nécessaire."),
        ],
    },
    "ce1": {
        "hero": "L'anglais au CE1 poursuit la sensibilisation avec un vocabulaire plus riche et les premières structures de phrases. Votre enfant apprend à se présenter, à décrire son environnement et à comprendre des consignes simples en anglais.",
        "topics": [
            ("Vocabulaire étendu", "list", "La nourriture, les vêtements, la maison, le temps qu'il fait, l'école."),
            ("Structures de phrases", "message-circle", "I like / I don't like, I have / I haven't, I can / I can't."),
            ("Phonétique", "volume-2", "Distinguer les sons de l'anglais, accent tonique, rythme de la phrase."),
            ("Culture anglophone", "globe", "Découvrir le Royaume-Uni, les fêtes anglaises, la vie quotidienne."),
        ],
        "method": "En CE1, nous augmentons progressivement le temps d'exposition à l'anglais oral. Les séances restent ludiques avec des jeux de rôle, des activités interactives et des histoires en anglais simplifié.",
        "faq": [
            ("Mon enfant ne retient pas le vocabulaire anglais, que faire ?", "La répétition espacée et les associations visuelles sont nos meilleurs outils. Nos enseignants révisent le vocabulaire appris à chaque séance, dans des contextes variés et amusants."),
            ("Combien de séances par semaine faut-il ?", "Une à deux séances hebdomadaires suffisent au CE1 pour maintenir un contact régulier avec la langue. La régularité est plus importante que l'intensité à cet âge."),
        ],
    },
    "ce2": {
        "hero": "L'anglais au CE2 introduit les premières bases écrites : votre enfant commence à lire et écrire des mots et des phrases simples en anglais, tout en poursuivant le travail oral. Le vocabulaire s'enrichit et les structures grammaticales deviennent plus variées.",
        "topics": [
            ("Lecture et écriture", "book-open", "Lire et écrire des mots et phrases simples, correspondance son-graphie en anglais."),
            ("Grammaire de base", "list", "Pluriel, articles, adjectifs possessifs, there is/there are."),
            ("Dialogues", "message-circle", "Petits dialogues de la vie quotidienne : acheter, demander son chemin, commander."),
            ("Compréhension", "ear", "Comprendre des textes et des vidéos simples en anglais."),
        ],
        "method": "En CE2, nous introduisons progressivement l'écrit tout en maintenant la priorité sur l'oral. Les séances incluent des activités de lecture et d'écriture courtes et ciblées, intégrées dans des projets motivants.",
        "faq": [
            ("L'anglais écrit est très différent de l'oral, comment aider mon enfant ?", "La correspondance son-graphie en anglais est en effet complexe. Nous l'abordons progressivement en groupant les mots par similitudes phonétiques, ce qui facilite la mémorisation."),
            ("Mon enfant confond l'anglais et le français à l'écrit, est-ce normal ?", "Tout à fait normal au début. Le cerveau fait naturellement des transferts entre les langues. Nos enseignants corrigent ces interférences en douceur et les erreurs disparaissent progressivement."),
        ],
    },
    "cm1": {
        "hero": "L'anglais au CM1 développe les quatre compétences linguistiques : compréhension orale et écrite, expression orale et écrite. Votre enfant apprend à construire des phrases plus complexes, à raconter une histoire courte et à comprendre des textes simples.",
        "topics": [
            ("Grammaire", "list", "Présent simple et continu, past simple régulier, comparatifs et superlatifs."),
            ("Expression orale", "mic", "Raconter une histoire, décrire une image, donner son opinion."),
            ("Compréhension écrite", "book-open", "Lire des textes courts, repérer des informations, comprendre le sens global."),
            ("Projets culturels", "globe", "Découvrir les pays anglophones, traditions, géographie, personnalités."),
        ],
        "method": "En CM1, nous structurons l'apprentissage autour de projets qui motivent l'élève : créer un mini-journal, préparer une présentation, écrire un dialogue. La grammaire et le vocabulaire sont enseignés en contexte.",
        "faq": [
            ("Mon enfant est timide pour parler anglais, comment l'encourager ?", "Le format en ligne offre un cadre rassurant pour s'exprimer sans le regard des camarades. Nos enseignants valorisent chaque tentative et créent un climat de confiance pour libérer la parole."),
            ("Le niveau d'anglais attendu en CM1 est-il important ?", "Le CM1 pose des bases essentielles pour le collège. Un bon niveau en fin de primaire facilite grandement l'apprentissage en 6ème, où le rythme s'accélère."),
        ],
    },
    "cm2": {
        "hero": "L'anglais au CM2 prépare le passage au collège : votre enfant consolide ses bases grammaticales, enrichit son vocabulaire et développe son aisance orale. L'objectif est d'atteindre le niveau A1 du CECRL pour aborder la 6ème avec confiance.",
        "topics": [
            ("Grammaire", "list", "Past simple irrégulier, futur (will/going to), modaux (can, must)."),
            ("Vocabulaire thématique", "book-open", "Les médias, les nouvelles technologies, l'environnement, les métiers."),
            ("Production orale et écrite", "pencil", "Écrire un email, se présenter en continu, argumenter simplement."),
            ("Préparation à la 6ème", "graduation-cap", "Méthodes de travail du collège, autonomie, niveau A1 du CECRL."),
        ],
        "method": "En CM2, nous préparons votre enfant aux exigences de la 6ème en anglais. Les séances combinent consolidation des acquis et introduction progressive des attendus du collège : plus d'écrit, plus de grammaire explicite, plus d'autonomie.",
        "faq": [
            ("Comment préparer mon enfant à l'anglais en 6ème ?", "Nous nous assurons que le niveau A1 est atteint : se présenter, décrire son environnement, interagir simplement. Les bases grammaticales et le vocabulaire courant doivent être solides."),
            ("Mon enfant n'a pas eu beaucoup d'anglais en primaire, est-il trop tard ?", "Non. Nos enseignants reprennent les bases si nécessaire. Avec un travail régulier en CM2, votre enfant peut rattraper et aborder la 6ème sereinement."),
        ],
    },
    "6eme": {
        "hero": "La 6ème est la première année du collège en anglais. Le rythme s'accélère avec plus d'heures de cours, une grammaire plus structurée et des évaluations régulières. L'objectif est de consolider le niveau A1 et d'avancer vers le A2 du CECRL.",
        "topics": [
            ("Grammaire", "list", "Temps du présent, du passé et du futur, pronoms, adjectifs, prépositions."),
            ("Compréhension orale", "ear", "Comprendre des dialogues, des annonces, des extraits audio et vidéo."),
            ("Expression écrite", "pencil", "Rédiger des textes courts : emails, descriptions, petits récits."),
            ("Culture et civilisation", "globe", "Le monde anglophone, traditions, mode de vie, géographie."),
        ],
        "method": "En 6ème, nous aidons votre enfant à s'adapter au rythme du collège en anglais. Les séances combinent travail de la grammaire, enrichissement du vocabulaire et pratique des quatre compétences linguistiques.",
        "faq": [
            ("Mon enfant a du mal à comprendre l'anglais oral, comment l'aider ?", "L'écoute régulière est la clé. Nos enseignants proposent des exercices d'écoute adaptés au niveau de votre enfant et lui apprennent des stratégies de compréhension (repérer les mots-clés, deviner par le contexte)."),
            ("La grammaire anglaise est très différente du français, comment s'y retrouver ?", "Nos enseignants expliquent les différences de manière claire et systématique (ordre des mots, temps verbaux). Des exercices comparatifs français/anglais aident à fixer les structures."),
        ],
    },
    "5eme": {
        "hero": "La 5ème approfondit les compétences en anglais : la grammaire se complexifie, le vocabulaire s'enrichit et les activités de communication deviennent plus ambitieuses. L'objectif est de progresser vers le niveau A2 du CECRL.",
        "topics": [
            ("Grammaire avancée", "list", "Present perfect, comparatifs, superlatifs, if-clauses (type 1)."),
            ("Vocabulaire étendu", "book-open", "L'environnement, la santé, les médias, les voyages."),
            ("Expression orale", "mic", "Dialogues plus longs, présentations, description d'images."),
            ("Compréhension écrite", "book-open", "Textes variés : articles, lettres, extraits de romans simplifiés."),
        ],
        "method": "En 5ème, nous développons la capacité à communiquer en anglais dans des situations variées. Les séances sont interactives et privilégient la pratique : jeux de rôle, projets, discussions guidées.",
        "faq": [
            ("Le present perfect est très difficile, comment l'expliquer ?", "Le present perfect n'existe pas en français, ce qui le rend abstrait. Nos enseignants l'expliquent par des situations concrètes et des comparaisons avec le passé composé, en insistant sur la notion de lien avec le présent."),
            ("Comment aider mon enfant à progresser en anglais oral ?", "L'exposition régulière à l'anglais est essentielle. En plus de nos séances, nous recommandons de regarder des séries ou écouter des podcasts en anglais, adaptés au niveau de votre enfant."),
        ],
    },
    "4eme": {
        "hero": "La 4ème est une année charnière en anglais : le programme aborde des thèmes plus complexes, la grammaire s'affine et les compétences rédactionnelles sont davantage sollicitées. L'objectif est d'atteindre un bon niveau A2, socle pour le Brevet.",
        "topics": [
            ("Grammaire", "list", "Past continuous, present perfect + for/since, modaux (should, could, would)."),
            ("Expression écrite", "pencil", "Rédiger des textes structurés : narration, description, lettre, email formel."),
            ("Culture et débat", "message-square", "Débattre sur des sujets de société en anglais, exprimer son opinion."),
            ("Compréhension", "ear", "Comprendre des documents authentiques : articles, vidéos, podcasts."),
        ],
        "method": "En 4ème, nous insistons sur la production (orale et écrite) et la capacité à exprimer des idées nuancées en anglais. Les séances incluent des débats, des rédactions et des exercices d'écoute sur des documents authentiques.",
        "faq": [
            ("Comment préparer le Brevet d'anglais ?", "Le Brevet évalue le niveau A2 en anglais. Nous préparons votre enfant aux épreuves de compréhension orale et écrite, ainsi qu'à l'expression écrite, avec des exercices types et des annales."),
            ("Mon enfant a des lacunes depuis la 6ème, est-il trop tard ?", "Non. Nos enseignants identifient les lacunes et construisent un parcours de remise à niveau ciblé. L'anglais s'apprend à tout âge et les progrès peuvent être rapides avec un accompagnement adapté."),
        ],
    },
    "3eme": {
        "hero": "La 3ème est l'année du Brevet en anglais. L'épreuve évalue la compréhension orale, la compréhension écrite et l'expression écrite au niveau A2/B1. Notre accompagnement prépare votre enfant à chaque composante de l'épreuve.",
        "topics": [
            ("Compréhension orale", "ear", "Écouter et comprendre des documents variés, prendre des notes en anglais."),
            ("Compréhension écrite", "book-open", "Analyser des textes authentiques, repérer les informations, inférer le sens."),
            ("Expression écrite", "pencil", "Rédiger des textes structurés de 100-120 mots, répondre à des questions."),
            ("Préparation au Brevet", "award", "Annales corrigées, méthodologie, gestion du temps."),
        ],
        "method": "En 3ème, notre priorité est la préparation au Brevet. Nous travaillons chaque compétence évaluée avec des exercices types et des annales. Les séances incluent aussi la conversation pour maintenir l'aisance orale.",
        "faq": [
            ("Comment bien préparer l'épreuve d'anglais du Brevet ?", "Nous entraînons votre enfant sur les trois compétences évaluées : compréhension orale, compréhension écrite et expression écrite. Des annales chronométrées et des stratégies de réponse complètent la préparation."),
            ("Mon enfant a un faible niveau en anglais, peut-il réussir le Brevet ?", "Avec un travail régulier et ciblé, oui. Nos enseignants identifient les priorités et concentrent les séances sur les compétences les plus rentables pour l'examen."),
        ],
    },
    "seconde": {
        "hero": "La Seconde en anglais est une année de transition vers le lycée. Le programme est ambitieux : étude de documents authentiques, expression orale et écrite développée, grammaire fine. L'objectif est d'atteindre le niveau B1 du CECRL.",
        "topics": [
            ("Grammaire avancée", "list", "Temps complexes, conditionnel, passif, discours indirect."),
            ("Expression orale", "mic", "Débats, présentations, prise de parole en continu."),
            ("Expression écrite", "pencil", "Essai, commentaire, lettre formelle, compte-rendu."),
            ("Compréhension de documents", "book-open", "Articles de presse, extraits littéraires, vidéos, podcasts."),
        ],
        "method": "En Seconde, nous augmentons significativement le temps de pratique en anglais. Les séances sont menées autant que possible en anglais, avec des activités de compréhension et de production ambitieuses.",
        "faq": [
            ("Comment progresser rapidement en anglais au lycée ?", "L'immersion est la clé : séances en anglais, lectures, podcasts, séries en VO. Nos enseignants poussent votre enfant à s'exprimer en anglais et corrigent en temps réel pour un progrès rapide."),
            ("Faut-il prendre la spécialité anglais en Première ?", "La spécialité LLCE (Langue, Littérature et Civilisation Étrangères) est idéale pour les élèves passionnés par l'anglais et la culture anglophone. Un bon niveau B1 en fin de Seconde est recommandé."),
        ],
    },
    "premiere": {
        "hero": "La Première en anglais (tronc commun ou spécialité LLCE) approfondit les compétences linguistiques et culturelles. L'objectif est d'atteindre le niveau B1+/B2 et de préparer les épreuves du bac, notamment le Grand Oral pour ceux qui choisissent l'anglais.",
        "topics": [
            ("Expression orale avancée", "mic", "Argumentation, débat, prise de parole structurée, Grand Oral."),
            ("Expression écrite", "pencil", "Essai argumenté, commentaire de document, synthèse."),
            ("Littérature et civilisation", "book-open", "Étude d'œuvres et de documents authentiques en lien avec les axes du programme."),
            ("Grammaire perfectionnée", "list", "Structures complexes, nuances modales, cohérence textuelle."),
        ],
        "method": "En Première, nous visons l'aisance et la nuance en anglais. Les séances sont intégralement en anglais quand le niveau le permet. Nous travaillons la compréhension fine et l'expression de haut niveau.",
        "faq": [
            ("Comment préparer le Grand Oral en anglais ?", "Nos enseignants accompagnent votre enfant dans le choix du sujet, la structuration de l'exposé et l'entraînement à la prise de parole. Des simulations d'oral sont proposées régulièrement."),
            ("La spécialité LLCE est-elle difficile ?", "La spécialité demande un bon niveau en anglais et un intérêt pour la littérature et la civilisation. Nos enseignants accompagnent les élèves dans l'analyse de textes littéraires et la rédaction d'essais en anglais."),
        ],
    },
    "terminale": {
        "hero": "La Terminale en anglais prépare les épreuves du bac et le niveau B2 du CECRL. Les compétences de compréhension et d'expression sont évaluées à un niveau élevé. Pour les élèves en spécialité LLCE, l'épreuve finale est exigeante.",
        "topics": [
            ("Préparation aux épreuves", "award", "Compréhension orale et écrite, expression orale et écrite, méthodologie."),
            ("Expression de haut niveau", "trending-up", "Argumentation nuancée, analyse critique, registre formel."),
            ("Compréhension avancée", "ear", "Documents authentiques complexes : conférences, débats, articles de fond."),
            ("Grand Oral / Spécialité", "mic", "Préparation spécifique selon le parcours de l'élève."),
        ],
        "method": "En Terminale, notre accompagnement est centré sur la performance aux épreuves du bac. Les séances simulent les conditions d'examen et ciblent les points d'amélioration pour maximiser les notes.",
        "faq": [
            ("Comment obtenir une bonne note en anglais au bac ?", "Nous travaillons chaque compétence évaluée avec des exercices types et des critères d'évaluation précis. La régularité de la pratique et la maîtrise de la méthodologie sont les clés de la réussite."),
            ("Mon enfant vise des études à l'international, comment le préparer ?", "Au-delà du bac, nous préparons votre enfant aux certifications internationales (TOEFL, IELTS, Cambridge) et aux exigences linguistiques des formations internationales."),
        ],
    },
}

AIDE_DEVOIRS_LEVELS = {
    "cp": {
        "hero": "L'aide aux devoirs au CP accompagne votre enfant dans ses premiers apprentissages fondamentaux : lecture, écriture et mathématiques. Nos enseignants l'aident à comprendre ses leçons, à faire ses exercices et à développer de bonnes habitudes de travail dès le début de sa scolarité.",
        "topics": [
            ("Lecture et écriture", "book-open", "Aide à la lecture syllabique, formation des lettres, copie et premiers écrits."),
            ("Mathématiques", "calculator", "Aide au dénombrement, aux premières additions et soustractions, aux formes géométriques."),
            ("Organisation du travail", "list", "Apprendre à organiser son cartable, à suivre les consignes, à travailler seul."),
            ("Confiance en soi", "heart", "Encourager, valoriser les réussites, dédramatiser les erreurs."),
        ],
        "method": "En CP, nos séances d'aide aux devoirs sont courtes et structurées (30-45 min). Nous commençons par les exercices les plus importants, alternons entre lecture et mathématiques, et terminons toujours par une activité valorisante.",
        "faq": [
            ("Mon enfant ne veut pas faire ses devoirs, comment le motiver ?", "Nos enseignants transforment le moment des devoirs en un temps agréable et structuré. Des récompenses symboliques, des encouragements et une ambiance positive aident votre enfant à y prendre goût."),
            ("Les devoirs sont-ils importants dès le CP ?", "Les devoirs au CP sont courts mais importants pour consolider les apprentissages de la journée. Notre aide vise à rendre ce moment efficace et serein, sans pression ni conflit."),
        ],
    },
    "ce1": {
        "hero": "L'aide aux devoirs au CE1 soutient votre enfant dans la consolidation de la lecture, l'apprentissage de la conjugaison et les premières multiplications. Nos enseignants l'accompagnent pour comprendre ses leçons et réussir ses exercices avec confiance.",
        "topics": [
            ("Français", "book-open", "Aide à la lecture fluide, grammaire, conjugaison, orthographe."),
            ("Mathématiques", "calculator", "Tables de multiplication, résolution de problèmes, géométrie."),
            ("Méthodologie", "list", "Apprendre à réviser une leçon, à préparer un contrôle, à s'organiser."),
            ("Toutes matières", "layers", "Découverte du monde, questionner le monde, enseignement moral et civique."),
        ],
        "method": "En CE1, nous structurons le temps des devoirs pour le rendre efficace : relecture de la leçon, exercices écrits, récitation ou mémorisation. L'enseignant adapte son aide au rythme et aux besoins de votre enfant.",
        "faq": [
            ("Mon enfant met trop de temps pour faire ses devoirs, que faire ?", "Nos enseignants apprennent à votre enfant à être efficace : lire les consignes, commencer par le plus difficile, se concentrer. En quelques séances, le temps des devoirs se réduit naturellement."),
            ("L'aide aux devoirs, est-ce que ça ne rend pas l'enfant dépendant ?", "Notre objectif est l'autonomie. Nous guidons votre enfant vers des stratégies qu'il pourra appliquer seul. Progressivement, il prend confiance et a de moins en moins besoin d'aide."),
        ],
    },
    "ce2": {
        "hero": "L'aide aux devoirs au CE2 accompagne votre enfant à un moment charnière : les apprentissages se complexifient et les devoirs deviennent plus conséquents. Nos enseignants l'aident à comprendre ses leçons, à réviser efficacement et à gagner en autonomie.",
        "topics": [
            ("Français", "book-open", "Orthographe, grammaire, conjugaison, compréhension de lecture, rédaction."),
            ("Mathématiques", "calculator", "Les quatre opérations, résolution de problèmes, mesures, géométrie."),
            ("Révision de leçons", "list", "Techniques de mémorisation, fiches de révision, préparation aux évaluations."),
            ("Sciences et histoire-géo", "globe", "Aide à la compréhension des leçons de sciences et d'histoire-géographie."),
        ],
        "method": "En CE2, nos enseignants développent l'autonomie de votre enfant face aux devoirs. Nous lui apprenons à organiser son travail, à identifier ce qu'il a compris et ce qui nécessite de l'aide, et à s'auto-corriger.",
        "faq": [
            ("Mon enfant a des difficultés dans plusieurs matières, comment prioriser ?", "Nos enseignants identifient les priorités en fonction du programme et des évaluations à venir. L'aide est ciblée sur les matières les plus urgentes tout en maintenant un suivi global."),
            ("Combien de séances par semaine sont recommandées ?", "En CE2, 2 à 3 séances hebdomadaires permettent un suivi régulier sans surcharger l'enfant. La fréquence s'adapte aux besoins et au calendrier scolaire."),
        ],
    },
    "cm1": {
        "hero": "L'aide aux devoirs au CM1 soutient votre enfant dans une année exigeante : les fractions, la grammaire avancée et les premières leçons d'histoire structurées demandent un travail régulier. Nos enseignants l'aident à comprendre, mémoriser et appliquer.",
        "topics": [
            ("Français", "book-open", "Analyse grammaticale, conjugaison avancée, rédaction, vocabulaire."),
            ("Mathématiques", "calculator", "Fractions, nombres décimaux, géométrie, résolution de problèmes."),
            ("Histoire-Géographie", "globe", "Comprendre et mémoriser les leçons, préparer les évaluations."),
            ("Méthodologie avancée", "list", "Prise de notes, organisation du travail, fiches de révision, gestion du temps."),
        ],
        "method": "En CM1, nous apprenons à votre enfant à travailler de manière autonome et efficace. Les séances combinent aide aux devoirs du jour et travail de fond sur les notions fragiles. Nous préparons aussi les évaluations en amont.",
        "faq": [
            ("Les devoirs deviennent trop lourds pour mon enfant, que faire ?", "Nos enseignants aident votre enfant à prioriser et à s'organiser. Nous lui apprenons à identifier les tâches urgentes, à planifier son travail et à éviter la procrastination."),
            ("L'aide aux devoirs peut-elle remplacer le soutien dans une matière ?", "L'aide aux devoirs est un suivi global et quotidien. Si des lacunes profondes existent dans une matière, un soutien spécifique complémentaire peut être recommandé."),
        ],
    },
    "cm2": {
        "hero": "L'aide aux devoirs au CM2 prépare votre enfant à l'entrée au collège. Les devoirs sont plus conséquents et exigent davantage d'autonomie. Nos enseignants l'aident à consolider ses acquis, à développer ses méthodes de travail et à aborder la 6ème sereinement.",
        "topics": [
            ("Français", "book-open", "Maîtrise de la langue, lecture littéraire, rédaction structurée."),
            ("Mathématiques", "calculator", "Opérations sur les décimaux, fractions, aires, volumes, proportionnalité."),
            ("Sciences et technologie", "flask-conical", "Comprendre les leçons de sciences, préparer les exposés."),
            ("Préparation au collège", "graduation-cap", "Autonomie, organisation du cartable, prise de notes, gestion du temps."),
        ],
        "method": "En CM2, nous visons l'autonomie. Votre enfant apprend à planifier ses devoirs, à réviser sans aide, à préparer ses affaires et à gérer son temps. C'est la meilleure préparation pour le collège.",
        "faq": [
            ("Comment préparer mon enfant aux devoirs du collège ?", "Le collège demande plus d'autonomie et d'organisation. Nos séances de CM2 développent ces compétences : planifier la semaine, anticiper les évaluations, travailler en plusieurs fois."),
            ("Mon enfant est stressé par l'arrivée au collège, que faire ?", "Nos enseignants rassurent et préparent concrètement. Un enfant qui se sent prêt scolairement aborde le collège avec confiance. Nous travaillons aussi la gestion du stress si nécessaire."),
        ],
    },
    "6eme": {
        "hero": "L'aide aux devoirs en 6ème accompagne la transition vers le collège. Les devoirs viennent de plusieurs professeurs, les matières se multiplient et l'organisation devient cruciale. Nos enseignants aident votre enfant à s'adapter à ce nouveau rythme.",
        "topics": [
            ("Organisation du travail", "list", "Utiliser l'agenda, planifier les devoirs, anticiper les évaluations."),
            ("Français et mathématiques", "book-open", "Aide ciblée dans les deux matières fondamentales."),
            ("Nouvelles matières", "globe", "Histoire-géographie, SVT, technologie : comprendre et mémoriser les leçons."),
            ("Méthodologie du collège", "graduation-cap", "Prise de notes, fiches de révision, techniques de mémorisation."),
        ],
        "method": "En 6ème, notre aide aux devoirs est un véritable coaching scolaire. Nous aidons votre enfant à s'organiser, à prioriser ses devoirs et à développer les méthodes de travail indispensables au collège.",
        "faq": [
            ("Mon enfant est débordé par les devoirs en 6ème, que faire ?", "L'adaptation au collège prend du temps. Nos enseignants aident votre enfant à hiérarchiser les tâches, à utiliser son agenda efficacement et à travailler de manière plus autonome."),
            ("L'aide aux devoirs est-elle adaptée au rythme du collège ?", "Oui. Nos séances s'adaptent à l'emploi du temps et aux devoirs du jour. L'enseignant est flexible et peut aider dans plusieurs matières selon les besoins de la semaine."),
        ],
    },
    "5eme": {
        "hero": "L'aide aux devoirs en 5ème soutient votre enfant face à des programmes plus exigeants. Les mathématiques s'abstraient, le français demande plus d'analyse et les langues vivantes progressent. Nos enseignants l'aident à rester organisé et performant.",
        "topics": [
            ("Mathématiques", "calculator", "Nombres relatifs, calcul littéral, statistiques, géométrie."),
            ("Français", "book-open", "Littérature, grammaire avancée, argumentation, vocabulaire."),
            ("Langues vivantes", "globe", "Aide en anglais et en LV2 (espagnol, allemand)."),
            ("Organisation et autonomie", "list", "Planification, révision, gestion du temps, préparation aux contrôles."),
        ],
        "method": "En 5ème, nous renforçons l'autonomie tout en assurant un suivi régulier. Les séances couvrent les devoirs du jour et incluent du travail de fond sur les matières où des lacunes apparaissent.",
        "faq": [
            ("Mon enfant a baissé en 5ème, est-ce normal ?", "La 5ème est souvent perçue comme une année de « creux ». Le programme se complexifie et la motivation peut baisser. Un accompagnement régulier permet de maintenir le cap et d'éviter l'accumulation de lacunes."),
            ("Peut-on aider dans toutes les matières ?", "Nos enseignants sont polyvalents et peuvent aider dans les matières principales. Pour des besoins très spécifiques (musique, arts), un accompagnement dédié peut être recommandé."),
        ],
    },
    "4eme": {
        "hero": "L'aide aux devoirs en 4ème accompagne votre enfant dans une année dense et exigeante. Le programme s'intensifie dans toutes les matières et les évaluations sont plus nombreuses. Nos enseignants l'aident à rester organisé et à préparer le Brevet.",
        "topics": [
            ("Mathématiques", "calculator", "Théorème de Pythagore, équations, puissances, transformations."),
            ("Français", "book-open", "Littérature, argumentation, grammaire avancée, préparation au Brevet."),
            ("Sciences", "flask-conical", "Physique-chimie, SVT, technologie : comprendre et réviser."),
            ("Préparation aux évaluations", "award", "Méthodologie de révision, fiches de synthèse, planning."),
        ],
        "method": "En 4ème, nos séances aident votre enfant à gérer la charge de travail croissante. Nous travaillons la méthodologie de révision et la préparation aux évaluations, tout en aidant aux devoirs quotidiens.",
        "faq": [
            ("Comment aider mon enfant à gérer le stress des évaluations ?", "Nos enseignants apprennent des techniques de gestion du stress : anticiper les révisions, faire des fiches, s'entraîner sur des sujets types. Un enfant bien préparé est un enfant serein."),
            ("L'aide aux devoirs prépare-t-elle au Brevet ?", "Oui. En 4ème, nous commençons à familiariser votre enfant avec les attendus du Brevet et nous consolidons les compétences évaluées. C'est un investissement pour l'année de 3ème."),
        ],
    },
    "3eme": {
        "hero": "L'aide aux devoirs en 3ème est un accompagnement global pour l'année du Brevet. Nos enseignants aident votre enfant à gérer les devoirs quotidiens tout en préparant méthodiquement le Brevet dans toutes les matières.",
        "topics": [
            ("Préparation au Brevet", "award", "Révision méthodique de toutes les matières, annales, planning de révision."),
            ("Français et mathématiques", "book-open", "Aide renforcée dans les deux matières principales du Brevet."),
            ("Sciences", "flask-conical", "Physique-chimie, SVT, technologie : préparation à l'épreuve de sciences."),
            ("Orientation", "compass", "Aide à la réflexion sur l'orientation, préparation du dossier de vœux."),
        ],
        "method": "En 3ème, notre aide aux devoirs devient un véritable coaching de préparation au Brevet. Nous combinons aide quotidienne et séances de révision thématiques. Un planning de révision personnalisé est élaboré pour les semaines précédant les épreuves.",
        "faq": [
            ("L'aide aux devoirs suffit-elle pour préparer le Brevet ?", "Pour les élèves sans lacunes profondes, oui. L'aide aux devoirs régulière permet de consolider les acquis au fil de l'année. Si des lacunes importantes existent, un soutien matière par matière peut être recommandé en complément."),
            ("Comment organiser les révisions du Brevet ?", "Nos enseignants élaborent un planning de révision personnalisé couvrant toutes les matières. Les séances alternent entre révisions ciblées et entraînements sur annales chronométrés."),
        ],
    },
}


def get_level_data(subject_slug, level_slug):
    """Return topic/FAQ/hero/method data for a given subject and level."""
    if subject_slug == "physique-chimie" and level_slug in PC_LEVELS:
        d = PC_LEVELS[level_slug]
        return {
            "hero": d.get("hero", ""),
            "topics": d.get("topics", []),
            "method": d.get("method", ""),
            "faq": d.get("faq", []),
        }
    lookup = {
        "mathematiques": MATHS_LEVELS,
        "francais": FRANCAIS_LEVELS,
        "anglais": ANGLAIS_LEVELS,
        "aide-aux-devoirs": AIDE_DEVOIRS_LEVELS,
    }
    lvls = lookup.get(subject_slug, {})
    d = lvls.get(level_slug, {})
    return {
        "hero": d.get("hero", ""),
        "topics": d.get("topics", []),
        "method": d.get("method", ""),
        "faq": d.get("faq", []),
    }


# ============================================================
# HTML GENERATORS
# ============================================================

# ------------------------------------------------------------------
# A) Ortho / Psycho Niveau 3 - City Hub
# ------------------------------------------------------------------

def generate_ortho_psycho_n3(category, pages_dict, city, base):
    """Generate a city hub page for orthophonie or psychologie."""
    prefix = "../../"
    cslug = city_slug(city)
    cdata = CITY_DATA[city]

    if category == "orthophonie":
        practitioner = "orthophoniste"
        practitioner_label = "Orthophoniste"
        cat_label = "Orthophonie"
    else:
        practitioner = "psychologue"
        practitioner_label = "Psychologue"
        cat_label = "Psychologie"

    title = practitioner_label + " enfant à " + city + " en ligne"
    meta_desc = (
        practitioner_label + " pour enfant à " + city + " en ligne. "
        "Consultation sous 48h avec un " + practitioner + " diplômé. "
        "Prise en charge rapide, 100% en visio depuis " + city + "."
    )

    out_dir = os.path.join(base, category, "villes")
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, cslug + ".html")

    html = ""
    # 1. Head
    html += get_head(title, meta_desc, include_faq_css=False)
    # 2. Navbar
    html += get_navbar(prefix)
    # 3. Main
    html += '    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">\n'
    # 4. Breadcrumb
    html += get_breadcrumb([
        ("Accueil", prefix + "index.html"),
        (cat_label, prefix + category + "/"),
        (city, None),
    ])

    # 5. Hero section
    wait_text = cdata["wait_text"].format(practitioner=practitioner)
    html += (
        '    <section class="py-16">\n'
        '        <div class="text-center max-w-3xl mx-auto">\n'
        '            <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6">\n'
        '                ' + practitioner_label + ' enfant à <span class="text-primary">' + city + '</span> - Consultation en ligne\n'
        '            </h1>\n'
        '            <p class="text-lg text-gray-600 leading-relaxed mb-8">' + wait_text + '</p>\n'
        '            <div class="flex flex-col sm:flex-row justify-center gap-4 mb-8">\n'
        '                <a href="' + prefix + 'contact.html" class="bg-primary text-white px-8 py-4 rounded-full font-bold hover:bg-primaryHover transition text-lg shadow-lg inline-flex items-center justify-center gap-2">\n'
        '                    <i data-lucide="calendar" class="w-5 h-5"></i> Prendre rendez-vous\n'
        '                </a>\n'
        '                <a href="#specialites" class="border-2 border-gray-200 text-gray-700 px-8 py-4 rounded-full font-bold hover:border-primary hover:text-primary transition text-lg inline-flex items-center justify-center gap-2">\n'
        '                    Voir nos spécialités\n'
        '                </a>\n'
        '            </div>\n'
        '            <div class="flex flex-wrap justify-center gap-4">\n'
        '                <span class="bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-1.5"><i data-lucide="clock" class="w-4 h-4"></i> Prise en charge rapide</span>\n'
        '                <span class="bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-1.5"><i data-lucide="monitor" class="w-4 h-4"></i> 100% en ligne</span>\n'
        '                <span class="bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-1.5"><i data-lucide="map-pin" class="w-4 h-4"></i> ' + city + ' et environs</span>\n'
        '            </div>\n'
        '        </div>\n'
        '    </section>\n'
    )

    # 6. Pourquoi consulter en ligne depuis {City}
    transport_text = cdata["transport_text"]
    html += (
        '    <section class="py-16 bg-white rounded-3xl mb-16">\n'
        '        <div class="max-w-6xl mx-auto px-6">\n'
        '            <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Pourquoi consulter en ligne depuis ' + city + ' ?</h2>\n'
        '            <div class="grid md:grid-cols-3 gap-8">\n'
        '                <div class="bg-light rounded-2xl p-8 text-center">\n'
        '                    <div class="w-14 h-14 bg-red-100 text-red-600 rounded-2xl flex items-center justify-center mx-auto mb-4"><i data-lucide="clock" class="w-7 h-7"></i></div>\n'
        '                    <h3 class="text-xl font-bold text-gray-900 mb-2">Pas d\'attente</h3>\n'
        '                    <p class="text-gray-600 text-sm">' + wait_text + '</p>\n'
        '                </div>\n'
        '                <div class="bg-light rounded-2xl p-8 text-center">\n'
        '                    <div class="w-14 h-14 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4"><i data-lucide="home" class="w-7 h-7"></i></div>\n'
        '                    <h3 class="text-xl font-bold text-gray-900 mb-2">Depuis chez vous</h3>\n'
        '                    <p class="text-gray-600 text-sm">' + transport_text + '</p>\n'
        '                </div>\n'
        '                <div class="bg-light rounded-2xl p-8 text-center">\n'
        '                    <div class="w-14 h-14 bg-purple-100 text-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4"><i data-lucide="award" class="w-7 h-7"></i></div>\n'
        '                    <h3 class="text-xl font-bold text-gray-900 mb-2">Spécialistes diplômés</h3>\n'
        '                    <p class="text-gray-600 text-sm">Tous nos ' + practitioner + 's sont diplômés d\'État et formés aux dernières avancées dans leur domaine. Vous bénéficiez d\'un suivi de qualité.</p>\n'
        '                </div>\n'
        '            </div>\n'
        '        </div>\n'
        '    </section>\n'
    )

    # 7. Grille des spécialités
    html += (
        '    <section id="specialites" class="py-16">\n'
        '        <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Nos spécialités à ' + city + '</h2>\n'
        '        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">\n'
    )
    for slug, data in pages_dict.items():
        dname = display_name(slug)
        short_desc = data.get("meta_desc", "")[:120]
        if len(data.get("meta_desc", "")) > 120:
            short_desc += "..."
        link = slug + "-" + cslug + ".html"
        html += (
            '            <a href="' + link + '" class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-primary/30 transition group">\n'
            '                <h3 class="text-lg font-bold text-gray-900 group-hover:text-primary transition mb-2">' + dname + '</h3>\n'
            '                <p class="text-gray-600 text-sm mb-3">' + short_desc + '</p>\n'
            '                <span class="text-primary font-semibold text-sm flex items-center gap-1">En savoir plus <i data-lucide="arrow-right" class="w-4 h-4"></i></span>\n'
            '            </a>\n'
        )
    html += (
        '        </div>\n'
        '    </section>\n'
    )

    html += '    </main>\n'

    # 8. About, CTA, Footer, JS
    html += get_about_section(practitioner, prefix)
    html += get_cta_section(
        "Prenez rendez-vous à " + city,
        "Nos " + practitioner + "s diplômés sont disponibles sous 48h pour accompagner votre enfant depuis " + city + ".",
    )
    html += get_footer(prefix)
    html += get_js(include_faq=False)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath


# ------------------------------------------------------------------
# B) Ortho / Psycho Niveau 4 - Trouble + City
# ------------------------------------------------------------------

def generate_ortho_psycho_n4(category, slug, data, city, base):
    """Generate a trouble+city page for orthophonie or psychologie."""
    prefix = "../../"
    cslug = city_slug(city)
    cdata = CITY_DATA[city]
    dname = display_name(slug)

    if category == "orthophonie":
        practitioner = "orthophoniste"
        practitioner_label = "Orthophoniste"
        cat_label = "Orthophonie"
    else:
        practitioner = "psychologue"
        practitioner_label = "Psychologue"
        cat_label = "Psychologie"

    title = practitioner_label + " " + dname + " à " + city + " en ligne"
    meta_desc = (
        practitioner_label + " spécialisé en " + dname.lower() + " pour enfant à " + city
        + ". Consultation en ligne sous 48h avec un " + practitioner
        + " diplômé. Accompagnement personnalisé depuis " + city + "."
    )

    out_dir = os.path.join(base, category, "villes")
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, slug + "-" + cslug + ".html")

    html = ""
    # 1. Head
    html += get_head(title, meta_desc)
    # 2. Navbar
    html += get_navbar(prefix)
    # 3. Main
    html += '    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">\n'
    # 4. Breadcrumb
    html += get_breadcrumb([
        ("Accueil", prefix + "index.html"),
        (cat_label, prefix + category + "/"),
        (dname, prefix + category + "/" + slug + ".html"),
        (city, None),
    ])

    # 5. Hero
    hero_desc = data.get("hero_desc", "")
    wait_text = cdata["wait_text"].format(practitioner=practitioner)
    combined_desc = hero_desc + " " + wait_text
    html += (
        '    <section class="py-16">\n'
        '        <div class="text-center max-w-3xl mx-auto">\n'
        '            <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6">\n'
        '                ' + practitioner_label + ' <span class="text-primary">' + dname + '</span> à ' + city + ' en ligne\n'
        '            </h1>\n'
        '            <p class="text-lg text-gray-600 leading-relaxed mb-8">' + combined_desc + '</p>\n'
        '            <div class="flex flex-col sm:flex-row justify-center gap-4 mb-8">\n'
        '                <a href="' + prefix + 'contact.html" class="bg-primary text-white px-8 py-4 rounded-full font-bold hover:bg-primaryHover transition text-lg shadow-lg inline-flex items-center justify-center gap-2">\n'
        '                    <i data-lucide="calendar" class="w-5 h-5"></i> Prendre rendez-vous\n'
        '                </a>\n'
        '                <a href="' + prefix + category + '/' + slug + '.html" class="border-2 border-gray-200 text-gray-700 px-8 py-4 rounded-full font-bold hover:border-primary hover:text-primary transition text-lg inline-flex items-center justify-center gap-2">\n'
        '                    En savoir plus sur ' + dname.lower() + '\n'
        '                </a>\n'
        '            </div>\n'
        '            <div class="flex flex-wrap justify-center gap-4">\n'
        '                <span class="bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-1.5"><i data-lucide="clock" class="w-4 h-4"></i> Sous 48h</span>\n'
        '                <span class="bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-1.5"><i data-lucide="monitor" class="w-4 h-4"></i> 100% en ligne</span>\n'
        '                <span class="bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-1.5"><i data-lucide="map-pin" class="w-4 h-4"></i> ' + city + '</span>\n'
        '            </div>\n'
        '        </div>\n'
        '    </section>\n'
    )

    # 6. Symptoms section (from parent N2 data)
    symptoms_title = data.get("symptoms_title", "")
    symptoms_intro = data.get("symptoms_intro", "")
    symptoms = data.get("symptoms", [])
    approach_title = data.get("approach_title", "")
    approach_desc = data.get("approach_desc", "")

    if symptoms:
        color_map = {"red": "red", "orange": "orange", "purple": "purple"}
        html += (
            '    <section class="py-16">\n'
            '        <div class="max-w-6xl mx-auto">\n'
            '            <div class="grid md:grid-cols-2 gap-12">\n'
            '                <div>\n'
            '                    <h2 class="text-3xl font-bold text-gray-900 mb-4">' + symptoms_title + '</h2>\n'
            '                    <p class="text-gray-600 leading-relaxed mb-8">' + symptoms_intro + '</p>\n'
            '                    <div class="space-y-6">\n'
        )
        for s in symptoms:
            c = color_map.get(s.get("color", "red"), "red")
            html += (
                '                        <div class="flex items-start gap-4">\n'
                '                            <div class="w-12 h-12 bg-' + c + '-100 text-' + c + '-600 rounded-xl flex items-center justify-center shrink-0"><i data-lucide="' + s["icon"] + '" class="w-6 h-6"></i></div>\n'
                '                            <div>\n'
                '                                <h3 class="font-bold text-gray-900 mb-1">' + s["title"] + '</h3>\n'
                '                                <p class="text-gray-600 text-sm">' + s["desc"] + '</p>\n'
                '                            </div>\n'
                '                        </div>\n'
            )
        html += (
            '                    </div>\n'
            '                </div>\n'
            '                <div class="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">\n'
            '                    <h3 class="text-xl font-bold text-gray-900 mb-4">' + approach_title + '</h3>\n'
            '                    <p class="text-gray-600 leading-relaxed">' + approach_desc + '</p>\n'
            '                </div>\n'
            '            </div>\n'
            '        </div>\n'
            '    </section>\n'
        )

    # 7. Pourquoi consulter depuis {City}
    transport_text = cdata["transport_text"]
    html += (
        '    <section class="py-16 bg-white rounded-3xl mb-16">\n'
        '        <div class="max-w-6xl mx-auto px-6">\n'
        '            <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Pourquoi consulter depuis ' + city + ' ?</h2>\n'
        '            <div class="grid md:grid-cols-3 gap-8">\n'
        '                <div class="bg-light rounded-2xl p-8 text-center">\n'
        '                    <div class="w-14 h-14 bg-red-100 text-red-600 rounded-2xl flex items-center justify-center mx-auto mb-4"><i data-lucide="clock" class="w-7 h-7"></i></div>\n'
        '                    <h3 class="text-xl font-bold text-gray-900 mb-2">Pas d\'attente</h3>\n'
        '                    <p class="text-gray-600 text-sm">' + wait_text + '</p>\n'
        '                </div>\n'
        '                <div class="bg-light rounded-2xl p-8 text-center">\n'
        '                    <div class="w-14 h-14 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4"><i data-lucide="home" class="w-7 h-7"></i></div>\n'
        '                    <h3 class="text-xl font-bold text-gray-900 mb-2">Depuis chez vous</h3>\n'
        '                    <p class="text-gray-600 text-sm">' + transport_text + '</p>\n'
        '                </div>\n'
        '                <div class="bg-light rounded-2xl p-8 text-center">\n'
        '                    <div class="w-14 h-14 bg-purple-100 text-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4"><i data-lucide="award" class="w-7 h-7"></i></div>\n'
        '                    <h3 class="text-xl font-bold text-gray-900 mb-2">Spécialiste ' + dname.lower() + '</h3>\n'
        '                    <p class="text-gray-600 text-sm">Nos ' + practitioner + 's sont spécialisés en ' + dname.lower() + ' et formés aux méthodes les plus récentes pour un accompagnement de qualité.</p>\n'
        '                </div>\n'
        '            </div>\n'
        '        </div>\n'
        '    </section>\n'
    )

    # 8. Liens utiles
    html += (
        '    <section class="py-16">\n'
        '        <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Liens utiles</h2>\n'
        '        <div class="grid sm:grid-cols-3 gap-6">\n'
        '            <a href="' + prefix + category + '/' + slug + '.html" class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-primary/30 transition group text-center">\n'
        '                <div class="w-12 h-12 bg-primary/10 text-primary rounded-xl flex items-center justify-center mx-auto mb-4"><i data-lucide="book-open" class="w-6 h-6"></i></div>\n'
        '                <h3 class="font-bold text-gray-900 group-hover:text-primary transition">Tout savoir sur ' + dname.lower() + '</h3>\n'
        '            </a>\n'
        '            <a href="' + cslug + '.html" class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-primary/30 transition group text-center">\n'
        '                <div class="w-12 h-12 bg-primary/10 text-primary rounded-xl flex items-center justify-center mx-auto mb-4"><i data-lucide="map-pin" class="w-6 h-6"></i></div>\n'
        '                <h3 class="font-bold text-gray-900 group-hover:text-primary transition">' + practitioner_label + ' enfant à ' + city + '</h3>\n'
        '            </a>\n'
        '            <a href="' + prefix + category + '/" class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-primary/30 transition group text-center">\n'
        '                <div class="w-12 h-12 bg-primary/10 text-primary rounded-xl flex items-center justify-center mx-auto mb-4"><i data-lucide="grid" class="w-6 h-6"></i></div>\n'
        '                <h3 class="font-bold text-gray-900 group-hover:text-primary transition">Toutes nos spécialités</h3>\n'
        '            </a>\n'
        '        </div>\n'
        '    </section>\n'
    )

    # 9. Autres villes
    other_cities = [c for c in VILLES if c != city][:4]
    html += (
        '    <section class="py-16">\n'
        '        <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Consultez aussi dans d\'autres villes</h2>\n'
        '        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">\n'
    )
    for oc in other_cities:
        ocs = city_slug(oc)
        html += (
            '            <a href="' + slug + '-' + ocs + '.html" class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-primary/30 transition group text-center">\n'
            '                <div class="w-10 h-10 bg-primary/10 text-primary rounded-full flex items-center justify-center mx-auto mb-3"><i data-lucide="map-pin" class="w-5 h-5"></i></div>\n'
            '                <h3 class="font-bold text-gray-900 group-hover:text-primary transition">' + dname + ' à ' + oc + '</h3>\n'
            '            </a>\n'
        )
    html += (
        '        </div>\n'
        '    </section>\n'
    )

    # 10. FAQ section
    faq_items = data.get("faq", [])[:2]
    if faq_items:
        html += (
            '    <section class="py-16">\n'
            '        <div class="max-w-3xl mx-auto">\n'
            '            <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Questions fréquentes</h2>\n'
            '            <div class="space-y-4">\n'
        )
        for faq in faq_items:
            q = faq.get("q", faq[0] if isinstance(faq, (list, tuple)) else "")
            a = faq.get("a", faq[1] if isinstance(faq, (list, tuple)) else "")
            html += (
                '                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">\n'
                '                    <button onclick="toggleFaq(this)" class="w-full text-left p-6 flex justify-between items-center gap-4">\n'
                '                        <span class="font-semibold text-gray-900">' + q + '</span>\n'
                '                        <i data-lucide="plus" class="w-5 h-5 text-primary shrink-0 faq-icon transition-transform"></i>\n'
                '                    </button>\n'
                '                    <div class="faq-content px-6">\n'
                '                        <p class="text-gray-600 leading-relaxed pb-6">' + a + '</p>\n'
                '                    </div>\n'
                '                </div>\n'
            )
        html += (
            '            </div>\n'
            '        </div>\n'
            '    </section>\n'
        )

    html += '    </main>\n'

    # 11. CTA, Footer, JS
    html += get_cta_section(
        data.get("cta_title", "Prenez rendez-vous"),
        data.get("cta_desc", "Réservez votre bilan en ligne et bénéficiez d'un accompagnement personnalisé."),
    )
    html += get_footer(prefix)
    html += get_js(include_faq=bool(faq_items))

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath


# ------------------------------------------------------------------
# C) Soutien-Scolaire Niveau 3 - City Hub
# ------------------------------------------------------------------

def generate_scolaire_n3(city, base):
    """Generate a soutien-scolaire city hub page."""
    prefix = "../../"
    cslug = city_slug(city)
    cdata = CITY_DATA[city]

    title = "Soutien scolaire à " + city + " en ligne"
    meta_desc = (
        "Soutien scolaire en ligne à " + city + " : cours particuliers de mathématiques, "
        "français, anglais, physique-chimie et aide aux devoirs. Enseignants qualifiés, "
        "premier cours sous 48h."
    )

    out_dir = os.path.join(base, "soutien-scolaire", "villes")
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, cslug + ".html")

    wait_text = cdata["wait_text"].format(practitioner="enseignant")
    transport_text = cdata["transport_text"]

    html = ""
    html += get_head(title, meta_desc, include_faq_css=False)
    html += get_navbar(prefix)
    html += '    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">\n'

    # Breadcrumb
    html += get_breadcrumb([
        ("Accueil", prefix + "index.html"),
        ("Soutien Scolaire", prefix + "soutien-scolaire/"),
        (city, None),
    ])

    # Hero
    html += (
        '    <section class="py-16">\n'
        '        <div class="text-center max-w-3xl mx-auto">\n'
        '            <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6">\n'
        '                Soutien scolaire à <span class="text-primary">' + city + '</span> - Cours en ligne\n'
        '            </h1>\n'
        '            <p class="text-lg text-gray-600 leading-relaxed mb-8">Cours particuliers en ligne avec des enseignants qualifiés, du primaire au lycée. ' + wait_text + '</p>\n'
        '            <div class="flex flex-col sm:flex-row justify-center gap-4 mb-8">\n'
        '                <a href="' + prefix + 'contact.html" class="bg-primary text-white px-8 py-4 rounded-full font-bold hover:bg-primaryHover transition text-lg shadow-lg inline-flex items-center justify-center gap-2">\n'
        '                    <i data-lucide="calendar" class="w-5 h-5"></i> Réserver un cours\n'
        '                </a>\n'
        '            </div>\n'
        '            <div class="flex flex-wrap justify-center gap-4">\n'
        '                <span class="bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-1.5"><i data-lucide="clock" class="w-4 h-4"></i> Premier cours sous 48h</span>\n'
        '                <span class="bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-1.5"><i data-lucide="monitor" class="w-4 h-4"></i> 100% en ligne</span>\n'
        '                <span class="bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-1.5"><i data-lucide="map-pin" class="w-4 h-4"></i> ' + city + ' et environs</span>\n'
        '            </div>\n'
        '        </div>\n'
        '    </section>\n'
    )

    # Benefits
    html += (
        '    <section class="py-16 bg-white rounded-3xl mb-16">\n'
        '        <div class="max-w-6xl mx-auto px-6">\n'
        '            <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Pourquoi choisir le soutien scolaire en ligne depuis ' + city + ' ?</h2>\n'
        '            <div class="grid md:grid-cols-3 gap-8">\n'
        '                <div class="bg-light rounded-2xl p-8 text-center">\n'
        '                    <div class="w-14 h-14 bg-red-100 text-red-600 rounded-2xl flex items-center justify-center mx-auto mb-4"><i data-lucide="clock" class="w-7 h-7"></i></div>\n'
        '                    <h3 class="text-xl font-bold text-gray-900 mb-2">Démarrage rapide</h3>\n'
        '                    <p class="text-gray-600 text-sm">' + wait_text + '</p>\n'
        '                </div>\n'
        '                <div class="bg-light rounded-2xl p-8 text-center">\n'
        '                    <div class="w-14 h-14 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4"><i data-lucide="home" class="w-7 h-7"></i></div>\n'
        '                    <h3 class="text-xl font-bold text-gray-900 mb-2">Depuis chez vous</h3>\n'
        '                    <p class="text-gray-600 text-sm">' + transport_text + '</p>\n'
        '                </div>\n'
        '                <div class="bg-light rounded-2xl p-8 text-center">\n'
        '                    <div class="w-14 h-14 bg-purple-100 text-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4"><i data-lucide="award" class="w-7 h-7"></i></div>\n'
        '                    <h3 class="text-xl font-bold text-gray-900 mb-2">Enseignants qualifiés</h3>\n'
        '                    <p class="text-gray-600 text-sm">Tous nos enseignants sont diplômés et expérimentés. Ils s\'adaptent au programme et au rythme de votre enfant.</p>\n'
        '                </div>\n'
        '            </div>\n'
        '        </div>\n'
        '    </section>\n'
    )

    # Subjects grid with level badges
    html += (
        '    <section class="py-16">\n'
        '        <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Nos matières à ' + city + '</h2>\n'
        '        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">\n'
    )
    for subj_slug, subj_data in SCOLAIRE_SUBJECTS.items():
        html += (
            '            <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">\n'
            '                <div class="flex items-center gap-3 mb-4">\n'
            '                    <div class="w-12 h-12 bg-primary/10 text-primary rounded-xl flex items-center justify-center"><i data-lucide="' + subj_data["icon"] + '" class="w-6 h-6"></i></div>\n'
            '                    <h3 class="text-lg font-bold text-gray-900">' + subj_data["label"] + '</h3>\n'
            '                </div>\n'
            '                <p class="text-gray-600 text-sm mb-4">' + subj_data["desc"] + ' pour les élèves de ' + city + '.</p>\n'
            '                <div class="flex flex-wrap gap-2">\n'
        )
        for lvl_slug, lvl_info in subj_data["levels"].items():
            badge_link = prefix + "soutien-scolaire/" + subj_slug + "/" + lvl_slug + "-" + cslug + ".html"
            html += (
                '                    <a href="' + badge_link + '" class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-xs font-medium hover:bg-primary/10 hover:text-primary transition">' + lvl_info["label"] + '</a>\n'
            )
        html += (
            '                </div>\n'
            '            </div>\n'
        )
    html += (
        '        </div>\n'
        '    </section>\n'
    )

    html += '    </main>\n'

    html += get_about_section("enseignant", prefix)
    html += get_cta_section(
        "Soutien scolaire à " + city,
        "Réservez le premier cours de votre enfant et bénéficiez d'un accompagnement personnalisé avec nos enseignants qualifiés.",
    )
    html += get_footer(prefix)
    html += get_js(include_faq=False)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath


# ------------------------------------------------------------------
# D) Soutien-Scolaire Niveau 4 - Level + City
# ------------------------------------------------------------------

def generate_scolaire_n4(subject_slug, subject_data, level_slug, level_info, city, base):
    """Generate a level+city page for soutien-scolaire."""
    prefix = "../../"
    cslug = city_slug(city)
    cdata = CITY_DATA[city]
    level_label = level_info["label"]
    cycle = level_info["cycle"]
    subj_label = subject_data["label"]

    title = subj_label + " " + level_label + " à " + city + " - Cours en ligne"
    meta_desc = (
        "Cours de " + subj_label.lower() + " " + level_label + " en ligne à " + city
        + ". Soutien scolaire avec un enseignant qualifié. Premier cours sous 48h. "
        + cycle + ", programme officiel."
    )

    out_dir = os.path.join(base, "soutien-scolaire", subject_slug)
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, level_slug + "-" + cslug + ".html")

    ldata = get_level_data(subject_slug, level_slug)
    wait_text = cdata["wait_text"].format(practitioner="enseignant")

    html = ""
    has_faq = bool(ldata.get("faq"))
    html += get_head(title, meta_desc, include_faq_css=has_faq)
    html += get_navbar(prefix)
    html += '    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">\n'

    # Breadcrumb (5 levels)
    html += get_breadcrumb([
        ("Accueil", prefix + "index.html"),
        ("Soutien Scolaire", prefix + "soutien-scolaire/"),
        (subj_label, prefix + "soutien-scolaire/" + subject_slug + "/"),
        (level_label, prefix + "soutien-scolaire/" + subject_slug + "/" + level_slug + ".html" if level_slug else None),
        (city, None),
    ])

    # Hero
    hero_desc = ldata.get("hero", "")
    if not hero_desc:
        hero_desc = "Cours de " + subj_label.lower() + " " + level_label + " en ligne à " + city + " avec un enseignant qualifié."
    html += (
        '    <section class="py-16">\n'
        '        <div class="max-w-3xl mx-auto">\n'
        '            <div class="flex flex-wrap gap-2 mb-6">\n'
        '                <span class="bg-primary/10 text-primary px-3 py-1 rounded-full text-sm font-semibold">' + cycle + '</span>\n'
        '                <span class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-semibold flex items-center gap-1"><i data-lucide="map-pin" class="w-3 h-3"></i> ' + city + '</span>\n'
        '            </div>\n'
        '            <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6">\n'
        '                Soutien scolaire <span class="text-primary">' + subj_label.lower() + ' ' + level_label + '</span> à ' + city + '\n'
        '            </h1>\n'
        '            <p class="text-lg text-gray-600 leading-relaxed mb-8">' + hero_desc + '</p>\n'
        '            <a href="' + prefix + 'contact.html" class="bg-primary text-white px-8 py-4 rounded-full font-bold hover:bg-primaryHover transition text-lg shadow-lg inline-flex items-center gap-2">\n'
        '                <i data-lucide="calendar" class="w-5 h-5"></i> Réserver un cours\n'
        '            </a>\n'
        '        </div>\n'
        '    </section>\n'
    )

    # Programme section (topics)
    topics = ldata.get("topics", [])
    if topics:
        html += (
            '    <section class="py-16">\n'
            '        <div class="max-w-6xl mx-auto">\n'
            '            <h2 class="text-3xl font-bold text-gray-900 mb-8">Programme de ' + subj_label.lower() + ' ' + level_label + '</h2>\n'
            '            <div class="grid sm:grid-cols-2 gap-6 mb-8">\n'
        )
        for topic in topics:
            t_title = topic[0]
            t_icon = topic[1]
            t_desc = topic[2]
            html += (
                '                <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">\n'
                '                    <div class="flex items-start gap-4">\n'
                '                        <div class="w-10 h-10 bg-primary/10 text-primary rounded-xl flex items-center justify-center shrink-0"><i data-lucide="' + t_icon + '" class="w-5 h-5"></i></div>\n'
                '                        <div>\n'
                '                            <h3 class="font-bold text-gray-900 mb-1">' + t_title + '</h3>\n'
                '                            <p class="text-gray-600 text-sm">' + t_desc + '</p>\n'
                '                        </div>\n'
                '                    </div>\n'
                '                </div>\n'
            )
        html += (
            '            </div>\n'
        )
        # Link to parent level page
        parent_link = prefix + "soutien-scolaire/" + subject_slug + "/" + level_slug + ".html"
        html += (
            '            <a href="' + parent_link + '" class="text-primary font-semibold inline-flex items-center gap-1 hover:underline">\n'
            '                Voir le programme complet de ' + subj_label.lower() + ' ' + level_label + ' <i data-lucide="arrow-right" class="w-4 h-4"></i>\n'
            '            </a>\n'
            '        </div>\n'
            '    </section>\n'
        )

    # Method section
    method = ldata.get("method", "")
    if method:
        html += (
            '    <section class="py-16 bg-white rounded-3xl mb-16">\n'
            '        <div class="max-w-4xl mx-auto px-6">\n'
            '            <h2 class="text-3xl font-bold text-gray-900 mb-6">Notre méthode</h2>\n'
            '            <p class="text-gray-600 leading-relaxed text-lg">' + method + '</p>\n'
            '        </div>\n'
            '    </section>\n'
        )

    # Autres villes
    other_cities = [c for c in VILLES if c != city][:4]
    html += (
        '    <section class="py-16">\n'
        '        <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Même cours dans d\'autres villes</h2>\n'
        '        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">\n'
    )
    for oc in other_cities:
        ocs = city_slug(oc)
        html += (
            '            <a href="' + level_slug + '-' + ocs + '.html" class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-primary/30 transition group text-center">\n'
            '                <div class="w-10 h-10 bg-primary/10 text-primary rounded-full flex items-center justify-center mx-auto mb-3"><i data-lucide="map-pin" class="w-5 h-5"></i></div>\n'
            '                <h3 class="font-bold text-gray-900 group-hover:text-primary transition">' + subj_label + ' ' + level_label + ' à ' + oc + '</h3>\n'
            '            </a>\n'
        )
    html += (
        '        </div>\n'
        '    </section>\n'
    )

    # FAQ section
    faq_items = ldata.get("faq", [])[:2]
    if faq_items:
        html += (
            '    <section class="py-16">\n'
            '        <div class="max-w-3xl mx-auto">\n'
            '            <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Questions fréquentes</h2>\n'
            '            <div class="space-y-4">\n'
        )
        for faq in faq_items:
            if isinstance(faq, (list, tuple)):
                q, a = faq[0], faq[1]
            else:
                q, a = faq.get("q", ""), faq.get("a", "")
            html += (
                '                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">\n'
                '                    <button onclick="toggleFaq(this)" class="w-full text-left p-6 flex justify-between items-center gap-4">\n'
                '                        <span class="font-semibold text-gray-900">' + q + '</span>\n'
                '                        <i data-lucide="plus" class="w-5 h-5 text-primary shrink-0 faq-icon transition-transform"></i>\n'
                '                    </button>\n'
                '                    <div class="faq-content px-6">\n'
                '                        <p class="text-gray-600 leading-relaxed pb-6">' + a + '</p>\n'
                '                    </div>\n'
                '                </div>\n'
            )
        html += (
            '            </div>\n'
            '        </div>\n'
            '    </section>\n'
        )

    html += '    </main>\n'

    html += get_cta_section(
        "Cours de " + subj_label.lower() + " " + level_label + " à " + city,
        "Réservez le premier cours de votre enfant et bénéficiez d'un accompagnement personnalisé avec nos enseignants qualifiés.",
    )
    html += get_footer(prefix)
    html += get_js(include_faq=has_faq)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath


# ============================================================
# MAIN
# ============================================================

def main():
    base = "/workspaces/Logoestudios/site"
    count = 0

    # --- A) Ortho N3: city hubs ---
    print("Generating orthophonie city hubs (N3)...")
    for city in VILLES:
        generate_ortho_psycho_n3("orthophonie", ORTHO_PAGES, city, base)
        count += 1
    print(f"  -> {len(VILLES)} ortho N3 pages")

    # --- B) Ortho N4: trouble+city ---
    print("Generating orthophonie trouble+city pages (N4)...")
    ortho_n4 = 0
    for slug, data in ORTHO_PAGES.items():
        for city in VILLES:
            generate_ortho_psycho_n4("orthophonie", slug, data, city, base)
            count += 1
            ortho_n4 += 1
    print(f"  -> {ortho_n4} ortho N4 pages")

    # --- C) Psycho N3: city hubs ---
    print("Generating psychologie city hubs (N3)...")
    for city in VILLES:
        generate_ortho_psycho_n3("psychologie", PSYCHO_PAGES, city, base)
        count += 1
    print(f"  -> {len(VILLES)} psycho N3 pages")

    # --- D) Psycho N4: trouble+city ---
    print("Generating psychologie trouble+city pages (N4)...")
    psycho_n4 = 0
    for slug, data in PSYCHO_PAGES.items():
        for city in VILLES:
            generate_ortho_psycho_n4("psychologie", slug, data, city, base)
            count += 1
            psycho_n4 += 1
    print(f"  -> {psycho_n4} psycho N4 pages")

    # --- E) Scolaire N3: city hubs ---
    print("Generating soutien-scolaire city hubs (N3)...")
    for city in VILLES:
        generate_scolaire_n3(city, base)
        count += 1
    print(f"  -> {len(VILLES)} scolaire N3 pages")

    # --- F) Scolaire N4: level+city ---
    print("Generating soutien-scolaire level+city pages (N4)...")
    scolaire_n4 = 0
    for subj_slug, subj_data in SCOLAIRE_SUBJECTS.items():
        for lvl_slug, lvl_info in subj_data["levels"].items():
            for city in VILLES:
                generate_scolaire_n4(subj_slug, subj_data, lvl_slug, lvl_info, city, base)
                count += 1
                scolaire_n4 += 1
    print(f"  -> {scolaire_n4} scolaire N4 pages")

    print(f"\nDone! Generated {count} pages total.")


if __name__ == "__main__":
    main()
