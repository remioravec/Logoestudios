# -*- coding: utf-8 -*-
"""Enrichit les pages templatisées (villes×trouble ortho/psy + soutien
matière×niveau[×ville]) : contenu unique (programme réel / trouble), bloc LOCAL
avec intention « autour de moi » (insight GSC), FAQ variée, maillage interne dense.
Insère un <section> avant <footer>. Idempotent (marqueur logopsi-enrich)."""
import re, glob, os
from collections import Counter
HTML="wp-plugin/logopsi-deployer/data/html"; SITE="https://logopsietudes.com"; MARK="logopsi-enrich"

CITIES={"paris":("Paris","Paris et toute l'Île-de-France — du Marais à Montparnasse en passant par les Batignolles"),
 "lyon":("Lyon","Lyon et son agglomération — Presqu'île, Croix-Rousse, Part-Dieu, Villeurbanne"),
 "marseille":("Marseille","Marseille et ses 16 arrondissements — du Vieux-Port à La Valentine, Castellane, Le Panier"),
 "toulouse":("Toulouse","Toulouse et sa métropole — Capitole, Saint-Cyprien, Rangueil, Blagnac"),
 "nice":("Nice","Nice et la Côte d'Azur — Vieux-Nice, Cimiez, Libération, jusqu'à Cagnes et Antibes")}
CITY_ORDER=["paris","lyon","marseille","toulouse","nice"]
MAT_LABEL={"mathematiques":"mathématiques","francais":"français","anglais":"anglais","espagnol":"espagnol","physique-chimie":"physique-chimie","aide-aux-devoirs":"aide aux devoirs"}
DE_MAT={"mathematiques":"de mathématiques","francais":"de français","anglais":"d'anglais","espagnol":"d'espagnol","physique-chimie":"de physique-chimie","aide-aux-devoirs":"d'aide aux devoirs"}
MAT_ORDER=["mathematiques","francais","anglais","espagnol","physique-chimie","aide-aux-devoirs"]
NIV_LABEL={"cp":"CP","ce1":"CE1","ce2":"CE2","cm1":"CM1","cm2":"CM2","6eme":"6ème","5eme":"5ème","4eme":"4ème","3eme":"3ème","seconde":"Seconde","premiere":"Première","terminale":"Terminale"}
NIV_ORDER=["cp","ce1","ce2","cm1","cm2","6eme","5eme","4eme","3eme","seconde","premiere","terminale"]
def band(n): return "primaire" if n in ("cp","ce1","ce2","cm1","cm2") else ("college" if n in ("6eme","5eme","4eme","3eme") else "lycee")
CURRIC={
 "mathematiques":{"cp":["les nombres jusqu'à 100","l'addition et la soustraction","les formes et le repérage","résoudre de petits problèmes"],"ce1":["les nombres jusqu'à 1000","les tables de multiplication","mesurer longueurs et durées","problèmes à deux étapes"],"ce2":["les nombres jusqu'à 10 000","la multiplication et la division posées","périmètres et mesures","résolution de problèmes"],"cm1":["fractions et nombres décimaux","aires et périmètres","la proportionnalité","géométrie (angles, symétrie)"],"cm2":["opérations sur les décimaux","pourcentages et proportionnalité","volumes et symétrie","préparer la 6ème"],"6eme":["fractions et décimaux","droites, angles et aires","proportionnalité","initiation à l'algorithmique"],"5eme":["nombres relatifs","début du calcul littéral","triangles et parallélogrammes","proportionnalité"],"4eme":["puissances et notation scientifique","théorème de Pythagore","calcul littéral et équations","cosinus"],"3eme":["théorème de Thalès et trigonométrie","fonctions linéaires et affines","équations et systèmes","préparation au brevet"],"seconde":["fonctions de référence","vecteurs et géométrie repérée","statistiques et probabilités","algorithmique (Python)"],"premiere":["dérivation et étude de fonctions","suites numériques","produit scalaire","probabilités conditionnelles"],"terminale":["limites et continuité","exponentielle et logarithme","calcul intégral","préparation au bac"]},
 "francais":{"cp":["le déchiffrage et la lecture","la phonologie","l'écriture et la copie","comprendre de courts textes"],"ce1":["lire de façon fluide","le présent des verbes","l'orthographe des sons","produire de courtes phrases"],"ce2":["natures et fonctions des mots","passé, présent, futur","enrichir le vocabulaire","rédiger un court texte"],"cm1":["les accords dans la phrase","les temps composés","la rédaction structurée","lecture et compréhension"],"cm2":["l'analyse grammaticale","tous les temps de l'indicatif","argumenter à l'écrit","préparer la 6ème"],"6eme":["le récit et le conte","classes grammaticales","conjugaison des temps du passé","expression écrite"],"5eme":["le récit d'aventure","les propositions subordonnées","imparfait / passé simple","vocabulaire et expression"],"4eme":["le réalisme et le fantastique","le discours rapporté","les registres de langue","la lettre et l'argumentation"],"3eme":["l'autobiographie et l'argumentation","la poésie engagée","méthode du brevet","expression écrite et orale"],"seconde":["le roman et le théâtre","la poésie et la littérature d'idées","le commentaire de texte","l'écriture d'invention"],"premiere":["les objets d'étude au programme","la dissertation littéraire","le commentaire","l'oral de l'EAF"],"terminale":["méthodologie de l'écrit et de l'oral","perfectionnement de l'expression","culture littéraire","aisance à l'oral"]},
 "anglais":{"primaire":["le vocabulaire du quotidien","les premières structures (I am, I have)","nombres, couleurs et animaux","la prononciation et les comptines"],"college":["les temps (present, past, present perfect)","le vocabulaire thématique","la compréhension orale et écrite","s'exprimer à l'oral"],"lycee":["l'expression écrite argumentée","la compréhension de documents","le vocabulaire des notions du bac","fluidité à l'oral"]},
 "espagnol":{"college":["les bases (ser/estar, présent)","le vocabulaire du quotidien","les passés (pretérito, imperfecto)","la prise de parole"],"lycee":["la grammaire (subjonctif)","la compréhension de documents","le vocabulaire des notions du bac","l'expression orale et écrite"]},
 "physique-chimie":{"college":["organisation de la matière","circuits et électricité","mouvements et forces","énergie et signaux"],"lycee":["mécanique et énergie","transformations chimiques","ondes et signaux","méthode expérimentale"]},
 "aide-aux-devoirs":{"primaire":["l'organisation des devoirs","apprendre une leçon efficacement","la lecture et les maths","reprendre confiance"],"college":["la méthode de travail et les fiches","gérer agenda et contrôles","aide dans toutes les matières","autonomie et motivation"],"lycee":["l'organisation et la prise de notes","la préparation au bac","le soutien pluridisciplinaire","gestion du stress"]},
}
def curric(mat,niv):
    d=CURRIC.get(mat,{}); return d.get(niv) or d.get(band(niv)) or d.get("college") or []
TROUBLE={"begaiement":("le bégaiement","des exercices de fluence, de respiration et de gestion des blocages"),"dyscalculie":("la dyscalculie","un travail sur le sens du nombre, le calcul et le raisonnement logico-mathématique"),"dyslexie":("la dyslexie","une rééducation de la conscience phonologique, du déchiffrage et de la fluidité de lecture"),"dysorthographie":("la dysorthographie","un renforcement de l'orthographe et de l'écriture"),"dysphasie":("la dysphasie","un accompagnement du langage oral, du vocabulaire et des phrases"),"fente-palatine":("la fente palatine","un suivi de l'articulation, de la voix et de l'alimentation"),"oralite":("les troubles de l'oralité","un travail progressif sur l'alimentation et la sensorialité"),"paralysie-cerebrale":("la paralysie cérébrale","un accompagnement de la communication et du langage"),"surdite":("la surdité","un travail du langage et de la communication adapté"),"trisomie-21":("la trisomie 21","un accompagnement du langage, de la communication et de l'autonomie"),"tsa":("les troubles du spectre de l'autisme","un travail de la communication avec des outils visuels et structurés"),"addictions-ecrans":("l'addiction aux écrans","un accompagnement pour retrouver un équilibre et poser un cadre"),"anxiete":("l'anxiété","des outils de gestion des émotions et de relaxation"),"depression":("la dépression","un soutien bienveillant pour retrouver élan et estime de soi"),"enuresie":("l'énurésie","un accompagnement en douceur, sans culpabilisation"),"harcelement-scolaire":("le harcèlement scolaire","un espace d'écoute pour reprendre confiance"),"phobie-scolaire":("la phobie scolaire","un accompagnement du retour à l'école"),"tca":("les troubles du comportement alimentaire","un suivi de la relation au corps et à l'alimentation"),"tdah":("le TDAH","des stratégies d'attention, d'organisation et de gestion de l'impulsivité"),"traumatismes-deuil":("les traumatismes et le deuil","un espace sécurisant pour traverser l'épreuve"),"troubles-sommeil":("les troubles du sommeil","un travail sur les routines et l'endormissement")}
ORTHO_TR=["begaiement","dyscalculie","dyslexie","dysorthographie","dysphasie","fente-palatine","oralite","paralysie-cerebrale","surdite","trisomie-21","tsa"]
PSY_TR=["addictions-ecrans","anxiete","depression","enuresie","harcelement-scolaire","phobie-scolaire","tca","tdah","traumatismes-deuil","troubles-sommeil"]

def li(items): return "".join(f'<li class="flex items-start gap-2"><span class="text-primary mt-1">&#10003;</span><span>{x}</span></li>' for x in items)
def card(href,label): return f'<a href="{href}" class="block bg-white rounded-xl border border-gray-100 px-4 py-3 hover:border-primary hover:shadow-sm transition-all text-gray-700 hover:text-primary font-medium">{label}</a>'
def wrap(inner): return (f'\n<!-- {MARK} -->\n<section class="py-16 bg-light border-t border-gray-100"><div class="max-w-5xl mx-auto px-6 space-y-12">{inner}</div></section>\n<!-- /{MARK} -->\n')
def mesh(cards,title):
    if not cards: return ""
    return f'<div><h2 class="text-2xl font-bold text-gray-900 mb-5">{title}</h2><div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">{"".join(cards)}</div></div>'
def faq(qas):
    items="".join(f'<div class="bg-white rounded-xl border border-gray-100 p-5"><p class="font-semibold text-gray-900 mb-1">{q}</p><p class="text-gray-600 text-sm">{a}</p></div>' for q,a in qas)
    return f'<div><h2 class="text-2xl font-bold text-gray-900 mb-5">Questions fréquentes</h2><div class="space-y-3">{items}</div></div>'

def enrich_soutien(mat,niv,ville):
    ml,nl,dm=MAT_LABEL[mat],NIV_LABEL[niv],DE_MAT[mat]; parts=[]
    topics=curric(mat,niv)
    if topics:
        parts.append(f'<div><h2 class="text-2xl font-bold text-gray-900 mb-5">Le programme {dm} en {nl}</h2><p class="text-gray-600 mb-4">En {nl}, nos enseignants travaillent précisément les attendus du programme officiel :</p><ul class="grid sm:grid-cols-2 gap-3 text-gray-700">{li(topics)}</ul></div>')
    if ville:
        cl,ctx=CITIES[ville]
        parts.append(f'<div><h2 class="text-2xl font-bold text-gray-900 mb-4">Cours {dm} en {nl} à {cl}</h2><p class="text-gray-600">Vous cherchez un professeur {dm} pour un élève de {nl} <strong>à {cl}</strong> ou <strong>autour de vous</strong> ? Nos cours sont <strong>100&nbsp;% en ligne</strong>, accessibles partout à {ctx}, sans déplacement. Le même enseignant qualifié suit votre enfant d\'une séance à l\'autre, avec des horaires souples le soir et le week-end.</p></div>')
    cards_niv=[card(f"{SITE}/soutien-scolaire/{mat}/{n}{'-'+ville if ville else ''}/", f"{ml.capitalize()} {NIV_LABEL[n]}"+(f" à {CITIES[ville][0]}" if ville else "")) for n in NIV_ORDER if n!=niv and (n in CURRIC.get(mat,{}) or band(n) in CURRIC.get(mat,{}))][:6]
    cards_mat=[card(f"{SITE}/soutien-scolaire/{m}/{niv}{'-'+ville if ville else ''}/", f"{MAT_LABEL[m].capitalize()} {nl}"+(f" à {CITIES[ville][0]}" if ville else "")) for m in MAT_ORDER if m!=mat][:5]
    m1=mesh(cards_niv,f"Autres niveaux en {ml}"+(f" à {CITIES[ville][0]}" if ville else ""))
    m2=mesh(cards_mat,f"Autres matières en {nl}"+(f" à {CITIES[ville][0]}" if ville else ""))
    hub=[card(f"{SITE}/soutien-scolaire/{mat}/",f"Tout le {ml}"),card(f"{SITE}/soutien-scolaire/","Soutien scolaire"),card(f"{SITE}/tarifs/","Nos tarifs")]
    if ville: hub.insert(1,card(f"{SITE}/soutien-scolaire/villes/{ville}/",f"Soutien scolaire à {CITIES[ville][0]}"))
    m3=mesh(hub,"Aller plus loin")
    qas=[(f"Comment se déroule un cours {dm} en {nl} ?",f"En visioconférence, avec un enseignant spécialisé du {nl}. La première séance est un bilan pour cibler les besoins, puis un programme sur mesure."),
         (f"Le suivi {dm} est-il adapté au {nl} ?",f"Oui, chaque séance suit le programme officiel de {nl} et s'adapte au rythme de l'élève.")]
    if ville: qas.append((f"Trouver un professeur {dm} à {CITIES[ville][0]} ?",f"À {CITIES[ville][0]} comme partout, nos cours sont 100&nbsp;% en ligne, sans déplacement, premier bilan sous 48h."))
    return wrap("".join(parts)+m1+m2+m3+faq(qas))

def enrich_trouble(disc,trouble,ville):
    tl,angle=TROUBLE[trouble]; cl,ctx=CITIES[ville]; prof="orthophoniste" if disc=="orthophonie" else "psychologue"
    parts=[f'<div><h2 class="text-2xl font-bold text-gray-900 mb-4">Prise en charge de {tl} à {cl}</h2><p class="text-gray-600">Vous cherchez un <strong>{prof} pour {tl} à {cl}</strong> ou <strong>autour de vous</strong> ? Les délais sont souvent longs. Avec Logopsi Études, votre enfant est suivi par un <strong>{prof} diplômé</strong> en téléconsultation, partout à {ctx}, avec un premier bilan sous 48h. Notre approche&nbsp;: {angle}.</p></div>']
    cv=[card(f"{SITE}/{disc}/villes/{trouble}-{v}/", f"{tl.capitalize()} à {CITIES[v][0]}") for v in CITY_ORDER if v!=ville]
    m1=mesh(cv,f"{tl.capitalize()} dans d'autres villes")
    disc_tr=[t for t in (ORTHO_TR if disc=="orthophonie" else PSY_TR) if t!=trouble]
    ct=[card(f"{SITE}/{disc}/villes/{t}-{ville}/", f"{TROUBLE[t][0].capitalize()} à {cl}") for t in disc_tr][:6]
    m2=mesh(ct,f"Autres accompagnements à {cl}")
    hub=[card(f"{SITE}/{disc}/{trouble}/",f"En savoir plus sur {tl}"),card(f"{SITE}/{disc}/villes/{ville}/",f"{'Orthophonie' if disc=='orthophonie' else 'Psychologie'} à {cl}"),card(f"{SITE}/{disc}/","Orthophonie en ligne" if disc=="orthophonie" else "Psychologie en ligne"),card(f"{SITE}/tarifs/","Nos tarifs")]
    m3=mesh(hub,"Aller plus loin")
    qas=[(f"Consulter pour {tl} à {cl} sans se déplacer ?",f"Oui. Les séances se font en visioconférence, de chez vous à {cl}, avec un {prof} diplômé."),
         (f"Quel délai pour un premier bilan à {cl} ?",f"Un premier rendez-vous sous 48h, sans les listes d'attente habituelles à {cl}.")]
    return wrap("".join(parts)+m1+m2+m3+faq(qas))

def main():
    files=sorted(glob.glob(f"{HTML}/*.html")); st=Counter(); CS=set(CITIES)
    for f in files:
        slug=os.path.basename(f)[:-5]; s=slug.split("__")
        block=None
        if s[0]=="soutien-scolaire" and len(s)==3:
            last=s[2]
            if "-" in last and last.rsplit("-",1)[1] in CS:
                niv,ville=last.rsplit("-",1)
                if niv in NIV_LABEL and s[1] in MAT_LABEL: block=enrich_soutien(s[1],niv,ville)
            elif last in NIV_LABEL and s[1] in MAT_LABEL:
                block=enrich_soutien(s[1],last,None)
        elif s[0] in ("orthophonie","psychologie") and len(s)==3 and s[1]=="villes":
            last=s[2]
            if "-" in last and last.rsplit("-",1)[1] in CS:
                t,ville=last.rsplit("-",1)
                if t in TROUBLE: block=enrich_trouble(s[0],t,ville)
        if not block: continue
        h=open(f,encoding="utf-8",errors="replace").read()
        if MARK in h: st["deja"]+=1; continue
        h=re.sub(r"\bde (anglais|espagnol)\b", r"d'\1", h)
        idx=h.lower().rfind('<footer')
        if idx==-1: idx=h.lower().rfind('</body>')
        if idx==-1: st["nofooter"]+=1; continue
        h=h[:idx]+block+h[idx:]
        open(f,"w",encoding="utf-8").write(h); st["enrichies"]+=1
    print("enrichies:",st["enrichies"],"| déjà:",st["deja"],"| sans footer:",st["nofooter"])
if __name__=="__main__": main()
