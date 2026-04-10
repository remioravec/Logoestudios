#!/usr/bin/env python3
"""Generate all Level 2 pages for Logopsi Studios with new template design."""

import os
import json

# ============================================================
# DATA DEFINITIONS
# ============================================================

VILLES = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"]

ORTHO_PAGES = {
    "dyslexie": {
        "title": "Orthophoniste Dyslexie en ligne",
        "meta_desc": "Votre enfant a des difficultés en lecture ? Nos orthophonistes spécialisés en dyslexie proposent un accompagnement en ligne personnalisé et efficace.",
        "h1": "Orthophoniste spécialisé dans la <span class=\"text-primary\">Dyslexie</span> en ligne",
        "hero_desc": "Votre enfant confond les lettres, lit avec difficulté ou évite la lecture ? Nos orthophonistes experts en troubles spécifiques des apprentissages l'accompagnent avec des méthodes éprouvées, sans temps d'attente.",
        "hero_img": "https://images.unsplash.com/photo-1456406644174-8ddd4cd52a06?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant apprenant à lire",
        "hero_card_icon": "book-open",
        "hero_card_title": "Méthodes adaptées",
        "hero_card_desc": "Outils visuels et ludiques",
        "hero_card_color": "blue",
        "symptoms_title": "Comment reconnaître les signes de la dyslexie ?",
        "symptoms_intro": "La dyslexie est un trouble spécifique et durable de l'acquisition de la lecture. Elle n'est pas liée à un manque d'intelligence ou de travail, mais à un fonctionnement neurologique différent. Voici les signes qui doivent vous alerter :",
        "symptoms": [
            {"icon": "activity", "color": "red", "title": "Confusions visuelles ou auditives", "desc": "Inversion de lettres (b/d, p/q) ou de sons proches (ch/j, f/v)."},
            {"icon": "file-text", "color": "orange", "title": "Lecture lente et saccadée", "desc": "Difficulté à déchiffrer les mots, lecture syllabe par syllabe, perte de la ligne."},
            {"icon": "brain", "color": "purple", "title": "Fatigue importante", "desc": "L'effort cognitif fourni pour lire entraîne une grande fatigabilité et parfois un rejet de l'école."},
        ],
        "approach_title": "Notre approche de rééducation",
        "approach_desc": "Lors de nos séances en ligne, nos orthophonistes utilisent des supports numériques interactifs spécifiquement conçus pour les enfants DYS. Nous travaillons sur la conscience phonologique, le déchiffrage et la compréhension, tout en restaurant la confiance en soi de l'enfant.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant confond-il souvent des lettres proches (b/d, p/q) ?", "opts": ["Oui, très souvent", "Parfois", "Rarement ou jamais"]},
            {"q": "La lecture à voix haute est-elle lente et hésitante ?", "opts": ["Oui, il déchiffre syllabe par syllabe", "C'est un peu lent mais fluide", "Non, la lecture est fluide"]},
            {"q": "Votre enfant évite-t-il les activités de lecture ?", "opts": ["Oui, il refuse de lire", "Il lit si on l'y oblige", "Non, il aime lire"]},
        ],
        "faq": [
            {"q": "À quel âge peut-on diagnostiquer la dyslexie ?", "a": "Le diagnostic de dyslexie peut être posé à partir de 7-8 ans, soit après au moins 18 mois d'apprentissage formel de la lecture (fin de CE1). Avant cet âge, on parle plutôt de difficultés de lecture ou de risque de dyslexie. Toutefois, un bilan orthophonique peut être réalisé dès la grande section de maternelle si des signes d'alerte sont présents."},
            {"q": "La dyslexie peut-elle être corrigée ?", "a": "La dyslexie est un trouble durable qui ne disparaît pas complètement. Cependant, une rééducation orthophonique adaptée permet de développer des stratégies compensatoires efficaces. La plupart des patients dyslexiques parviennent à atteindre un niveau de lecture fonctionnel."},
            {"q": "L'orthophonie en ligne est-elle efficace pour la dyslexie ?", "a": "Oui, plusieurs études scientifiques démontrent que la rééducation orthophonique en ligne est aussi efficace que les séances en cabinet pour la dyslexie. Les outils numériques offrent même des avantages spécifiques : supports visuels interactifs, exercices gamifiés, enregistrements pour le suivi des progrès."},
        ],
        "cta_title": "Besoin d'un orthophoniste spécialisé en dyslexie ?",
        "cta_desc": "Réservez votre bilan en ligne et bénéficiez d'un accompagnement personnalisé par nos orthophonistes diplômés et spécialisés.",
    },
    "dysorthographie": {
        "title": "Orthophoniste Dysorthographie en ligne",
        "meta_desc": "Votre enfant fait beaucoup de fautes d'orthographe ? Nos orthophonistes spécialisés en dysorthographie proposent un suivi en ligne adapté et efficace.",
        "h1": "Orthophoniste spécialisé dans la <span class=\"text-primary\">Dysorthographie</span> en ligne",
        "hero_desc": "Votre enfant accumule les fautes d'orthographe malgré ses efforts ? La dysorthographie est un trouble spécifique de l'écriture. Nos orthophonistes l'accompagnent avec des stratégies adaptées pour progresser durablement.",
        "hero_img": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant écrivant",
        "hero_card_icon": "pencil",
        "hero_card_title": "Stratégies d'écriture",
        "hero_card_desc": "Méthodes visuelles et mnémotechniques",
        "hero_card_color": "amber",
        "symptoms_title": "Comment reconnaître les signes de la dysorthographie ?",
        "symptoms_intro": "La dysorthographie est un trouble persistant de l'acquisition et de la maîtrise de l'orthographe. Elle accompagne souvent la dyslexie mais peut exister de manière isolée. Voici les signes à surveiller :",
        "symptoms": [
            {"icon": "pencil", "color": "red", "title": "Fautes d'orthographe persistantes", "desc": "Erreurs fréquentes sur les mots courants, oubli de lettres, ajouts ou inversions dans les mots."},
            {"icon": "copy", "color": "orange", "title": "Difficultés en copie et dictée", "desc": "L'enfant peine à recopier un texte sans erreurs et la dictée est particulièrement difficile."},
            {"icon": "brain", "color": "purple", "title": "Effort disproportionné", "desc": "L'enfant se concentre tellement sur l'orthographe qu'il perd le fil de sa pensée à l'écrit."},
        ],
        "approach_title": "Notre approche de rééducation",
        "approach_desc": "Nos séances ciblent la mémorisation orthographique par des techniques multisensorielles : visualisation des mots, épellation rythmée, cartes mentales et exercices informatisés. Nous renforçons les règles grammaticales par le jeu et la manipulation pour une acquisition durable.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant fait-il beaucoup de fautes d'orthographe sur des mots courants ?", "opts": ["Oui, très fréquemment", "Parfois", "Rarement"]},
            {"q": "A-t-il des difficultés à recopier un texte sans erreurs ?", "opts": ["Oui, même en copiant", "Quelques erreurs", "Non, la copie est correcte"]},
            {"q": "L'écriture est-elle source de frustration pour lui ?", "opts": ["Oui, il évite d'écrire", "Un peu", "Non, il aime écrire"]},
        ],
        "faq": [
            {"q": "Quelle est la différence entre dysorthographie et dyslexie ?", "a": "La dyslexie concerne la lecture tandis que la dysorthographie touche l'écriture et l'orthographe. Les deux troubles sont souvent associés mais peuvent exister indépendamment. Un enfant peut être dysorthographique sans être dyslexique."},
            {"q": "La dysorthographie se corrige-t-elle ?", "a": "Avec une rééducation orthophonique adaptée, l'enfant développe des stratégies compensatoires efficaces. L'objectif est d'automatiser les règles orthographiques et de réduire le coût cognitif de l'écriture. Les progrès sont significatifs avec un suivi régulier."},
            {"q": "Comment se déroule un bilan de dysorthographie ?", "a": "Le bilan comprend des épreuves de dictée, de copie, d'orthographe lexicale et grammaticale. L'orthophoniste évalue aussi la conscience phonologique et les capacités de mémorisation visuelle. Le bilan dure environ 1h30 et permet de poser un diagnostic précis."},
        ],
        "cta_title": "Besoin d'un orthophoniste spécialisé en dysorthographie ?",
        "cta_desc": "Réservez votre bilan en ligne et bénéficiez d'un accompagnement personnalisé pour aider votre enfant à progresser en écriture.",
    },
    "dyscalculie": {
        "title": "Orthophoniste Dyscalculie en ligne",
        "meta_desc": "Votre enfant a des difficultés en mathématiques ? Nos orthophonistes spécialisés en dyscalculie l'accompagnent en ligne avec des méthodes adaptées.",
        "h1": "Orthophoniste spécialisé dans la <span class=\"text-primary\">Dyscalculie</span> en ligne",
        "hero_desc": "Votre enfant peine avec les chiffres, le calcul mental ou la résolution de problèmes ? La dyscalculie est un trouble spécifique des apprentissages mathématiques. Nos orthophonistes experts l'accompagnent en ligne.",
        "hero_img": "https://images.unsplash.com/photo-1596495578065-6e0763fa1178?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant avec des chiffres",
        "hero_card_icon": "calculator",
        "hero_card_title": "Approche concrète",
        "hero_card_desc": "Manipulation et visualisation",
        "hero_card_color": "indigo",
        "symptoms_title": "Comment reconnaître les signes de la dyscalculie ?",
        "symptoms_intro": "La dyscalculie est un trouble neurodéveloppemental qui affecte l'acquisition des compétences numériques et mathématiques. Elle touche environ 5% des enfants. Voici les signes qui doivent vous alerter :",
        "symptoms": [
            {"icon": "hash", "color": "red", "title": "Difficultés avec les nombres", "desc": "Confusion dans l'ordre des chiffres, difficulté à dénombrer, à comparer des quantités ou à compter à rebours."},
            {"icon": "clock", "color": "orange", "title": "Calcul mental laborieux", "desc": "L'enfant utilise encore ses doigts pour compter, ne mémorise pas les tables et met beaucoup de temps pour des calculs simples."},
            {"icon": "puzzle", "color": "purple", "title": "Problèmes de logique", "desc": "Difficulté à comprendre les énoncés de problèmes, à choisir la bonne opération et à organiser un raisonnement mathématique."},
        ],
        "approach_title": "Notre approche de rééducation",
        "approach_desc": "Nos séances s'appuient sur la manipulation concrète (jetons virtuels, barres numériques, abaques) avant de passer à l'abstraction. Nous travaillons le sens du nombre, la construction des opérations et la résolution de problèmes par étapes, avec des supports interactifs ludiques.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant a-t-il du mal à compter ou à comparer des quantités ?", "opts": ["Oui, c'est très difficile", "Parfois", "Non, pas de souci"]},
            {"q": "Utilise-t-il encore ses doigts pour des calculs simples ?", "opts": ["Oui, systématiquement", "De temps en temps", "Non, il calcule de tête"]},
            {"q": "Les problèmes mathématiques sont-ils source d'angoisse ?", "opts": ["Oui, il panique", "Un peu de stress", "Non, il aime les maths"]},
        ],
        "faq": [
            {"q": "La dyscalculie est-elle liée à un manque de travail ?", "a": "Non. La dyscalculie est un trouble neurodéveloppemental d'origine neurobiologique. L'enfant n'est ni paresseux ni en manque d'intelligence. Son cerveau traite les informations numériques différemment, ce qui nécessite un accompagnement spécifique."},
            {"q": "À quel âge peut-on dépister la dyscalculie ?", "a": "Les premiers signes peuvent être repérés dès la maternelle (difficultés à dénombrer, à comparer). Un diagnostic formel est généralement posé en CE1-CE2, après un bilan orthophonique complet incluant des épreuves numériques standardisées."},
            {"q": "La rééducation en ligne fonctionne-t-elle pour la dyscalculie ?", "a": "Oui. Les outils numériques sont particulièrement adaptés à la dyscalculie : manipulations virtuelles, jeux interactifs, visualisation des quantités. Nos patients montrent des progrès significatifs grâce à ces supports engageants."},
        ],
        "cta_title": "Besoin d'un orthophoniste spécialisé en dyscalculie ?",
        "cta_desc": "Réservez votre bilan en ligne et offrez à votre enfant un accompagnement adapté pour progresser en mathématiques.",
    },
    "dysphasie": {
        "title": "Orthophoniste Dysphasie en ligne",
        "meta_desc": "Votre enfant a des difficultés à s'exprimer ou comprendre le langage oral ? Nos orthophonistes spécialisés en dysphasie proposent un suivi en ligne.",
        "h1": "Orthophoniste spécialisé dans la <span class=\"text-primary\">Dysphasie</span> en ligne",
        "hero_desc": "Votre enfant a du mal à construire des phrases, à trouver ses mots ou à comprendre les consignes ? La dysphasie est un trouble sévère du langage oral. Nos orthophonistes experts l'accompagnent en ligne avec des méthodes éprouvées.",
        "hero_img": "https://images.unsplash.com/photo-1544776193-352d25ca82cd?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant en communication",
        "hero_card_icon": "message-circle",
        "hero_card_title": "Communication adaptée",
        "hero_card_desc": "Supports visuels et gestuels",
        "hero_card_color": "teal",
        "symptoms_title": "Comment reconnaître les signes de la dysphasie ?",
        "symptoms_intro": "La dysphasie est un trouble structurel et durable du développement du langage oral. Elle affecte l'expression, la compréhension ou les deux. Voici les signes qui doivent alerter :",
        "symptoms": [
            {"icon": "message-circle", "color": "red", "title": "Retard de langage sévère", "desc": "L'enfant parle tard, utilise peu de mots et ses phrases restent très courtes ou agrammatiques au-delà de 4 ans."},
            {"icon": "ear", "color": "orange", "title": "Difficultés de compréhension", "desc": "L'enfant ne comprend pas les consignes complexes, confond les mots ou a du mal à suivre une conversation."},
            {"icon": "users", "color": "purple", "title": "Impact sur la socialisation", "desc": "Les difficultés de communication entraînent un repli sur soi, des frustrations ou des comportements de substitution."},
        ],
        "approach_title": "Notre approche de rééducation",
        "approach_desc": "Nous utilisons une approche multimodale combinant supports visuels (pictogrammes, images), gestes de communication (Makaton) et stimulation langagière intensive. Chaque séance est structurée pour développer le vocabulaire, la syntaxe et la pragmatique du langage, en s'appuyant sur les centres d'intérêt de l'enfant.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant a-t-il du mal à construire des phrases correctes ?", "opts": ["Oui, ses phrases sont très courtes", "Un peu", "Non, il s'exprime bien"]},
            {"q": "Comprend-il les consignes à plusieurs étapes ?", "opts": ["Non, c'est très difficile", "Parfois", "Oui, sans problème"]},
            {"q": "Est-il frustré par ses difficultés à communiquer ?", "opts": ["Oui, souvent", "Parfois", "Non, il est à l'aise"]},
        ],
        "faq": [
            {"q": "Quelle est la différence entre retard de langage et dysphasie ?", "a": "Le retard de langage est un décalage temporel qui se rattrape avec le temps, tandis que la dysphasie est un trouble structurel et durable du langage. La dysphasie nécessite une rééducation orthophonique intensive et prolongée."},
            {"q": "La dysphasie affecte-t-elle l'intelligence ?", "a": "Non. La dysphasie est un trouble spécifique du langage qui n'affecte pas les capacités intellectuelles. L'enfant dysphasique peut avoir un QI normal voire supérieur, mais ses difficultés langagières peuvent masquer ses compétences."},
            {"q": "Combien de temps dure la rééducation ?", "a": "La rééducation de la dysphasie est généralement longue (plusieurs années) car c'est un trouble structurel. L'intensité et la fréquence des séances sont adaptées à chaque enfant. Les progrès sont réels mais graduels."},
        ],
        "cta_title": "Besoin d'un orthophoniste spécialisé en dysphasie ?",
        "cta_desc": "Réservez votre bilan en ligne et bénéficiez d'un accompagnement spécialisé pour aider votre enfant à développer son langage.",
    },
    "begaiement": {
        "title": "Orthophoniste Bégaiement en ligne",
        "meta_desc": "Votre enfant bégaie ? Nos orthophonistes spécialisés en bégaiement proposent un accompagnement en ligne avec des techniques efficaces et bienveillantes.",
        "h1": "Orthophoniste spécialisé dans le <span class=\"text-primary\">Bégaiement</span> en ligne",
        "hero_desc": "Votre enfant répète des syllabes, bloque sur certains mots ou évite de parler ? Le bégaiement touche 5% des enfants. Nos orthophonistes experts l'accompagnent en ligne avec des techniques éprouvées, dans un cadre bienveillant.",
        "hero_img": "https://images.unsplash.com/photo-1491013516836-7db643ee125a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant en séance d'orthophonie",
        "hero_card_icon": "mic",
        "hero_card_title": "Fluence verbale",
        "hero_card_desc": "Techniques de parole fluide",
        "hero_card_color": "green",
        "symptoms_title": "Comment reconnaître les signes du bégaiement ?",
        "symptoms_intro": "Le bégaiement est un trouble de la fluence verbale qui apparaît généralement entre 2 et 5 ans. Il peut être passager ou persister. Voici les signes à observer :",
        "symptoms": [
            {"icon": "repeat", "color": "red", "title": "Répétitions de sons ou syllabes", "desc": "L'enfant répète le début des mots (« pa-pa-papa ») ou des sons de manière involontaire."},
            {"icon": "pause", "color": "orange", "title": "Blocages et prolongations", "desc": "Des blocages silencieux avant certains mots ou des prolongations de sons (« ssssserpent »)."},
            {"icon": "alert-triangle", "color": "purple", "title": "Comportements d'évitement", "desc": "L'enfant évite de parler, change de mot, utilise des gestes ou laisse les autres parler à sa place."},
        ],
        "approach_title": "Notre approche de rééducation",
        "approach_desc": "Nous combinons les approches directes (techniques de fluence, respiration, débit contrôlé) et indirectes (guidance parentale, réduction de la pression communicative). Pour les enfants, nous utilisons le programme Lidcombe et des jeux de parole. Pour les adolescents, nous intégrons la gestion de l'anxiété sociale.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant répète-t-il des syllabes ou des sons involontairement ?", "opts": ["Oui, très souvent", "Parfois", "Rarement"]},
            {"q": "Y a-t-il des blocages ou des moments de tension en parlant ?", "opts": ["Oui, fréquemment", "De temps en temps", "Non"]},
            {"q": "Évite-t-il de prendre la parole en groupe ?", "opts": ["Oui, il se tait", "Un peu", "Non, il participe"]},
        ],
        "faq": [
            {"q": "Le bégaiement disparaît-il de lui-même ?", "a": "Chez environ 75% des enfants, le bégaiement se résout spontanément avant 6 ans. Toutefois, il est recommandé de consulter un orthophoniste dès les premiers signes pour évaluer les facteurs de risque de chronicisation et intervenir précocement si nécessaire."},
            {"q": "L'orthophonie en ligne est-elle adaptée au bégaiement ?", "a": "Oui, les séances en ligne sont particulièrement efficaces pour le bégaiement. L'enfant est dans son environnement habituel, ce qui réduit le stress. De plus, les parents peuvent participer facilement aux séances de guidance parentale."},
            {"q": "Le stress cause-t-il le bégaiement ?", "a": "Le stress ne cause pas le bégaiement mais peut l'aggraver. Le bégaiement a une composante neurologique et souvent génétique. En revanche, la pression communicative, la fatigue et les situations émotionnellement chargées peuvent augmenter les dysfluences."},
        ],
        "cta_title": "Besoin d'un orthophoniste spécialisé en bégaiement ?",
        "cta_desc": "Réservez votre bilan en ligne et offrez à votre enfant un accompagnement bienveillant pour retrouver une parole fluide.",
    },
    "tsa": {
        "title": "Orthophoniste TSA (Autisme) en ligne",
        "meta_desc": "Votre enfant est diagnostiqué TSA ? Nos orthophonistes spécialisés en troubles du spectre autistique proposent un accompagnement en ligne adapté.",
        "h1": "Orthophoniste spécialisé dans les <span class=\"text-primary\">Troubles du Spectre Autistique</span> en ligne",
        "hero_desc": "Votre enfant a un diagnostic de TSA et des difficultés de communication ? Nos orthophonistes formés aux spécificités de l'autisme l'accompagnent en ligne avec des méthodes structurées et adaptées à son profil.",
        "hero_img": "https://images.unsplash.com/photo-1587654780291-39c9404d7dd0?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant avec des pictogrammes",
        "hero_card_icon": "puzzle",
        "hero_card_title": "Approche structurée",
        "hero_card_desc": "PECS, ABA et supports visuels",
        "hero_card_color": "cyan",
        "symptoms_title": "Quand consulter un orthophoniste pour un TSA ?",
        "symptoms_intro": "Les troubles du spectre autistique s'accompagnent souvent de difficultés de communication et de langage. L'orthophonie joue un rôle clé dans l'accompagnement. Voici les situations nécessitant un suivi :",
        "symptoms": [
            {"icon": "message-square", "color": "red", "title": "Absence ou retard de langage", "desc": "L'enfant ne parle pas, utilise peu de mots ou présente un langage écholalique (répétition de mots entendus)."},
            {"icon": "users", "color": "orange", "title": "Difficultés de communication sociale", "desc": "Peu de contact visuel, difficulté à initier ou maintenir une conversation, compréhension littérale du langage."},
            {"icon": "utensils", "color": "purple", "title": "Troubles de l'oralité associés", "desc": "Sélectivité alimentaire, hypersensibilité orale, difficultés de mastication ou de déglutition."},
        ],
        "approach_title": "Notre approche de rééducation",
        "approach_desc": "Nos séances s'appuient sur les recommandations HAS pour le TSA : utilisation de supports visuels (PECS, tableaux de communication), approche comportementale (ABA), scénarios sociaux et habiletés pragmatiques. Chaque programme est individualisé et construit en collaboration avec les parents et l'équipe pluridisciplinaire.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant utilise-t-il le langage pour communiquer ?", "opts": ["Non, il ne parle pas encore", "Quelques mots isolés", "Oui, mais de manière atypique"]},
            {"q": "A-t-il des difficultés avec les interactions sociales ?", "opts": ["Oui, très marquées", "Modérées", "Légères"]},
            {"q": "Utilise-t-il des gestes ou des images pour communiquer ?", "opts": ["Non", "Un peu", "Oui, c'est son mode principal"]},
        ],
        "faq": [
            {"q": "L'orthophonie en ligne est-elle possible pour un enfant TSA ?", "a": "Oui, à condition d'adapter le cadre. Nos orthophonistes utilisent des supports visuels structurés, des renforçateurs motivants et travaillent en collaboration étroite avec les parents qui deviennent co-thérapeutes. Le cadre familier du domicile est souvent un avantage pour les enfants TSA."},
            {"q": "À quel âge commencer l'orthophonie pour un TSA ?", "a": "Le plus tôt possible. L'intervention précoce (avant 4 ans) donne les meilleurs résultats. Dès qu'un retard de communication est identifié, une prise en charge orthophonique doit être initiée, même avant le diagnostic formel de TSA."},
            {"q": "Quel rôle jouent les parents dans la rééducation ?", "a": "Les parents sont des partenaires essentiels. Nous les formons aux techniques de stimulation du langage pour qu'ils puissent les appliquer au quotidien. Cette généralisation est cruciale pour les progrès de l'enfant TSA."},
        ],
        "cta_title": "Besoin d'un orthophoniste spécialisé en TSA ?",
        "cta_desc": "Réservez votre bilan en ligne et bénéficiez d'un accompagnement structuré et adapté au profil de votre enfant.",
    },
    "oralite": {
        "title": "Orthophoniste Troubles de l'Oralité en ligne",
        "meta_desc": "Votre enfant refuse de manger certains aliments ou a des difficultés à la mastication ? Nos orthophonistes spécialisés en oralité l'accompagnent en ligne.",
        "h1": "Orthophoniste spécialisé dans les <span class=\"text-primary\">Troubles de l'Oralité</span> en ligne",
        "hero_desc": "Votre enfant refuse de goûter de nouveaux aliments, a des haut-le-cœur ou des difficultés à mastiquer ? Les troubles de l'oralité alimentaire touchent de nombreux enfants. Nos orthophonistes experts l'accompagnent en ligne.",
        "hero_img": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant mangeant",
        "hero_card_icon": "utensils",
        "hero_card_title": "Exploration sensorielle",
        "hero_card_desc": "Approche progressive et ludique",
        "hero_card_color": "pink",
        "symptoms_title": "Comment reconnaître les troubles de l'oralité ?",
        "symptoms_intro": "Les troubles de l'oralité alimentaire se manifestent par des difficultés liées à l'alimentation, dépassant la simple caprice. Voici les signes à surveiller :",
        "symptoms": [
            {"icon": "x-circle", "color": "red", "title": "Refus alimentaire marqué", "desc": "L'enfant refuse catégoriquement certaines textures, couleurs ou températures d'aliments, limitant fortement son alimentation."},
            {"icon": "alert-triangle", "color": "orange", "title": "Nausées et haut-le-cœur", "desc": "Des réflexes nauséeux se déclenchent au contact de certains aliments, même au simple fait de les voir ou les sentir."},
            {"icon": "clock", "color": "purple", "title": "Repas très longs et conflictuels", "desc": "Les repas deviennent une source de stress pour toute la famille, avec des durées anormalement longues."},
        ],
        "approach_title": "Notre approche de rééducation",
        "approach_desc": "Notre protocole de désensibilisation sensorielle est progressif : nous commençons par l'exploration visuelle et tactile des aliments avant de travailler le contact buccal. Nous guidons les parents pour transformer les repas en moments apaisés et utilisons des supports ludiques pour que l'enfant apprivoise les nouvelles textures.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant refuse-t-il de goûter de nouveaux aliments ?", "opts": ["Oui, systématiquement", "Souvent", "Rarement"]},
            {"q": "A-t-il des haut-le-cœur au contact de certaines textures ?", "opts": ["Oui, régulièrement", "Parfois", "Non"]},
            {"q": "Les repas sont-ils source de conflit familial ?", "opts": ["Oui, à chaque repas", "De temps en temps", "Non, ça se passe bien"]},
        ],
        "faq": [
            {"q": "Mon enfant est-il simplement capricieux ?", "a": "Non. Les troubles de l'oralité sont d'origine sensorielle ou fonctionnelle. L'enfant ne refuse pas de manger par caprice mais parce que certaines sensations sont réellement insupportables pour lui. C'est un trouble qui nécessite un accompagnement spécialisé."},
            {"q": "L'orthophonie peut-elle aider pour l'alimentation ?", "a": "Oui, l'orthophoniste est le spécialiste de la sphère orale. Il intervient sur la motricité buccale, la sensibilité orale et les fonctions de succion, mastication et déglutition. La rééducation de l'oralité fait partie intégrante du champ d'exercice de l'orthophonie."},
            {"q": "Comment se passe une séance en ligne pour l'oralité ?", "a": "L'orthophoniste guide les parents pour réaliser des exercices de désensibilisation à la maison, avec les aliments du quotidien. Le parent devient co-thérapeute, ce qui est un vrai avantage du format en ligne pour ce type de trouble."},
        ],
        "cta_title": "Besoin d'un orthophoniste spécialisé en oralité ?",
        "cta_desc": "Réservez votre bilan en ligne et offrez à votre enfant un accompagnement pour retrouver le plaisir de manger.",
    },
    "surdite": {
        "title": "Orthophoniste Surdité en ligne",
        "meta_desc": "Votre enfant est sourd ou malentendant ? Nos orthophonistes spécialisés en surdité proposent un accompagnement en ligne adapté au développement du langage.",
        "h1": "Orthophoniste spécialisé dans la <span class=\"text-primary\">Surdité</span> en ligne",
        "hero_desc": "Votre enfant est sourd ou malentendant et a besoin d'un accompagnement pour développer son langage ? Nos orthophonistes spécialisés en surdité l'accompagnent en ligne avec des méthodes adaptées à son profil auditif.",
        "hero_img": "https://images.unsplash.com/photo-1516627145497-ae6968895b74?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant avec appareil auditif",
        "hero_card_icon": "ear",
        "hero_card_title": "Éducation auditive",
        "hero_card_desc": "Lecture labiale et LPC",
        "hero_card_color": "violet",
        "symptoms_title": "Quand consulter un orthophoniste pour la surdité ?",
        "symptoms_intro": "La surdité, qu'elle soit légère ou profonde, impacte le développement du langage oral. Une prise en charge orthophonique précoce est essentielle. Voici les situations nécessitant un suivi :",
        "symptoms": [
            {"icon": "volume-x", "color": "red", "title": "Retard de langage", "desc": "L'enfant ne babille pas, tarde à dire ses premiers mots ou développe un langage peu intelligible."},
            {"icon": "ear", "color": "orange", "title": "Difficultés de compréhension", "desc": "L'enfant fait répéter, augmente le volume de la TV ou ne réagit pas quand on l'appelle."},
            {"icon": "graduation-cap", "color": "purple", "title": "Difficultés scolaires", "desc": "Les apprentissages de la lecture et de l'écriture sont ralentis en raison du déficit auditif."},
        ],
        "approach_title": "Notre approche de rééducation",
        "approach_desc": "Nous proposons un accompagnement adapté au degré de surdité et au projet linguistique de la famille : éducation auditive, lecture labiale, LPC (Langue française Parlée Complétée), développement du lexique et de la syntaxe. Nos orthophonistes travaillent en lien avec les audioprothésistes et ORL.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant a-t-il un diagnostic de surdité ?", "opts": ["Oui, surdité sévère/profonde", "Oui, surdité légère/moyenne", "Suspicion de surdité"]},
            {"q": "Porte-t-il des aides auditives ou un implant ?", "opts": ["Oui", "En cours d'appareillage", "Non"]},
            {"q": "Son langage oral est-il en retard par rapport à son âge ?", "opts": ["Oui, significativement", "Un peu", "Non, il se débrouille bien"]},
        ],
        "faq": [
            {"q": "L'orthophonie en ligne est-elle possible pour un enfant sourd ?", "a": "Oui, à condition que l'enfant soit appareillé (prothèses auditives ou implant cochléaire). Le format en ligne permet de travailler la perception auditive, la lecture labiale et le langage dans l'environnement quotidien de l'enfant."},
            {"q": "À quel âge commencer l'orthophonie ?", "a": "Le plus tôt possible, dès le diagnostic de surdité. L'intervention précoce, idéalement avant 1 an, est cruciale pour le développement du langage. Les progrès sont directement liés à la précocité de la prise en charge."},
            {"q": "L'orthophoniste remplace-t-il le cours de LSF ?", "a": "Non. L'orthophoniste travaille sur le langage oral et les compétences auditives. La LSF est une langue à part entière qui peut être complémentaire. Le choix du mode de communication dépend du projet linguistique de la famille."},
        ],
        "cta_title": "Besoin d'un orthophoniste spécialisé en surdité ?",
        "cta_desc": "Réservez votre bilan en ligne et bénéficiez d'un accompagnement adapté au profil auditif de votre enfant.",
    },
    "paralysie-cerebrale": {
        "title": "Orthophoniste Paralysie Cérébrale en ligne",
        "meta_desc": "Votre enfant est atteint de paralysie cérébrale ? Nos orthophonistes spécialisés l'accompagnent en ligne pour développer sa communication et son alimentation.",
        "h1": "Orthophoniste spécialisé dans la <span class=\"text-primary\">Paralysie Cérébrale</span> en ligne",
        "hero_desc": "Votre enfant est atteint de paralysie cérébrale et rencontre des difficultés de communication ou d'alimentation ? Nos orthophonistes spécialisés proposent un accompagnement en ligne adapté, en lien avec l'équipe pluridisciplinaire.",
        "hero_img": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Séance de rééducation",
        "hero_card_icon": "accessibility",
        "hero_card_title": "Accompagnement global",
        "hero_card_desc": "Communication et alimentation",
        "hero_card_color": "emerald",
        "symptoms_title": "Quand consulter un orthophoniste pour la paralysie cérébrale ?",
        "symptoms_intro": "La paralysie cérébrale peut affecter la motricité bucco-faciale, le langage et la déglutition. L'orthophonie est un pilier de la prise en charge pluridisciplinaire. Voici les indications principales :",
        "symptoms": [
            {"icon": "message-circle", "color": "red", "title": "Troubles de la parole", "desc": "Dysarthrie (parole peu intelligible), difficultés d'articulation liées à l'atteinte motrice des muscles de la bouche."},
            {"icon": "utensils", "color": "orange", "title": "Troubles de la déglutition", "desc": "Difficultés à avaler, fausses routes, bavage excessif lié à un manque de contrôle de la motricité orale."},
            {"icon": "tablet", "color": "purple", "title": "Besoin de communication alternative", "desc": "Lorsque la parole est trop limitée, mise en place d'outils de CAA (tablettes, synthèse vocale, pictogrammes)."},
        ],
        "approach_title": "Notre approche de rééducation",
        "approach_desc": "Nous proposons un travail sur la motricité bucco-faciale, l'articulation, le souffle et la déglutition. Pour les enfants dont la parole est très limitée, nous mettons en place des outils de communication alternative et augmentée (CAA) adaptés à leurs capacités motrices. Le parent est guidé pour faciliter la communication au quotidien.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant a-t-il des difficultés à articuler les mots ?", "opts": ["Oui, sa parole est peu compréhensible", "Un peu", "Non"]},
            {"q": "Présente-t-il des difficultés à manger ou à avaler ?", "opts": ["Oui, fausses routes fréquentes", "Quelques difficultés", "Non"]},
            {"q": "Utilise-t-il un outil de communication alternative ?", "opts": ["Non, mais il en aurait besoin", "Oui, mais il faut l'adapter", "Oui, ça fonctionne bien"]},
        ],
        "faq": [
            {"q": "L'orthophonie en ligne est-elle possible pour la paralysie cérébrale ?", "a": "Oui. L'orthophoniste guide les parents pour réaliser les exercices de motricité orale et de communication à la maison. Le format en ligne facilite la fréquence des séances et l'implication parentale, deux facteurs clés de progrès."},
            {"q": "Qu'est-ce que la CAA ?", "a": "La Communication Alternative et Augmentée (CAA) regroupe tous les outils qui complètent ou remplacent la parole : pictogrammes, tableaux de communication, applications sur tablette, synthèse vocale. L'orthophoniste choisit et adapte l'outil au profil moteur et cognitif de l'enfant."},
            {"q": "À quelle fréquence sont recommandées les séances ?", "a": "La fréquence dépend des besoins de l'enfant, généralement 2 à 3 séances par semaine. Le format en ligne permet de maintenir cette intensité plus facilement qu'en cabinet, en supprimant les temps de transport."},
        ],
        "cta_title": "Besoin d'un orthophoniste pour la paralysie cérébrale ?",
        "cta_desc": "Réservez votre bilan en ligne et bénéficiez d'un accompagnement spécialisé et adapté aux besoins de votre enfant.",
    },
    "fente-palatine": {
        "title": "Orthophoniste Fente Palatine en ligne",
        "meta_desc": "Votre enfant est né avec une fente palatine ? Nos orthophonistes spécialisés proposent un accompagnement en ligne pour la parole et l'alimentation.",
        "h1": "Orthophoniste spécialisé dans la <span class=\"text-primary\">Fente Palatine</span> en ligne",
        "hero_desc": "Votre enfant est né avec une fente labio-palatine et rencontre des difficultés de parole ou d'alimentation ? Nos orthophonistes spécialisés l'accompagnent en ligne, en coordination avec l'équipe chirurgicale.",
        "hero_img": "https://images.unsplash.com/photo-1565843708714-52ecf69ab81f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Bébé souriant",
        "hero_card_icon": "smile",
        "hero_card_title": "Suivi pré et post-op",
        "hero_card_desc": "Accompagnement dès la naissance",
        "hero_card_color": "rose",
        "symptoms_title": "Quand consulter un orthophoniste pour une fente palatine ?",
        "symptoms_intro": "La fente labio-palatine nécessite un suivi orthophonique dès la naissance et tout au long de la croissance. Voici les principaux domaines d'intervention :",
        "symptoms": [
            {"icon": "baby", "color": "red", "title": "Difficultés d'alimentation précoces", "desc": "Dès la naissance, le bébé peut avoir des difficultés à téter en raison de la fente. L'orthophoniste guide les parents pour l'alimentation."},
            {"icon": "volume-2", "color": "orange", "title": "Nasalisation de la parole", "desc": "Après la chirurgie, la parole peut rester nasillarde (rhinolalie) si le voile du palais ne fonctionne pas correctement."},
            {"icon": "ear", "color": "purple", "title": "Otites et audition", "desc": "Les enfants porteurs de fente sont plus sujets aux otites séreuses, pouvant impacter l'audition et donc le langage."},
        ],
        "approach_title": "Notre approche de rééducation",
        "approach_desc": "Notre prise en charge suit les étapes de développement de l'enfant : guidance alimentaire néonatale, stimulation du langage oral, rééducation de l'articulation et du souffle nasal après chirurgie. Nous travaillons en lien étroit avec l'équipe chirurgicale et ORL pour ajuster les objectifs à chaque étape.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant a-t-il une voix nasillarde ?", "opts": ["Oui, très marquée", "Un peu", "Non"]},
            {"q": "A-t-il des difficultés d'articulation ?", "opts": ["Oui, on le comprend difficilement", "Quelques sons posent problème", "Non, sa parole est claire"]},
            {"q": "A-t-il déjà été opéré ?", "opts": ["Oui, chirurgie réalisée", "Chirurgie prévue", "Pas encore planifié"]},
        ],
        "faq": [
            {"q": "L'orthophonie est-elle nécessaire pour toutes les fentes ?", "a": "Oui, un suivi orthophonique est recommandé pour toutes les fentes, même les fentes labiales isolées. L'intensité du suivi varie selon le type de fente et les difficultés rencontrées. Un bilan régulier permet de surveiller le développement du langage."},
            {"q": "À quel âge commencer l'orthophonie ?", "a": "L'orthophoniste peut intervenir dès la naissance pour la guidance alimentaire (succion, alimentation au biberon adapté). Le suivi du langage oral commence vers 12-18 mois, et la rééducation de l'articulation après la chirurgie du palais."},
            {"q": "Combien de temps dure le suivi orthophonique ?", "a": "Le suivi est généralement long, de la naissance jusqu'à la fin de la croissance faciale (vers 18 ans). L'intensité varie : séances régulières après la chirurgie, puis suivi ponctuel pour contrôler le développement du langage et de l'articulation."},
        ],
        "cta_title": "Besoin d'un orthophoniste pour la fente palatine ?",
        "cta_desc": "Réservez votre bilan en ligne et bénéficiez d'un accompagnement spécialisé, en coordination avec l'équipe chirurgicale.",
    },
    "trisomie-21": {
        "title": "Orthophoniste Trisomie 21 en ligne",
        "meta_desc": "Votre enfant est porteur de trisomie 21 ? Nos orthophonistes spécialisés proposent un accompagnement en ligne pour développer la communication et le langage.",
        "h1": "Orthophoniste spécialisé dans la <span class=\"text-primary\">Trisomie 21</span> en ligne",
        "hero_desc": "Votre enfant est porteur de trisomie 21 et a besoin d'un accompagnement pour développer son langage et sa communication ? Nos orthophonistes spécialisés proposent un suivi en ligne adapté, dès le plus jeune âge.",
        "hero_img": "https://images.unsplash.com/photo-1590650516541-ef1d9b32d946?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant trisomique souriant",
        "hero_card_icon": "heart",
        "hero_card_title": "Stimulation précoce",
        "hero_card_desc": "Accompagnement dès la naissance",
        "hero_card_color": "red",
        "symptoms_title": "Pourquoi un suivi orthophonique pour la trisomie 21 ?",
        "symptoms_intro": "La trisomie 21 s'accompagne systématiquement de particularités impactant le développement du langage. Un suivi orthophonique précoce et régulier est essentiel :",
        "symptoms": [
            {"icon": "message-circle", "color": "red", "title": "Retard de langage", "desc": "Le développement du langage oral est plus lent, avec des premières phrases souvent après 3-4 ans. Le vocabulaire s'enrichit progressivement."},
            {"icon": "volume-2", "color": "orange", "title": "Articulation et intelligibilité", "desc": "L'hypotonie faciale et la macroglossie rendent la parole moins intelligible. Un travail de motricité orale est nécessaire."},
            {"icon": "book-open", "color": "purple", "title": "Accès à la lecture", "desc": "La lecture est un levier puissant pour les enfants T21 car ils ont souvent de bonnes compétences visuelles. L'orthophoniste accompagne cet apprentissage."},
        ],
        "approach_title": "Notre approche de rééducation",
        "approach_desc": "Notre prise en charge débute par la stimulation précoce : motricité bucco-faciale, communication gestuelle (Makaton), enrichissement du vocabulaire. Nous exploitons les points forts de l'enfant T21 (mémoire visuelle, imitation) pour développer le langage oral et écrit. Le programme est ajusté au rythme de chaque enfant.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant a-t-il un retard de langage par rapport à son âge ?", "opts": ["Oui, significatif", "Modéré", "Léger"]},
            {"q": "Sa parole est-elle facilement compréhensible ?", "opts": ["Non, difficilement", "Par les proches seulement", "Oui, assez bien"]},
            {"q": "Bénéficie-t-il déjà d'un suivi orthophonique ?", "opts": ["Non, pas encore", "Oui, mais on souhaite compléter", "Oui, en cabinet"]},
        ],
        "faq": [
            {"q": "À quel âge commencer l'orthophonie pour la trisomie 21 ?", "a": "Dès les premiers mois de vie. La stimulation précoce (motricité orale, alimentation, communication gestuelle) prépare le terrain pour le développement du langage. Plus l'intervention est précoce, meilleurs sont les résultats à long terme."},
            {"q": "Quelle est la fréquence des séances recommandée ?", "a": "Généralement 2 à 3 séances par semaine, en fonction de l'âge et des besoins de l'enfant. Le format en ligne permet de maintenir cette régularité plus facilement. La guidance parentale est un complément essentiel entre les séances."},
            {"q": "Les enfants T21 peuvent-ils apprendre à lire ?", "a": "Oui ! De nombreux enfants porteurs de trisomie 21 apprennent à lire, souvent avec des méthodes adaptées qui s'appuient sur leur mémoire visuelle. L'orthophoniste accompagne cet apprentissage avec des supports spécifiques."},
        ],
        "cta_title": "Besoin d'un orthophoniste pour la trisomie 21 ?",
        "cta_desc": "Réservez votre bilan en ligne et offrez à votre enfant un accompagnement précoce et adapté pour développer son langage.",
    },
}

PSYCHO_PAGES = {
    "anxiete": {
        "title": "Psychologue Anxiété enfant en ligne",
        "meta_desc": "Votre enfant souffre d'anxiété ? Nos psychologues spécialisés proposent un accompagnement en ligne avec TCC, relaxation et exposition progressive.",
        "h1": "Psychologue spécialisé dans l'<span class=\"text-primary\">Anxiété</span> de l'enfant en ligne",
        "hero_desc": "Votre enfant a des peurs excessives, des crises d'angoisse ou évite certaines situations ? L'anxiété touche 1 enfant sur 10. Nos psychologues experts l'accompagnent en ligne avec des approches validées scientifiquement.",
        "hero_img": "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant anxieux",
        "hero_card_icon": "shield",
        "hero_card_title": "TCC adaptée",
        "hero_card_desc": "Thérapies validées scientifiquement",
        "hero_card_color": "blue",
        "symptoms_title": "Comment reconnaître l'anxiété chez l'enfant ?",
        "symptoms_intro": "L'anxiété chez l'enfant dépasse la simple peur. C'est une inquiétude excessive et persistante qui interfère avec le quotidien. Voici les signes d'alerte :",
        "symptoms": [
            {"icon": "alert-circle", "color": "red", "title": "Inquiétudes excessives", "desc": "L'enfant s'inquiète de manière disproportionnée pour l'école, la santé, la séparation avec les parents ou des catastrophes imaginaires."},
            {"icon": "moon", "color": "orange", "title": "Troubles du sommeil", "desc": "Difficultés d'endormissement, cauchemars fréquents, peur de dormir seul, réveils nocturnes liés à l'anxiété."},
            {"icon": "x-circle", "color": "purple", "title": "Évitements et somatisations", "desc": "L'enfant évite les situations angoissantes et peut développer des maux de ventre, de tête ou des nausées."},
        ],
        "approach_title": "Notre approche thérapeutique",
        "approach_desc": "Nos psychologues utilisent les Thérapies Cognitivo-Comportementales (TCC), recommandées par la HAS pour l'anxiété de l'enfant. Le programme inclut la psychoéducation, la relaxation, la restructuration cognitive et l'exposition progressive. Les parents sont intégrés au processus thérapeutique.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant s'inquiète-t-il de manière excessive au quotidien ?", "opts": ["Oui, constamment", "Souvent", "Rarement"]},
            {"q": "Évite-t-il certaines situations par peur ?", "opts": ["Oui, régulièrement", "Parfois", "Non"]},
            {"q": "A-t-il des symptômes physiques liés au stress (maux de ventre, etc.) ?", "opts": ["Oui, fréquemment", "Parfois", "Rarement"]},
        ],
        "faq": [
            {"q": "L'anxiété de l'enfant est-elle normale ?", "a": "Certaines peurs sont normales à certains âges (peur du noir, de la séparation). On parle de trouble anxieux quand l'anxiété est excessive, persistante (plus de 6 mois), et qu'elle interfère avec le quotidien de l'enfant (école, amis, famille)."},
            {"q": "La thérapie en ligne fonctionne-t-elle pour l'anxiété ?", "a": "Oui. Les études montrent que la TCC en ligne est aussi efficace que la TCC en présentiel pour l'anxiété de l'enfant. Le cadre familier du domicile peut même faciliter les exercices d'exposition progressive."},
            {"q": "Combien de séances faut-il ?", "a": "Un programme de TCC pour l'anxiété comprend généralement 12 à 16 séances. Les premiers résultats sont souvent visibles après 4-6 séances. Un suivi de consolidation peut être proposé ensuite pour prévenir les rechutes."},
        ],
        "cta_title": "Besoin d'un psychologue spécialisé en anxiété ?",
        "cta_desc": "Réservez votre première consultation en ligne et aidez votre enfant à surmonter son anxiété avec des méthodes éprouvées.",
        "category": "psychologie",
    },
    "depression": {
        "title": "Psychologue Dépression enfant en ligne",
        "meta_desc": "Votre enfant semble triste, se replie sur lui-même ? Nos psychologues spécialisés en dépression de l'enfant proposent un suivi en ligne adapté.",
        "h1": "Psychologue spécialisé dans la <span class=\"text-primary\">Dépression</span> de l'enfant en ligne",
        "hero_desc": "Votre enfant est triste en permanence, se replie sur lui-même ou a perdu goût à ses activités ? La dépression touche aussi les enfants. Nos psychologues spécialisés l'accompagnent en ligne avec bienveillance et efficacité.",
        "hero_img": "https://images.unsplash.com/photo-1541199249251-f713e6145474?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant triste",
        "hero_card_icon": "cloud-rain",
        "hero_card_title": "Écoute bienveillante",
        "hero_card_desc": "Approche adaptée à l'enfant",
        "hero_card_color": "slate",
        "symptoms_title": "Comment reconnaître la dépression chez l'enfant ?",
        "symptoms_intro": "La dépression de l'enfant se manifeste souvent différemment de celle de l'adulte. Elle peut être masquée par de l'irritabilité ou des plaintes somatiques. Voici les signes à surveiller :",
        "symptoms": [
            {"icon": "frown", "color": "red", "title": "Tristesse ou irritabilité persistante", "desc": "L'enfant est triste, pleure facilement ou devient inhabituellement irritable et colérique depuis plus de deux semaines."},
            {"icon": "battery-low", "color": "orange", "title": "Perte d'intérêt et fatigue", "desc": "Il ne prend plus plaisir à ses activités habituelles, se fatigue vite et manque d'énergie."},
            {"icon": "trending-down", "color": "purple", "title": "Baisse des résultats scolaires", "desc": "Les notes chutent, la concentration diminue et l'enfant peut exprimer un sentiment de nullité ou de culpabilité."},
        ],
        "approach_title": "Notre approche thérapeutique",
        "approach_desc": "Nous combinons TCC (restructuration des pensées négatives, activation comportementale) et approches créatives adaptées à l'âge (art-thérapie, jeux thérapeutiques). La guidance parentale est intégrée pour que les parents deviennent des alliés thérapeutiques au quotidien.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant semble-t-il triste ou irritable depuis plus de 2 semaines ?", "opts": ["Oui, en permanence", "Souvent", "Rarement"]},
            {"q": "A-t-il perdu intérêt pour ses activités habituelles ?", "opts": ["Oui, complètement", "En partie", "Non"]},
            {"q": "Son sommeil ou son appétit ont-ils changé ?", "opts": ["Oui, beaucoup", "Un peu", "Non"]},
        ],
        "faq": [
            {"q": "Un enfant peut-il vraiment être déprimé ?", "a": "Oui. La dépression touche environ 2% des enfants et 5-8% des adolescents. Elle se manifeste souvent différemment que chez l'adulte : irritabilité plutôt que tristesse, plaintes physiques, agitation ou repli."},
            {"q": "Faut-il des médicaments ?", "a": "Dans la majorité des cas, la psychothérapie seule est suffisante pour la dépression légère à modérée de l'enfant. Les antidépresseurs ne sont envisagés que pour les formes sévères ou résistantes, toujours en complément de la thérapie et sous suivi médical."},
            {"q": "Comment en parler à mon enfant ?", "a": "Normalisez le fait de parler de ses émotions. Dites-lui que consulter un psychologue, c'est comme aller chez le médecin quand on est malade, mais pour les émotions. Évitez de minimiser sa souffrance ou de lui dire de 'faire un effort'."},
        ],
        "cta_title": "Besoin d'un psychologue pour votre enfant ?",
        "cta_desc": "Réservez votre première consultation en ligne et offrez à votre enfant un espace d'écoute bienveillant pour aller mieux.",
    },
    "tdah": {
        "title": "Psychologue TDAH enfant en ligne",
        "meta_desc": "Votre enfant a un TDAH ? Nos psychologues spécialisés proposent un accompagnement en ligne : stratégies d'organisation, gestion des émotions et guidance parentale.",
        "h1": "Psychologue spécialisé dans le <span class=\"text-primary\">TDAH</span> de l'enfant en ligne",
        "hero_desc": "Votre enfant a des difficultés de concentration, bouge sans cesse ou agit de manière impulsive ? Le TDAH touche 5% des enfants. Nos psychologues spécialisés l'accompagnent en ligne avec des stratégies concrètes et efficaces.",
        "hero_img": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant énergique",
        "hero_card_icon": "zap",
        "hero_card_title": "Stratégies concrètes",
        "hero_card_desc": "Organisation et gestion des émotions",
        "hero_card_color": "yellow",
        "symptoms_title": "Comment reconnaître le TDAH chez l'enfant ?",
        "symptoms_intro": "Le TDAH (Trouble Déficit de l'Attention avec ou sans Hyperactivité) est un trouble neurodéveloppemental. Il se manifeste par trois symptômes cardinaux :",
        "symptoms": [
            {"icon": "eye-off", "color": "red", "title": "Inattention", "desc": "L'enfant a du mal à se concentrer, oublie ses affaires, est facilement distrait et peine à terminer ses tâches."},
            {"icon": "zap", "color": "orange", "title": "Hyperactivité", "desc": "Agitation motrice constante, difficulté à rester assis, besoin de bouger, parle excessivement."},
            {"icon": "fast-forward", "color": "purple", "title": "Impulsivité", "desc": "Réponses précipitées, difficulté à attendre son tour, interruption des conversations, prise de risques."},
        ],
        "approach_title": "Notre approche thérapeutique",
        "approach_desc": "Nous proposons un programme structuré incluant : des stratégies d'organisation et de planification, des techniques de gestion des émotions, un entraînement aux habiletés sociales et une guidance parentale Barkley. L'objectif est de valoriser les forces de l'enfant TDAH tout en compensant ses difficultés.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant a-t-il du mal à rester concentré sur une tâche ?", "opts": ["Oui, constamment", "Souvent", "Rarement"]},
            {"q": "Est-il souvent agité ou incapable de rester en place ?", "opts": ["Oui, en permanence", "Selon les situations", "Non"]},
            {"q": "Agit-il souvent sans réfléchir aux conséquences ?", "opts": ["Oui, très souvent", "Parfois", "Rarement"]},
        ],
        "faq": [
            {"q": "Le TDAH est-il un simple manque de discipline ?", "a": "Non. Le TDAH est un trouble neurodéveloppemental d'origine neurobiologique. Le cerveau de l'enfant TDAH fonctionne différemment, notamment au niveau de la dopamine. Ce n'est ni un caprice, ni un manque d'éducation, ni de la paresse."},
            {"q": "La psychothérapie peut-elle suffire sans médicaments ?", "a": "Pour les formes légères à modérées, les interventions psychocomportementales (TCC, guidance parentale) peuvent suffire. Pour les formes sévères, une combinaison médicament + thérapie donne les meilleurs résultats. La décision est prise avec le médecin."},
            {"q": "Le TDAH disparaît-il à l'adolescence ?", "a": "Dans environ 60% des cas, le TDAH persiste à l'âge adulte, bien que les symptômes évoluent. L'hyperactivité motrice diminue souvent, mais l'inattention et l'impulsivité peuvent persister. Les stratégies apprises en thérapie restent utiles toute la vie."},
        ],
        "cta_title": "Besoin d'un psychologue spécialisé en TDAH ?",
        "cta_desc": "Réservez votre première consultation en ligne et aidez votre enfant à développer ses stratégies pour réussir.",
    },
    "hpi": {
        "title": "Psychologue HPI enfant en ligne",
        "meta_desc": "Votre enfant est à haut potentiel intellectuel (HPI) ? Nos psychologues spécialisés proposent un accompagnement en ligne adapté à ses besoins spécifiques.",
        "h1": "Psychologue spécialisé dans le <span class=\"text-primary\">Haut Potentiel (HPI)</span> en ligne",
        "hero_desc": "Votre enfant est intellectuellement précoce, s'ennuie en classe ou a des difficultés relationnelles ? Le haut potentiel est une richesse qui nécessite parfois un accompagnement adapté. Nos psychologues experts l'aident à s'épanouir.",
        "hero_img": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant réfléchissant",
        "hero_card_icon": "lightbulb",
        "hero_card_title": "Potentiel valorisé",
        "hero_card_desc": "Comprendre et accompagner",
        "hero_card_color": "amber",
        "symptoms_title": "Comment identifier un enfant à haut potentiel ?",
        "symptoms_intro": "Le haut potentiel intellectuel (QI ≥ 130) concerne environ 2,3% de la population. Ces enfants ont des besoins spécifiques qui, s'ils ne sont pas compris, peuvent générer de la souffrance :",
        "symptoms": [
            {"icon": "brain", "color": "red", "title": "Pensée en arborescence", "desc": "L'enfant HPI pense différemment, fait des liens inattendus, pose beaucoup de questions et a une curiosité insatiable."},
            {"icon": "heart", "color": "orange", "title": "Hypersensibilité émotionnelle", "desc": "Émotions intenses, grande empathie, sensibilité aux injustices, réactions émotionnelles parfois disproportionnées."},
            {"icon": "users", "color": "purple", "title": "Décalage avec les pairs", "desc": "Sentiment de différence, difficultés à trouver des amis du même âge, préférence pour les adultes ou les enfants plus âgés."},
        ],
        "approach_title": "Notre approche thérapeutique",
        "approach_desc": "Notre accompagnement vise à aider l'enfant HPI à comprendre son fonctionnement, à gérer ses émotions intenses et à développer ses compétences sociales. Nous travaillons aussi avec les parents et l'école pour adapter l'environnement. L'objectif est que le haut potentiel soit vécu comme une force, pas comme un handicap.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant s'ennuie-t-il souvent à l'école ?", "opts": ["Oui, constamment", "Parfois", "Rarement"]},
            {"q": "A-t-il des réactions émotionnelles intenses ?", "opts": ["Oui, très souvent", "De temps en temps", "Rarement"]},
            {"q": "A-t-il du mal à se faire des amis de son âge ?", "opts": ["Oui", "Un peu", "Non, il est sociable"]},
        ],
        "faq": [
            {"q": "Comment diagnostiquer le HPI ?", "a": "Le diagnostic repose sur un bilan psychométrique (test WISC-V pour les enfants) réalisé par un psychologue. Un QI total ≥ 130 confirme le haut potentiel. Le bilan évalue aussi le profil cognitif, émotionnel et comportemental de l'enfant."},
            {"q": "Un enfant HPI a-t-il forcément des difficultés ?", "a": "Non. Beaucoup d'enfants HPI s'épanouissent parfaitement. Environ un tiers rencontre des difficultés (ennui scolaire, anxiété, difficultés relationnelles). L'accompagnement est utile quand le décalage génère de la souffrance."},
            {"q": "Faut-il sauter une classe ?", "a": "Le saut de classe peut être bénéfique pour certains enfants HPI, mais ce n'est pas systématique. La décision dépend de la maturité émotionnelle, sociale et physique de l'enfant. Le psychologue peut aider à évaluer la pertinence de cette option."},
        ],
        "cta_title": "Besoin d'un psychologue spécialisé HPI ?",
        "cta_desc": "Réservez votre première consultation en ligne et aidez votre enfant à s'épanouir avec son haut potentiel.",
    },
    "phobie-scolaire": {
        "title": "Psychologue Phobie Scolaire en ligne",
        "meta_desc": "Votre enfant refuse d'aller à l'école ? Nos psychologues spécialisés en phobie scolaire proposent un accompagnement en ligne pour un retour progressif.",
        "h1": "Psychologue spécialisé dans la <span class=\"text-primary\">Phobie Scolaire</span> en ligne",
        "hero_desc": "Votre enfant refuse d'aller à l'école, a des crises d'angoisse le matin ou présente des symptômes physiques les jours d'école ? La phobie scolaire touche 2 à 5% des enfants. Nos psychologues experts l'accompagnent en ligne.",
        "hero_img": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "École",
        "hero_card_icon": "home",
        "hero_card_title": "Retour progressif",
        "hero_card_desc": "Réintégration pas à pas",
        "hero_card_color": "emerald",
        "symptoms_title": "Comment reconnaître la phobie scolaire ?",
        "symptoms_intro": "La phobie scolaire (ou refus scolaire anxieux) n'est pas un caprice. C'est une angoisse massive liée au milieu scolaire qui empêche l'enfant de s'y rendre. Voici les signes :",
        "symptoms": [
            {"icon": "alert-triangle", "color": "red", "title": "Refus de se rendre à l'école", "desc": "Crises de larmes, supplications, tentatives de négociation ou fugues le matin au moment de partir."},
            {"icon": "thermometer", "color": "orange", "title": "Symptômes physiques", "desc": "Maux de ventre, vomissements, maux de tête qui apparaissent les jours d'école et disparaissent le week-end."},
            {"icon": "trending-down", "color": "purple", "title": "Déscolarisation progressive", "desc": "Absences de plus en plus fréquentes, retards, départs de l'école en cours de journée."},
        ],
        "approach_title": "Notre approche thérapeutique",
        "approach_desc": "Notre protocole combine TCC (exposition progressive au milieu scolaire), gestion de l'anxiété (relaxation, respiration) et travail sur l'estime de soi. Nous collaborons avec l'école pour aménager le retour. Le format en ligne est particulièrement adapté car l'enfant déscolarisé peut commencer la thérapie depuis chez lui.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant refuse-t-il d'aller à l'école ?", "opts": ["Oui, refus total", "Souvent", "Parfois"]},
            {"q": "A-t-il des symptômes physiques les jours d'école ?", "opts": ["Oui, systématiquement", "Souvent", "Rarement"]},
            {"q": "Depuis combien de temps dure cette situation ?", "opts": ["Plus d'un mois", "Quelques semaines", "Quelques jours"]},
        ],
        "faq": [
            {"q": "Mon enfant est-il fainéant ou a-t-il vraiment peur ?", "a": "La phobie scolaire n'est pas de la paresse. L'enfant ressent une angoisse réelle et incontrôlable. Il veut souvent aller à l'école mais n'y arrive pas. Cette distinction est cruciale pour adopter la bonne attitude parentale."},
            {"q": "Le forcer à aller à l'école est-il la solution ?", "a": "Non. Forcer un enfant en phobie scolaire aggrave généralement la situation. L'approche recommandée est une réintégration progressive, avec un accompagnement psychologique et des aménagements scolaires. La collaboration école-famille-thérapeute est essentielle."},
            {"q": "La thérapie en ligne est-elle adaptée pour un enfant déscolarisé ?", "a": "C'est même un format idéal. L'enfant déscolarisé n'a pas à se déplacer, ce qui lève un obstacle important. La thérapie peut démarrer immédiatement, sans attente. Et le travail d'exposition progressive vers l'école se fait ensuite par étapes."},
        ],
        "cta_title": "Besoin d'un psychologue pour la phobie scolaire ?",
        "cta_desc": "Réservez votre première consultation en ligne et accompagnez votre enfant vers un retour serein à l'école.",
    },
    "harcelement-scolaire": {
        "title": "Psychologue Harcèlement Scolaire en ligne",
        "meta_desc": "Votre enfant est victime de harcèlement scolaire ? Nos psychologues proposent un accompagnement en ligne pour l'aider à surmonter cette épreuve.",
        "h1": "Psychologue spécialisé dans le <span class=\"text-primary\">Harcèlement Scolaire</span> en ligne",
        "hero_desc": "Votre enfant est victime de moqueries, d'exclusion ou de violence à l'école ? Le harcèlement scolaire touche 1 enfant sur 10. Nos psychologues l'accompagnent en ligne pour restaurer sa confiance et développer ses ressources.",
        "hero_img": "https://images.unsplash.com/photo-1509062522246-3755977927d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant seul",
        "hero_card_icon": "shield-check",
        "hero_card_title": "Protection et confiance",
        "hero_card_desc": "Restaurer l'estime de soi",
        "hero_card_color": "blue",
        "symptoms_title": "Comment détecter le harcèlement scolaire ?",
        "symptoms_intro": "Le harcèlement scolaire est souvent silencieux. L'enfant harcelé a honte et n'ose pas en parler. Voici les signaux d'alerte à surveiller :",
        "symptoms": [
            {"icon": "eye-off", "color": "red", "title": "Changement de comportement", "desc": "L'enfant devient renfermé, ne veut plus aller à l'école, ses notes baissent et il perd confiance en lui."},
            {"icon": "smartphone", "color": "orange", "title": "Cyberharcèlement", "desc": "Messages menaçants, exclusion des groupes, photos humiliantes en ligne, anxiété liée au téléphone."},
            {"icon": "heart-crack", "color": "purple", "title": "Impact émotionnel", "desc": "Tristesse, anxiété, troubles du sommeil, perte d'appétit, et dans les cas graves, idées noires."},
        ],
        "approach_title": "Notre approche thérapeutique",
        "approach_desc": "Notre accompagnement vise à restaurer l'estime de soi de l'enfant, à développer ses habiletés sociales et d'affirmation de soi, et à traiter le traumatisme. Nous travaillons aussi avec les parents pour les aider à agir efficacement auprès de l'école. Le format en ligne offre un espace sécurisant pour l'enfant.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant a-t-il changé de comportement récemment ?", "opts": ["Oui, nettement", "Un peu", "Non"]},
            {"q": "Refuse-t-il ou évite-t-il d'aller à l'école ?", "opts": ["Oui, souvent", "Parfois", "Non"]},
            {"q": "A-t-il mentionné des problèmes avec d'autres élèves ?", "opts": ["Oui", "Il laisse entendre", "Non, mais j'ai des doutes"]},
        ],
        "faq": [
            {"q": "Comment aider mon enfant à en parler ?", "a": "Créez un climat de confiance sans pression. Posez des questions ouvertes sur sa journée, ses amis. Si vous suspectez du harcèlement, exprimez votre inquiétude sans dramatiser. Rassurez-le : ce n'est pas de sa faute et vous êtes là pour l'aider."},
            {"q": "Faut-il changer d'école ?", "a": "Le changement d'école peut être nécessaire dans certains cas, mais ce n'est pas toujours la solution. L'essentiel est de travailler sur les compétences de l'enfant pour qu'il ne soit plus dans une position de vulnérabilité. Le psychologue évalue la situation au cas par cas."},
            {"q": "Le harcèlement a-t-il des conséquences à long terme ?", "a": "Oui, le harcèlement non pris en charge peut avoir des séquelles durables : anxiété, dépression, difficultés relationnelles, syndrome de stress post-traumatique. D'où l'importance d'un accompagnement psychologique précoce pour traiter le traumatisme."},
        ],
        "cta_title": "Besoin d'un psychologue pour le harcèlement scolaire ?",
        "cta_desc": "Réservez votre première consultation en ligne et aidez votre enfant à retrouver confiance et sérénité.",
    },
    "tca": {
        "title": "Psychologue TCA enfant en ligne",
        "meta_desc": "Votre enfant a des troubles du comportement alimentaire ? Nos psychologues spécialisés en TCA proposent un accompagnement en ligne adapté.",
        "h1": "Psychologue spécialisé dans les <span class=\"text-primary\">Troubles du Comportement Alimentaire</span> en ligne",
        "hero_desc": "Votre enfant ou adolescent a un rapport problématique avec la nourriture ? Les TCA (anorexie, boulimie, hyperphagie) touchent de plus en plus de jeunes. Nos psychologues spécialisés l'accompagnent en ligne.",
        "hero_img": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Adolescent",
        "hero_card_icon": "apple",
        "hero_card_title": "Rapport sain à l'alimentation",
        "hero_card_desc": "Thérapie spécialisée TCA",
        "hero_card_color": "green",
        "symptoms_title": "Comment reconnaître un TCA chez l'enfant ou l'adolescent ?",
        "symptoms_intro": "Les troubles du comportement alimentaire se développent souvent à l'adolescence mais peuvent apparaître dès l'enfance. Voici les signaux d'alerte :",
        "symptoms": [
            {"icon": "scale", "color": "red", "title": "Préoccupation excessive du poids", "desc": "Fixation sur le poids, les calories, le corps. Comparaisons constantes, refus de certains aliments, pesées fréquentes."},
            {"icon": "eye-off", "color": "orange", "title": "Comportements cachés", "desc": "Manger en cachette, dissimuler de la nourriture, aller aux toilettes après les repas, port de vêtements amples."},
            {"icon": "trending-down", "color": "purple", "title": "Changements physiques et émotionnels", "desc": "Perte ou prise de poids rapide, fatigue, isolement, irritabilité, repli social."},
        ],
        "approach_title": "Notre approche thérapeutique",
        "approach_desc": "Notre approche combine TCC spécialisée TCA (travail sur les pensées dysfonctionnelles liées au corps et à l'alimentation), thérapie familiale (modèle Maudsley pour les jeunes patients) et psychoéducation. Nous travaillons en lien avec le médecin traitant et le nutritionniste pour une prise en charge globale.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant est-il préoccupé par son poids ou son image corporelle ?", "opts": ["Oui, de manière excessive", "Un peu", "Non"]},
            {"q": "Ses habitudes alimentaires ont-elles changé récemment ?", "opts": ["Oui, nettement", "Légèrement", "Non"]},
            {"q": "S'isole-t-il ou évite-t-il les repas en famille ?", "opts": ["Oui, souvent", "Parfois", "Non"]},
        ],
        "faq": [
            {"q": "Les TCA touchent-ils aussi les garçons ?", "a": "Oui. Même si les filles sont plus touchées (ratio 3:1), les garçons ne sont pas épargnés, notamment pour la boulimie et l'hyperphagie. Les TCA chez les garçons sont souvent sous-diagnostiqués car les signes peuvent être différents."},
            {"q": "La thérapie en ligne est-elle adaptée pour un TCA ?", "a": "Oui, pour les TCA légers à modérés. Le format en ligne permet un suivi régulier et accessible. Pour les formes sévères avec risque médical, une prise en charge en présentiel ou en hospitalisation peut être nécessaire en complément."},
            {"q": "Comment réagir si je suspecte un TCA ?", "a": "Exprimez votre inquiétude avec bienveillance, sans jugement ni commentaire sur le poids. Évitez les injonctions autour de l'alimentation. Consultez un professionnel spécialisé rapidement. Plus la prise en charge est précoce, meilleur est le pronostic."},
        ],
        "cta_title": "Besoin d'un psychologue spécialisé en TCA ?",
        "cta_desc": "Réservez votre première consultation en ligne et accompagnez votre enfant vers un rapport apaisé avec l'alimentation.",
    },
    "addictions-ecrans": {
        "title": "Psychologue Addiction aux Écrans en ligne",
        "meta_desc": "Votre enfant est accro aux écrans ? Nos psychologues spécialisés proposent un accompagnement en ligne pour retrouver un usage raisonné du numérique.",
        "h1": "Psychologue spécialisé dans les <span class=\"text-primary\">Addictions aux Écrans</span> en ligne",
        "hero_desc": "Votre enfant passe trop de temps sur les écrans, devient agressif quand on les lui retire ou néglige ses autres activités ? Nos psychologues l'accompagnent en ligne pour retrouver un équilibre numérique sain.",
        "hero_img": "https://images.unsplash.com/photo-1596742578443-7682ef5251cd?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant avec écran",
        "hero_card_icon": "monitor-off",
        "hero_card_title": "Équilibre numérique",
        "hero_card_desc": "Usage raisonné des écrans",
        "hero_card_color": "orange",
        "symptoms_title": "Comment reconnaître une addiction aux écrans ?",
        "symptoms_intro": "L'usage problématique des écrans dépasse la simple habitude. Il impacte le développement, les relations et la scolarité. Voici les signes d'alerte :",
        "symptoms": [
            {"icon": "clock", "color": "red", "title": "Perte de contrôle du temps", "desc": "L'enfant n'arrive plus à limiter son temps d'écran, ment sur sa consommation et augmente progressivement sa durée d'utilisation."},
            {"icon": "zap", "color": "orange", "title": "Réactions émotionnelles au sevrage", "desc": "Colères, agressivité, anxiété ou tristesse quand on limite ou retire l'accès aux écrans."},
            {"icon": "book-x", "color": "purple", "title": "Désinvestissement des autres activités", "desc": "Abandon du sport, des amis, baisse des résultats scolaires, perturbation du sommeil et de l'alimentation."},
        ],
        "approach_title": "Notre approche thérapeutique",
        "approach_desc": "Notre programme combine entretien motivationnel (aider l'enfant à vouloir changer), TCC (identifier les situations déclencheuses, développer des alternatives) et guidance parentale (établir un cadre numérique familial cohérent). Nous ne diabolisons pas les écrans mais travaillons sur un usage raisonné.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant passe-t-il plus de 3h/jour sur les écrans (hors école) ?", "opts": ["Oui, bien plus", "Environ 3h", "Moins de 3h"]},
            {"q": "Réagit-il fortement quand on lui retire les écrans ?", "opts": ["Oui, crises de colère", "Mécontent mais gérable", "Il accepte"]},
            {"q": "Les écrans perturbent-ils son sommeil ou sa scolarité ?", "opts": ["Oui, clairement", "Un peu", "Non"]},
        ],
        "faq": [
            {"q": "À partir de quand parle-t-on d'addiction aux écrans ?", "a": "On parle d'usage problématique quand l'enfant perd le contrôle de sa consommation, quand les écrans prennent la place des autres activités et quand le retrait provoque des réactions émotionnelles intenses. L'OMS reconnaît le trouble du jeu vidéo comme un trouble depuis 2018."},
            {"q": "Faut-il supprimer tous les écrans ?", "a": "Non. L'objectif n'est pas la suppression mais l'apprentissage d'un usage raisonné. Tous les usages ne se valent pas : créer du contenu est différent de consommer passivement. Le psychologue aide la famille à définir des règles adaptées à l'âge et au profil de l'enfant."},
            {"q": "Comment utiliser les écrans à son avantage en thérapie ?", "a": "Le format en ligne de nos séances est un paradoxe utile : l'enfant voit que l'écran peut servir à autre chose que le divertissement. Nous utilisons aussi des outils numériques thérapeutiques (applications de suivi, jeux thérapeutiques) pour maintenir sa motivation."},
        ],
        "cta_title": "Besoin d'un psychologue pour l'addiction aux écrans ?",
        "cta_desc": "Réservez votre première consultation en ligne et aidez votre enfant à retrouver un équilibre numérique sain.",
    },
    "troubles-sommeil": {
        "title": "Psychologue Troubles du Sommeil enfant en ligne",
        "meta_desc": "Votre enfant a des troubles du sommeil ? Nos psychologues proposent un accompagnement en ligne pour retrouver des nuits sereines.",
        "h1": "Psychologue spécialisé dans les <span class=\"text-primary\">Troubles du Sommeil</span> de l'enfant en ligne",
        "hero_desc": "Votre enfant a des difficultés d'endormissement, des réveils nocturnes ou des cauchemars fréquents ? Les troubles du sommeil touchent 25% des enfants. Nos psychologues l'accompagnent en ligne pour retrouver des nuits sereines.",
        "hero_img": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant dormant",
        "hero_card_icon": "moon",
        "hero_card_title": "Nuits sereines",
        "hero_card_desc": "Hygiène du sommeil et relaxation",
        "hero_card_color": "indigo",
        "symptoms_title": "Comment reconnaître les troubles du sommeil chez l'enfant ?",
        "symptoms_intro": "Les troubles du sommeil de l'enfant sont fréquents et impactent son développement, sa scolarité et l'équilibre familial. Voici les principaux signes :",
        "symptoms": [
            {"icon": "clock", "color": "red", "title": "Difficultés d'endormissement", "desc": "L'enfant met plus de 30 minutes à s'endormir, a besoin de rituels excessifs ou refuse de rester seul dans sa chambre."},
            {"icon": "alert-circle", "color": "orange", "title": "Réveils nocturnes et cauchemars", "desc": "Réveils fréquents, terreurs nocturnes, cauchemars récurrents qui perturbent la qualité du sommeil."},
            {"icon": "battery-low", "color": "purple", "title": "Fatigue diurne", "desc": "Somnolence en journée, difficultés de concentration, irritabilité, hyperactivité compensatoire."},
        ],
        "approach_title": "Notre approche thérapeutique",
        "approach_desc": "Notre programme inclut la psychoéducation sur le sommeil, la mise en place d'une hygiène du sommeil adaptée, des techniques de relaxation (respiration, imagerie mentale) et, si nécessaire, une TCC-I (Thérapie Cognitivo-Comportementale de l'Insomnie) adaptée à l'enfant. La guidance parentale est essentielle pour installer de bonnes habitudes.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant met-il plus de 30 minutes à s'endormir ?", "opts": ["Oui, souvent plus", "Environ 30 min", "Non, il s'endort vite"]},
            {"q": "Se réveille-t-il fréquemment la nuit ?", "opts": ["Oui, plusieurs fois", "Parfois", "Rarement"]},
            {"q": "Est-il fatigué ou irritable en journée ?", "opts": ["Oui, constamment", "Souvent", "Rarement"]},
        ],
        "faq": [
            {"q": "Les troubles du sommeil sont-ils normaux chez l'enfant ?", "a": "Certaines perturbations sont normales à certains âges (peur du noir vers 3-4 ans, cauchemars). On parle de trouble quand le problème persiste, impacte le quotidien et que l'enfant dort significativement moins que les recommandations pour son âge."},
            {"q": "La mélatonine est-elle une solution ?", "a": "La mélatonine peut être utile ponctuellement, sur avis médical, mais elle ne traite pas la cause. Les interventions comportementales (hygiène du sommeil, TCC-I) sont le traitement de première intention recommandé et donnent des résultats durables."},
            {"q": "Combien de temps dure la thérapie ?", "a": "Les problèmes de sommeil répondent généralement bien à un programme court de 6 à 8 séances. Les premiers résultats sont souvent visibles dès les premières semaines avec la mise en place des nouvelles routines."},
        ],
        "cta_title": "Besoin d'un psychologue pour les troubles du sommeil ?",
        "cta_desc": "Réservez votre première consultation en ligne et aidez votre enfant à retrouver un sommeil réparateur.",
    },
    "enuresie": {
        "title": "Psychologue Énurésie enfant en ligne",
        "meta_desc": "Votre enfant fait encore pipi au lit ? Nos psychologues proposent un accompagnement en ligne adapté et bienveillant pour l'énurésie.",
        "h1": "Psychologue spécialisé dans l'<span class=\"text-primary\">Énurésie</span> de l'enfant en ligne",
        "hero_desc": "Votre enfant fait encore pipi au lit après 5 ans ? L'énurésie touche 10% des enfants de 6 ans et 5% des enfants de 10 ans. Nos psychologues l'accompagnent en ligne avec bienveillance et des méthodes efficaces.",
        "hero_img": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant dormant paisiblement",
        "hero_card_icon": "droplets",
        "hero_card_title": "Accompagnement bienveillant",
        "hero_card_desc": "Sans culpabilisation",
        "hero_card_color": "sky",
        "symptoms_title": "Quand consulter pour l'énurésie ?",
        "symptoms_intro": "L'énurésie nocturne est le fait de mouiller son lit de manière involontaire et régulière après 5 ans. Elle est plus fréquente qu'on ne le pense et a souvent un impact important sur l'estime de soi :",
        "symptoms": [
            {"icon": "moon", "color": "red", "title": "Pipi au lit régulier", "desc": "L'enfant mouille son lit au moins 2 fois par semaine depuis plus de 3 mois, malgré un âge où la propreté nocturne est attendue."},
            {"icon": "frown", "color": "orange", "title": "Impact sur l'estime de soi", "desc": "Honte, culpabilité, refus d'aller dormir chez des amis, peur des moqueries, impact sur la confiance en soi."},
            {"icon": "users", "color": "purple", "title": "Retentissement social", "desc": "Évitement des nuits chez les amis, des colonies de vacances, repli social lié à la peur d'être découvert."},
        ],
        "approach_title": "Notre approche thérapeutique",
        "approach_desc": "Notre accompagnement combine psychoéducation (comprendre le mécanisme de l'énurésie), techniques comportementales (calendrier mictionnel, alarme si indiqué), gestion du stress et travail sur l'estime de soi. L'enfant est acteur de sa prise en charge, dans un cadre bienveillant et sans culpabilisation.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant mouille-t-il son lit régulièrement ?", "opts": ["Oui, plusieurs fois par semaine", "1-2 fois par semaine", "Occasionnellement"]},
            {"q": "L'énurésie impacte-t-elle sa vie sociale ?", "opts": ["Oui, il refuse les nuits chez les amis", "Un peu", "Non"]},
            {"q": "A-t-il déjà été propre la nuit pendant une période ?", "opts": ["Non, jamais", "Oui, puis c'est revenu", "Oui, longtemps"]},
        ],
        "faq": [
            {"q": "L'énurésie est-elle d'origine psychologique ?", "a": "L'énurésie primaire (l'enfant n'a jamais été propre la nuit) est le plus souvent d'origine maturative et/ou génétique. L'énurésie secondaire (retour du pipi au lit après une période de propreté) peut avoir une composante psychologique (stress, changement familial)."},
            {"q": "Faut-il punir ou gronder ?", "a": "Absolument pas. L'enfant ne fait pas exprès. Punir ou gronder aggrave le problème en augmentant le stress et en détériorant l'estime de soi. L'encouragement et la valorisation des nuits sèches sont bien plus efficaces."},
            {"q": "L'énurésie disparaît-elle toute seule ?", "a": "L'énurésie se résout spontanément chez la plupart des enfants (15% de résolution spontanée par an). Toutefois, un accompagnement accélère la résolution et surtout limite l'impact psychologique sur l'enfant et la famille."},
        ],
        "cta_title": "Besoin d'un psychologue pour l'énurésie ?",
        "cta_desc": "Réservez votre première consultation en ligne et aidez votre enfant à surmonter l'énurésie dans un cadre bienveillant.",
    },
    "traumatismes-deuil": {
        "title": "Psychologue Traumatismes et Deuil enfant en ligne",
        "meta_desc": "Votre enfant traverse un deuil ou un traumatisme ? Nos psychologues proposent un accompagnement en ligne adapté pour l'aider à traverser cette épreuve.",
        "h1": "Psychologue spécialisé dans les <span class=\"text-primary\">Traumatismes et le Deuil</span> de l'enfant en ligne",
        "hero_desc": "Votre enfant a vécu un événement traumatisant ou traverse un deuil ? Les enfants ont besoin d'un accompagnement adapté à leur âge pour traverser ces épreuves. Nos psychologues experts les accompagnent en ligne avec douceur et professionnalisme.",
        "hero_img": "https://images.unsplash.com/photo-1516627145497-ae6968895b74?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "hero_img_alt": "Enfant réconforté",
        "hero_card_icon": "hand-heart",
        "hero_card_title": "Accompagnement en douceur",
        "hero_card_desc": "EMDR et thérapie du jeu",
        "hero_card_color": "violet",
        "symptoms_title": "Comment reconnaître un traumatisme ou un deuil difficile chez l'enfant ?",
        "symptoms_intro": "Les enfants expriment leur souffrance différemment des adultes. Un traumatisme ou un deuil peut se manifester de manière inattendue. Voici les signes à surveiller :",
        "symptoms": [
            {"icon": "repeat", "color": "red", "title": "Reviviscences et jeux répétitifs", "desc": "L'enfant rejoue la scène traumatique, fait des cauchemars récurrents ou parle de manière obsessionnelle de l'événement."},
            {"icon": "alert-triangle", "color": "orange", "title": "Régressions comportementales", "desc": "Retour à des comportements plus jeunes (pipi au lit, succion du pouce), agrippement au parent, peur d'être seul."},
            {"icon": "trending-down", "color": "purple", "title": "Changement de personnalité", "desc": "Repli sur soi, agressivité inhabituelle, perte d'intérêt pour les activités, difficultés scolaires soudaines."},
        ],
        "approach_title": "Notre approche thérapeutique",
        "approach_desc": "Nous utilisons des approches validées pour le trauma chez l'enfant : EMDR adapté, thérapie par le jeu, bibliothérapie et techniques de stabilisation émotionnelle. Pour le deuil, nous accompagnons l'enfant dans la compréhension de la mort (adaptée à son âge), l'expression de ses émotions et la reconstruction de son sentiment de sécurité.",
        "approach_btn": "Découvrir le déroulement d'une séance",
        "about_img": "https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        "quiz": [
            {"q": "Votre enfant a-t-il vécu un événement traumatisant récemment ?", "opts": ["Oui, un deuil", "Oui, un autre traumatisme", "Non, mais il est en difficulté"]},
            {"q": "A-t-il des cauchemars ou des angoisses nouvelles ?", "opts": ["Oui, fréquemment", "Parfois", "Non"]},
            {"q": "Son comportement a-t-il changé depuis l'événement ?", "opts": ["Oui, nettement", "Un peu", "Non"]},
        ],
        "faq": [
            {"q": "Les enfants comprennent-ils la mort ?", "a": "La compréhension de la mort évolue avec l'âge. Avant 5-6 ans, l'enfant ne comprend pas l'irréversibilité. Entre 6 et 9 ans, il comprend que la mort est définitive mais ne se sent pas concerné. Après 9-10 ans, la compréhension est similaire à celle de l'adulte."},
            {"q": "Faut-il consulter rapidement après un traumatisme ?", "a": "Il est recommandé de consulter si les symptômes persistent au-delà de 4 semaines ou s'ils sont très intenses dès le départ. Une intervention précoce permet de prévenir l'installation d'un stress post-traumatique chronique."},
            {"q": "L'EMDR en ligne est-il efficace pour les enfants ?", "a": "Oui. L'EMDR adapté à l'enfant peut être pratiqué en ligne avec des protocoles spécifiques. Le psychologue guide l'enfant à travers des exercices de stimulation bilatérale adaptés au format vidéo, avec des résultats comparables au présentiel."},
        ],
        "cta_title": "Besoin d'un psychologue pour un traumatisme ou un deuil ?",
        "cta_desc": "Réservez votre première consultation en ligne et offrez à votre enfant un espace sûr pour traverser cette épreuve.",
    },
}

# ============================================================
# HTML TEMPLATE
# ============================================================

def generate_page(slug, data, category):
    """Generate a complete level 2 page HTML."""

    is_ortho = category == "orthophonie"
    is_psycho = category == "psychologie"
    practitioner = "orthophoniste" if is_ortho else "psychologue"

    # Build quiz JS
    quiz_js = "var quizData = [\n"
    for i, q in enumerate(data["quiz"]):
        opts_str = ", ".join([f'"{o}"' for o in q["opts"]])
        quiz_js += f'    {{q: "{q["q"]}", opts: [{opts_str}]}},\n'
    quiz_js += "];"

    # Build FAQ HTML
    faq_html = ""
    for fq in data["faq"]:
        faq_html += f"""
                <div class="border border-gray-200 rounded-2xl overflow-hidden">
                    <button class="faq-toggle w-full flex justify-between items-center p-6 text-left" onclick="toggleFaq(this)">
                        <span class="font-semibold text-gray-900 pr-4">{fq["q"]}</span>
                        <i data-lucide="plus" class="w-5 h-5 text-primary flex-shrink-0 faq-icon transition-transform"></i>
                    </button>
                    <div class="faq-content px-6 pb-0">
                        <p class="text-gray-600 leading-relaxed pb-6">{fq["a"]}</p>
                    </div>
                </div>"""

    # Build symptoms HTML
    symptoms_html = ""
    for s in data["symptoms"]:
        symptoms_html += f"""
                    <li class="flex items-start gap-3">
                        <div class="mt-1 bg-{s["color"]}-100 text-{s["color"]}-500 rounded-full p-1"><i data-lucide="{s["icon"]}" class="w-4 h-4"></i></div>
                        <span class="text-gray-700"><strong>{s["title"]} :</strong> {s["desc"]}</span>
                    </li>"""

    # Build city links
    city_links_html = ""
    for v in VILLES:
        v_slug = v.lower()
        city_links_html += f"""
                    <a href="villes/{slug}-{v_slug}.html" class="bg-white rounded-2xl p-5 text-center hover:shadow-lg transition-all group border border-gray-100">
                        <div class="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3 group-hover:bg-primary transition-colors">
                            <i data-lucide="map-pin" class="w-5 h-5 text-primary group-hover:text-white transition-colors"></i>
                        </div>
                        <span class="font-semibold text-gray-800 group-hover:text-primary transition-colors">{v}</span>
                    </a>"""

    breadcrumb_parent = "Orthophonie" if is_ortho else "Psychologie"
    breadcrumb_parent_link = f"../{category}/"
    display_name = slug.replace("-", " ").title()
    if slug == "tsa":
        display_name = "TSA"
    elif slug == "hpi":
        display_name = "HPI"
    elif slug == "tca":
        display_name = "TCA"
    elif slug == "tdah":
        display_name = "TDAH"
    elif slug == "trisomie-21":
        display_name = "Trisomie 21"

    card_color = data.get("hero_card_color", "blue")

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data["title"]} - Logopsi Studios</title>
    <meta name="description" content="{data["meta_desc"]}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: '#05C86B',
                        primaryHover: '#04b05e',
                        light: '#FBF9F6',
                        dark: '#111111'
                    }},
                    fontFamily: {{
                        sans: ['Inter', 'system-ui', 'sans-serif'],
                    }}
                }}
            }}
        }}
    </script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        body {{ font-family: 'Inter', sans-serif; }}
        .faq-content {{ transition: max-height 0.3s ease-in-out, opacity 0.3s ease-in-out, padding-bottom 0.3s ease; max-height: 0; opacity: 0; overflow: hidden; }}
        .faq-content.open {{ max-height: 500px; opacity: 1; }}
        .mega-menu-enter {{ animation: fadeInDown 0.2s ease-out forwards; }}
        @keyframes fadeInDown {{ from {{ opacity: 0; transform: translateY(-10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .modal-enter {{ animation: fadeIn 0.2s ease-out forwards; }}
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        .mega-menu {{ display: none; }}
        .mega-menu.active {{ display: block; }}
    </style>
</head>
<body class="font-sans text-gray-900 bg-light min-h-screen">

    <!-- NAVBAR -->
    <nav class="bg-white shadow-sm sticky top-0 z-50 relative">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-20">
                <a href="../index.html" class="flex items-center space-x-2 z-50">
                    <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                        <span class="text-white font-bold text-sm">L</span>
                    </div>
                    <span class="text-xl font-bold text-dark">Logopsi <span class="text-primary">Studios</span></span>
                </a>

                <div class="hidden lg:flex items-center space-x-1">
                    <div class="relative" id="ortho-trigger" onmouseenter="openMegaMenu('ortho')" onmouseleave="scheduleMegaClose('ortho')">
                        <button class="px-4 py-2 flex items-center gap-1 font-semibold text-[15px] text-gray-800 hover:text-primary transition-colors">
                            Orthophonie <i data-lucide="chevron-down" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <div class="relative" id="psycho-trigger" onmouseenter="openMegaMenu('psycho')" onmouseleave="scheduleMegaClose('psycho')">
                        <button class="px-4 py-2 flex items-center gap-1 font-semibold text-[15px] text-gray-800 hover:text-primary transition-colors">
                            Psychologie <i data-lucide="chevron-down" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <a href="../soutien-scolaire/" class="px-4 py-2 font-semibold text-[15px] text-gray-800 hover:text-primary transition-colors">Soutien Scolaire</a>
                </div>

                <div class="hidden lg:flex items-center gap-4">
                    <button class="bg-primary text-white font-semibold px-6 py-2.5 rounded-full hover:bg-primaryHover transition-colors shadow-md text-[15px]">
                        Prendre rendez-vous
                    </button>
                </div>

                <button class="lg:hidden p-2 text-gray-900 z-50" onclick="toggleMobileMenu()">
                    <i data-lucide="menu" class="w-7 h-7"></i>
                </button>
            </div>
        </div>

        <!-- Orthophonie Mega Menu -->
        <div id="ortho-mega" class="mega-menu absolute left-0 w-full bg-white shadow-xl border-t border-gray-100 z-50 mega-menu-enter" onmouseenter="cancelMegaClose('ortho')" onmouseleave="scheduleMegaClose('ortho')">
            <div class="max-w-7xl mx-auto px-6 py-8 grid grid-cols-12 gap-8">
                <div class="col-span-3 border-r border-gray-100 pr-6">
                    <h3 class="text-lg font-bold text-gray-900 mb-2">Orthophonie en ligne</h3>
                    <p class="text-sm text-gray-600 leading-relaxed">Rééducation des troubles du langage, de la communication et des apprentissages.</p>
                </div>
                <div class="col-span-6 pr-6">
                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Explorer par besoin</h4>
                    <ul class="grid grid-cols-2 gap-x-6 gap-y-2.5">
                        <li><a href="../orthophonie/dyslexie.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Dyslexie</a></li>
                        <li><a href="../orthophonie/dysorthographie.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Dysorthographie</a></li>
                        <li><a href="../orthophonie/dyscalculie.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Dyscalculie</a></li>
                        <li><a href="../orthophonie/dysphasie.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Dysphasie</a></li>
                        <li><a href="../orthophonie/begaiement.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Bégaiement</a></li>
                        <li><a href="../orthophonie/tsa.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">TSA</a></li>
                        <li><a href="../orthophonie/oralite.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Troubles de l'oralité</a></li>
                        <li><a href="../orthophonie/surdite.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Surdité</a></li>
                        <li><a href="../orthophonie/paralysie-cerebrale.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Paralysie cérébrale</a></li>
                        <li><a href="../orthophonie/fente-palatine.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Fente palatine</a></li>
                        <li><a href="../orthophonie/trisomie-21.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Trisomie 21</a></li>
                    </ul>
                </div>
                <div class="col-span-3 bg-light rounded-2xl p-5 border border-gray-100">
                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Par ville</h4>
                    <ul class="space-y-2.5">
                        <li><a href="../orthophonie/villes/paris.html" class="text-sm font-medium text-gray-800 hover:text-primary">Orthophonie à Paris</a></li>
                        <li><a href="../orthophonie/villes/marseille.html" class="text-sm font-medium text-gray-800 hover:text-primary">Orthophonie à Marseille</a></li>
                        <li><a href="../orthophonie/villes/lyon.html" class="text-sm font-medium text-gray-800 hover:text-primary">Orthophonie à Lyon</a></li>
                        <li><a href="../orthophonie/villes/toulouse.html" class="text-sm font-medium text-gray-800 hover:text-primary">Orthophonie à Toulouse</a></li>
                        <li><a href="../orthophonie/villes/nice.html" class="text-sm font-medium text-gray-800 hover:text-primary">Orthophonie à Nice</a></li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Psychologie Mega Menu -->
        <div id="psycho-mega" class="mega-menu absolute left-0 w-full bg-white shadow-xl border-t border-gray-100 z-50 mega-menu-enter" onmouseenter="cancelMegaClose('psycho')" onmouseleave="scheduleMegaClose('psycho')">
            <div class="max-w-7xl mx-auto px-6 py-8 grid grid-cols-12 gap-8">
                <div class="col-span-3 border-r border-gray-100 pr-6">
                    <h3 class="text-lg font-bold text-gray-900 mb-2">Psychologie en ligne</h3>
                    <p class="text-sm text-gray-600 leading-relaxed">Accompagnement psychologique des enfants et adolescents, partout en France.</p>
                </div>
                <div class="col-span-6 pr-6">
                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Explorer par besoin</h4>
                    <ul class="grid grid-cols-2 gap-x-6 gap-y-2.5">
                        <li><a href="../psychologie/anxiete.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Anxiété</a></li>
                        <li><a href="../psychologie/depression.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Dépression</a></li>
                        <li><a href="../psychologie/tdah.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">TDAH</a></li>
                        <li><a href="../psychologie/hpi.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Haut Potentiel (HPI)</a></li>
                        <li><a href="../psychologie/phobie-scolaire.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Phobie scolaire</a></li>
                        <li><a href="../psychologie/harcelement-scolaire.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Harcèlement scolaire</a></li>
                        <li><a href="../psychologie/tca.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">TCA</a></li>
                        <li><a href="../psychologie/addictions-ecrans.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Addictions aux écrans</a></li>
                        <li><a href="../psychologie/troubles-sommeil.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Troubles du sommeil</a></li>
                        <li><a href="../psychologie/enuresie.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Énurésie</a></li>
                        <li><a href="../psychologie/traumatismes-deuil.html" class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">Traumatismes & deuil</a></li>
                    </ul>
                </div>
                <div class="col-span-3 bg-light rounded-2xl p-5 border border-gray-100">
                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Par ville</h4>
                    <ul class="space-y-2.5">
                        <li><a href="../psychologie/villes/paris.html" class="text-sm font-medium text-gray-800 hover:text-primary">Psychologie à Paris</a></li>
                        <li><a href="../psychologie/villes/marseille.html" class="text-sm font-medium text-gray-800 hover:text-primary">Psychologie à Marseille</a></li>
                        <li><a href="../psychologie/villes/lyon.html" class="text-sm font-medium text-gray-800 hover:text-primary">Psychologie à Lyon</a></li>
                        <li><a href="../psychologie/villes/toulouse.html" class="text-sm font-medium text-gray-800 hover:text-primary">Psychologie à Toulouse</a></li>
                        <li><a href="../psychologie/villes/nice.html" class="text-sm font-medium text-gray-800 hover:text-primary">Psychologie à Nice</a></li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Mobile Menu -->
        <div id="mobile-menu" class="hidden lg:hidden bg-white border-t border-gray-100">
            <div class="px-6 py-6 space-y-4">
                <a href="../orthophonie/" class="block text-gray-900 hover:text-primary font-semibold py-2">Orthophonie</a>
                <a href="../psychologie/" class="block text-gray-900 hover:text-primary font-semibold py-2">Psychologie</a>
                <a href="../soutien-scolaire/" class="block text-gray-900 hover:text-primary font-semibold py-2">Soutien Scolaire</a>
                <button class="w-full bg-primary text-white font-semibold py-3 rounded-full shadow-md mt-4">Prendre rendez-vous</button>
            </div>
        </div>
    </nav>

    <!-- HERO SECTION -->
    <section class="pt-16 pb-20 px-6 max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center">
        <div class="space-y-6">
            <div class="flex items-center gap-2 text-sm text-gray-500 mb-4">
                <a href="../index.html" class="hover:text-primary transition-colors">Accueil</a>
                <i data-lucide="chevron-right" class="w-3.5 h-3.5"></i>
                <a href="{breadcrumb_parent_link}" class="hover:text-primary transition-colors">{breadcrumb_parent}</a>
                <i data-lucide="chevron-right" class="w-3.5 h-3.5"></i>
                <span class="text-gray-900 font-medium">{display_name}</span>
            </div>

            <h1 class="text-4xl md:text-5xl font-bold leading-[1.1] tracking-tight text-gray-900">
                {data["h1"]}
            </h1>
            <p class="text-lg text-gray-700 leading-relaxed">
                {data["hero_desc"]}
            </p>
            <div class="flex flex-col sm:flex-row gap-4 pt-4">
                <button class="bg-primary text-white font-semibold px-8 py-4 rounded-full hover:bg-primaryHover transition-colors shadow-lg flex items-center justify-center gap-2">
                    Réserver un bilan <i data-lucide="arrow-right" class="w-5 h-5"></i>
                </button>
                <button onclick="openModal()" class="bg-white text-gray-900 border-2 border-gray-200 font-semibold px-8 py-4 rounded-full hover:border-primary hover:text-primary transition-colors flex items-center justify-center">
                    Faire le test gratuit
                </button>
            </div>

            <div class="flex items-center gap-6 pt-6 border-t border-gray-200 mt-8">
                <div class="flex items-center gap-2 text-sm font-semibold text-gray-800">
                    <i data-lucide="check-circle-2" class="w-[18px] h-[18px] text-primary"></i> Prise en charge rapide
                </div>
                <div class="flex items-center gap-2 text-sm font-semibold text-gray-800">
                    <i data-lucide="check-circle-2" class="w-[18px] h-[18px] text-primary"></i> 100% en ligne
                </div>
            </div>
        </div>
        <div class="relative">
            <img src="{data["hero_img"]}" alt="{data["hero_img_alt"]}" class="rounded-[2rem] shadow-xl object-cover w-full h-[400px]">
            <div class="absolute -bottom-6 -right-6 bg-white p-5 rounded-2xl shadow-xl border border-gray-100 hidden md:block">
                <div class="flex items-center gap-3">
                    <div class="bg-{card_color}-100 text-{card_color}-600 p-2 rounded-lg">
                        <i data-lucide="{data["hero_card_icon"]}" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <p class="font-bold text-gray-900">{data["hero_card_title"]}</p>
                        <p class="text-xs text-gray-500">{data["hero_card_desc"]}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- SIMULATOR MODAL -->
    <div id="simulator-modal" class="hidden fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm modal-enter">
        <div class="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden relative">
            <button onclick="closeModal()" class="absolute top-4 right-4 p-2 text-gray-400 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-colors">
                <i data-lucide="x" class="w-6 h-6"></i>
            </button>
            <div class="p-8">
                <div id="quiz-container">
                    <div class="mb-8">
                        <span id="quiz-step-text" class="text-sm font-bold text-primary uppercase tracking-wider">Question 1 sur 3</span>
                        <div class="w-full bg-gray-100 h-2 rounded-full mt-3">
                            <div id="quiz-progress-bar" class="bg-primary h-2 rounded-full transition-all duration-300" style="width: 0%;"></div>
                        </div>
                    </div>
                    <h3 id="quiz-question-text" class="text-2xl font-bold text-gray-900 mb-8 leading-tight">Question...</h3>
                    <div id="quiz-options-container" class="space-y-3"></div>
                </div>
                <div id="result-container" class="hidden text-center py-6">
                    <div class="w-16 h-16 bg-primary/20 text-primary rounded-full flex items-center justify-center mx-auto mb-6">
                        <i data-lucide="check-circle-2" class="w-8 h-8"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-900 mb-4">Test terminé</h3>
                    <p id="result-text" class="text-gray-600 mb-8"></p>
                    <button class="w-full bg-primary text-white font-bold py-4 rounded-xl hover:bg-primaryHover transition-colors shadow-lg">
                        Prendre rendez-vous avec un expert
                    </button>
                    <button onclick="closeModal()" class="w-full mt-4 text-gray-500 font-medium hover:text-gray-800">Fermer</button>
                </div>
            </div>
        </div>
    </div>

    <!-- SYMPTOMES SECTION -->
    <section class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-6 grid md:grid-cols-2 gap-16 items-center">
            <div class="space-y-8">
                <h2 class="text-3xl font-bold text-gray-900">{data["symptoms_title"]}</h2>
                <p class="text-gray-600 leading-relaxed">{data["symptoms_intro"]}</p>
                <ul class="space-y-4">{symptoms_html}
                </ul>
            </div>
            <div class="bg-light p-8 md:p-12 rounded-3xl border border-gray-200">
                <h3 class="text-2xl font-bold mb-6 text-gray-900">{data["approach_title"]}</h3>
                <p class="text-gray-600 mb-6 text-sm leading-relaxed">{data["approach_desc"]}</p>
                <button class="w-full bg-white border-2 border-primary text-primary font-bold py-3 rounded-full hover:bg-primary hover:text-white transition-colors">
                    {data["approach_btn"]}
                </button>
            </div>
        </div>
    </section>

    <!-- A PROPOS SECTION -->
    <section class="py-20 px-6 bg-light border-t border-gray-100">
        <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center">
            <div class="order-2 md:order-1 relative">
                <div class="absolute -inset-4 bg-primary/10 rounded-3xl transform -rotate-3"></div>
                <img src="{data["about_img"]}" alt="Équipe Logopsi Studios" class="relative rounded-2xl shadow-lg w-full object-cover h-[400px]">
            </div>
            <div class="order-1 md:order-2 space-y-6">
                <div class="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold">
                    <i data-lucide="award" class="w-4 h-4"></i> Professionnels diplômés
                </div>
                <h2 class="text-3xl font-bold text-gray-900">Pourquoi choisir Logopsi Studios ?</h2>
                <p class="text-gray-600 leading-relaxed">Chez Logopsi Studios, nous réunissons des {practitioner}s diplômés d'État, formés aux dernières avancées scientifiques. Notre plateforme vous connecte avec le bon professionnel en moins de 48h, partout en France.</p>
                <div class="space-y-4">
                    <div class="flex items-start gap-3">
                        <div class="mt-1 bg-primary/10 text-primary rounded-full p-1"><i data-lucide="check" class="w-4 h-4"></i></div>
                        <span class="text-gray-700"><strong>Rendez-vous sous 48h</strong> — Plus de listes d'attente interminables</span>
                    </div>
                    <div class="flex items-start gap-3">
                        <div class="mt-1 bg-primary/10 text-primary rounded-full p-1"><i data-lucide="check" class="w-4 h-4"></i></div>
                        <span class="text-gray-700"><strong>Séances remboursables</strong> — Éligible Sécurité sociale et mutuelles</span>
                    </div>
                    <div class="flex items-start gap-3">
                        <div class="mt-1 bg-primary/10 text-primary rounded-full p-1"><i data-lucide="check" class="w-4 h-4"></i></div>
                        <span class="text-gray-700"><strong>100% en ligne</strong> — Depuis chez vous, sans déplacement</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- CITY LINKS -->
    <section class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-6">
            <div class="text-center mb-12">
                <h2 class="text-3xl font-bold text-gray-900">Consultez un {practitioner} près de chez vous</h2>
                <p class="text-gray-600 mt-3">Nos {practitioner}s sont disponibles en ligne, partout en France.</p>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">{city_links_html}
            </div>
        </div>
    </section>

    <!-- FAQ -->
    <section class="py-20 bg-light">
        <div class="max-w-3xl mx-auto px-6">
            <div class="text-center mb-12">
                <h2 class="text-3xl font-bold text-gray-900">Questions fréquentes</h2>
                <p class="text-gray-600 mt-3">Tout ce que vous devez savoir.</p>
            </div>
            <div class="space-y-4">{faq_html}
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="py-20">
        <div class="max-w-4xl mx-auto px-6">
            <div class="bg-primary rounded-3xl p-12 text-center text-white relative overflow-hidden">
                <div class="absolute inset-0 opacity-10">
                    <svg class="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                        <path d="M0,20 Q25,0 50,20 T100,20 V100 H0 Z" fill="white"/>
                    </svg>
                </div>
                <div class="relative z-10">
                    <h2 class="text-3xl font-bold mb-4">{data["cta_title"]}</h2>
                    <p class="text-lg mb-8 text-green-50">{data["cta_desc"]}</p>
                    <a href="#" class="bg-white text-primary px-8 py-4 rounded-full font-bold hover:bg-green-50 transition text-lg inline-block shadow-lg">
                        Réserver mon bilan
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- FOOTER -->
    <footer class="bg-dark py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-4 gap-8 mb-12">
                <div>
                    <div class="flex items-center space-x-2 mb-4">
                        <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                            <span class="text-white font-bold text-sm">L</span>
                        </div>
                        <span class="text-xl font-bold text-white">Logopsi <span class="text-primary">Studios</span></span>
                    </div>
                    <p class="text-gray-400 text-sm">Orthophonie, psychologie et soutien scolaire en ligne. Des professionnels diplômés, partout en France.</p>
                </div>
                <div>
                    <h4 class="text-white font-semibold mb-4">Orthophonie</h4>
                    <ul class="space-y-2">
                        <li><a href="../orthophonie/dyslexie.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Dyslexie</a></li>
                        <li><a href="../orthophonie/dysorthographie.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Dysorthographie</a></li>
                        <li><a href="../orthophonie/dyscalculie.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Dyscalculie</a></li>
                        <li><a href="../orthophonie/begaiement.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Bégaiement</a></li>
                        <li><a href="../orthophonie/tsa.html" class="text-gray-400 hover:text-primary text-sm transition-colors">TSA</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-white font-semibold mb-4">Psychologie</h4>
                    <ul class="space-y-2">
                        <li><a href="../psychologie/tdah.html" class="text-gray-400 hover:text-primary text-sm transition-colors">TDAH</a></li>
                        <li><a href="../psychologie/hpi.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Haut Potentiel</a></li>
                        <li><a href="../psychologie/phobie-scolaire.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Phobie scolaire</a></li>
                        <li><a href="../psychologie/anxiete.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Anxiété</a></li>
                        <li><a href="../psychologie/depression.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Dépression</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-white font-semibold mb-4">Soutien Scolaire</h4>
                    <ul class="space-y-2">
                        <li><a href="../soutien-scolaire/mathematiques/" class="text-gray-400 hover:text-primary text-sm transition-colors">Mathématiques</a></li>
                        <li><a href="../soutien-scolaire/francais/" class="text-gray-400 hover:text-primary text-sm transition-colors">Français</a></li>
                        <li><a href="../soutien-scolaire/anglais/" class="text-gray-400 hover:text-primary text-sm transition-colors">Anglais</a></li>
                        <li><a href="../soutien-scolaire/physique-chimie/" class="text-gray-400 hover:text-primary text-sm transition-colors">Physique-Chimie</a></li>
                        <li><a href="../soutien-scolaire/aide-aux-devoirs/" class="text-gray-400 hover:text-primary text-sm transition-colors">Aide aux devoirs</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
                <p class="text-gray-500 text-sm">&copy; 2025 Logopsi Studios. Tous droits réservés.</p>
                <div class="flex space-x-6 mt-4 md:mt-0">
                    <a href="#" class="text-gray-500 hover:text-primary text-sm transition-colors">Mentions légales</a>
                    <a href="#" class="text-gray-500 hover:text-primary text-sm transition-colors">Politique de confidentialité</a>
                    <a href="#" class="text-gray-500 hover:text-primary text-sm transition-colors">CGV</a>
                </div>
            </div>
        </div>
    </footer>

    <script>
        lucide.createIcons();

        // Mega Menu
        var megaCloseTimers = {{ ortho: null, psycho: null }};
        function openMegaMenu(menu) {{
            cancelMegaClose(menu);
            var menus = {{ ortho: 'ortho-mega', psycho: 'psycho-mega' }};
            Object.keys(menus).forEach(function(key) {{
                var el = document.getElementById(menus[key]);
                if (key === menu) {{ el.classList.add('active'); }}
                else {{ el.classList.remove('active'); clearTimeout(megaCloseTimers[key]); }}
            }});
        }}
        function scheduleMegaClose(menu) {{
            megaCloseTimers[menu] = setTimeout(function() {{
                document.getElementById(menu === 'ortho' ? 'ortho-mega' : 'psycho-mega').classList.remove('active');
            }}, 200);
        }}
        function cancelMegaClose(menu) {{ clearTimeout(megaCloseTimers[menu]); }}
        function toggleMobileMenu() {{ document.getElementById('mobile-menu').classList.toggle('hidden'); }}

        // FAQ
        function toggleFaq(btn) {{
            var content = btn.nextElementSibling;
            var icon = btn.querySelector('.faq-icon');
            var isOpen = content.classList.contains('open');
            document.querySelectorAll('.faq-content').forEach(function(c) {{ c.classList.remove('open'); }});
            document.querySelectorAll('.faq-icon').forEach(function(i) {{ i.style.transform = ''; }});
            if (!isOpen) {{
                content.classList.add('open');
                if (icon) icon.style.transform = 'rotate(45deg)';
            }}
        }}

        // Quiz Modal
        {quiz_js}
        var currentQ = 0;
        var score = 0;

        function openModal() {{
            currentQ = 0; score = 0;
            document.getElementById('simulator-modal').classList.remove('hidden');
            document.getElementById('quiz-container').classList.remove('hidden');
            document.getElementById('result-container').classList.add('hidden');
            showQuestion();
            lucide.createIcons();
        }}
        function closeModal() {{ document.getElementById('simulator-modal').classList.add('hidden'); }}
        function showQuestion() {{
            var q = quizData[currentQ];
            document.getElementById('quiz-step-text').textContent = 'Question ' + (currentQ + 1) + ' sur ' + quizData.length;
            document.getElementById('quiz-progress-bar').style.width = ((currentQ) / quizData.length * 100) + '%';
            document.getElementById('quiz-question-text').textContent = q.q;
            var container = document.getElementById('quiz-options-container');
            container.innerHTML = '';
            q.opts.forEach(function(opt, i) {{
                var btn = document.createElement('button');
                btn.className = 'w-full text-left p-4 rounded-xl border-2 border-gray-200 hover:border-primary hover:bg-primary/5 font-medium transition-all';
                btn.textContent = opt;
                btn.onclick = function() {{ selectOption(i); }};
                container.appendChild(btn);
            }});
        }}
        function selectOption(idx) {{
            if (idx === 0) score += 2;
            else if (idx === 1) score += 1;
            currentQ++;
            if (currentQ < quizData.length) {{ showQuestion(); }}
            else {{ showResult(); }}
        }}
        function showResult() {{
            document.getElementById('quiz-progress-bar').style.width = '100%';
            document.getElementById('quiz-container').classList.add('hidden');
            document.getElementById('result-container').classList.remove('hidden');
            var text = '';
            if (score >= 5) {{ text = "Les réponses indiquent des signes qui méritent une évaluation approfondie par un professionnel. Nous vous recommandons de prendre rendez-vous pour un bilan complet."; }}
            else if (score >= 3) {{ text = "Certaines réponses suggèrent des difficultés modérées. Un bilan pourrait aider à clarifier la situation et proposer un accompagnement adapté si nécessaire."; }}
            else {{ text = "Les réponses ne semblent pas indiquer de difficultés majeures pour le moment. N'hésitez pas à consulter si vous avez des doutes ou si la situation évolue."; }}
            document.getElementById('result-text').textContent = text;
            lucide.createIcons();
        }}

        // Close modal on backdrop click
        document.getElementById('simulator-modal').addEventListener('click', function(e) {{
            if (e.target === this) closeModal();
        }});
    </script>
</body>
</html>"""
    return html


# ============================================================
# GENERATION
# ============================================================

def main():
    base = "/workspaces/Logoestudios/site"
    count = 0

    # Generate orthophonie pages
    for slug, data in ORTHO_PAGES.items():
        path = os.path.join(base, "orthophonie", f"{slug}.html")
        html = generate_page(slug, data, "orthophonie")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1
        print(f"  Generated: orthophonie/{slug}.html")

    # Generate psychologie pages
    for slug, data in PSYCHO_PAGES.items():
        path = os.path.join(base, "psychologie", f"{slug}.html")
        html = generate_page(slug, data, "psychologie")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1
        print(f"  Generated: psychologie/{slug}.html")

    print(f"\nDone! Generated {count} level 2 pages.")


if __name__ == "__main__":
    main()
