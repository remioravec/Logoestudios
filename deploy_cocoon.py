#!/usr/bin/env python3
"""
deploy_cocoon.py - Deploy a complete SEO semantic cocoon to WordPress via REST API.

Usage:
    python deploy_cocoon.py            # Deploy all pages as drafts
    python deploy_cocoon.py --dry-run  # Preview without creating pages

Creates ~194 pages organized as:
  - 2 Pillar pages (Orthophonie en ligne, Psychologie en ligne)
  - 16 City mother pages (5 ortho + 5 psy, but shared structure)
  - 22 Trouble mother pages (11 ortho + 11 psy)
  - 110 Trouble+City pages for ortho (11 troubles x 5 cities)
  - 55 Trouble+City pages for psy (11 troubles x 5 cities)
"""

import argparse
import base64
import json
import logging
import sys
import time
from typing import Optional

import requests

# ---------------------------------------------------------------------------
# WordPress Configuration
# ---------------------------------------------------------------------------
WP_SITE = "https://logopsiestudios.com"
WP_API = f"{WP_SITE}/wp-json/wp/v2/pages"
WP_USER = "remi-oravec@seo-monkey.fr"
WP_APP_PASSWORD = "vbRF zqNs F7KM BRFL 4X04 rnIK"

AUTH_HEADER = "Basic " + base64.b64encode(
    f"{WP_USER}:{WP_APP_PASSWORD}".encode()
).decode()

HEADERS = {
    "Authorization": AUTH_HEADER,
    "Content-Type": "application/json",
}

CITIES = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"]

# ---------------------------------------------------------------------------
# Trouble data
# ---------------------------------------------------------------------------
ORTHO_TROUBLES = {
    "dyslexie": {
        "name": "Dyslexie",
        "full_name": "Dyslexie",
        "definition": "Trouble spécifique de l'apprentissage de la lecture affectant le décodage et la compréhension écrite.",
        "symptoms": [
            ("Confusion de lettres", "Votre enfant confond régulièrement des lettres visuellement proches comme b/d, p/q, ou m/n, rendant la lecture laborieuse."),
            ("Lecture lente et saccadée", "La lecture à voix haute est hésitante, syllabe par syllabe, avec de nombreuses erreurs de déchiffrage."),
            ("Fatigue lors de la lecture", "Après quelques minutes de lecture, votre enfant montre des signes de fatigue intense, se frotte les yeux ou refuse de continuer."),
            ("Difficulté de compréhension écrite", "Malgré un bon niveau oral, la compréhension de textes écrits reste difficile car l'énergie est mobilisée par le déchiffrage."),
        ],
        "approach": "Notre prise en charge de la dyslexie repose sur le renforcement de la conscience phonologique, l'entraînement au déchiffrage par des méthodes multisensorielles et l'utilisation d'outils visuels adaptés. Les séances en ligne permettent d'utiliser des supports interactifs particulièrement efficaces.",
        "faq": [
            ("À quel âge peut-on diagnostiquer une dyslexie ?", "Le diagnostic de dyslexie est généralement posé à partir de la fin du CE1 (7-8 ans), lorsqu'un retard de lecture significatif est constaté malgré un enseignement adapté. Toutefois, des signes d'alerte peuvent être repérés dès la maternelle."),
            ("La dyslexie peut-elle être corrigée ?", "La dyslexie ne se guérit pas, mais une rééducation orthophonique adaptée permet de développer des stratégies compensatoires très efficaces. Plus la prise en charge est précoce, meilleurs sont les résultats."),
            ("L'orthophonie en ligne est-elle efficace pour la dyslexie ?", "Oui, les études montrent que la télé-orthophonie est aussi efficace que les séances en présentiel pour la dyslexie. Les outils numériques interactifs offrent même des avantages supplémentaires pour l'entraînement à la lecture."),
        ],
    },
    "dysorthographie": {
        "name": "Dysorthographie",
        "full_name": "Dysorthographie",
        "definition": "Trouble spécifique de l'acquisition et de la maîtrise de l'orthographe, souvent associé à la dyslexie.",
        "symptoms": [
            ("Fautes persistantes", "Malgré les apprentissages répétés, les mêmes erreurs d'orthographe reviennent systématiquement dans les productions écrites."),
            ("Omission ou ajout de lettres", "Des lettres sont régulièrement oubliées ou ajoutées dans les mots, rendant l'écriture difficilement lisible."),
            ("Difficultés grammaticales", "Les accords, conjugaisons et règles grammaticales restent confus malgré un apprentissage régulier et soutenu."),
            ("Lenteur à l'écrit", "L'écriture demande un effort considérable, ce qui ralentit considérablement le rythme scolaire de l'enfant."),
        ],
        "approach": "Notre approche de la dysorthographie combine des stratégies de mémorisation visuelle, des règles orthographiques simplifiées et imagées, et des dictées adaptées progressives. En ligne, nous utilisons des applications d'écriture interactive qui rendent l'entraînement motivant.",
        "faq": [
            ("Quelle est la différence entre dyslexie et dysorthographie ?", "La dyslexie touche principalement la lecture tandis que la dysorthographie concerne l'orthographe. Elles sont souvent associées, mais un enfant peut être dysorthographique sans être dyslexique."),
            ("Combien de temps dure la rééducation de la dysorthographie ?", "La durée varie selon la sévérité du trouble, généralement entre 1 et 3 ans à raison d'une à deux séances hebdomadaires. Les progrès sont visibles dès les premiers mois."),
            ("Mon enfant fait beaucoup de fautes, est-ce forcément une dysorthographie ?", "Pas nécessairement. Un bilan orthophonique complet permet de distinguer un simple retard d'acquisition d'un véritable trouble spécifique de l'orthographe."),
        ],
    },
    "dyscalculie": {
        "name": "Dyscalculie",
        "full_name": "Dyscalculie",
        "definition": "Trouble spécifique des apprentissages numériques touchant la compréhension des nombres et le calcul.",
        "symptoms": [
            ("Difficulté à comprendre les quantités", "Votre enfant peine à estimer des quantités, à comparer des nombres ou à comprendre la notion de « plus que » et « moins que »."),
            ("Confusion des signes mathématiques", "Les symboles +, -, × et ÷ sont régulièrement confondus, entraînant des erreurs de calcul systématiques."),
            ("Problèmes de logique numérique", "La résolution de problèmes mathématiques, même simples, reste un défi majeur car la logique numérique sous-jacente n'est pas intuitive."),
            ("Difficulté à mémoriser les tables", "Les tables de multiplication et d'addition ne « restent pas », malgré des révisions répétées et des efforts importants."),
        ],
        "approach": "Notre rééducation de la dyscalculie s'appuie sur la manipulation concrète d'objets virtuels, des supports visuels interactifs et des jeux mathématiques ludiques. L'environnement numérique de la télé-orthophonie est particulièrement adapté à cette prise en charge.",
        "faq": [
            ("La dyscalculie est-elle courante ?", "La dyscalculie touche environ 5 à 7 % des enfants. Elle est aussi fréquente que la dyslexie mais reste moins connue et souvent sous-diagnostiquée."),
            ("L'orthophoniste prend-il en charge la dyscalculie ?", "Oui, la rééducation logico-mathématique fait partie du champ de compétences de l'orthophoniste. Un bilan spécifique permet d'évaluer les compétences numériques de l'enfant."),
            ("Mon enfant est nul en maths, est-ce une dyscalculie ?", "Des difficultés en mathématiques ne signifient pas automatiquement une dyscalculie. Un bilan orthophonique permettra de différencier un retard d'apprentissage d'un trouble spécifique."),
        ],
    },
    "dysphasie": {
        "name": "Dysphasie",
        "full_name": "Dysphasie (Trouble Développemental du Langage)",
        "definition": "Trouble développemental du langage oral affectant l'expression et/ou la compréhension, sans cause identifiable (auditive, neurologique ou intellectuelle).",
        "symptoms": [
            ("Retard de parole significatif", "À 3 ans, l'enfant ne forme pas de phrases de plus de 2 mots et son langage est difficilement compréhensible par l'entourage."),
            ("Difficulté à construire des phrases", "L'enfant utilise des phrases courtes, mal structurées, avec des erreurs de syntaxe persistantes bien au-delà de l'âge normal."),
            ("Vocabulaire limité", "Le stock lexical est nettement inférieur à celui des enfants du même âge, l'enfant « cherche ses mots » fréquemment."),
            ("Compréhension altérée", "Les consignes complexes ou les phrases longues ne sont pas bien comprises, l'enfant a besoin de reformulations constantes."),
        ],
        "approach": "La prise en charge de la dysphasie chez Logopsi Studios combine stimulation langagière intensive, supports visuels type pictogrammes et renforcement de la syntaxe par des exercices structurés. La régularité des séances en ligne facilite un suivi soutenu essentiel pour ce trouble.",
        "faq": [
            ("Quelle différence entre retard de langage et dysphasie ?", "Le retard de langage se rattrape avec le temps, tandis que la dysphasie est un trouble structurel durable qui nécessite une rééducation spécifique et prolongée."),
            ("La dysphasie affecte-t-elle l'intelligence ?", "Non, la dysphasie n'est pas liée à un déficit intellectuel. Les enfants dysphasiques ont une intelligence normale mais un langage qui ne se développe pas selon les étapes attendues."),
            ("La télé-orthophonie convient-elle pour la dysphasie ?", "Oui, à condition d'utiliser des outils adaptés. Nos orthophonistes utilisent des supports visuels numériques, des jeux interactifs et des pictogrammes en ligne qui rendent les séances très efficaces."),
        ],
    },
    "begaiement": {
        "name": "Bégaiement",
        "full_name": "Bégaiement",
        "definition": "Trouble de la fluence verbale caractérisé par des interruptions involontaires du flux de parole.",
        "symptoms": [
            ("Répétitions de sons ou syllabes", "L'enfant répète involontairement des sons (« b-b-b-bonjour ») ou des syllabes (« pa-pa-papa ») au début ou au milieu des mots."),
            ("Blocages", "La parole se « bloque » : l'enfant ouvre la bouche mais aucun son ne sort pendant quelques secondes, créant une tension visible."),
            ("Prolongations", "Certains sons sont anormalement allongés (« sssssalut »), perturbant le rythme naturel de la parole."),
            ("Tension musculaire", "Des crispations du visage, des mouvements de la mâchoire ou des clignements des yeux accompagnent les moments de bégaiement."),
        ],
        "approach": "Notre approche du bégaiement combine techniques de fluence (parole ralentie, respiration diaphragmatique), gestion du stress communicationnel et travail sur le rythme de la parole. Les séances en ligne offrent un cadre confortable et sécurisant pour l'enfant.",
        "faq": [
            ("Le bégaiement disparaît-il tout seul ?", "Chez les jeunes enfants (avant 5 ans), un bégaiement peut être transitoire. Cependant, si le trouble persiste au-delà de 6 mois, une consultation orthophonique est recommandée pour éviter qu'il ne se chronicise."),
            ("Le stress cause-t-il le bégaiement ?", "Le stress n'est pas la cause du bégaiement, qui a des origines neurologiques, mais il peut l'aggraver. La rééducation travaille aussi sur la gestion des émotions liées à la parole."),
            ("Les séances en ligne fonctionnent-elles pour le bégaiement ?", "Absolument. Le cadre de la maison est souvent plus rassurant pour l'enfant qui bégaie, ce qui facilite le travail thérapeutique. Les exercices de fluence se pratiquent très bien en visioconférence."),
        ],
    },
    "tsa": {
        "name": "TSA",
        "full_name": "Trouble du Spectre de l'Autisme (TSA)",
        "definition": "Trouble neurodéveloppemental affectant la communication sociale et les interactions, avec des comportements répétitifs ou restreints.",
        "symptoms": [
            ("Difficulté dans les interactions sociales", "L'enfant a du mal à comprendre les codes sociaux, le tour de rôle dans la conversation, et les intentions d'autrui."),
            ("Langage atypique", "Le langage peut être absent, en retard, ou présenter des particularités : ton monotone, inversion pronominale, langage formel ou pédant."),
            ("Écholalie", "L'enfant répète des mots, phrases ou passages entendus (dans un film, une chanson) de manière différée ou immédiate, hors contexte."),
            ("Compréhension littérale", "Les expressions figurées, l'humour, l'ironie et le second degré sont difficiles à comprendre pour l'enfant."),
        ],
        "approach": "Notre accompagnement orthophonique du TSA utilise la communication augmentée et alternative (PECS, Makaton), les scénarios sociaux structurés et la structuration visuelle des apprentissages. Les séances en ligne permettent d'intégrer l'environnement familier de l'enfant.",
        "faq": [
            ("Un enfant autiste peut-il suivre des séances en ligne ?", "Oui, de nombreux enfants avec TSA s'adaptent très bien aux séances en ligne. L'environnement familier et la médiation par l'écran peuvent même faciliter l'interaction pour certains profils."),
            ("Quel est le rôle de l'orthophoniste dans le TSA ?", "L'orthophoniste travaille sur le développement de la communication fonctionnelle : compréhension, expression orale, pragmatique du langage, et mise en place de moyens de communication alternatifs si nécessaire."),
            ("À quel âge commencer l'orthophonie pour un enfant TSA ?", "Le plus tôt possible. L'intervention précoce (avant 3 ans) donne les meilleurs résultats. Dès qu'un retard de communication est suspecté, une consultation est recommandée."),
        ],
    },
    "oralite-alimentaire": {
        "name": "Troubles de l'oralité alimentaire",
        "full_name": "Troubles de l'oralité alimentaire",
        "definition": "Ensemble de difficultés liées à l'alimentation, touchant la sphère orale et impactant la nutrition et le repas en famille.",
        "symptoms": [
            ("Refus alimentaires", "L'enfant refuse catégoriquement certains aliments ou textures, rendant les repas conflictuels et stressants pour toute la famille."),
            ("Hypersensibilité buccale", "Le moindre contact avec certaines textures dans la bouche provoque des réactions de dégoût, de rejet ou de détresse chez l'enfant."),
            ("Nausées et haut-le-cœur", "La vue, l'odeur ou le contact de certains aliments déclenche des nausées ou des réflexes nauséeux disproportionnés."),
            ("Répertoire alimentaire restreint", "L'enfant n'accepte qu'un nombre très limité d'aliments (parfois moins de 10), souvent de même couleur ou texture."),
        ],
        "approach": "Notre prise en charge des troubles de l'oralité alimentaire repose sur une désensibilisation progressive et respectueuse, une approche sensorielle ludique et une guidance parentale active. Les séances en ligne permettent de travailler directement dans l'environnement alimentaire de l'enfant.",
        "faq": [
            ("Mon enfant est-il juste « difficile » à table ?", "Un enfant sélectif qui mange au moins 20 aliments différents est dans la norme. En dessous, ou si les repas sont source de grande détresse, il peut s'agir d'un trouble de l'oralité nécessitant un accompagnement."),
            ("L'orthophonie aide-t-elle pour les problèmes alimentaires ?", "Oui, l'orthophoniste est le spécialiste de la sphère orale. Il intervient sur la motricité buccale, la sensibilité orale et les réflexes de déglutition liés à l'alimentation."),
            ("Comment se passe une séance en ligne pour l'oralité ?", "Les séances se déroulent souvent à l'heure du repas ou du goûter, dans la cuisine familiale. L'orthophoniste guide les parents en direct pour les exercices de désensibilisation et d'exploration alimentaire."),
        ],
    },
    "surdite": {
        "name": "Surdité",
        "full_name": "Surdité et troubles de l'audition",
        "definition": "Déficience auditive congénitale ou acquise impactant le développement du langage oral et la communication.",
        "symptoms": [
            ("Retard de langage", "L'enfant malentendant présente souvent un retard dans l'apparition des premiers mots et des premières phrases."),
            ("Difficulté d'articulation", "Certains sons sont déformés ou absents car l'enfant ne les perçoit pas correctement et ne peut les reproduire fidèlement."),
            ("Incompréhension dans le bruit", "En milieu bruyant (cantine, cour de récréation), l'enfant ne comprend plus les conversations et se retrouve en difficulté."),
            ("Isolement social", "Les difficultés de communication peuvent entraîner un repli sur soi et des difficultés à nouer des amitiés avec les pairs."),
        ],
        "approach": "Notre rééducation auditive combine entraînement perceptif, lecture labiale, introduction au langage signé selon les besoins, et optimisation de l'appareillage auditif. Les outils numériques de la télé-orthophonie offrent un excellent support pour le travail auditif.",
        "faq": [
            ("L'orthophonie en ligne convient-elle aux enfants sourds ?", "Oui, avec un équipement adapté (casque de qualité, micro), les séances en ligne fonctionnent très bien. Le format numérique permet même d'ajuster finement les paramètres sonores des exercices."),
            ("Mon enfant porte des appareils auditifs, a-t-il besoin d'orthophonie ?", "L'appareillage ne suffit pas toujours : l'orthophonie aide l'enfant à « apprendre à écouter » avec ses appareils et à développer son langage oral de manière optimale."),
            ("Quand commencer l'orthophonie après un diagnostic de surdité ?", "Dès le diagnostic, quel que soit l'âge. La stimulation précoce du langage est essentielle pour le développement cognitif et social de l'enfant malentendant."),
        ],
    },
    "paralysie-cerebrale": {
        "name": "Paralysie Cérébrale",
        "full_name": "Paralysie Cérébrale (IMC)",
        "definition": "Atteinte neurologique survenue pendant la période périnatale, affectant la motricité et pouvant impacter le langage et la déglutition.",
        "symptoms": [
            ("Dysarthrie", "La parole est rendue difficile par un manque de contrôle des muscles de la bouche, de la langue et du larynx, affectant l'intelligibilité."),
            ("Difficulté de déglutition", "L'alimentation peut être compliquée par des troubles de la coordination des muscles impliqués dans la mastication et la déglutition."),
            ("Troubles de la motricité fine buccale", "Les mouvements précis de la langue, des lèvres et des joues sont altérés, impactant l'articulation et l'alimentation."),
        ],
        "approach": "Notre prise en charge de la paralysie cérébrale inclut la rééducation oro-faciale, la mise en place de communication alternative et augmentative, et l'adaptation posturale en collaboration avec l'équipe pluridisciplinaire. Les séances en ligne facilitent le suivi régulier dans l'environnement habituel de l'enfant.",
        "faq": [
            ("Un enfant avec paralysie cérébrale peut-il progresser en langage ?", "Oui, avec une rééducation adaptée et régulière, des progrès significatifs sont possibles en communication, qu'il s'agisse de langage oral ou de communication alternative."),
            ("Quels outils de communication alternative utilisez-vous ?", "Nous utilisons des tableaux de communication, des applications de synthèse vocale, le Makaton et d'autres supports visuels adaptés au profil de chaque enfant."),
            ("La télé-orthophonie est-elle adaptée pour la paralysie cérébrale ?", "Oui, elle permet un suivi fréquent et régulier dans l'environnement naturel de l'enfant. Les parents sont accompagnés pour poursuivre les exercices au quotidien."),
        ],
    },
    "fente-palatine": {
        "name": "Fente palatine",
        "full_name": "Fente palatine (Fente labio-palatine)",
        "definition": "Malformation congénitale de la lèvre et/ou du palais nécessitant une prise en charge chirurgicale et orthophonique coordonnée.",
        "symptoms": [
            ("Nasalisation", "La voix et certains sons prennent une résonance nasale excessive car l'air s'échappe par le nez lors de la parole."),
            ("Troubles articulatoires", "Certains sons, notamment les occlusives (p, b, t, d) et les fricatives (f, s, ch), sont déformés ou remplacés par d'autres."),
            ("Reflux nasal", "Lors de l'alimentation, du liquide ou des aliments peuvent remonter par le nez, signe d'une insuffisance vélo-pharyngée."),
            ("Voix nasonnée", "La qualité vocale est altérée avec un timbre nasal caractéristique qui peut persister après la chirurgie sans rééducation."),
        ],
        "approach": "Notre rééducation post-fente palatine comprend un travail vélo-pharyngé ciblé, des exercices articulatoires progressifs et un suivi post-chirurgical coordonné avec l'équipe médicale. Les séances en ligne permettent de maintenir un suivi rapproché entre les rendez-vous hospitaliers.",
        "faq": [
            ("Quand commencer l'orthophonie après chirurgie de la fente ?", "La rééducation orthophonique débute généralement quelques semaines après la chirurgie du palais (vers 12-18 mois), en commençant par la stimulation du langage oral."),
            ("La nasalisation disparaît-elle après la chirurgie ?", "La chirurgie corrige la structure anatomique, mais la rééducation orthophonique est souvent nécessaire pour apprendre à l'enfant à utiliser correctement son palais réparé."),
            ("L'orthophonie en ligne est-elle possible pour la fente palatine ?", "Oui, les exercices articulatoires et le travail vélo-pharyngé se pratiquent très bien en visioconférence. C'est un complément précieux entre les consultations hospitalières."),
        ],
    },
    "trisomie-21": {
        "name": "Trisomie 21",
        "full_name": "Trisomie 21",
        "definition": "Anomalie chromosomique (présence de 3 chromosomes 21) nécessitant un accompagnement orthophonique précoce et prolongé du développement langagier.",
        "symptoms": [
            ("Retard de langage", "Les premières étapes du langage (babillage, premiers mots, premières phrases) apparaissent avec un décalage par rapport au développement typique."),
            ("Hypotonie buccale", "Le tonus musculaire réduit au niveau de la bouche impacte l'articulation, la mastication et la déglutition."),
            ("Difficulté de compréhension", "La compréhension du langage oral peut être limitée, nécessitant des supports visuels et des consignes simplifiées."),
            ("Trouble articulatoire", "Les sons sont souvent déformés ou simplifiés en raison de particularités anatomiques et de l'hypotonie."),
        ],
        "approach": "Notre accompagnement de la trisomie 21 repose sur une stimulation précoce du langage, l'utilisation du Makaton comme soutien à la communication, le renforcement musculaire buccal et la mise en place d'une communication multimodale. La télé-orthophonie permet un suivi régulier impliquant activement les parents.",
        "faq": [
            ("À quel âge commencer l'orthophonie pour un enfant trisomique ?", "L'accompagnement orthophonique devrait commencer dès les premiers mois de vie, bien avant l'apparition du langage, pour stimuler la motricité buccale et la communication préverbale."),
            ("Le Makaton, c'est quoi ?", "Le Makaton est un programme d'aide à la communication associant gestes, pictogrammes et parole. Il facilite la compréhension et l'expression chez les enfants dont le langage oral tarde à se développer."),
            ("La télé-orthophonie est-elle adaptée pour la trisomie 21 ?", "Oui, les séances en ligne fonctionnent très bien, surtout avec la participation active des parents. L'environnement familier et les outils numériques ludiques favorisent l'engagement de l'enfant."),
        ],
    },
}

PSY_TROUBLES = {
    "tdah": {
        "name": "TDAH",
        "full_name": "TDAH (Trouble de l'Attention avec/sans Hyperactivité)",
        "definition": "Trouble neurodéveloppemental caractérisé par l'inattention, l'impulsivité et/ou l'hyperactivité, impactant la vie scolaire et familiale.",
        "symptoms": [
            ("Inattention et distractibilité", "L'enfant a du mal à maintenir son attention sur une tâche, se laisse facilement distraire par les stimuli environnants et perd fréquemment ses affaires."),
            ("Impulsivité", "Il agit avant de réfléchir, coupe la parole, a du mal à attendre son tour et prend des décisions précipitées sans en mesurer les conséquences."),
            ("Agitation motrice", "L'enfant ne tient pas en place, se tortille sur sa chaise, court ou grimpe dans des situations inappropriées et semble « monté sur ressorts »."),
            ("Difficulté d'organisation", "Les devoirs, les affaires scolaires et les routines quotidiennes sont sources de chaos : oublis fréquents, planification défaillante."),
        ],
        "approach": "Notre accompagnement du TDAH combine des stratégies de régulation attentionnelle et émotionnelle, une thérapie cognitivo-comportementale adaptée et une guidance parentale outillée. Les séances en ligne sont particulièrement adaptées car l'enfant évolue dans son environnement habituel.",
        "faq": [
            ("Le TDAH est-il un manque de volonté ?", "Non, le TDAH est un trouble neurobiologique réel qui affecte les fonctions exécutives du cerveau. L'enfant ne choisit pas d'être inattentif ou agité. Un accompagnement adapté l'aide à développer des stratégies compensatoires."),
            ("Mon enfant a-t-il besoin de médicaments ?", "La médication n'est pas systématique dans le TDAH. Un psychologue peut mettre en place des stratégies comportementales efficaces. La décision de médicamenter relève du médecin et se fait au cas par cas."),
            ("Les séances en ligne conviennent-elles à un enfant TDAH ?", "Oui, les séances en ligne peuvent être très efficaces grâce à des supports interactifs variés. Les séances sont adaptées (durée, pauses) pour maintenir l'attention de l'enfant."),
        ],
    },
    "hpi": {
        "name": "HPI",
        "full_name": "HPI (Haut Potentiel Intellectuel)",
        "definition": "Fonctionnement intellectuel significativement supérieur à la norme (QI ≥ 130), pouvant s'accompagner de difficultés émotionnelles et relationnelles.",
        "symptoms": [
            ("Décalage avec les pairs", "L'enfant HPI se sent différent de ses camarades, a des centres d'intérêt atypiques pour son âge et peut avoir du mal à trouver sa place dans le groupe."),
            ("Hypersensibilité émotionnelle", "Les émotions sont vécues avec une intensité extrême : un commentaire anodin peut provoquer une crise de larmes, l'injustice déclenche une colère profonde."),
            ("Ennui scolaire et démotivation", "L'enfant s'ennuie en classe, peut devenir perturbateur ou au contraire se replier sur lui-même. Ses résultats ne reflètent pas son potentiel."),
            ("Perfectionnisme et anxiété de performance", "La peur de l'échec peut paralyser l'enfant qui préfère ne pas essayer plutôt que de risquer de ne pas être parfait."),
        ],
        "approach": "Notre accompagnement du HPI se concentre sur l'aide émotionnelle, le développement de stratégies d'adaptation sociale, et le travail sur l'estime de soi. Nous aidons l'enfant à comprendre et accepter son fonctionnement différent comme une force.",
        "faq": [
            ("HPI signifie-t-il forcément réussite scolaire ?", "Non, de nombreux enfants HPI sont en échec scolaire. Leur mode de pensée différent (pensée en arborescence, besoin de sens) peut être incompatible avec l'enseignement classique sans adaptation."),
            ("Comment savoir si mon enfant est HPI ?", "Un bilan psychométrique (test de QI type WISC) réalisé par un psychologue est le seul moyen fiable de confirmer un HPI. Les signes peuvent inclure une curiosité intense, un langage précoce et une sensibilité exacerbée."),
            ("Un suivi psychologique est-il nécessaire pour un enfant HPI ?", "Pas systématiquement, mais si l'enfant souffre (difficultés relationnelles, anxiété, démotivation), un accompagnement psychologique l'aide à mieux vivre sa différence et à développer ses compétences socio-émotionnelles."),
        ],
    },
    "phobie-scolaire": {
        "name": "Phobie Scolaire",
        "full_name": "Phobie Scolaire",
        "definition": "Refus scolaire anxieux caractérisé par une incapacité émotionnelle à se rendre à l'école, malgré la volonté de l'enfant.",
        "symptoms": [
            ("Anxiété intense", "L'enfant manifeste une détresse majeure à l'idée d'aller à l'école : pleurs, supplications, voire crises de panique le matin."),
            ("Maux somatiques", "Maux de ventre, maux de tête, nausées ou vomissements apparaissent les jours d'école et disparaissent le week-end ou pendant les vacances."),
            ("Crises de panique", "Des attaques de panique surviennent à l'approche de l'école ou en classe : tachycardie, sensation d'étouffement, tremblements."),
            ("Isolement progressif", "L'enfant se coupe de ses amis, refuse les sorties et passe de plus en plus de temps dans sa chambre."),
        ],
        "approach": "Notre prise en charge de la phobie scolaire combine une désensibilisation progressive, une TCC adaptée, un travail collaboratif avec la famille et l'école, et un plan de retour progressif en milieu scolaire. Les séances en ligne sont un atout majeur car l'enfant peut commencer la thérapie depuis son espace sécurisant.",
        "faq": [
            ("Mon enfant refuse d'aller à l'école, est-ce de la paresse ?", "Non, la phobie scolaire est un trouble anxieux réel. L'enfant n'est pas fainéant : il est dans l'incapacité émotionnelle de se rendre à l'école. Forcer ne fait qu'aggraver l'anxiété."),
            ("Combien de temps faut-il pour surmonter une phobie scolaire ?", "La durée varie de quelques semaines à plusieurs mois. Un accompagnement précoce et une collaboration école-famille-thérapeute sont les clés d'une résolution plus rapide."),
            ("La thérapie en ligne est-elle efficace pour la phobie scolaire ?", "C'est même un format idéal : l'enfant déscolarisé peut consulter facilement depuis chez lui, sans la contrainte d'un déplacement qui pourrait déclencher de l'anxiété."),
        ],
    },
    "harcelement-scolaire": {
        "name": "Harcèlement Scolaire",
        "full_name": "Harcèlement Scolaire et Cyberharcèlement",
        "definition": "Violence répétée (physique, verbale ou en ligne) en milieu scolaire, ayant des conséquences psychologiques graves sur la victime.",
        "symptoms": [
            ("Repli sur soi", "L'enfant se referme, ne parle plus de sa journée, évite les interactions et passe de plus en plus de temps seul dans sa chambre."),
            ("Troubles du sommeil", "Des difficultés d'endormissement, des cauchemars ou des réveils nocturnes apparaissent en lien avec l'anxiété générée par le harcèlement."),
            ("Baisse des résultats scolaires", "Les notes chutent car l'enfant n'arrive plus à se concentrer, submergé par le stress et la peur liés au harcèlement."),
            ("Changement de comportement", "L'enfant devient irritable, agressif ou au contraire excessivement docile. Il peut refuser d'aller à l'école ou réclamer un changement d'établissement."),
        ],
        "approach": "Notre accompagnement du harcèlement scolaire offre un soutien psychologique pour reconstruire l'estime de soi, des techniques de renforcement de l'affirmation de soi, un accompagnement dans la médiation scolaire et une guidance parentale. La confidentialité des séances en ligne est un atout pour les enfants victimes.",
        "faq": [
            ("Comment savoir si mon enfant est harcelé ?", "Les signes incluent un repli soudain, des affaires abîmées, une aversion nouvelle pour l'école, des troubles du sommeil et un changement d'humeur. L'enfant ne verbalise pas toujours le harcèlement."),
            ("Que faire si je soupçonne un harcèlement ?", "Écoutez votre enfant sans minimiser, contactez l'établissement scolaire, et consultez un psychologue pour évaluer l'impact émotionnel et accompagner votre enfant."),
            ("Les séances en ligne sont-elles adaptées après un harcèlement ?", "Oui, le cadre sécurisant du domicile et la confidentialité de la visioconférence facilitent la parole de l'enfant. C'est un format particulièrement adapté pour les victimes de cyberharcèlement."),
        ],
    },
    "anxiete": {
        "name": "Troubles de l'Anxiété",
        "full_name": "Troubles de l'Anxiété et Angoisse",
        "definition": "Ensemble de troubles caractérisés par une anxiété excessive et persistante chez l'enfant ou l'adolescent, impactant le quotidien.",
        "symptoms": [
            ("Inquiétude excessive", "L'enfant s'inquiète de manière disproportionnée pour tout : l'école, la santé de ses proches, les catastrophes naturelles, son avenir."),
            ("Troubles du sommeil", "L'endormissement est difficile car l'enfant rumine, les réveils nocturnes sont fréquents et le sommeil n'est pas réparateur."),
            ("Irritabilité", "L'anxiété se manifeste par de l'irritabilité, des colères soudaines ou une intolérance à la frustration qui surprend l'entourage."),
            ("Somatisations", "L'anxiété s'exprime par le corps : maux de ventre récurrents, maux de tête, tensions musculaires, nausées sans cause médicale identifiée."),
        ],
        "approach": "Notre prise en charge des troubles anxieux utilise la TCC adaptée à l'enfant, des techniques de relaxation et de pleine conscience, l'exposition progressive aux situations anxiogènes et un travail sur les pensées automatiques. Le format en ligne permet des séances régulières dans un cadre rassurant.",
        "faq": [
            ("L'anxiété chez l'enfant est-elle normale ?", "Une certaine dose d'anxiété est normale et même utile. Cependant, quand l'anxiété est permanente, intense et empêche l'enfant de vivre normalement, un accompagnement est nécessaire."),
            ("Mon enfant a des crises d'angoisse, que faire ?", "Restez calme, aidez-le à respirer lentement et rassurez-le. Si les crises se répètent, consultez un psychologue qui pourra lui apprendre des techniques de gestion et identifier les facteurs déclencheurs."),
            ("La TCC en ligne fonctionne-t-elle pour l'anxiété ?", "La TCC en ligne a fait la preuve de son efficacité dans de nombreuses études. Le format visio permet les mêmes exercices qu'en cabinet, avec l'avantage d'un cadre familier pour l'enfant."),
        ],
    },
    "depression": {
        "name": "Dépression",
        "full_name": "Dépression (Enfant/Adolescent)",
        "definition": "Trouble de l'humeur caractérisé par une tristesse persistante, une perte d'intérêt et un ralentissement global chez l'enfant ou l'adolescent.",
        "symptoms": [
            ("Tristesse persistante", "L'enfant semble triste en permanence, pleure souvent ou exprime un sentiment de vide, de désespoir ou d'inutilité."),
            ("Perte d'intérêt", "Les activités qui passionnaient l'enfant (sport, jeux, amis) ne l'intéressent plus. Il refuse les invitations et reste passif."),
            ("Fatigue et ralentissement", "L'enfant est constamment fatigué, manque d'énergie même après une bonne nuit, et ses mouvements semblent ralentis."),
            ("Troubles du sommeil et de l'appétit", "Insomnie ou hypersomnie, perte d'appétit ou au contraire alimentation compulsive sont des signaux d'alerte importants."),
        ],
        "approach": "Notre accompagnement de la dépression chez l'enfant repose sur la psychothérapie, l'activation comportementale (réintroduction progressive d'activités plaisantes), le travail émotionnel et le soutien familial. Les séances en ligne facilitent le maintien du suivi même quand l'enfant a du mal à sortir de chez lui.",
        "faq": [
            ("Un enfant peut-il vraiment être dépressif ?", "Oui, la dépression peut toucher les enfants dès 5-6 ans. Elle se manifeste parfois différemment que chez l'adulte : irritabilité, troubles du comportement, plaintes somatiques."),
            ("Comment distinguer tristesse normale et dépression ?", "La tristesse est passagère et liée à un événement. La dépression dure plus de 2 semaines, n'a pas toujours de cause identifiable et impacte le fonctionnement global de l'enfant."),
            ("Les séances en ligne sont-elles efficaces pour la dépression ?", "Oui, les études montrent une efficacité comparable au présentiel. Pour l'enfant dépressif qui a du mal à sortir, le format en ligne lève un obstacle majeur à la prise en charge."),
        ],
    },
    "tca": {
        "name": "TCA",
        "full_name": "Troubles du Comportement Alimentaire (TCA)",
        "definition": "Ensemble de troubles (anorexie, boulimie, hyperphagie) caractérisés par un rapport pathologique à l'alimentation et à l'image corporelle.",
        "symptoms": [
            ("Restriction alimentaire", "L'enfant ou l'adolescent réduit progressivement ses apports alimentaires, élimine des catégories entières d'aliments ou saute des repas."),
            ("Comportements compensatoires", "Des comportements comme l'exercice physique excessif, les vomissements provoqués ou l'usage de laxatifs apparaissent pour « compenser » les prises alimentaires."),
            ("Préoccupation excessive du poids", "L'enfant se pèse fréquemment, commente son corps négativement et compare constamment son physique à celui des autres."),
            ("Distorsion de l'image corporelle", "Malgré un poids normal ou insuffisant, l'enfant se perçoit comme « trop gros » et refuse de croire les observations de l'entourage."),
        ],
        "approach": "Notre approche des TCA est pluridisciplinaire : TCC spécialisée, travail sur l'image de soi et l'estime de soi, déconstruction des pensées dysfonctionnelles sur l'alimentation et le corps, et guidance parentale active. Les séances en ligne offrent une souplesse précieuse pour le suivi régulier.",
        "faq": [
            ("Les TCA ne touchent-ils que les adolescentes ?", "Non, les TCA peuvent toucher les garçons comme les filles, et des enfants de plus en plus jeunes sont concernés. Les formes cliniques varient selon l'âge et le sexe."),
            ("Comment aborder le sujet avec mon enfant ?", "Exprimez votre inquiétude avec bienveillance, sans accusation ni commentaire sur le poids. Proposez un rendez-vous avec un professionnel en présentant cela comme un soutien, non une punition."),
            ("Un suivi en ligne est-il possible pour les TCA ?", "Oui, la thérapie en ligne est efficace pour les TCA, en complément d'un suivi médical pour la surveillance du poids et de la santé physique."),
        ],
    },
    "addictions-ecrans": {
        "name": "Addictions aux écrans",
        "full_name": "Addictions (Écrans, Réseaux sociaux, Jeux vidéo)",
        "definition": "Usage problématique des écrans, réseaux sociaux et jeux vidéo chez l'enfant et l'adolescent, impactant la vie sociale, scolaire et familiale.",
        "symptoms": [
            ("Usage excessif", "L'enfant passe un nombre d'heures déraisonnable devant les écrans, dépassant largement les recommandations pour son âge."),
            ("Irritabilité sans écran", "Quand on lui retire les écrans ou qu'il en est privé, l'enfant réagit par de la colère, de l'agressivité ou de l'anxiété intense."),
            ("Impact scolaire", "Les résultats scolaires chutent, les devoirs ne sont plus faits et l'enfant est épuisé en classe à cause de sessions nocturnes."),
            ("Isolement social", "L'enfant délaisse ses amis « réels », ses activités et sa famille au profit de ses interactions virtuelles."),
        ],
        "approach": "Notre accompagnement des addictions aux écrans repose sur une régulation progressive et négociée, la mise en place d'activités alternatives motivantes, l'établissement d'un contrat familial et un travail motivationnel avec l'adolescent. Le paradoxe thérapeutique de traiter l'addiction aux écrans en ligne est un levier de discussion intéressant.",
        "faq": [
            ("À partir de quand parle-t-on d'addiction aux écrans ?", "On parle d'addiction quand l'usage est incontrôlable, qu'il y a perte de contrôle du temps passé, que les autres activités sont délaissées et que l'arrêt provoque un mal-être significatif."),
            ("Comment limiter les écrans sans conflit ?", "La clé est la progressivité et la négociation : établir ensemble des règles claires, proposer des alternatives attrayantes et être cohérent dans l'application. Un psychologue peut vous accompagner dans cette démarche."),
            ("La thérapie en ligne n'est-elle pas contradictoire pour cette addiction ?", "Au contraire, utiliser l'écran de manière constructive (pour une thérapie) montre à l'enfant que l'écran peut être un outil positif. C'est un point de départ intéressant pour le travail thérapeutique."),
        ],
    },
    "troubles-sommeil": {
        "name": "Troubles du Sommeil",
        "full_name": "Troubles du Sommeil",
        "definition": "Ensemble de difficultés liées au sommeil chez l'enfant : endormissement, maintien du sommeil, parasomnies, impactant la vie diurne.",
        "symptoms": [
            ("Endormissement difficile", "L'enfant met plus de 30 minutes à s'endormir, a besoin de la présence d'un parent ou manifeste de l'anxiété au moment du coucher."),
            ("Réveils nocturnes", "L'enfant se réveille une ou plusieurs fois par nuit, vient dans le lit parental ou appelle ses parents, perturbant le sommeil de toute la famille."),
            ("Cauchemars et terreurs nocturnes", "Des cauchemars fréquents ou des épisodes de terreur nocturne (cris, agitation sans réveil) perturbent la qualité du sommeil."),
            ("Fatigue diurne", "L'enfant est fatigué en journée, a du mal à se concentrer en classe, bâille fréquemment et peut s'endormir dans des situations inadaptées."),
        ],
        "approach": "Notre prise en charge des troubles du sommeil combine des techniques d'hygiène du sommeil, des exercices de relaxation adaptés à l'âge, la mise en place de routines apaisantes et la TCC de l'insomnie pour les plus grands. Les séances en ligne en soirée facilitent le travail sur les routines du coucher.",
        "faq": [
            ("Les troubles du sommeil de mon enfant sont-ils psychologiques ?", "Ils peuvent être d'origine psychologique (anxiété, stress), mais aussi liés à de mauvaises habitudes de sommeil ou à un trouble médical. Un bilan permet d'identifier la cause et d'adapter la prise en charge."),
            ("Comment aider mon enfant à mieux dormir ?", "Établissez une routine de coucher régulière, limitez les écrans 1h avant le coucher, assurez un environnement de sommeil calme et sombre, et évitez les activités stimulantes en soirée."),
            ("La consultation en ligne est-elle adaptée pour les troubles du sommeil ?", "Oui, le format en ligne permet même de planifier des séances en fin de journée pour travailler concrètement sur la routine du coucher avec l'enfant et ses parents."),
        ],
    },
    "enuresie": {
        "name": "Énurésie et Encoprésie",
        "full_name": "Énurésie et Encoprésie",
        "definition": "Troubles du contrôle sphinctérien (urinaire et/ou fécal) au-delà de l'âge habituel de la propreté, avec un retentissement psychologique important.",
        "symptoms": [
            ("Fuites urinaires nocturnes", "L'enfant de plus de 5 ans mouille son lit régulièrement (au moins 2 fois par semaine), sans parvenir à se réveiller pour aller aux toilettes."),
            ("Fuites diurnes", "Des accidents urinaires surviennent en journée, à l'école ou lors d'activités, source de grande honte pour l'enfant."),
            ("Souillures (encoprésie)", "Des souillures fécales involontaires se produisent chez un enfant de plus de 4 ans ayant acquis la propreté, souvent en lien avec une constipation chronique."),
            ("Impact psychologique", "L'enfant se sent honteux, évite les invitations chez les amis, les colonies de vacances et tout contexte où son trouble pourrait être découvert."),
        ],
        "approach": "Notre approche combine une dimension comportementale (calendrier mictionnel, alarmes, renforcement positif) et un travail émotionnel sur la honte et l'estime de soi. La guidance parentale est essentielle pour créer un environnement bienveillant et encourageant.",
        "faq": [
            ("L'énurésie est-elle fréquente ?", "Oui, l'énurésie nocturne touche environ 10 % des enfants de 6 ans et 5 % des enfants de 10 ans. C'est un trouble courant qui se résout dans la grande majorité des cas avec un accompagnement adapté."),
            ("Mon enfant fait pipi au lit exprès ?", "Non, l'énurésie n'est jamais volontaire. L'enfant ne peut pas contrôler ses sphincters pendant le sommeil. La punition est contre-productive et aggrave le problème."),
            ("La visioconférence convient-elle pour ce type de trouble ?", "Oui, le cadre confidentiel de la maison est même un avantage : l'enfant est dans son environnement et n'a pas à en parler dans une salle d'attente. Le psychologue accompagne aussi les parents dans leur posture."),
        ],
    },
    "traumatismes-deuil": {
        "name": "Traumatismes et Deuil",
        "full_name": "Traumatismes et Deuil",
        "definition": "Accompagnement psychologique de l'enfant confronté à un événement traumatique (accident, violence, séparation) ou au décès d'un proche.",
        "symptoms": [
            ("Flashbacks et reviviscences", "L'enfant revit l'événement traumatique de manière intrusive, par des images, des pensées ou des sensations qui s'imposent à lui."),
            ("Cauchemars récurrents", "Des cauchemars en lien avec le traumatisme ou le décès perturbent le sommeil, provoquant peur du coucher et fatigue."),
            ("Évitement", "L'enfant évite les lieux, personnes ou situations qui lui rappellent l'événement traumatique, limitant progressivement ses activités."),
            ("Régression", "L'enfant retourne à des comportements antérieurs : sucer son pouce, parler bébé, avoir peur du noir, refuser de dormir seul."),
        ],
        "approach": "Notre accompagnement post-traumatique utilise l'EMDR adapté à l'enfant, la thérapie par le jeu et le dessin, un travail d'expression émotionnelle et un soutien familial systémique. Les séances en ligne permettent à l'enfant de travailler dans son espace sécurisant, à son rythme.",
        "faq": [
            ("Mon enfant a-t-il besoin d'aide après un deuil ?", "Tous les enfants ne développent pas de trouble après un deuil, mais un accompagnement peut aider à traverser cette épreuve. Consultez si vous observez des changements de comportement durables ou une détresse importante."),
            ("L'EMDR est-il adapté aux enfants ?", "Oui, l'EMDR a été adapté pour les enfants avec des protocoles spécifiques utilisant le jeu, le dessin et des techniques adaptées à l'âge. C'est une méthode recommandée par la HAS pour le stress post-traumatique."),
            ("La thérapie en ligne peut-elle traiter un traumatisme ?", "Oui, la thérapie en ligne est efficace pour le trauma. L'enfant est dans son environnement sécurisant et les protocoles (EMDR, TCC) s'adaptent très bien au format visioconférence."),
        ],
    },
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Slug helpers
# ---------------------------------------------------------------------------
_SLUG_TABLE = str.maketrans(
    "àâäéèêëïîôùûüÿçœæÀÂÄÉÈÊËÏÎÔÙÛÜŸÇŒÆ",
    "aaaeeeeiioouuycoaAAEEEEIIOOUUYCOAA",
)


def slugify(text: str) -> str:
    """Produce a clean URL-safe slug from French text."""
    import re
    s = text.lower().translate(_SLUG_TABLE)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


# ---------------------------------------------------------------------------
# WordPress API helpers
# ---------------------------------------------------------------------------
def create_wp_page(
    title: str,
    slug: str,
    content: str,
    excerpt: str,
    parent: int = 0,
    dry_run: bool = False,
) -> Optional[int]:
    """Create a WordPress page via REST API. Returns page ID or None."""
    payload = {
        "title": title,
        "slug": slug,
        "content": content,
        "excerpt": excerpt,
        "status": "draft",
        "parent": parent,
    }
    if dry_run:
        log.info("  [DRY RUN] Would create page: %s (slug=%s, parent=%d)", title, slug, parent)
        return None

    for attempt in range(3):
        try:
            resp = requests.post(WP_API, headers=HEADERS, json=payload, timeout=30)
            if resp.status_code == 201:
                page_id = resp.json()["id"]
                log.info("  ✅ Created page #%d: %s", page_id, title)
                return page_id
            else:
                log.warning(
                    "  ⚠️  Attempt %d failed for '%s': HTTP %d – %s",
                    attempt + 1, title, resp.status_code, resp.text[:200],
                )
        except requests.RequestException as exc:
            log.warning("  ⚠️  Attempt %d network error for '%s': %s", attempt + 1, title, exc)
        time.sleep(2 * (attempt + 1))

    log.error("  ❌ Failed to create page after 3 attempts: %s", title)
    return None


# ---------------------------------------------------------------------------
# Content generation
# ---------------------------------------------------------------------------
SITE_NAME = "Logopsi Studios"
BOOKING_URL = "https://logopsiestudios.com/prendre-rendez-vous"


def _schema_medical_business(discipline: str) -> str:
    """Return schema.org MedicalBusiness JSON-LD."""
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "MedicalBusiness",
  "name": "{SITE_NAME}",
  "description": "{discipline} en ligne pour enfants et adolescents",
  "url": "https://logopsiestudios.com",
  "medicalSpecialty": "{discipline}",
  "availableService": {{
    "@type": "MedicalTherapy",
    "name": "{discipline} en ligne",
    "serviceType": "Téléconsultation"
  }},
  "areaServed": {{
    "@type": "Country",
    "name": "France"
  }}
}}
</script>"""


def _breadcrumb_html(crumbs: list[tuple[str, str]]) -> str:
    """Build breadcrumb HTML + schema.org BreadcrumbList."""
    items_html = []
    schema_items = []
    for i, (label, url) in enumerate(crumbs, 1):
        if i < len(crumbs):
            items_html.append(f'<a href="{url}" class="text-blue-600 hover:underline">{label}</a>')
        else:
            items_html.append(f'<span class="text-gray-500">{label}</span>')
        schema_items.append(f'{{"@type":"ListItem","position":{i},"name":"{label}","item":"{url}"}}')

    nav = ' <span class="text-gray-400 mx-1">&gt;</span> '.join(items_html)
    schema = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{",".join(schema_items)}]}}
</script>"""
    return f'<nav class="text-sm mb-6">{nav}</nav>\n{schema}'


def _cta_section() -> str:
    return f"""
<section class="bg-blue-50 rounded-2xl p-8 text-center my-12">
  <h2 class="text-2xl font-bold text-blue-900 mb-4">Prenez rendez-vous dès aujourd'hui</h2>
  <p class="text-gray-700 mb-6">Nos professionnels sont disponibles rapidement pour un premier bilan en ligne.</p>
  <a href="{BOOKING_URL}" class="inline-block bg-blue-600 text-white font-semibold px-8 py-3 rounded-full hover:bg-blue-700 transition">Réserver une consultation</a>
</section>"""


def _trust_badges() -> str:
    return """
<div class="flex flex-wrap gap-4 my-6">
  <span class="inline-flex items-center bg-green-50 text-green-700 px-4 py-2 rounded-full text-sm font-medium">⚡ Prise en charge rapide</span>
  <span class="inline-flex items-center bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-medium">💻 100% en ligne</span>
  <span class="inline-flex items-center bg-purple-50 text-purple-700 px-4 py-2 rounded-full text-sm font-medium">🎓 Professionnels diplômés</span>
  <span class="inline-flex items-center bg-yellow-50 text-yellow-700 px-4 py-2 rounded-full text-sm font-medium">👨‍👩‍👧 Guidance parentale incluse</span>
</div>"""


# ---- Pillar page content ------------------------------------------------
def generate_pillar_content(discipline: str, troubles: dict, slug_prefix: str) -> str:
    """Generate content for pillar pages (Orthophonie en ligne / Psychologie en ligne)."""
    if discipline == "Orthophonie":
        pro = "orthophoniste"
        intro = (
            "L'orthophonie en ligne chez Logopsi Studios, c'est un accès rapide à des "
            "orthophonistes diplômés, depuis chez vous. Nos professionnels accompagnent votre "
            "enfant dans la prise en charge de tous les troubles du langage, de la parole et de "
            "la communication, grâce à la télé-orthophonie."
        )
        city_pro = "Orthophoniste"
    else:
        pro = "psychologue"
        intro = (
            "La psychologie en ligne chez Logopsi Studios offre un accompagnement psychologique "
            "adapté aux enfants et adolescents, accessible partout en France. Nos psychologues "
            "diplômés prennent en charge les troubles émotionnels, comportementaux et relationnels "
            "via des séances de visioconférence interactives."
        )
        city_pro = "Psychologue enfant"

    # Trouble links
    trouble_links = ""
    for key, data in troubles.items():
        t_slug = f"{slug_prefix}-{slugify(data['name'])}"
        trouble_links += (
            f'<li class="mb-3"><a href="/{t_slug}/" class="text-blue-600 hover:underline font-medium">'
            f'{data["full_name"]}</a> – {data["definition"][:80]}…</li>\n'
        )

    # City links
    city_links = ""
    for city in CITIES:
        c_slug = f"{slugify(city_pro)}-{slugify(city)}"
        city_links += (
            f'<li class="mb-2"><a href="/{c_slug}/" class="text-blue-600 hover:underline">'
            f'{city_pro} à {city}</a></li>\n'
        )

    return f"""
{_schema_medical_business(discipline)}
<section class="max-w-4xl mx-auto">
  <h1 class="text-4xl font-extrabold text-blue-900 mb-6">{discipline} en ligne – {SITE_NAME}</h1>
  <p class="text-lg text-gray-700 mb-8">{intro}</p>
  {_trust_badges()}
  {_cta_section()}

  <h2 class="text-2xl font-bold text-blue-800 mt-12 mb-6">Nos prises en charge spécialisées</h2>
  <ul class="list-disc pl-6 space-y-2">
    {trouble_links}
  </ul>

  <h2 class="text-2xl font-bold text-blue-800 mt-12 mb-6">{discipline} par ville</h2>
  <p class="text-gray-700 mb-4">Consultez un {pro} en ligne depuis votre ville :</p>
  <ul class="list-disc pl-6 space-y-2">
    {city_links}
  </ul>

  {_cta_section()}
</section>"""


# ---- Trouble mother page content ----------------------------------------
def generate_trouble_mother_content(
    discipline: str,
    trouble_key: str,
    trouble_data: dict,
    slug_prefix: str,
) -> str:
    """Rich SEO content for a trouble mother page."""
    if discipline == "Orthophonie":
        pro = "Orthophoniste"
        pro_lower = "orthophoniste"
        pillar_slug = "orthophonie-en-ligne"
        pillar_label = "Orthophonie en ligne"
    else:
        pro = "Psychologue"
        pro_lower = "psychologue"
        pillar_slug = "psychologie-en-ligne"
        pillar_label = "Psychologie en ligne"

    name = trouble_data["name"]
    full_name = trouble_data["full_name"]
    definition = trouble_data["definition"]
    symptoms = trouble_data["symptoms"]
    approach = trouble_data["approach"]
    faqs = trouble_data["faq"]

    page_slug = f"{slug_prefix}-{slugify(name)}"

    breadcrumbs = [
        ("Accueil", "https://logopsiestudios.com"),
        (pillar_label, f"/{pillar_slug}/"),
        (full_name, f"/{page_slug}/"),
    ]

    # Symptom cards
    symptom_html = ""
    for title, desc in symptoms:
        symptom_html += f"""
<div class="bg-white rounded-xl shadow-sm border p-6 mb-4">
  <h3 class="text-lg font-semibold text-blue-900 mb-2">{title}</h3>
  <p class="text-gray-600">{desc}</p>
</div>"""

    # City links
    city_links_html = ""
    for city in CITIES:
        city_slug = f"{page_slug}-{slugify(city)}"
        city_links_html += (
            f'<li class="mb-2"><a href="/{city_slug}/" class="text-blue-600 hover:underline">'
            f'{pro} {name} à {city}</a></li>\n'
        )

    # FAQ
    faq_html = ""
    faq_schema_items = []
    for q, a in faqs:
        faq_html += f"""
<div class="border-b border-gray-200 py-4">
  <h3 class="text-lg font-semibold text-blue-900 mb-2">{q}</h3>
  <p class="text-gray-600">{a}</p>
</div>"""
        faq_schema_items.append(
            f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        )

    faq_schema = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join(faq_schema_items)}]}}
</script>"""

    return f"""
{_breadcrumb_html(breadcrumbs)}
{_schema_medical_business(discipline)}

<section class="max-w-4xl mx-auto">
  <!-- Hero -->
  <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-8 mb-10">
    <h1 class="text-3xl md:text-4xl font-extrabold text-blue-900 mb-4">{pro} spécialisé dans la {full_name} en ligne</h1>
    <p class="text-lg text-gray-700 mb-6">{definition} Chez {SITE_NAME}, nos {pro_lower}s diplômés accompagnent votre enfant avec des séances en visioconférence adaptées, interactives et efficaces.</p>
    <div class="flex flex-wrap gap-3">
      <a href="{BOOKING_URL}" class="inline-block bg-blue-600 text-white font-semibold px-6 py-3 rounded-full hover:bg-blue-700 transition">Prendre rendez-vous</a>
      <a href="/{pillar_slug}/" class="inline-block bg-white text-blue-600 font-semibold px-6 py-3 rounded-full border border-blue-200 hover:bg-blue-50 transition">En savoir plus</a>
    </div>
    {_trust_badges()}
  </div>

  <!-- Symptômes -->
  <h2 class="text-2xl font-bold text-blue-800 mb-6">Reconnaître les signes de la {name}</h2>
  <p class="text-gray-700 mb-6">Voici les principaux signes qui peuvent vous alerter et justifier une consultation avec un {pro_lower} spécialisé :</p>
  {symptom_html}

  <!-- Approche -->
  <h2 class="text-2xl font-bold text-blue-800 mt-10 mb-4">Notre approche de la {name}</h2>
  <p class="text-gray-700 mb-8">{approach}</p>

  <!-- Villes -->
  <h2 class="text-2xl font-bold text-blue-800 mt-10 mb-4">{pro} {name} par ville</h2>
  <p class="text-gray-700 mb-4">Consultez un {pro_lower} spécialisé en {name} depuis votre ville :</p>
  <ul class="list-disc pl-6 space-y-2 mb-8">
    {city_links_html}
  </ul>

  {_cta_section()}

  <!-- FAQ -->
  <h2 class="text-2xl font-bold text-blue-800 mt-10 mb-4">Questions fréquentes sur la {name}</h2>
  {faq_html}
  {faq_schema}
</section>"""


# ---- City mother page content -------------------------------------------
def generate_city_mother_content(
    discipline: str,
    city: str,
    troubles: dict,
    slug_prefix: str,
) -> str:
    """Content for city mother pages (e.g. Orthophoniste à Paris)."""
    if discipline == "Orthophonie":
        pro = "Orthophoniste"
        pro_lower = "orthophoniste"
        pillar_slug = "orthophonie-en-ligne"
        pillar_label = "Orthophonie en ligne"
        title_pro = "Orthophoniste"
    else:
        pro = "Psychologue enfant"
        pro_lower = "psychologue"
        pillar_slug = "psychologie-en-ligne"
        pillar_label = "Psychologie en ligne"
        title_pro = "Psychologue enfant"

    page_slug = f"{slugify(title_pro)}-{slugify(city)}"

    breadcrumbs = [
        ("Accueil", "https://logopsiestudios.com"),
        (pillar_label, f"/{pillar_slug}/"),
        (f"{title_pro} à {city}", f"/{page_slug}/"),
    ]

    # Trouble+city links
    links_html = ""
    for key, data in troubles.items():
        trouble_slug = f"{slug_prefix}-{slugify(data['name'])}-{slugify(city)}"
        links_html += (
            f'<li class="mb-2"><a href="/{trouble_slug}/" class="text-blue-600 hover:underline">'
            f'{pro} {data["name"]} à {city}</a></li>\n'
        )

    # Sibling city links
    sibling_html = ""
    for c in CITIES:
        if c == city:
            continue
        c_slug = f"{slugify(title_pro)}-{slugify(c)}"
        sibling_html += (
            f'<li><a href="/{c_slug}/" class="text-blue-600 hover:underline">'
            f'{title_pro} à {c}</a></li>\n'
        )

    return f"""
{_breadcrumb_html(breadcrumbs)}
{_schema_medical_business(discipline)}

<section class="max-w-4xl mx-auto">
  <h1 class="text-3xl md:text-4xl font-extrabold text-blue-900 mb-6">{title_pro} à {city} – Consultation en ligne</h1>
  <p class="text-lg text-gray-700 mb-6">
    Vous cherchez un {pro_lower} à {city} ? Chez {SITE_NAME}, nos {pro_lower}s diplômés vous accompagnent en visioconférence,
    sans liste d'attente et sans déplacement. Bénéficiez d'un suivi professionnel de qualité depuis {city} ou sa région,
    dans le confort de votre domicile.
  </p>
  {_trust_badges()}

  <h2 class="text-2xl font-bold text-blue-800 mt-10 mb-4">Nos spécialisations disponibles à {city}</h2>
  <ul class="list-disc pl-6 space-y-2 mb-8">
    {links_html}
  </ul>

  <h2 class="text-2xl font-bold text-blue-800 mt-10 mb-4">Pourquoi choisir l'{pro_lower} en ligne à {city} ?</h2>
  <div class="grid md:grid-cols-2 gap-6 mb-8">
    <div class="bg-white rounded-xl shadow-sm border p-6">
      <h3 class="font-semibold text-blue-900 mb-2">Pas de liste d'attente</h3>
      <p class="text-gray-600">À {city}, les délais pour obtenir un rendez-vous chez un {pro_lower} peuvent dépasser 6 mois. En ligne, nous vous proposons un premier bilan sous 2 semaines.</p>
    </div>
    <div class="bg-white rounded-xl shadow-sm border p-6">
      <h3 class="font-semibold text-blue-900 mb-2">Gain de temps</h3>
      <p class="text-gray-600">Fini les trajets dans les transports de {city} ! Les séances se déroulent depuis chez vous, au moment qui vous convient.</p>
    </div>
    <div class="bg-white rounded-xl shadow-sm border p-6">
      <h3 class="font-semibold text-blue-900 mb-2">Même qualité de soin</h3>
      <p class="text-gray-600">Nos {pro_lower}s sont tous diplômés d'État. La téléconsultation offre la même qualité de prise en charge qu'en cabinet.</p>
    </div>
    <div class="bg-white rounded-xl shadow-sm border p-6">
      <h3 class="font-semibold text-blue-900 mb-2">Environnement familier</h3>
      <p class="text-gray-600">Votre enfant est dans son environnement, ce qui favorise sa concentration et son confort pendant les séances.</p>
    </div>
  </div>

  {_cta_section()}

  <h2 class="text-2xl font-bold text-blue-800 mt-10 mb-4">Autres villes</h2>
  <ul class="flex flex-wrap gap-3">
    {sibling_html}
  </ul>
</section>"""


# ---- Trouble + City page content ----------------------------------------
def generate_trouble_city_content(
    discipline: str,
    trouble_key: str,
    trouble_data: dict,
    city: str,
    slug_prefix: str,
) -> str:
    """Content for trouble+city pages (e.g. Orthophoniste dyslexie à Paris)."""
    if discipline == "Orthophonie":
        pro = "Orthophoniste"
        pro_lower = "orthophoniste"
        pillar_slug = "orthophonie-en-ligne"
        pillar_label = "Orthophonie en ligne"
        city_pro = "Orthophoniste"
    else:
        pro = "Psychologue"
        pro_lower = "psychologue"
        pillar_slug = "psychologie-en-ligne"
        pillar_label = "Psychologie en ligne"
        city_pro = "Psychologue enfant"

    name = trouble_data["name"]
    full_name = trouble_data["full_name"]
    definition = trouble_data["definition"]
    symptoms = trouble_data["symptoms"]
    approach = trouble_data["approach"]

    trouble_mother_slug = f"{slug_prefix}-{slugify(name)}"
    city_mother_slug = f"{slugify(city_pro)}-{slugify(city)}"
    page_slug = f"{trouble_mother_slug}-{slugify(city)}"

    breadcrumbs = [
        ("Accueil", "https://logopsiestudios.com"),
        (pillar_label, f"/{pillar_slug}/"),
        (full_name, f"/{trouble_mother_slug}/"),
        (f"{pro} {name} à {city}", f"/{page_slug}/"),
    ]

    # First 2 symptoms
    symptom_html = ""
    for title, desc in symptoms[:2]:
        symptom_html += f"""
<div class="bg-white rounded-xl shadow-sm border p-5 mb-3">
  <h3 class="font-semibold text-blue-900 mb-1">{title}</h3>
  <p class="text-gray-600 text-sm">{desc}</p>
</div>"""

    # Sibling cities
    sibling_html = ""
    for c in CITIES:
        if c == city:
            continue
        sib_slug = f"{trouble_mother_slug}-{slugify(c)}"
        sibling_html += (
            f'<li><a href="/{sib_slug}/" class="text-blue-600 hover:underline">'
            f'{pro} {name} à {c}</a></li>\n'
        )

    return f"""
{_breadcrumb_html(breadcrumbs)}

<section class="max-w-4xl mx-auto">
  <h1 class="text-3xl md:text-4xl font-extrabold text-blue-900 mb-4">{pro} {name} à {city} – Consultation en ligne</h1>
  <p class="text-lg text-gray-700 mb-6">
    Vous recherchez un {pro_lower} spécialisé en {name} à {city} ? {SITE_NAME} vous propose des séances de
    {pro_lower.replace("enfant", "").strip()} en ligne, accessibles depuis {city} et ses environs. {definition}
  </p>
  {_trust_badges()}

  <h2 class="text-2xl font-bold text-blue-800 mt-8 mb-4">Les signes de la {name} chez l'enfant</h2>
  {symptom_html}
  <p class="text-gray-600 text-sm mb-8">
    <a href="/{trouble_mother_slug}/" class="text-blue-600 hover:underline">Voir tous les symptômes de la {name} →</a>
  </p>

  <h2 class="text-2xl font-bold text-blue-800 mt-8 mb-4">Notre prise en charge à {city}</h2>
  <p class="text-gray-700 mb-6">{approach}</p>
  <p class="text-gray-700 mb-8">
    Depuis {city}, connectez-vous en quelques clics pour une séance interactive avec un {pro_lower} expert.
    Pas de déplacement, pas de liste d'attente : votre enfant est pris en charge rapidement dans un cadre bienveillant.
  </p>

  {_cta_section()}

  <h2 class="text-2xl font-bold text-blue-800 mt-10 mb-4">Liens utiles</h2>
  <ul class="list-disc pl-6 space-y-2 mb-6">
    <li><a href="/{trouble_mother_slug}/" class="text-blue-600 hover:underline">En savoir plus sur la {full_name}</a></li>
    <li><a href="/{city_mother_slug}/" class="text-blue-600 hover:underline">Tous nos {pro_lower}s à {city}</a></li>
    <li><a href="/{pillar_slug}/" class="text-blue-600 hover:underline">{pillar_label}</a></li>
  </ul>

  <h2 class="text-2xl font-bold text-blue-800 mt-10 mb-4">{name} dans d'autres villes</h2>
  <ul class="flex flex-wrap gap-3 mb-10">
    {sibling_html}
  </ul>
</section>"""


# ---------------------------------------------------------------------------
# Deploy orchestration
# ---------------------------------------------------------------------------
def deploy(dry_run: bool = False) -> dict:
    """Deploy the full semantic cocoon. Returns slug -> page_id mapping."""
    mapping: dict[str, Optional[int]] = {}

    log.info("🚀 Starting semantic cocoon deployment (dry_run=%s)", dry_run)

    # ======================================================================
    # 1. PILLAR PAGES
    # ======================================================================
    log.info("📄 Creating pillar pages…")

    # Orthophonie pillar
    ortho_content = generate_pillar_content("Orthophonie", ORTHO_TROUBLES, "orthophoniste-specialise")
    ortho_pillar_id = create_wp_page(
        title="Orthophonie en ligne",
        slug="orthophonie-en-ligne",
        content=ortho_content,
        excerpt="Orthophonie en ligne pour enfants : bilan et rééducation avec des orthophonistes diplômés. Séances en visioconférence, sans liste d'attente. Logopsi Studios.",
        dry_run=dry_run,
    )
    mapping["orthophonie-en-ligne"] = ortho_pillar_id

    # Psychologie pillar
    psy_content = generate_pillar_content("Psychologie", PSY_TROUBLES, "psychologue-specialise")
    psy_pillar_id = create_wp_page(
        title="Psychologie en ligne",
        slug="psychologie-en-ligne",
        content=psy_content,
        excerpt="Psychologue en ligne pour enfants et adolescents : accompagnement psychologique adapté en visioconférence. Professionnels diplômés, sans liste d'attente. Logopsi Studios.",
        dry_run=dry_run,
    )
    mapping["psychologie-en-ligne"] = psy_pillar_id

    # ======================================================================
    # 2. CITY MOTHER PAGES
    # ======================================================================
    log.info("🏙️  Creating city mother pages…")

    ortho_city_ids: dict[str, Optional[int]] = {}
    for city in CITIES:
        slug = f"orthophoniste-{slugify(city)}"
        content = generate_city_mother_content("Orthophonie", city, ORTHO_TROUBLES, "orthophoniste-specialise")
        page_id = create_wp_page(
            title=f"Orthophoniste à {city}",
            slug=slug,
            content=content,
            excerpt=f"Orthophoniste à {city} en ligne : bilan et rééducation orthophonique en visioconférence depuis {city}. Sans liste d'attente. Logopsi Studios.",
            parent=ortho_pillar_id or 0,
            dry_run=dry_run,
        )
        mapping[slug] = page_id
        ortho_city_ids[city] = page_id

    psy_city_ids: dict[str, Optional[int]] = {}
    for city in CITIES:
        slug = f"psychologue-enfant-{slugify(city)}"
        content = generate_city_mother_content("Psychologie", city, PSY_TROUBLES, "psychologue-specialise")
        page_id = create_wp_page(
            title=f"Psychologue enfant à {city}",
            slug=slug,
            content=content,
            excerpt=f"Psychologue enfant à {city} en ligne : accompagnement psychologique en visioconférence depuis {city}. Professionnels diplômés. Logopsi Studios.",
            parent=psy_pillar_id or 0,
            dry_run=dry_run,
        )
        mapping[slug] = page_id
        psy_city_ids[city] = page_id

    # ======================================================================
    # 3. TROUBLE MOTHER PAGES
    # ======================================================================
    log.info("📋 Creating trouble mother pages…")

    ortho_trouble_ids: dict[str, Optional[int]] = {}
    for key, data in ORTHO_TROUBLES.items():
        slug = f"orthophoniste-specialise-{slugify(data['name'])}"
        content = generate_trouble_mother_content("Orthophonie", key, data, "orthophoniste-specialise")
        page_id = create_wp_page(
            title=f"Orthophoniste spécialisé {data['full_name']}",
            slug=slug,
            content=content,
            excerpt=f"Orthophoniste spécialisé en {data['full_name']} en ligne. {data['definition'][:100]} Séances en visioconférence chez Logopsi Studios.",
            parent=ortho_pillar_id or 0,
            dry_run=dry_run,
        )
        mapping[slug] = page_id
        ortho_trouble_ids[key] = page_id

    psy_trouble_ids: dict[str, Optional[int]] = {}
    for key, data in PSY_TROUBLES.items():
        slug = f"psychologue-specialise-{slugify(data['name'])}"
        content = generate_trouble_mother_content("Psychologie", key, data, "psychologue-specialise")
        page_id = create_wp_page(
            title=f"Psychologue spécialisé {data['full_name']}",
            slug=slug,
            content=content,
            excerpt=f"Psychologue spécialisé en {data['full_name']} en ligne pour enfants. {data['definition'][:100]} Séances en visioconférence chez Logopsi Studios.",
            parent=psy_pillar_id or 0,
            dry_run=dry_run,
        )
        mapping[slug] = page_id
        psy_trouble_ids[key] = page_id

    # ======================================================================
    # 4. TROUBLE + CITY PAGES
    # ======================================================================
    log.info("🗺️  Creating trouble+city pages (orthophonie)…")

    for key, data in ORTHO_TROUBLES.items():
        for city in CITIES:
            slug = f"orthophoniste-specialise-{slugify(data['name'])}-{slugify(city)}"
            content = generate_trouble_city_content("Orthophonie", key, data, city, "orthophoniste-specialise")
            page_id = create_wp_page(
                title=f"Orthophoniste {data['name']} à {city}",
                slug=slug,
                content=content,
                excerpt=f"Orthophoniste spécialisé {data['name']} à {city} en ligne. Bilan et rééducation en visioconférence. Logopsi Studios.",
                parent=ortho_trouble_ids.get(key) or 0,
                dry_run=dry_run,
            )
            mapping[slug] = page_id

    log.info("🗺️  Creating trouble+city pages (psychologie)…")

    for key, data in PSY_TROUBLES.items():
        for city in CITIES:
            slug = f"psychologue-specialise-{slugify(data['name'])}-{slugify(city)}"
            content = generate_trouble_city_content("Psychologie", key, data, city, "psychologue-specialise")
            page_id = create_wp_page(
                title=f"Psychologue {data['name']} à {city}",
                slug=slug,
                content=content,
                excerpt=f"Psychologue spécialisé {data['name']} à {city} en ligne pour enfants. Séances en visioconférence. Logopsi Studios.",
                parent=psy_trouble_ids.get(key) or 0,
                dry_run=dry_run,
            )
            mapping[slug] = page_id

    # ======================================================================
    # 5. SAVE MAPPING
    # ======================================================================
    mapping_file = "page_mapping.json"
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    log.info("💾 Page mapping saved to %s", mapping_file)

    total = len(mapping)
    created = sum(1 for v in mapping.values() if v is not None)
    failed = sum(1 for v in mapping.values() if v is None) if not dry_run else 0
    log.info("🏁 Deployment complete! Total: %d | Created: %d | Failed: %d", total, created, failed)

    return mapping


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Deploy SEO semantic cocoon to WordPress"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview pages without creating them on WordPress",
    )
    args = parser.parse_args()

    mapping = deploy(dry_run=args.dry_run)

    # Summary
    print("\n" + "=" * 60)
    print(f"  Total pages: {len(mapping)}")
    if not args.dry_run:
        created = sum(1 for v in mapping.values() if v is not None)
        print(f"  Successfully created: {created}")
        print(f"  Failed: {len(mapping) - created}")
    else:
        print("  Mode: DRY RUN (no pages created)")
    print("=" * 60)


if __name__ == "__main__":
    main()
