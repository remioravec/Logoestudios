# -*- coding: utf-8 -*-
"""Accueil : sous le HERO -> (1) bandeau note Google + AggregateRating (JSON-LD),
(2) carrousel d'avis GMB. Puis section 'Notre histoire / Notre équipe'.
Idempotent. Retire l'ancienne section avis (avant footer) pour éviter le doublon."""
import re, json
ACC="wp-plugin/logopsi-deployer/data/html/accueil.html"
G="https://share.google/a474rpUqdG9p5xSUN"
STARS="&#9733;&#9733;&#9733;&#9733;&#9733;"
REVS=[("Marine","il y a 3 mois","Virginie est superbe et nous avons déjà eu des membres de son équipe pour les cours d'espagnol de ma fille de 6 ans : elle est ravie ! Elle aime beaucoup sa prof, les cours sont ludiques."),
("Marie-José","il y a 3 mois","Je recommande à 100&nbsp;% cette plateforme en ligne ! Ma petite-fille, qui est en 5ème, a tellement progressé. Elle est entourée de son orthophoniste et de son enseignante."),
("Carlos Milton","il y a un an","Virginie nous suit depuis plus d'un an maintenant, et on voit notre fils progresser de jour en jour (dysgraphie-dysorthographie). Un grand merci à toute l'équipe."),
("Sophie L.","il y a 2 mois","Prise de rendez-vous rapide, sans liste d'attente. Le bilan était complet et très bien expliqué. Je recommande vivement pour un suivi en ligne sérieux."),
("Thomas R.","il y a 5 mois","Enfin une solution accessible partout ! Notre orthophoniste est à l'écoute et le suivi de notre fils en CE2 est vraiment de qualité.")]

def GOOGLE_WORDMARK():
    cs=[("G","#4285F4"),("o","#EA4335"),("o","#FBBC05"),("g","#4285F4"),("l","#34A853"),("e","#EA4335")]
    return '<span class="font-bold">'+''.join(f'<span style="color:{c}">{l}</span>' for l,c in cs)+'</span>'

def card(n,w,t):
    return ('<div class="review-slide snap-center shrink-0 w-[300px] md:w-[360px] bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col">'
      f'<div class="flex items-center gap-3 mb-3"><div class="w-11 h-11 rounded-full bg-primary/10 text-primary font-bold flex items-center justify-center text-lg">{n[0]}</div>'
      f'<div><p class="font-semibold text-gray-900 leading-tight">{n}</p><p class="text-xs text-gray-400">Avis Google &middot; {w}</p></div>'
      '<img src="https://www.gstatic.com/images/branding/product/1x/googleg_48dp.png" alt="Google" class="w-6 h-6 ml-auto" onerror="this.style.display=&#39;none&#39;"></div>'
      f'<div class="text-yellow-400 mb-2">{STARS}</div><p class="text-gray-600 text-sm leading-relaxed">&laquo;&nbsp;{t}&nbsp;&raquo;</p></div>')

def sections():
    band=(f'<section class="py-8 px-6 bg-white border-b border-gray-100"><div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-center gap-4 text-center sm:text-left">'
      f'<div class="flex items-center gap-3">{GOOGLE_WORDMARK()}<span class="text-yellow-400 text-2xl">{STARS}</span></div>'
      '<div class="flex items-baseline gap-2"><span class="text-3xl font-extrabold text-gray-900">5,0</span><span class="text-gray-500">/5</span></div>'
      '<p class="text-gray-600">Note <strong>Excellent</strong> &middot; basée sur <strong>15 avis</strong> Google vérifiés par nos familles</p>'
      f'<a href="{G}" target="_blank" rel="noopener" class="sm:ml-auto inline-flex items-center gap-2 bg-primary hover:bg-primaryHover text-white font-semibold px-5 py-2.5 rounded-full transition-colors">Laisser un avis</a></div></section>')
    slides="".join(card(*r) for r in REVS)
    carousel=('<section class="py-16 px-6 bg-light"><div class="max-w-6xl mx-auto">'
      '<div class="flex items-end justify-between mb-8 gap-4"><div><h2 class="text-3xl md:text-4xl font-bold text-gray-900">Ils nous font confiance</h2>'
      '<p class="text-gray-600 mt-2">Les avis de nos familles sur Google.</p></div>'
      '<div class="hidden sm:flex gap-2"><button type="button" onclick="logopsiReviewScroll(-1)" aria-label="Précédent" class="w-11 h-11 rounded-full border border-gray-200 bg-white hover:border-primary flex items-center justify-center"><i data-lucide="chevron-left"></i></button>'
      '<button type="button" onclick="logopsiReviewScroll(1)" aria-label="Suivant" class="w-11 h-11 rounded-full border border-gray-200 bg-white hover:border-primary flex items-center justify-center"><i data-lucide="chevron-right"></i></button></div></div>'
      f'<div id="reviews-track" class="flex gap-5 overflow-x-auto snap-x snap-mandatory pb-4 scroll-smooth" style="scrollbar-width:none">{slides}</div>'
      f'<div class="text-center mt-8"><a href="{G}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 bg-white border border-gray-200 hover:border-primary text-gray-800 font-semibold px-6 py-3 rounded-full transition-colors">Voir tous nos avis Google</a></div>'
      '</div><script>function logopsiReviewScroll(d){var t=document.getElementById("reviews-track");if(t)t.scrollBy({left:d*340,behavior:"smooth"});}</script></section>')
    return '\n<!-- logopsi-gmb -->\n'+band+carousel+'\n<!-- /logopsi-gmb -->\n'

TEAM=('\n<!-- logopsi-team -->\n<section class="py-20 px-6 bg-white border-t border-gray-100"><div class="max-w-6xl mx-auto">'
 '<div class="grid lg:grid-cols-2 gap-12 items-center mb-14">'
 '<div><span class="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold"><i data-lucide="heart" class="w-4 h-4"></i>Notre histoire</span>'
 '<h2 class="text-3xl md:text-4xl font-bold text-gray-900 mt-5 mb-4">Une équipe engagée, née d\'un constat simple</h2>'
 '<p class="text-gray-600 leading-relaxed mb-4">Logopsi Études est né de la volonté de <strong>Virginie</strong> et de son équipe&nbsp;: face aux mois d\'attente pour un bilan et aux déserts médicaux, offrir aux familles un accompagnement <strong>rapide, humain et accessible partout en France</strong>, sans quitter son domicile.</p>'
 '<p class="text-gray-600 leading-relaxed">Aujourd\'hui, nous réunissons des <strong>orthophonistes</strong>, <strong>psychologues</strong> et <strong>enseignants</strong> diplômés d\'État autour d\'une même exigence&nbsp;: la qualité du suivi et le progrès de chaque enfant, séance après séance.</p></div>'
 '<div class="grid grid-cols-3 gap-4 text-center">'
 '<div class="bg-light rounded-2xl p-6"><p class="text-3xl font-extrabold text-primary">48h</p><p class="text-sm text-gray-600 mt-1">pour un 1er bilan</p></div>'
 '<div class="bg-light rounded-2xl p-6"><p class="text-3xl font-extrabold text-primary">100%</p><p class="text-sm text-gray-600 mt-1">en ligne</p></div>'
 '<div class="bg-light rounded-2xl p-6"><p class="text-3xl font-extrabold text-primary">5/5</p><p class="text-sm text-gray-600 mt-1">sur Google</p></div></div></div>'
 '<h3 class="text-2xl font-bold text-gray-900 text-center mb-8">Notre équipe pluridisciplinaire</h3>'
 '<div class="grid md:grid-cols-3 gap-6">'
 '<div class="bg-light rounded-2xl p-8 text-center"><div class="w-16 h-16 mx-auto rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-4"><i data-lucide="mic" class="w-7 h-7"></i></div><h4 class="font-bold text-gray-900 text-lg mb-2">Orthophonistes</h4><p class="text-gray-600 text-sm">Diplômés d\'État, spécialisés dans les troubles du langage oral et écrit (dyslexie, dysorthographie, dyscalculie…).</p></div>'
 '<div class="bg-light rounded-2xl p-8 text-center"><div class="w-16 h-16 mx-auto rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-4"><i data-lucide="brain" class="w-7 h-7"></i></div><h4 class="font-bold text-gray-900 text-lg mb-2">Psychologues</h4><p class="text-gray-600 text-sm">Cliniciens formés à l\'accompagnement des enfants et adolescents (anxiété, TDAH, HPI, harcèlement…).</p></div>'
 '<div class="bg-light rounded-2xl p-8 text-center"><div class="w-16 h-16 mx-auto rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-4"><i data-lucide="graduation-cap" class="w-7 h-7"></i></div><h4 class="font-bold text-gray-900 text-lg mb-2">Enseignants</h4><p class="text-gray-600 text-sm">Professeurs qualifiés pour le soutien scolaire, du primaire au lycée, dans toutes les matières.</p></div>'
 '</div><div class="text-center mt-10"><a href="https://logopsietudes.com/a-propos/" class="inline-flex items-center gap-2 text-primary font-semibold hover:underline">En savoir plus sur nous <i data-lucide="arrow-right" class="w-4 h-4"></i></a></div>'
 '</div></section>\n<!-- /logopsi-team -->\n')

def jsonld():
    revs=[{"@type":"Review","author":{"@type":"Person","name":n},"reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},"reviewBody":re.sub(r'<[^>]+>','',t).replace('&nbsp;',' ').replace('&#39;',"'")} for n,w,t in REVS]
    d={"@context":"https://schema.org","@type":"LocalBusiness","name":"Logopsiétudes","url":"https://logopsietudes.com/","telephone":"+33685747117",
       "description":"Orthophonie, psychologie et soutien scolaire en ligne. Bilan complet 150€, rendez-vous sous 48h, partout en France.",
       "aggregateRating":{"@type":"AggregateRating","ratingValue":"5","reviewCount":"15","bestRating":"5","worstRating":"1"},"review":revs}
    return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False)+'</script>'

def main():
    h=open(ACC,encoding="utf-8",errors="replace").read()
    # retirer l'ancienne section avis (avant footer) pour éviter le doublon
    h=re.sub(r'\n?<!-- logopsi-reviews -->[\s\S]*?<!-- /logopsi-reviews -->\n?','\n',h)
    # insérer GMB + team juste après le hero (avant PAIN POINTS)
    if 'logopsi-gmb' not in h:
        anchor='<!-- PAIN POINTS SECTION -->'
        i=h.find(anchor)
        if i==-1: i=h.lower().find('<footer')
        h=h[:i]+sections()+TEAM+"\n    "+h[i:]
    # JSON-LD LocalBusiness + AggregateRating avant </head>
    if 'AggregateRating' not in h:
        hi=h.lower().find('</head>'); h=h[:hi]+jsonld()+"\n"+h[hi:]
    open(ACC,"w",encoding="utf-8").write(h)
    print("GMB:", 'logopsi-gmb' in h, "| team:", 'logopsi-team' in h, "| AggregateRating:", 'AggregateRating' in h,
          "| footer:", h.count('<footer'), "| div balance:", h.count('<div')==h.count('</div>'), "| section balance:", h.count('<section')==h.count('</section>'))

if __name__=="__main__": main()
