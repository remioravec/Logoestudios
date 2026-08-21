# -*- coding: utf-8 -*-
"""Convertit un contenu markdown (rédaction) en HTML stylé Tailwind et l'injecte
dans une page mère orthophonie (H1, title, meta, section contenu, FAQ + schema)."""
import re, json, html as _html

def inline(t):
    t=_html.escape(t, quote=False)
    t=re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', r'<a href="\2" class="text-primary font-semibold hover:underline">\1</a>', t)
    t=re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t=t.replace(' :',' :').replace('« ','« ').replace(' »',' »')
    return t

def md_table(rows):
    # rows: list of list of cells ; 1re ligne = header
    head="".join(f'<th class="text-left font-semibold text-gray-900 px-4 py-3 border-b border-gray-200">{inline(c)}</th>' for c in rows[0])
    body=""
    for r in rows[1:]:
        body+='<tr class="border-b border-gray-100 align-top">'+"".join(f'<td class="px-4 py-3 text-gray-600">{inline(c)}</td>' for c in r)+'</tr>'
    return f'<div class="overflow-x-auto my-6"><table class="w-full text-sm border border-gray-100 rounded-xl bg-white"><thead class="bg-light">{head}</thead><tbody>{body}</tbody></table></div>'

def render_body(md):
    lines=md.split('\n')
    out=[]; i=0; n=len(lines)
    def flush_para(buf):
        if buf.strip(): out.append(f'<p>{inline(buf.strip())}</p>')
    para=""
    while i<n:
        ln=lines[i].rstrip()
        s=ln.strip()
        if not s:
            flush_para(para); para=""; i+=1; continue
        # HTML table passthrough
        if s.startswith('<table'):
            flush_para(para); para=""
            tb=[]
            while i<n and '</table>' not in lines[i]:
                tb.append(lines[i]); i+=1
            if i<n: tb.append(lines[i]); i+=1
            html="\n".join(tb)
            # re-parse cells to restyle
            rows=[]
            for tr in re.findall(r'<tr>([\s\S]*?)</tr>', html):
                cells=[re.sub(r'<[^>]+>','',c).strip() for c in re.findall(r'<t[hd]>([\s\S]*?)</t[hd]>', tr)]
                if cells: rows.append(cells)
            if rows: out.append(md_table(rows))
            continue
        # markdown table
        if s.startswith('|') and '|' in s[1:]:
            flush_para(para); para=""
            rows=[]
            while i<n and lines[i].strip().startswith('|'):
                cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c or '-') for c in cells):
                    rows.append(cells)
                i+=1
            if rows: out.append(md_table(rows))
            continue
        # H3
        if s.startswith('### '):
            flush_para(para); para=""
            out.append(f'<h3 class="text-xl font-bold text-gray-900 mt-8 mb-3">{inline(s[4:])}</h3>'); i+=1; continue
        # blockquote
        if s.startswith('> '):
            flush_para(para); para=""
            q=[]
            while i<n and lines[i].strip().startswith('> '):
                q.append(lines[i].strip()[2:]); i+=1
            out.append(f'<blockquote class="border-l-4 border-primary bg-light rounded-r-xl px-6 py-4 my-6 text-gray-700 italic">{inline(" ".join(q))}</blockquote>')
            continue
        # unordered list
        if s.startswith('- ') or s.startswith('* '):
            flush_para(para); para=""
            items=[]
            while i<n and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ')):
                items.append(lines[i].strip()[2:]); i+=1
            lis="".join(f'<li class="flex items-start gap-2"><span class="text-primary mt-1.5 shrink-0">&#10003;</span><span>{inline(x)}</span></li>' for x in items)
            out.append(f'<ul class="space-y-2 my-4 text-gray-700">{lis}</ul>'); continue
        # ordered list
        if re.match(r'\d+\.\s', s):
            flush_para(para); para=""
            items=[]
            while i<n and re.match(r'\d+\.\s', lines[i].strip()):
                items.append(re.sub(r'^\d+\.\s','',lines[i].strip())); i+=1
            lis="".join(f'<li>{inline(x)}</li>' for x in items)
            out.append(f'<ol class="list-decimal list-inside space-y-2 my-4 text-gray-700 marker:text-primary marker:font-bold">{lis}</ol>'); continue
        # bold lead-in "Xxx. reste" -> treat first sentence bold
        para=(para+" "+s).strip(); i+=1
    flush_para(para)
    return "\n".join(out)

def build(file, h1, title, metadesc, body_md, faq, faq_title):
    h=open(file,encoding="utf-8",errors="replace").read()
    # H1
    h=re.sub(r'(<h1[^>]*>)[\s\S]*?(</h1>)', lambda m:m.group(1)+_html.escape(h1,quote=False)+m.group(2), h, count=1)
    # sections
    sections=[]
    # split body into H2 sections
    parts=re.split(r'(?m)^##\s+', body_md.strip())
    lead=parts[0].strip()
    if lead:
        sections.append(f'<section class="py-14 px-6 bg-white border-t border-gray-100"><div class="max-w-4xl mx-auto text-gray-600 leading-relaxed text-lg space-y-4">{render_body(lead)}</div></section>')
    idx=0
    for p in parts[1:]:
        nl=p.find('\n'); htitle=p[:nl].strip() if nl!=-1 else p.strip(); content=p[nl+1:] if nl!=-1 else ""
        bg="bg-light" if idx%2==0 else "bg-white"; idx+=1
        sections.append(f'<section class="py-16 px-6 {bg} border-t border-gray-100"><div class="max-w-4xl mx-auto"><h2 class="text-3xl font-bold text-gray-900 mb-6">{inline(htitle)}</h2><div class="text-gray-600 leading-relaxed text-lg space-y-4">{render_body(content)}</div></div></section>')
    # FAQ
    faq_html="".join(f'<div class="bg-white rounded-2xl border border-gray-100 p-6"><h3 class="text-lg font-bold text-gray-900 mb-2">{inline(q)}</h3><p class="text-gray-600 leading-relaxed">{inline(a)}</p></div>' for q,a in faq)
    sections.append(f'<section class="py-16 px-6 bg-light border-t border-gray-100"><div class="max-w-4xl mx-auto"><h2 class="text-3xl font-bold text-gray-900 mb-6">{inline(faq_title)}</h2><div class="space-y-4">{faq_html}</div></div></section>')
    # inject between hero and CTA. Bornes robustes : après le hero (1re </section> après </nav>),
    # avant la section CTA (dernière <section ...> avant <footer>).
    nav_end=re.search(r'</nav>',h,re.I).end()
    hero_end=h.find('</section>', h.find('<section', nav_end))+len('</section>')
    foot=h.lower().find('<footer')
    cta=h.rfind('<section', 0, foot)
    h=h[:hero_end]+"\n"+"\n".join(sections)+"\n    "+h[cta:]
    # FAQ schema — on retire tout ancien FAQPage puis on ré-injecte le bon
    strip=lambda t: re.sub(r'<[^>]+>','',t)
    h=re.sub(r'<script type="application/ld\+json">[^<]*FAQPage[\s\S]*?</script>\s*', '', h)
    ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":strip(q),"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q,a in faq]}
    hi=h.lower().find('</head>'); h=h[:hi]+'<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>\n'+h[hi:]
    if title: h=re.sub(r'<title>.*?</title>',f'<title>{_html.escape(title,quote=False)}</title>',h,flags=re.S)
    if metadesc: h=re.sub(r'(<meta name="description" content=")[^"]*(")',lambda m:m.group(1)+_html.escape(metadesc,quote=True)+m.group(2),h,flags=re.I)
    open(file,"w",encoding="utf-8").write(h)
    return len(sections)
