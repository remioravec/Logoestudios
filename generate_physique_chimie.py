#!/usr/bin/env python3
"""Generate all physique-chimie pages following the same template as mathematiques."""

import os

SITE_DIR = "/workspaces/Logoestudios/site/soutien-scolaire/physique-chimie"
CITIES = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"]

LEVELS = {
    "5eme": {
        "label": "5ème",
        "cycle": "Collège",
        "slug": "5eme",
        "desc_short": "Introduction aux circuits électriques et aux mélanges",
        "hero": "La 5ème marque l'entrée dans l'univers de la physique-chimie en tant que discipline à part entière. Votre enfant découvre les bases de l'électricité avec les circuits simples, explore les propriétés de la matière à travers les mélanges et les dissolutions, et s'initie à la démarche scientifique expérimentale. C'est une année fondatrice où la curiosité et la rigueur se construisent ensemble.",
        "topics": [
            ("L'eau et les mélanges", "book-open", "Distinguer mélanges homogènes et hétérogènes, techniques de séparation (filtration, décantation, distillation)."),
            ("Les circuits électriques simples", "zap", "Comprendre les composants d'un circuit, réaliser des montages en série et en dérivation."),
            ("Les changements d'état", "thermometer", "Étudier la fusion, la solidification, l'ébullition et les courbes de changement d'état."),
            ("La lumière", "sun", "Sources lumineuses, propagation rectiligne de la lumière et ombres.")
        ],
        "method": "En 5ème, notre approche privilégie l'expérimentation et la manipulation. Chaque notion est introduite par une expérience concrète que l'élève peut reproduire chez lui. Nous construisons progressivement le vocabulaire scientifique et la rigueur du compte-rendu expérimental, compétences essentielles pour la suite du collège.",
        "faq": [
            ("Mon enfant n'a jamais fait de physique-chimie, comment l'aider ?", "La 5ème est le début ! Nos enseignants partent de zéro et s'appuient sur des expériences du quotidien (cuisine, électricité domestique) pour rendre la matière concrète et accessible."),
            ("Les manipulations sont-elles possibles en ligne ?", "Absolument. Nous utilisons des simulations interactives et proposons des expériences réalisables avec du matériel courant. L'enseignant guide l'élève pas à pas via la visioconférence."),
            ("Mon enfant confond les notions, est-ce normal en 5ème ?", "Tout à fait. Le vocabulaire scientifique est nouveau et les concepts abstraits. Nos enseignants utilisent des schémas, des analogies et beaucoup de répétition pour ancrer les apprentissages.")
        ]
    },
    "4eme": {
        "label": "4ème",
        "cycle": "Collège",
        "slug": "4eme",
        "desc_short": "Lois de l'électricité et transformations chimiques",
        "hero": "La 4ème approfondit les bases posées en 5ème et introduit des concepts plus quantitatifs. Votre enfant découvre les lois fondamentales de l'électricité (tension, intensité), aborde les premières transformations chimiques et commence à maîtriser le modèle moléculaire. C'est une année charnière où la physique-chimie devient plus rigoureuse et mathématisée.",
        "topics": [
            ("Lois de l'électricité", "zap", "Loi d'Ohm, loi d'additivité des tensions et des intensités dans les circuits."),
            ("Les atomes et les molécules", "atom", "Modèle particulaire de la matière, symboles chimiques, formules moléculaires."),
            ("Les transformations chimiques", "flask-conical", "Réactifs, produits, conservation de la masse, premières équations chimiques."),
            ("La vitesse et le mouvement", "gauge", "Calcul de vitesse, distinction entre mouvement uniforme et non uniforme.")
        ],
        "method": "En 4ème, nous combinons compréhension conceptuelle et entraînement au calcul. Les lois de l'électricité nécessitent de savoir manipuler des formules, et les transformations chimiques demandent de la méthode. Nos enseignants proposent des exercices progressifs qui renforcent à la fois la compréhension et la technique.",
        "faq": [
            ("Mon enfant a du mal avec la loi d'Ohm, que faire ?", "La loi d'Ohm combine physique et mathématiques. Nos enseignants reprennent les bases du calcul littéral si nécessaire, puis travaillent sur de nombreux exercices d'application avec des situations concrètes."),
            ("Les transformations chimiques sont abstraites, comment les rendre concrètes ?", "Nous utilisons des animations moléculaires et des analogies visuelles pour représenter les réactions. L'élève apprend à « voir » les atomes se réorganiser, ce qui facilite la compréhension des équations."),
            ("Comment préparer la 3ème depuis la 4ème ?", "Les notions de 4ème sont les fondations de la 3ème. Nous nous assurons que chaque concept est solidement acquis, notamment les lois de l'électricité et le modèle moléculaire, pour aborder sereinement l'année du Brevet.")
        ]
    },
    "3eme": {
        "label": "3ème",
        "cycle": "Collège",
        "slug": "3eme",
        "desc_short": "Énergie, chimie et préparation au Brevet",
        "hero": "La 3ème est l'année du Brevet et l'aboutissement du cycle du collège en physique-chimie. Votre enfant approfondit les notions d'énergie et de puissance, maîtrise les équations chimiques et découvre les enjeux énergétiques contemporains. L'épreuve du Brevet évalue la démarche scientifique, la capacité d'analyse et la restitution des connaissances.",
        "topics": [
            ("Énergie et puissance électrique", "battery-charging", "Calculer l'énergie consommée, comprendre la puissance, lire une facture d'électricité."),
            ("Les équations chimiques", "flask-conical", "Équilibrer une équation, identifier réactifs et produits, conservation des atomes."),
            ("La gravitation et le poids", "globe", "Distinguer masse et poids, comprendre la gravitation universelle et ses effets."),
            ("Préparation au Brevet", "award", "Méthodologie de l'épreuve, entraînement sur annales, rédaction scientifique.")
        ],
        "method": "Notre accompagnement en 3ème combine approfondissement du programme et préparation intensive au Brevet. Nous travaillons chaque chapitre en profondeur tout en proposant régulièrement des exercices type Brevet. Les séances incluent des annales corrigées, des méthodes de rédaction scientifique et une gestion efficace du temps lors des épreuves.",
        "faq": [
            ("Comment bien préparer l'épreuve de sciences du Brevet ?", "L'épreuve de sciences au Brevet porte sur la physique-chimie, les SVT et la technologie. Nos enseignants entraînent votre enfant sur des sujets complets, en insistant sur la méthodologie de réponse et la rigueur de la rédaction."),
            ("Mon enfant confond masse et poids, comment l'aider ?", "C'est une confusion très courante. Nos enseignants utilisent des exemples concrets (peser sur Terre vs sur la Lune) et des exercices ciblés pour que l'élève intègre définitivement la distinction."),
            ("Les équations chimiques sont trop difficiles, que faire ?", "Nous décomposons l'équilibrage en étapes simples et méthodiques. Avec de la pratique régulière et une bonne méthode, tous les élèves peuvent maîtriser cette compétence.")
        ]
    },
    "seconde": {
        "label": "Seconde",
        "cycle": "Lycée",
        "slug": "seconde",
        "desc_short": "Constitution de la matière et ondes sonores",
        "hero": "La Seconde représente une marche importante en physique-chimie. Le programme s'élargit considérablement : votre enfant étudie la structure de l'atome en détail, découvre la mole et les quantités de matière, aborde les ondes sonores et lumineuses, et approfondit la mécanique. C'est l'année où se joue souvent le choix de la spécialité pour la Première.",
        "topics": [
            ("Structure de l'atome et classification périodique", "atom", "Modèle de l'atome, numéro atomique, configuration électronique, tableau de Mendeleïev."),
            ("La mole et les quantités de matière", "scale", "Nombre d'Avogadro, masse molaire, concentration, dilution."),
            ("Ondes sonores et lumineuses", "waves", "Fréquence, longueur d'onde, vitesse de propagation, spectre lumineux."),
            ("Mécanique : forces et mouvements", "move", "Principe d'inertie, forces, interactions, référentiels.")
        ],
        "method": "En Seconde, le niveau d'abstraction augmente significativement. Notre méthode associe la compréhension conceptuelle à la maîtrise des outils mathématiques nécessaires (conversions, calculs de concentration, analyse dimensionnelle). Nous aidons l'élève à développer une vraie démarche scientifique autonome.",
        "faq": [
            ("Mon enfant hésite à prendre la spécialité physique-chimie, comment l'aider à choisir ?", "Nos enseignants peuvent évaluer le niveau et le potentiel de votre enfant en physique-chimie. Si la motivation est là, un accompagnement régulier permet souvent de combler les lacunes et d'aborder la spécialité sereinement."),
            ("La mole est un concept très abstrait, comment le comprendre ?", "Nous partons d'analogies concrètes (une douzaine d'œufs, une ramette de papier) pour introduire progressivement le concept de quantité de matière. Beaucoup d'exercices pratiques aident à rendre la mole intuitive."),
            ("Le programme de Seconde est très dense, comment s'organiser ?", "Nous proposons un planning de révision structuré et travaillons en priorité les chapitres les plus importants pour la suite. La régularité des séances est clé pour ne pas accumuler de retard.")
        ]
    },
    "premiere": {
        "label": "Première",
        "cycle": "Lycée",
        "slug": "premiere",
        "desc_short": "Réactions chimiques, optique et lois de Newton",
        "hero": "La Première spécialité physique-chimie est une année exigeante qui pose les fondements du programme de Terminale. Votre enfant approfondit les réactions chimiques avec les titrages, découvre les lois de Newton appliquées au mouvement, étudie l'optique géométrique et aborde les conversions d'énergie. La rigueur mathématique et la capacité d'analyse sont essentielles.",
        "topics": [
            ("Réactions chimiques et titrages", "flask-conical", "Avancement d'une réaction, réactif limitant, titrage acido-basique et colorimétrique."),
            ("Les lois de Newton", "rocket", "Principe fondamental de la dynamique, chute libre, mouvement parabolique."),
            ("Optique géométrique", "eye", "Lois de Snell-Descartes, lentilles convergentes, formation des images."),
            ("Conversions et transferts d'énergie", "battery-charging", "Travail d'une force, énergie cinétique, énergie potentielle, conservation de l'énergie.")
        ],
        "method": "En Première, nous insistons sur la méthodologie de résolution de problèmes scientifiques. Chaque séance combine cours théorique, exercices d'application et problèmes de synthèse. Nous préparons aussi les évaluations communes et anticipons le programme de Terminale pour les élèves les plus avancés.",
        "faq": [
            ("Les lois de Newton sont difficiles, comment aider mon enfant ?", "Les lois de Newton nécessitent de combiner raisonnement physique et outils mathématiques (vecteurs, projections). Nos enseignants décomposent chaque problème en étapes claires et entraînent l'élève sur des exercices de difficulté progressive."),
            ("Mon enfant a du mal avec les titrages, est-ce rattrapable ?", "Les titrages combinent beaucoup de notions (concentration, réaction, équivalence). Avec un travail méthodique et des exercices ciblés, nos enseignants aident l'élève à maîtriser chaque étape du raisonnement."),
            ("Comment préparer le bac dès la Première ?", "Le contrôle continu compte pour le bac. Nous préparons chaque évaluation avec rigueur et commençons à travailler les compétences évaluées au Grand Oral et à l'épreuve de Terminale.")
        ]
    },
    "terminale": {
        "label": "Terminale",
        "cycle": "Lycée",
        "slug": "terminale",
        "desc_short": "Chimie organique, ondes et mécanique avancée",
        "hero": "La Terminale spécialité physique-chimie est l'aboutissement du parcours scientifique au lycée. Le programme couvre la chimie organique, les ondes, la mécanique avancée et la physique nucléaire. L'épreuve du bac, coefficient 16, exige une maîtrise approfondie du programme et une capacité à résoudre des problèmes complexes de manière autonome.",
        "topics": [
            ("Chimie organique", "hexagon", "Groupes caractéristiques, réactions d'estérification, polymères, spectroscopie IR et RMN."),
            ("Ondes et signaux", "waves", "Interférences, diffraction, effet Doppler, lunette astronomique."),
            ("Mécanique avancée", "orbit", "Mouvement dans un champ uniforme, satellites, lois de Kepler."),
            ("Physique nucléaire et énergie", "atom", "Radioactivité, réactions nucléaires, équivalence masse-énergie, bilan énergétique.")
        ],
        "method": "En Terminale, notre priorité est la préparation au bac (coefficient 16). Nous combinons révision approfondie du programme, entraînement intensif sur des sujets de bac et perfectionnement de la méthodologie. Nous préparons aussi le Grand Oral pour les élèves qui choisissent un sujet en physique-chimie.",
        "faq": [
            ("Comment bien préparer l'épreuve de physique-chimie au bac ?", "Notre méthode combine révision systématique du cours, entraînement sur des sujets de bac chronométrés et travail sur la rédaction scientifique. Nous ciblons les chapitres les plus fréquents et les erreurs les plus courantes."),
            ("La chimie organique est très complexe, par où commencer ?", "Nous structurons l'apprentissage en partant de la nomenclature, puis des groupes caractéristiques, avant d'aborder les mécanismes réactionnels. Des fiches synthétiques et beaucoup de pratique aident à mémoriser efficacement."),
            ("Mon enfant vise une prépa scientifique, comment le préparer ?", "Au-delà du programme de Terminale, nous proposons des exercices de niveau supérieur et travaillons l'autonomie dans la résolution de problèmes. Nous conseillons aussi sur les méthodes de travail adaptées au rythme de la prépa.")
        ]
    }
}

# ── Common HTML parts ──

def head(title, description):
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Logopsi Studios</title>
    <meta name="description" content="{description}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{ primary: '#05C86B', primaryHover: '#04b05e', light: '#FBF9F6', dark: '#111111' }},
                    fontFamily: {{ sans: ['Inter', 'system-ui', 'sans-serif'] }}
                }}
            }}
        }}
    </script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>'''

def nav():
    return '''
    <nav class="bg-white border-b border-gray-100 sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
            <a href="/site/" class="text-2xl font-bold text-primary">Logopsi Studios</a>
            <div class="flex items-center gap-6">
                <a href="/site/soutien-scolaire/" class="text-dark hover:text-primary transition">Soutien Scolaire</a>
                <a href="/site/soutien-scolaire/physique-chimie/" class="text-primary font-semibold">Physique-Chimie</a>
                <a href="#cta" class="bg-primary text-white px-5 py-2.5 rounded-lg font-semibold hover:bg-primaryHover transition">Prendre rendez-vous</a>
            </div>
        </div>
    </nav>'''

def footer():
    return '''
    <footer class="bg-dark text-white py-12">
        <div class="max-w-6xl mx-auto px-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div>
                    <h3 class="text-xl font-bold text-primary mb-4">Logopsi Studios</h3>
                    <p class="text-gray-400">Soutien scolaire et accompagnement en ligne pour tous les niveaux.</p>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Matières</h4>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="/site/soutien-scolaire/mathematiques/" class="hover:text-primary transition">Mathématiques</a></li>
                        <li><a href="/site/soutien-scolaire/francais/" class="hover:text-primary transition">Français</a></li>
                        <li><a href="/site/soutien-scolaire/anglais/" class="hover:text-primary transition">Anglais</a></li>
                        <li><a href="/site/soutien-scolaire/physique-chimie/" class="hover:text-primary transition">Physique-Chimie</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Contact</h4>
                    <p class="text-gray-400">contact@logopsistudios.fr</p>
                    <div class="flex gap-4 mt-4">
                        <a href="#" class="text-gray-400 hover:text-primary transition"><i data-lucide="facebook" class="w-5 h-5"></i></a>
                        <a href="#" class="text-gray-400 hover:text-primary transition"><i data-lucide="instagram" class="w-5 h-5"></i></a>
                    </div>
                </div>
            </div>
            <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-500 text-sm">
                <p>&copy; 2025 Logopsi Studios. Tous droits réservés.</p>
            </div>
        </div>
    </footer>

    <script>lucide.createIcons();</script>
</body>
</html>'''

def cta_section(title, subtitle):
    return f'''
    <section id="cta" class="py-20 bg-primary">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <h2 class="text-3xl md:text-4xl font-bold text-white mb-6">{title}</h2>
            <p class="text-green-100 text-lg mb-8">{subtitle}</p>
            <a href="#" class="inline-block bg-white text-primary px-8 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 transition">Réserver un cours d\'essai gratuit</a>
        </div>
    </section>'''

# ── INDEX PAGE ──

def generate_index():
    level_cards = ""
    for slug, data in LEVELS.items():
        level_cards += f'''
                <a href="{slug}.html" class="bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition group">
                    <div class="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center mb-4 group-hover:bg-primary group-hover:text-white transition">
                        <i data-lucide="flask-conical" class="w-6 h-6 text-primary group-hover:text-white"></i>
                    </div>
                    <h3 class="text-xl font-bold mb-2">{data["label"]}</h3>
                    <p class="text-gray-500 text-sm mb-3">{data["cycle"]}</p>
                    <p class="text-gray-600 text-sm">{data["desc_short"]}</p>
                    <span class="inline-flex items-center gap-1 text-primary font-semibold text-sm mt-4">Découvrir <i data-lucide="arrow-right" class="w-4 h-4"></i></span>
                </a>'''

    html = f'''{head("Soutien scolaire Physique-Chimie en ligne", "Soutien scolaire en physique-chimie en ligne pour tous les niveaux : de la 5ème à la Terminale. Enseignants qualifiés, pédagogie adaptée, cours en visio.")}
<body class="bg-light text-dark font-sans">
{nav()}

    <!-- BREADCRUMB -->
    <div class="max-w-6xl mx-auto px-4 py-4">
        <nav class="text-sm text-gray-500">
            <a href="/site/" class="hover:text-primary">Accueil</a>
            <span class="mx-2">></span>
            <a href="/site/soutien-scolaire/" class="hover:text-primary">Soutien Scolaire</a>
            <span class="mx-2">></span>
            <span class="text-dark font-medium">Physique-Chimie</span>
        </nav>
    </div>

    <!-- HERO -->
    <section class="bg-white py-16">
        <div class="max-w-6xl mx-auto px-4">
            <div class="max-w-3xl">
                <h1 class="text-4xl md:text-5xl font-extrabold mb-6">Soutien scolaire Physique-Chimie en ligne</h1>
                <p class="text-lg text-gray-600 mb-8">De la 5ème à la Terminale, nos enseignants qualifiés accompagnent votre enfant en physique-chimie avec une pédagogie personnalisée, 100% en ligne. Que ce soit pour comprendre les lois fondamentales, réussir les expériences ou préparer le Brevet et le Bac, nous proposons un suivi adapté à chaque niveau et à chaque profil d'élève.</p>
                <div class="flex gap-4 flex-wrap">
                    <a href="#cta" class="bg-primary text-white px-8 py-3.5 rounded-lg font-semibold text-lg hover:bg-primaryHover transition">Prendre rendez-vous</a>
                    <a href="#niveaux" class="border-2 border-primary text-primary px-8 py-3.5 rounded-lg font-semibold text-lg hover:bg-primary hover:text-white transition">Voir tous les niveaux</a>
                </div>
            </div>
        </div>
    </section>

    <!-- WHY SECTION -->
    <section class="py-20">
        <div class="max-w-6xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-12 text-center">Pourquoi choisir Logopsi Studios pour la physique-chimie ?</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="bg-white rounded-2xl p-8 shadow-sm text-center">
                    <div class="w-14 h-14 bg-green-50 rounded-xl flex items-center justify-center mx-auto mb-6">
                        <i data-lucide="graduation-cap" class="w-7 h-7 text-primary"></i>
                    </div>
                    <h3 class="text-xl font-bold mb-3">Enseignants spécialisés</h3>
                    <p class="text-gray-600">Nos professeurs sont diplômés en physique ou en chimie et maîtrisent les programmes officiels. Ils savent rendre accessibles les concepts les plus abstraits grâce à des expériences et des démonstrations visuelles.</p>
                </div>
                <div class="bg-white rounded-2xl p-8 shadow-sm text-center">
                    <div class="w-14 h-14 bg-green-50 rounded-xl flex items-center justify-center mx-auto mb-6">
                        <i data-lucide="flask-conical" class="w-7 h-7 text-primary"></i>
                    </div>
                    <h3 class="text-xl font-bold mb-3">Approche expérimentale</h3>
                    <p class="text-gray-600">Même en ligne, nous intégrons des expériences, des simulations interactives et des vidéos de manipulations pour que votre enfant développe une vraie démarche scientifique.</p>
                </div>
                <div class="bg-white rounded-2xl p-8 shadow-sm text-center">
                    <div class="w-14 h-14 bg-green-50 rounded-xl flex items-center justify-center mx-auto mb-6">
                        <i data-lucide="monitor" class="w-7 h-7 text-primary"></i>
                    </div>
                    <h3 class="text-xl font-bold mb-3">100% en ligne</h3>
                    <p class="text-gray-600">Les cours se déroulent en visioconférence avec un tableau interactif. Pas de déplacement, des horaires flexibles et un confort d'apprentissage optimal depuis chez vous.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- LEVELS GRID -->
    <section id="niveaux" class="py-20 bg-white">
        <div class="max-w-6xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4 text-center">Tous les niveaux</h2>
            <p class="text-gray-600 text-center max-w-2xl mx-auto mb-12">Sélectionnez le niveau de votre enfant pour découvrir le programme et notre approche pédagogique adaptée.</p>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">{level_cards}
            </div>
        </div>
    </section>

    {cta_section("Prêt à progresser en physique-chimie ?", "Nos enseignants qualifiés accompagnent votre enfant avec une pédagogie adaptée, 100% en ligne. Première séance d'évaluation offerte.")}
{footer()}'''
    return html

# ── LEVEL PAGE ──

def generate_level(slug, data):
    topics_html = ""
    icons = ["book-open", "target", "ruler", "brain"]
    for i, (title, icon, desc) in enumerate(data["topics"]):
        topics_html += f'''
                <div class="bg-white rounded-2xl p-6 shadow-sm">
                    <div class="w-10 h-10 bg-green-50 rounded-lg flex items-center justify-center mb-4">
                        <i data-lucide="{icon}" class="w-5 h-5 text-primary"></i>
                    </div>
                    <h3 class="font-bold mb-2">{title}</h3>
                    <p class="text-gray-600 text-sm">{desc}</p>
                </div>'''

    cities_html = ""
    for city in CITIES:
        city_slug = city.lower()
        cities_html += f'''
                <a href="{slug}-{city_slug}.html" class="bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition text-center group">
                    <div class="w-10 h-10 bg-green-50 rounded-lg flex items-center justify-center mx-auto mb-3 group-hover:bg-primary transition">
                        <i data-lucide="map-pin" class="w-5 h-5 text-primary group-hover:text-white"></i>
                    </div>
                    <h3 class="font-bold mb-1">Physique-chimie {data["label"]} à {city}</h3>
                    <p class="text-gray-500 text-sm">Soutien accessible depuis {city}</p>
                </a>'''

    faq_html = ""
    for q, a in data["faq"]:
        faq_html += f'''
                <div class="bg-white rounded-2xl p-6 shadow-sm">
                    <h3 class="font-bold mb-3">{q}</h3>
                    <p class="text-gray-600">{a}</p>
                </div>'''

    topic_names = ", ".join([t[0] for t in data["topics"][:2]])
    title = f"Soutien scolaire physique-chimie {data['label']} en ligne"
    meta_desc = f"Soutien scolaire en physique-chimie niveau {data['label']} en ligne. Programme adapté, enseignants qualifiés, cours en visio. {topic_names} et plus."

    html = f'''{head(title, meta_desc)}
<body class="bg-light text-dark font-sans">
{nav()}

    <!-- BREADCRUMB -->
    <div class="max-w-6xl mx-auto px-4 py-4">
        <nav class="text-sm text-gray-500">
            <a href="/site/" class="hover:text-primary">Accueil</a>
            <span class="mx-2">></span>
            <a href="/site/soutien-scolaire/" class="hover:text-primary">Soutien Scolaire</a>
            <span class="mx-2">></span>
            <a href="/site/soutien-scolaire/physique-chimie/" class="hover:text-primary">Physique-Chimie</a>
            <span class="mx-2">></span>
            <span class="text-dark font-medium">{data["label"]}</span>
        </nav>
    </div>

    <!-- HERO -->
    <section class="bg-white py-16">
        <div class="max-w-6xl mx-auto px-4">
            <div class="max-w-3xl">
                <span class="inline-block bg-green-50 text-primary font-semibold px-4 py-1.5 rounded-full text-sm mb-4">{data["cycle"]}</span>
                <h1 class="text-4xl md:text-5xl font-extrabold mb-6">{title}</h1>
                <p class="text-lg text-gray-600 mb-8">{data["hero"]}</p>
                <div class="flex flex-col sm:flex-row gap-4">
                    <a href="#cta" class="bg-primary text-white px-8 py-3.5 rounded-lg font-semibold text-lg hover:bg-primaryHover transition text-center">Réserver un cours d'essai</a>
                    <a href="#programme" class="border-2 border-primary text-primary px-8 py-3.5 rounded-lg font-semibold text-lg hover:bg-primary hover:text-white transition text-center">Voir le programme</a>
                </div>
            </div>
        </div>
    </section>

    <!-- PROGRAMME -->
    <section id="programme" class="py-20">
        <div class="max-w-6xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">Programme et objectifs en {data["label"]}</h2>
            <p class="text-gray-600 max-w-3xl mb-12">Voici les principales notions travaillées lors de nos séances de soutien scolaire en physique-chimie niveau {data["label"]}.</p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">{topics_html}
            </div>
        </div>
    </section>

    <!-- METHODE -->
    <section class="py-20 bg-white">
        <div class="max-w-6xl mx-auto px-4">
            <div class="max-w-3xl">
                <h2 class="text-3xl font-bold mb-6">Notre méthode pour le niveau {data["label"]}</h2>
                <p class="text-gray-600 text-lg mb-8">{data["method"]}</p>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
                    <div class="flex items-start gap-3">
                        <div class="w-8 h-8 bg-green-50 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                            <i data-lucide="search" class="w-4 h-4 text-primary"></i>
                        </div>
                        <div>
                            <h4 class="font-semibold mb-1">Diagnostic</h4>
                            <p class="text-gray-500 text-sm">Évaluation précise du niveau et identification des lacunes</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3">
                        <div class="w-8 h-8 bg-green-50 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                            <i data-lucide="route" class="w-4 h-4 text-primary"></i>
                        </div>
                        <div>
                            <h4 class="font-semibold mb-1">Parcours adapté</h4>
                            <p class="text-gray-500 text-sm">Programme personnalisé selon les besoins de l'élève</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3">
                        <div class="w-8 h-8 bg-green-50 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                            <i data-lucide="trending-up" class="w-4 h-4 text-primary"></i>
                        </div>
                        <div>
                            <h4 class="font-semibold mb-1">Progression</h4>
                            <p class="text-gray-500 text-sm">Suivi régulier et ajustement du programme</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- CITIES -->
    <section class="py-20">
        <div class="max-w-6xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">Physique-chimie {data["label"]} par ville</h2>
            <p class="text-gray-600 max-w-3xl mb-12">Nos cours en ligne sont accessibles partout en France. Retrouvez nos pages dédiées par ville.</p>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">{cities_html}
            </div>
        </div>
    </section>

    <!-- FAQ -->
    <section class="py-20 bg-white">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-12 text-center">Questions fréquentes - Physique-chimie {data["label"]}</h2>
            <div class="space-y-6">{faq_html}
            </div>
        </div>
    </section>

    {cta_section(f"Prêt à progresser en physique-chimie ?", "Nos enseignants qualifiés accompagnent votre enfant avec une pédagogie adaptée, 100% en ligne. Première séance d'évaluation offerte.")}
{footer()}'''
    return html

# ── LEVEL + CITY PAGE ──

def generate_level_city(slug, data, city):
    city_slug = city.lower()
    title = f"Soutien scolaire physique-chimie {data['label']} à {city}"
    meta_desc = f"Soutien scolaire en physique-chimie niveau {data['label']} à {city}. Cours en ligne avec enseignants qualifiés. {data['topics'][0][0]}, {data['topics'][1][0]}."

    topics_checklist = ""
    for t_name, _, _ in data["topics"]:
        topics_checklist += f'''
                <div class="flex items-center gap-3 bg-white rounded-xl p-4 shadow-sm">
                    <i data-lucide="check-circle" class="w-5 h-5 text-primary flex-shrink-0"></i>
                    <span class="font-medium">{t_name}</span>
                </div>'''

    other_cities = [c for c in CITIES if c != city]
    other_cities_html = ""
    for c in other_cities:
        c_slug = c.lower()
        other_cities_html += f'''
                <a href="{slug}-{c_slug}.html" class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition text-center">
                    <i data-lucide="map-pin" class="w-5 h-5 text-primary mx-auto mb-2"></i>
                    <p class="font-semibold text-sm">Physique-chimie {data["label"]} à {c}</p>
                </a>'''

    html = f'''{head(title, meta_desc)}
<body class="bg-light text-dark font-sans">
{nav()}

    <!-- BREADCRUMB -->
    <div class="max-w-6xl mx-auto px-4 py-4">
        <nav class="text-sm text-gray-500">
            <a href="/site/" class="hover:text-primary">Accueil</a>
            <span class="mx-2">></span>
            <a href="/site/soutien-scolaire/" class="hover:text-primary">Soutien Scolaire</a>
            <span class="mx-2">></span>
            <a href="/site/soutien-scolaire/physique-chimie/" class="hover:text-primary">Physique-Chimie</a>
            <span class="mx-2">></span>
            <a href="{slug}.html" class="hover:text-primary">{data["label"]}</a>
            <span class="mx-2">></span>
            <span class="text-dark font-medium">{city}</span>
        </nav>
    </div>

    <!-- HERO -->
    <section class="bg-white py-16">
        <div class="max-w-6xl mx-auto px-4">
            <div class="max-w-3xl">
                <div class="flex items-center gap-3 mb-4">
                    <span class="inline-block bg-green-50 text-primary font-semibold px-4 py-1.5 rounded-full text-sm">{data["cycle"]} - {data["label"]}</span>
                    <span class="inline-flex items-center gap-1 bg-gray-100 text-gray-700 px-3 py-1.5 rounded-full text-sm"><i data-lucide="map-pin" class="w-3.5 h-3.5"></i> {city}</span>
                </div>
                <h1 class="text-4xl md:text-5xl font-extrabold mb-6">{title}</h1>
                <p class="text-lg text-gray-600 mb-8">Vous habitez à {city} et recherchez un soutien scolaire en physique-chimie niveau {data["label"]} ? Nos enseignants qualifiés proposent des cours en ligne accessibles depuis {city} et ses environs. Grâce à notre plateforme de visioconférence, votre enfant bénéficie d'un accompagnement personnalisé sans perdre de temps dans les transports.</p>
                <a href="#cta" class="inline-block bg-primary text-white px-8 py-3.5 rounded-lg font-semibold text-lg hover:bg-primaryHover transition">Réserver un cours d'essai gratuit</a>
            </div>
        </div>
    </section>

    <!-- PROGRAMME OVERVIEW -->
    <section class="py-16">
        <div class="max-w-6xl mx-auto px-4">
            <h2 class="text-2xl font-bold mb-6">Ce que nous travaillons en {data["label"]}</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-2xl">{topics_checklist}
            </div>
            <a href="{slug}.html" class="inline-flex items-center gap-2 text-primary font-semibold mt-6 hover:underline">
                <i data-lucide="arrow-left" class="w-4 h-4"></i> Voir le programme complet en {data["label"]}
            </a>
        </div>
    </section>

    <!-- LINKS -->
    <section class="py-16 bg-white">
        <div class="max-w-6xl mx-auto px-4">
            <h2 class="text-2xl font-bold mb-8">Physique-chimie {data["label"]} dans d'autres villes</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">{other_cities_html}
            </div>
            <div class="mt-8 pt-8 border-t border-gray-100">
                <a href="../villes/{city_slug}.html" class="inline-flex items-center gap-2 text-primary font-semibold hover:underline">
                    <i data-lucide="building-2" class="w-4 h-4"></i> Tout le soutien scolaire à {city}
                </a>
            </div>
        </div>
    </section>

    <!-- CTA -->
    {cta_section(f"Progressez en physique-chimie {data['label']} depuis {city}", "Cours en ligne avec un enseignant dédié. Première séance d'évaluation offerte, sans engagement.")}
{footer()}'''
    return html


# ── MAIN ──

def main():
    os.makedirs(SITE_DIR, exist_ok=True)

    # Index
    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_index())
    print("Created: index.html")

    # Level pages + city pages
    for slug, data in LEVELS.items():
        with open(os.path.join(SITE_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(generate_level(slug, data))
        print(f"Created: {slug}.html")

        for city in CITIES:
            city_slug = city.lower()
            filename = f"{slug}-{city_slug}.html"
            with open(os.path.join(SITE_DIR, filename), "w", encoding="utf-8") as f:
                f.write(generate_level_city(slug, data, city))
            print(f"Created: {filename}")

    total = 1 + len(LEVELS) + len(LEVELS) * len(CITIES)
    print(f"\nTotal: {total} pages generated in {SITE_DIR}")

if __name__ == "__main__":
    main()
