# -*- coding: utf-8 -*-
"""Upgrade UX/UI + contenu + maillage des HUBS villes (orthophonie & psychologie).
Ajoute une grille des accompagnements de la ville (liens vers les pages filles
ville×trouble = maillage descendant), un bandeau de réassurance, du contenu
local et un maillage ascendant (page mère + accueil). Idempotent."""
import re, glob, os
HTML="wp-plugin/logopsi-deployer/data/html"; SITE="https://logopsietudes.com"; MARK="logopsi-hub"

CITY={"paris":("Paris","Paris et toute l'Île-de-France"),"lyon":("Lyon","Lyon et son agglomération"),
 "marseille":("Marseille","Marseille et ses environs"),"toulouse":("Toulouse","Toulouse et sa métropole"),
 "nice":("Nice","Nice et la Côte d'Azur")}

TR={"orthophonie":{
  "dyslexie":("Dyslexie","book-open"),"dysorthographie":("Dysorthographie","pen-line"),
  "dyscalculie":("Dyscalculie","calculator"),"dysphasie":("Dysphasie","messages-square"),
  "begaiement":("Bégaiement","audio-lines"),"tsa":("Autisme (TSA)","puzzle"),
  "oralite":("Troubles de l'oralité","utensils"),"surdite":("Surdité","ear"),
  "paralysie-cerebrale":("Paralysie cérébrale","activity"),"fente-palatine":("Fente palatine","smile"),
  "trisomie-21":("Trisomie 21","heart")},
 "psychologie":{
  "tdah":("TDAH","zap"),"hpi":("Haut potentiel (HPI)","brain"),"anxiete":("Anxiété","cloud-rain"),
  "depression":("Dépression","cloud"),"phobie-scolaire":("Phobie scolaire","door-open"),
  "harcelement-scolaire":("Harcèlement scolaire","shield"),"tca":("Troubles alimentaires","apple"),
  "addictions-ecrans":("Addiction aux écrans","smartphone"),"enuresie":("Énurésie","droplet"),
  "troubles-sommeil":("Troubles du sommeil","moon"),"traumatismes-deuil":("Traumatismes & deuil","heart-crack")}}
DISC_LABEL={"orthophonie":("orthophoniste","Orthophonie","bilan orthophonique"),
            "psychologie":("psychologue","Psychologie","bilan psychologique")}

def card(disc,trouble,city,label,icon):
    cl=CITY[city][0]
    return (f'<a href="{SITE}/{disc}/villes/{trouble}-{city}/" class="group flex items-center gap-4 bg-white rounded-2xl '
            f'border border-gray-100 p-5 hover:border-primary hover:shadow-lg transition-all">'
            f'<div class="w-12 h-12 rounded-xl bg-primary/10 text-primary flex items-center justify-center shrink-0 group-hover:bg-primary group-hover:text-white transition-colors"><i data-lucide="{icon}" class="w-6 h-6"></i></div>'
            f'<div class="min-w-0"><p class="font-semibold text-gray-900 group-hover:text-primary transition-colors">{label}</p>'
            f'<p class="text-sm text-gray-500 truncate">Bilan &amp; suivi à {cl}</p></div>'
            f'<i data-lucide="arrow-right" class="w-4 h-4 text-gray-300 group-hover:text-primary ml-auto shrink-0"></i></a>')

def section(disc, city):
    prof, disc_lab, bilan = DISC_LABEL[disc]
    cl, ctx = CITY[city]
    # enfants existants pour cette ville
    kids=[]
    for trouble,(label,icon) in TR[disc].items():
        if os.path.exists(f"{HTML}/{disc}__villes__{trouble}-{city}.html"):
            kids.append(card(disc,trouble,city,label,icon))
    grid=f'<div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">{"".join(kids)}</div>' if kids else ""
    other_cities=[c for c in CITY if c!=city]
    city_links="".join(f'<a href="{SITE}/{disc}/villes/{c}/" class="inline-flex items-center gap-1 bg-white border border-gray-200 hover:border-primary text-gray-700 hover:text-primary px-4 py-2 rounded-full text-sm font-medium transition-colors">{DISC_LABEL[disc][0].capitalize()} à {CITY[c][0]}</a>' for c in other_cities)
    return (f'\n<!-- {MARK} -->\n'
      f'<section class="py-16 px-6 bg-light border-t border-gray-100"><div class="max-w-6xl mx-auto">'
      # réassurance
      f'<div class="flex flex-wrap items-center justify-center gap-x-8 gap-y-3 mb-12 text-sm">'
      f'<span class="inline-flex items-center gap-2 font-semibold text-gray-800"><i data-lucide="badge-check" class="w-5 h-5 text-primary"></i>{prof.capitalize()}s diplômés d\'État</span>'
      f'<span class="inline-flex items-center gap-2 font-semibold text-gray-800"><i data-lucide="video" class="w-5 h-5 text-primary"></i>100&nbsp;% en ligne</span>'
      f'<span class="inline-flex items-center gap-2 font-semibold text-gray-800"><i data-lucide="clock" class="w-5 h-5 text-primary"></i>Premier bilan sous 48h</span>'
      f'<span class="inline-flex items-center gap-2 font-semibold text-gray-800"><span class="text-yellow-400">&#9733;&#9733;&#9733;&#9733;&#9733;</span>5/5 sur Google</span></div>'
      # grille accompagnements
      f'<h2 class="text-3xl font-bold text-gray-900 mb-3">Tous nos accompagnements en {disc_lab} à {cl}</h2>'
      f'<p class="text-gray-600 mb-8 max-w-3xl">Vous cherchez un <strong>{prof} à {cl}</strong> ou <strong>autour de vous</strong>&nbsp;? '
      f'Nos praticiens reçoivent en téléconsultation, partout à {ctx}, sans déplacement ni liste d\'attente. '
      f'Choisissez le trouble concerné pour découvrir le {bilan} adapté&nbsp;:</p>'
      f'{grid}'
      # contenu local
      f'<div class="mt-14 grid md:grid-cols-2 gap-8">'
      f'<div><h3 class="text-xl font-bold text-gray-900 mb-3">Pourquoi choisir la téléconsultation à {cl}&nbsp;?</h3>'
      f'<p class="text-gray-600 leading-relaxed">À {cl}, les délais pour obtenir un rendez-vous en cabinet peuvent atteindre plusieurs mois. '
      f'La téléconsultation supprime cette attente et les trajets&nbsp;: votre enfant est suivi depuis chez vous, '
      f'par le même {prof} d\'une séance à l\'autre, avec des créneaux le soir et le week-end.</p></div>'
      f'<div><h3 class="text-xl font-bold text-gray-900 mb-3">Un accompagnement reconnu et remboursable</h3>'
      f'<p class="text-gray-600 leading-relaxed">Sur prescription médicale, le suivi peut être pris en charge par l\'Assurance Maladie. '
      f'Chaque bilan donne lieu à un compte rendu écrit, utile pour l\'école (PAP) et les démarches MDPH éventuelles.</p></div></div>'
      # maillage ascendant + autres villes
      f'<div class="mt-12 pt-8 border-t border-gray-200">'
      f'<p class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Aller plus loin</p>'
      f'<div class="flex flex-wrap gap-3">'
      f'<a href="{SITE}/{disc}/" class="inline-flex items-center gap-2 bg-primary hover:bg-primaryHover text-white px-5 py-2.5 rounded-full text-sm font-semibold transition-colors"><i data-lucide="arrow-left" class="w-4 h-4"></i>Toute la {disc_lab} en ligne</a>'
      f'<a href="{SITE}/" class="inline-flex items-center gap-2 bg-white border border-gray-200 hover:border-primary text-gray-700 hover:text-primary px-5 py-2.5 rounded-full text-sm font-medium transition-colors">Accueil Logopsi Études</a>'
      f'{city_links}</div></div>'
      f'</div></section>\n<!-- /{MARK} -->\n')

def main():
    n=0
    for disc in ("orthophonie","psychologie"):
        for city in CITY:
            f=f"{HTML}/{disc}__villes__{city}.html"
            if not os.path.exists(f): continue
            h=open(f,encoding="utf-8",errors="replace").read()
            if MARK in h: continue
            idx=h.lower().rfind('<footer')
            if idx==-1: idx=h.lower().rfind('</body>')
            if idx==-1: continue
            h=h[:idx]+section(disc,city)+h[idx:]
            open(f,"w",encoding="utf-8").write(h); n+=1
    print("hubs villes upgradés:",n)

if __name__=="__main__": main()
