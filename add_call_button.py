# -*- coding: utf-8 -*-
"""Accueil : bouton Appeler (hero + FAB mobile), badge avis Google, section
témoignages + correction des numéros fictifs. Idempotent."""
import re, glob
HTML="wp-plugin/logopsi-deployer/data/html"; ACC=f"{HTML}/accueil.html"
TEL="+33685747117"; TELD="06 85 74 71 17"; G="https://share.google/a474rpUqdG9p5xSUN"

PRIMARY=('<a href="#" onclick="openBookingModal(); return false;" class="bg-primary hover:bg-primaryHover '
 'text-white font-semibold px-8 py-4 rounded-full transition-colors text-center text-lg">\n'
 '                            Prendre rendez-vous\n                        </a>')
CALL=('\n                        <a href="tel:'+TEL+'" class="inline-flex items-center justify-center gap-2 '
 'border-2 border-primary text-primary hover:bg-primary hover:text-white font-semibold px-8 py-4 rounded-full '
 'transition-colors text-center text-lg"><i data-lucide="phone" class="w-5 h-5"></i>Appeler : '+TELD+'</a>')
BADGE=('\n                        <div class="w-full flex flex-wrap items-center gap-2 mt-5 text-sm">'
 '<span class="text-yellow-400 text-lg tracking-tight">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
 '<span class="font-bold text-gray-900">5/5</span><span class="text-gray-500">&middot; 15 avis</span>'
 '<a href="'+G+'" target="_blank" rel="noopener" class="inline-flex items-center gap-1 font-semibold text-gray-700 hover:text-primary">sur '
 '<span class="font-bold"><span style="color:#4285F4">G</span><span style="color:#EA4335">o</span>'
 '<span style="color:#FBBC05">o</span><span style="color:#4285F4">g</span><span style="color:#34A853">l</span>'
 '<span style="color:#EA4335">e</span></span></a></div>')
FAB=('\n<!-- logopsi-call-fab -->\n<a href="tel:'+TEL+'" class="lg:hidden fixed bottom-5 right-5 z-[90] '
 'inline-flex items-center gap-2 bg-primary text-white font-bold px-5 py-3.5 rounded-full shadow-2xl '
 'hover:bg-primaryHover animate-pulse" aria-label="Appeler maintenant au '+TELD+'">'
 '<i data-lucide="phone" class="w-5 h-5"></i>Appeler</a>\n<!-- /logopsi-call-fab -->\n')

REVS=[("Marine","il y a 3 mois","Virginie est superbe et nous avons déjà eu des membres de son équipe pour les cours d'espagnol de ma fille de 6 ans : elle est ravie ! Elle aime beaucoup sa prof, les cours sont ludiques."),
("Marie-José","il y a 3 mois","Je recommande à 100&nbsp;% cette plateforme en ligne ! Ma petite-fille, qui est en 5ème, a tellement progressé. Elle est entourée de son orthophoniste et de son enseignante."),
("Carlos Milton","il y a un an","Virginie nous suit depuis plus d'un an maintenant, et on voit notre fils progresser de jour en jour (dysgraphie-dysorthographie). Un grand merci à toute l'équipe.")]
def card(n,w,t):
    return ('<div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col">'
      f'<div class="flex items-center gap-3 mb-3"><div class="w-10 h-10 rounded-full bg-primary/10 text-primary font-bold flex items-center justify-center">{n[0]}</div>'
      f'<div><p class="font-semibold text-gray-900 leading-tight">{n}</p><p class="text-xs text-gray-400">Avis Google &middot; {w}</p></div></div>'
      f'<div class="text-yellow-400 mb-2">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="text-gray-600 text-sm leading-relaxed">&laquo;&nbsp;{t}&nbsp;&raquo;</p></div>')
def reviews():
    cards="".join(card(*r) for r in REVS)
    return ('\n<!-- logopsi-reviews -->\n<section class="py-20 px-6 bg-light border-t border-gray-100"><div class="max-w-6xl mx-auto">'
      '<div class="text-center mb-12"><div class="inline-flex items-center gap-3 bg-white rounded-full shadow-sm border border-gray-100 px-6 py-3">'
      '<span class="font-bold text-lg"><span style="color:#4285F4">G</span><span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span>'
      '<span style="color:#4285F4">g</span><span style="color:#34A853">l</span><span style="color:#EA4335">e</span></span>'
      '<span class="text-yellow-400 text-xl">&#9733;&#9733;&#9733;&#9733;&#9733;</span><span class="font-bold text-gray-900">5/5</span>'
      '<span class="text-gray-500">&middot; 15 avis</span></div>'
      '<h2 class="text-3xl md:text-4xl font-bold text-gray-900 mt-6">Nos familles témoignent</h2>'
      '<p class="text-gray-600 mt-3 max-w-2xl mx-auto">Ils nous font confiance pour l\'orthophonie, la psychologie et le soutien scolaire de leurs enfants.</p></div>'
      f'<div class="grid md:grid-cols-3 gap-6">{cards}</div>'
      '<div class="text-center mt-10 flex flex-wrap gap-4 justify-center">'
      f'<a href="{G}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 bg-white border border-gray-200 hover:border-primary text-gray-800 font-semibold px-6 py-3 rounded-full transition-colors">Voir tous nos avis Google</a>'
      f'<a href="tel:{TEL}" class="inline-flex items-center gap-2 bg-primary hover:bg-primaryHover text-white font-semibold px-6 py-3 rounded-full transition-colors"><i data-lucide="phone" class="w-5 h-5"></i>Appeler : {TELD}</a></div></div></section>\n<!-- /logopsi-reviews -->\n')

def main():
    h=open(ACC,encoding="utf-8",errors="replace").read()
    if 'tel:'+TEL not in h and PRIMARY in h:
        h=h.replace(PRIMARY, PRIMARY+CALL+BADGE, 1)
    if 'logopsi-call-fab' not in h:
        i=h.lower().rfind('</body>'); h=h[:i]+FAB+h[i:]
    if 'logopsi-reviews' not in h:
        i=h.lower().rfind('<footer'); h=h[:i]+reviews()+"\n"+h[i:]
    open(ACC,"w",encoding="utf-8").write(h)
    print("accueil.html OK — call:",'tel:'+TEL in h,"fab:",'logopsi-call-fab' in h,"reviews:",'logopsi-reviews' in h)
    fixes={"tel:+33100000000":"tel:"+TEL,"tel:+3310000000":"tel:"+TEL,"+33100000000":TELD,"+3310000000":TELD,"01 23 45 67 89":TELD}
    n=0
    for f in glob.glob(f"{HTML}/*.html"):
        c=open(f,encoding="utf-8",errors="replace").read();o=c
        for a,b in fixes.items(): c=c.replace(a,b)
        if c!=o: open(f,"w",encoding="utf-8").write(c);n+=1
    print("numéros fictifs corrigés:",n,"fichiers")

if __name__=="__main__": main()
