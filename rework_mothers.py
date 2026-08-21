# -*- coding: utf-8 -*-
"""Rework SEO des pages mères : dyslexie, dysorthographie, HPI.
H1/H2 ciblés, maillage interne, FAQ + schema.org FAQPage. Idempotent."""
import re, json
SITE="https://logopsietudes.com"
def L(t,u): return f'<a href="{u}" class="text-primary font-semibold hover:underline">{t}</a>'

def build(file, H1, HERO, LEAD, SECTIONS, FAQ, FAQ_TITLE, TITLE, DESC):
    h=open(file,encoding="utf-8",errors="replace").read()
    h=re.sub(r'(<h1[^>]*>)[\s\S]*?(</h1>)', lambda m:m.group(1)+H1+m.group(2), h, count=1)
    h=re.sub(r'(<h1[^>]*>[\s\S]*?</h1>\s*<p[^>]*>)[\s\S]*?(</p>)', lambda m:m.group(1)+HERO+m.group(2), h, count=1)
    start=h.find('<section class="py-20 bg-white">'); end=h.find('<section class="py-20">\n')
    assert start!=-1 and end!=-1 and end>start,(file,start,end)
    out=[]
    if LEAD: out.append(f'<section class="py-14 px-6 bg-white border-t border-gray-100"><div class="max-w-4xl mx-auto text-gray-600 leading-relaxed text-lg">{LEAD}</div></section>')
    for i,(title,blocks) in enumerate(SECTIONS):
        bg="bg-light" if i%2==0 else "bg-white"
        out.append(f'<section class="py-16 px-6 {bg} border-t border-gray-100"><div class="max-w-4xl mx-auto"><h2 class="text-3xl font-bold text-gray-900 mb-6">{title}</h2><div class="space-y-4 text-gray-600 leading-relaxed text-lg">{"".join(blocks)}</div></div></section>')
    faq="".join(f'<div class="bg-white rounded-2xl border border-gray-100 p-6"><h3 class="text-lg font-bold text-gray-900 mb-2">{q}</h3><p class="text-gray-600 leading-relaxed">{a}</p></div>' for q,a in FAQ)
    out.append(f'<section class="py-16 px-6 bg-light border-t border-gray-100"><div class="max-w-4xl mx-auto"><h2 class="text-3xl font-bold text-gray-900 mb-6">{FAQ_TITLE}</h2><div class="space-y-4">{faq}</div></div></section>')
    h=h[:start]+"\n".join(out)+"\n    "+h[end:]
    strip=lambda t: re.sub(r'<[^>]+>','',t).replace('&nbsp;',' ').replace('&#39;',"'").replace('&amp;','&')
    if 'FAQPage' not in h:
        ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":strip(q),"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q,a in FAQ]}
        hi=h.lower().find('</head>'); h=h[:hi]+'<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>\n'+h[hi:]
    h=re.sub(r'<title>.*?</title>',f'<title>{TITLE}</title>',h,flags=re.S)
    h=re.sub(r'(<meta name="description" content=")[^"]*(")',lambda m:m.group(1)+DESC+m.group(2),h,flags=re.I)
    open(file,"w",encoding="utf-8").write(h)
    return SECTIONS, FAQ

# ---------------- DYSLEXIE ----------------
dysx_sections=[
 ("Quels sont les signes de la dyslexie ?",[
  "<p>La dyslexie est un <strong>trouble</strong> spécifique et durable de l'acquisition de la lecture. Elle n'est liée ni à l'intelligence ni au manque de travail. Repérer tôt les signes chez l'<strong>enfant dyslexique</strong> permet d'agir avant que les difficultés ne s'installent&nbsp;: <strong>difficulté à lire</strong>, <strong>lecture lente</strong> et hachée, tendance à <strong>confondre des lettres</strong> (b/d, p/q) ou des sons, <strong>accumulation de fautes</strong> et <strong>difficultés d'orthographe</strong>, <strong>conscience phonologique</strong> fragile et grande fatigue.</p>",
  "<p>Ce <strong>trouble des apprentissages</strong> est souvent associé à d'autres troubles dys&nbsp;: voyez notre "+L("bilan dysorthographie en ligne",f"{SITE}/orthophonie/dysorthographie/")+" et notre "+L("bilan dyscalculie en ligne",f"{SITE}/orthophonie/dyscalculie/")+".</p>"]),
 ("Comment diagnostiquer la dyslexie ?",[
  "<p>Le <strong>diagnostic de la dyslexie</strong> repose sur un <strong>bilan orthophonique</strong> approfondi du langage écrit. L'orthophoniste évalue lecture, orthographe et conscience phonologique, puis <strong>pose le diagnostic</strong> en comparant aux attendus de l'âge. Un <strong>dépistage tardif</strong> reste utile&nbsp;; en cas de tableau complexe, un <strong>neuropsychologue</strong> peut réaliser un <strong>bilan neuropsychologique</strong> pour écarter d'autres causes. L'essentiel est de <strong>consulter un professionnel</strong> dès les premiers doutes.</p>",
  "<p>Nous recevons en ligne partout en France&nbsp;: "+L("bilan dyslexie à Paris",f"{SITE}/orthophonie/villes/paris/")+", "+L("à Lyon",f"{SITE}/orthophonie/villes/dyslexie-lyon/")+" ou "+L("à Marseille",f"{SITE}/orthophonie/villes/dyslexie-marseille/")+".</p>"]),
 ("Comment faire un bilan dyslexie ?",["<p>Faire un bilan dyslexie, c'est réaliser une <strong>évaluation complète du langage écrit</strong> à l'aide de <strong>tests de dépistage</strong> étalonnés. Le <strong>bilan orthophonique</strong> se déroule en une à deux séances (entretien, épreuves de lecture et d'orthographe, analyse). En cas de troubles associés, un <strong>bilan pluridisciplinaire</strong> est proposé, avec un <strong>compte rendu</strong> écrit remis à la famille.</p>"]),
 ("Quel est le processus d'évaluation ?",["<p>Le processus vise un <strong>bilan complet</strong> et objectif&nbsp;: <strong>évaluation des compétences</strong> de langage écrit, des <strong>fonctions attentionnelles</strong>, avec des <strong>tests orthonormés</strong>, une éventuelle <strong>consultation médicale</strong> ou un <strong>bilan psychologique</strong>, puis une synthèse pluridisciplinaire.</p>"]),
 ("Quelles sont les recommandations pour le diagnostic ?",["<p>Les <strong>recommandations pour le diagnostic</strong> insistent sur le <strong>dépistage précoce</strong>. La <strong>Haute Autorité de Santé (HAS)</strong> et l'<strong>Inserm</strong> (<strong>expertise collective</strong>) rappellent l'importance d'un diagnostic fondé sur la <strong>science</strong> (rapports et articles évalués) plutôt que sur des méthodes non validées.</p>"]),
 ("Quels tests pour dépister la dyslexie ?",["<p>Le <strong>test de la dyslexie</strong> officiel repose sur des <strong>outils de dépistage</strong> et <strong>tests orthonormés</strong> passés par l'orthophoniste (lecture de mots, pseudo-mots, compréhension). Les questionnaires de <strong>test dyslexie en ligne</strong> permettent un <strong>dépistage rapide</strong> mais restent indicatifs et ne remplacent pas un bilan.</p>"]),
 ("Comment accompagner un enfant dyslexique ?",["<p>L'<strong>accompagnement d'un enfant dyslexique</strong> associe <strong>rééducation orthophonique</strong>, <strong>soutien scolaire</strong> et <strong>stratégies d'apprentissage</strong>, tout en restaurant la <strong>confiance en soi</strong> et l'<strong>estime de soi</strong>. À l'école, des <strong>aménagements</strong> (PAP) et, si besoin, une reconnaissance <strong>MDPH</strong> (PPS) sécurisent le <strong>parcours scolaire</strong>. Notre "+L("bilan Anxiété en ligne",f"{SITE}/psychologie/anxiete/")+" complète la prise en charge si le stress devient un frein.</p>"]),
]
dysx_faq=[
 ("À quel âge peut-on poser un diagnostic de dyslexie ?","Un diagnostic formel se pose généralement à partir de la fin du CE1 ou du début du CE2, après environ 18 mois d'apprentissage de la lecture. Un repérage précoce des signes d'alerte est toutefois possible dès la maternelle."),
 ("Qui est habilité à poser le diagnostic de la dyslexie ?","L'orthophoniste réalise le bilan initial du langage écrit. Le diagnostic peut faire intervenir un médecin (pédiatre) ou s'inscrire dans un bilan pluridisciplinaire (neuropsychologue) pour écarter d'autres causes."),
 ("Quelle est la différence entre dyslexie, dysorthographie et dysgraphie ?","La dyslexie touche la lecture (décodage), la dysorthographie l'orthographe, et la dysgraphie le geste d'écriture (motricité fine). Elles sont souvent associées mais distinctes."),
 ("Existe-t-il des spécificités chez les adultes dyslexiques ?","Oui&nbsp;: le diagnostic est souvent tardif, des stratégies de compensation masquant le trouble. La lenteur de lecture, la fatigue cognitive et l'anxiété restent de forts indicateurs."),
 ("Combien coûte un bilan dyslexie et quels sont les délais ?","Chez Logopsi Études, le bilan est à 150&nbsp;€ avec un premier rendez-vous sous 48h, 100&nbsp;% en ligne et partout en France."),
]

# ---------------- DYSORTHOGRAPHIE ----------------
dyso_lead=("<p>Le <strong>bilan dysorthographie</strong> évalue le <strong>langage écrit</strong> d'un <strong>enfant</strong> pour distinguer un simple retard d'un véritable <strong>trouble</strong>. Cet <strong>examen</strong> analyse le <strong>profil</strong> du <strong>patient</strong> dans une logique de <strong>santé</strong> et de <strong>développement</strong>. Ce <strong>processus</strong> s'inscrit dans un "+L("écosystème global d'accompagnement",f"{SITE}/")+".</p>")
dyso_sections=[
 ("Comment repérer la dysorthographie chez un enfant ?",["<p><strong>Repérer</strong> la <strong>dysorthographie</strong> chez un <strong>enfant</strong>, c'est observer une <strong>accumulation de fautes</strong> qui persiste malgré le travail, des <strong>difficultés d'écriture</strong>, et souvent une <strong>lecture lente</strong>. À l'<strong>école</strong>, ce décalage entre les efforts et les résultats — <strong>malgré</strong> l'investissement de l'élève — est caractéristique d'un <strong>trouble d'apprentissage</strong>.</p>"]),
 ("Quels sont les signes de la dysorthographie ?",["<p>Les <strong>signes</strong> de ce <strong>trouble de l'orthographe</strong>&nbsp;: <strong>confusions</strong> de <strong>lettres</strong> (b/d), inversions de <strong>nature</strong> phonologique, omissions de syllabes, orthographe grammaticale instable. C'est la fréquence de ces <strong>fautes d'orthographe</strong> et de ces <strong>difficultés d'écriture</strong> qu'il faut savoir <strong>repérer</strong> — leurs <strong>symptômes</strong> isolés étant banals.</p>"]),
 ("Comment poser un diagnostic de dysorthographie ?",["<p><strong>Poser un diagnostic</strong> passe par une <strong>consultation</strong> avec un <strong>professionnel spécialisé</strong>&nbsp;: l'orthophoniste <strong>réalise</strong> le <strong>bilan orthophonique</strong> et évalue la <strong>conscience phonologique</strong>. La démarche est proche de celle du "+L("diagnostic de la dyslexie",f"{SITE}/orthophonie/dyslexie/")+", ce <strong>trouble d'apprentissage</strong> touchant l'<strong>enfant dysorthographique</strong>.</p>"]),
 ("Quelles sont les étapes du diagnostic ?",["<p>Les <strong>étapes du diagnostic</strong>&nbsp;: <strong>entretien</strong> initial (anamnèse), passation des épreuves étalonnées, analyse, puis <strong>mise en place</strong> d'un plan de rééducation et rédaction du <strong>compte rendu</strong>. Ce <strong>bilan</strong> des <strong>troubles dys</strong> se construit dans le <strong>temps</strong>.</p>"]),
 ("Quels tests pour diagnostiquer la dysorthographie ?",["<p>Les <strong>tests</strong> du <strong>bilan orthophonique</strong> visent le <strong>diagnostic</strong> par l'<strong>utilisation</strong> d'épreuves étalonnées&nbsp;: dictées, transcription de sons, copie. L'objectif est d'observer la gestion du <strong>code</strong> écrit et la <strong>transcription</strong>, et de <strong>rechercher</strong> les fragilités via des <strong>exercices</strong> ciblés.</p>"]),
 ("Comment réaliser un bilan pluridisciplinaire ?",["<p>En cas de <strong>troubles associés</strong>, un <strong>bilan pluridisciplinaire</strong> réunit <strong>orthophoniste</strong>, <strong>neuropsychologue</strong>, <strong>psychologue</strong> et <strong>ergothérapeute</strong> (maladresse du <strong>graphisme</strong>). Pour des <strong>calculs</strong> <strong>mentaux</strong> <strong>atypiques</strong>, un "+L("bilan dyscalculie en ligne",f"{SITE}/orthophonie/dyscalculie/")+" complète l'évaluation.</p>"]),
 ("Comment aider un enfant dysorthographique ?",["<p><strong>Aider un enfant dysorthographique</strong>&nbsp;: <strong>rééducation</strong> orthophonique, <strong>soutien</strong> scolaire, aménagements et coordination des <strong>soins</strong> avec le <strong>médecin</strong> référent, pour gagner en <strong>autonomie</strong>. Notre "+L("prise en charge de l'anxiété scolaire",f"{SITE}/psychologie/anxiete/")+" aide quand le stress s'installe.</p>"]),
]
dyso_faq=[
 ("Quelle est la différence entre un simple retard et un trouble dys ?","Un simple retard se résorbe avec le temps&nbsp;; la dysorthographie est un trouble durable, comme la dyslexie, avec une composante en partie génétique confirmée par la recherche."),
 ("Comment fonctionne le remboursement par l'Assurance Maladie ?","Les séances d'orthophonie sur ordonnance sont prises en charge par l'Assurance Maladie (suivi sur votre compte Ameli). Le bilan en ligne Logopsi est un service privé&nbsp;: vérifiez un éventuel forfait auprès de votre mutuelle."),
 ("Un enfant dyslexique est-il toujours dysorthographique ?","Pas systématiquement, mais les deux sont très souvent associés car ils partagent la même base phonologique&nbsp;: un enfant qui déchiffre difficilement, syllabe par syllabe, à voix haute, présente souvent aussi des difficultés d'orthographe."),
 ("Quels sont les liens avec le haut potentiel ou le syndrome d'Asperger ?","Un haut potentiel intellectuel ou un trouble du spectre (syndrome d'Asperger) peuvent coexister avec une dysorthographie&nbsp;; la précocité masque parfois le trouble selon la personnalité de l'enfant."),
 ("Où trouver des structures d'aide comme la PMI ?","La Protection Maternelle et Infantile (PMI), les CMPP et les centres de référence accompagnent gratuitement&nbsp;; le site internet de votre département les recense, dès la maternelle."),
 ("Quel est l'apport des travaux de l'Inserm (2007) ?","L'expertise collective de l'Inserm (2007) a synthétisé les données universitaires et publié des recommandations reprises par la HAS&nbsp;; les fédérations de patients en diffusent l'article."),
 ("Comment gérer l'impact affectif au quotidien ?","L'impact affectif est réel&nbsp;: au quotidien, valorisez les efforts, dédramatisez (ce n'est pas une maladie) et maintenez des activités de réussite. L'attention des proches est essentielle."),
]

# ---------------- HPI ----------------
hpi_lead=("<p>Le <strong>bilan HPI</strong> (haut potentiel intellectuel) permet d'identifier le fonctionnement d'un <strong>enfant</strong> ou d'un adolescent «&nbsp;surdoué&nbsp;». Réalisé par un <strong>psychologue</strong>, il repose sur un <strong>test de QI</strong> étalonné (WISC) et un entretien clinique, pour comprendre le <strong>profil</strong> cognitif et affectif. Notre suivi s'inscrit dans un "+L("écosystème global d'accompagnement",f"{SITE}/")+".</p>")
hpi_sections=[
 ("Qu'est-ce que le haut potentiel intellectuel (HPI) ?",["<p>Le <strong>haut potentiel intellectuel</strong> (HPI), aussi appelé précocité ou douance, désigne un fonctionnement cognitif intense, avec un <strong>QI</strong> généralement supérieur à 130. Il s'accompagne souvent d'une grande sensibilité, d'une pensée en arborescence et d'un fort besoin de sens. Le HPI n'est pas un trouble&nbsp;: c'est une <strong>différence</strong> qui, mal comprise, peut générer ennui, anxiété ou décrochage.</p>"]),
 ("Quels sont les signes d'un enfant à haut potentiel ?",["<p>Parmi les <strong>signes</strong>&nbsp;: curiosité insatiable, vocabulaire riche et précoce, hypersensibilité émotionnelle, sens aigu de la justice, perfectionnisme, décalage avec les camarades. Attention&nbsp;: un enfant HPI peut aussi être en <strong>échec scolaire</strong> (ennui, faux-self), d'où l'intérêt d'un <strong>bilan</strong>.</p>"]),
 ("Comment se déroule un bilan HPI (test de QI) ?",["<p>Le <strong>bilan HPI</strong> comprend un entretien, la passation d'un <strong>test psychométrique</strong> de référence (<strong>WISC-V</strong> pour l'enfant, WAIS pour l'adulte), parfois complété par un <strong>bilan neuropsychologique</strong> (attention, mémoire, fonctions exécutives). Un <strong>compte rendu</strong> détaillé est remis, avec des préconisations concrètes.</p>",
  "<p>Beaucoup de familles cherchent un «&nbsp;<strong>bilan HPI</strong>&nbsp;» ou un «&nbsp;<strong>bilan neuropsychologique enfant HPI</strong>&nbsp;» près de chez elles&nbsp;: nous recevons en ligne, partout en France — "+L("bilan HPI à Nice",f"{SITE}/psychologie/villes/hpi-nice/")+", "+L("à Lyon",f"{SITE}/psychologie/villes/hpi-lyon/")+", "+L("à Paris",f"{SITE}/psychologie/villes/hpi-paris/")+".</p>"]),
 ("Pourquoi faire diagnostiquer le haut potentiel ?",["<p>Poser un <strong>diagnostic HPI</strong> aide à comprendre l'enfant, à adapter sa scolarité (aménagements, saut de classe) et à prévenir les difficultés associées&nbsp;: <strong>anxiété</strong>, faible estime de soi, troubles du sommeil. Le bilan met des mots sur le fonctionnement et rassure toute la famille.</p>"]),
 ("Comment accompagner un enfant HPI ?",["<p>L'accompagnement combine un <strong>suivi psychologique</strong> (gestion des émotions, confiance en soi), des aménagements scolaires et, si besoin, du <strong>soutien scolaire</strong> pour raccrocher au sens. Lorsque l'anxiété domine, notre "+L("prise en charge de l'anxiété",f"{SITE}/psychologie/anxiete/")+" est indiquée&nbsp;; le HPI coexiste parfois avec un "+L("TDAH",f"{SITE}/psychologie/tdah/")+".</p>"]),
]
hpi_faq=[
 ("À partir de quel âge faire un bilan HPI ?","Un bilan est possible dès 6 ans avec le WISC-V. Avant, des outils adaptés existent, mais le test de QI est plus fiable une fois l'enfant scolarisé."),
 ("HPI et QI : quel score définit le haut potentiel ?","On parle de haut potentiel à partir d'un QI total d'environ 130 (les 2&nbsp;% les plus élevés). Le score n'est qu'un repère&nbsp;: l'analyse qualitative du profil compte tout autant."),
 ("Un enfant HPI peut-il être en échec scolaire ?","Oui, c'est fréquent&nbsp;: ennui, perte de sens, perfectionnisme paralysant ou troubles associés peuvent conduire à un décrochage malgré de grandes capacités."),
 ("HPI, TDAH, autisme : quels liens ?","Le haut potentiel peut coexister avec un TDAH ou un trouble du spectre de l'autisme (Asperger). Un bilan complet permet de démêler ces profils et d'éviter les confusions."),
 ("Combien coûte un bilan HPI et sous quel délai ?","Le bilan est proposé à un tarif clair avec un premier rendez-vous sous 48h, 100&nbsp;% en ligne et partout en France — sans les longues listes d'attente."),
]

if __name__=="__main__":
    build("wp-plugin/logopsi-deployer/data/html/orthophonie__dyslexie.html",
      "Bilan dyslexie : Évaluation, test et diagnostic complet",
      "Un bilan orthophonique complet pour évaluer, tester et poser le diagnostic de la dyslexie, chez l'enfant comme chez l'adulte. En ligne, premier rendez-vous sous 48h — 150&nbsp;€.",
      "", dysx_sections, dysx_faq, "Questions fréquentes sur le bilan de la dyslexie (FAQ)",
      "Bilan dyslexie : évaluation, test et diagnostic | Logopsi Études",
      "Bilan dyslexie en ligne : évaluation, test et diagnostic complet par un orthophoniste. Signes, tests, processus et accompagnement. RDV sous 48h — 150€.")
    build("wp-plugin/logopsi-deployer/data/html/orthophonie__dysorthographie.html",
      "Bilan dysorthographie : Évaluation, test et diagnostic complet",
      "Un bilan orthophonique complet pour évaluer, tester et diagnostiquer la dysorthographie. En ligne par un orthophoniste, premier rendez-vous sous 48h — 150&nbsp;€.",
      dyso_lead, dyso_sections, dyso_faq, "Questions fréquentes sur l'évaluation de l'écriture (FAQ)",
      "Bilan dysorthographie : évaluation, test et diagnostic | Logopsi Études",
      "Bilan dysorthographie en ligne : évaluation, test et diagnostic. Signes, tests, étapes et accompagnement. RDV sous 48h — 150€.")
    build("wp-plugin/logopsi-deployer/data/html/psychologie__hpi.html",
      "Bilan HPI : test de QI, diagnostic et accompagnement du haut potentiel",
      "Un bilan complet pour identifier le haut potentiel intellectuel (HPI) de votre enfant : test de QI (WISC), entretien clinique et préconisations. En ligne, rendez-vous sous 48h.",
      hpi_lead, hpi_sections, hpi_faq, "Questions fréquentes sur le bilan HPI (FAQ)",
      "Bilan HPI : test de QI, diagnostic et accompagnement | Logopsi Études",
      "Bilan HPI (haut potentiel) en ligne : test de QI WISC, diagnostic et accompagnement par un psychologue. Signes, déroulé, aide. RDV sous 48h.")
    print("dyslexie + dysorthographie + HPI retravaillées")
