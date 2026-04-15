#!/usr/bin/env python3
"""Reusable HTML component functions for the Logopsi Studios site generator.

Every function returns a plain Python string containing final HTML.
The `prefix` parameter handles relative paths for pages at different depths:
  - site/psychologie/          -> prefix = "../"
  - site/psychologie/villes/   -> prefix = "../../"
  - site/ root                 -> prefix = "./"
"""


# ------------------------------------------------------------------
# 1. HEAD
# ------------------------------------------------------------------

def get_head(title, meta_desc, include_faq_css=True):
    """Return the full <head> block through the opening <body> tag."""

    faq_css = ""
    if include_faq_css:
        faq_css = (
            "        .faq-content { transition: max-height 0.3s ease-in-out, opacity 0.3s ease-in-out, padding-bottom 0.3s ease; max-height: 0; opacity: 0; overflow: hidden; }\n"
            "        .faq-content.open { max-height: 500px; opacity: 1; }\n"
        )

    return (
        '<!DOCTYPE html>\n'
        '<html lang="fr">\n'
        '<head>\n'
        '    <meta charset="UTF-8">\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '    <title>' + title + ' - Logopsi Studios</title>\n'
        '    <meta name="description" content="' + meta_desc + '">\n'
        '    <script src="https://cdn.tailwindcss.com"></script>\n'
        '    <script>\n'
        '        tailwind.config = {\n'
        '            theme: {\n'
        '                extend: {\n'
        '                    colors: {\n'
        "                        primary: '#05C86B',\n"
        "                        primaryHover: '#04b05e',\n"
        "                        light: '#FBF9F6',\n"
        "                        dark: '#111111'\n"
        '                    },\n'
        '                    fontFamily: {\n'
        "                        sans: ['Inter', 'system-ui', 'sans-serif'],\n"
        '                    }\n'
        '                }\n'
        '            }\n'
        '        }\n'
        '    </script>\n'
        '    <script src="https://unpkg.com/lucide@latest"></script>\n'
        '    <style>\n'
        "        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');\n"
        "        body { font-family: 'Inter', sans-serif; }\n"
        + faq_css +
        '        .mega-menu-enter { animation: fadeInDown 0.2s ease-out forwards; }\n'
        '        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }\n'
        '        .modal-enter { animation: fadeIn 0.2s ease-out forwards; }\n'
        '        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }\n'
        '        .mega-menu { display: none; }\n'
        '        .mega-menu.active { display: block; }\n'
        '    </style>\n'
        '</head>\n'
        '<body class="font-sans text-gray-900 bg-light min-h-screen">\n'
    )


# ------------------------------------------------------------------
# 2. NAVBAR
# ------------------------------------------------------------------

def get_navbar(prefix):
    """Return the complete navbar HTML with 3 mega menus and mobile menu."""

    # --- Orthophonie trouble links ---
    ortho_troubles = [
        ("dyslexie", "Dyslexie"),
        ("dysorthographie", "Dysorthographie"),
        ("dyscalculie", "Dyscalculie"),
        ("dysphasie", "Dysphasie"),
        ("begaiement", "B\u00e9gaiement"),
        ("tsa", "TSA"),
        ("oralite", "Troubles de l'oralit\u00e9"),
        ("surdite", "Surdit\u00e9"),
        ("paralysie-cerebrale", "Paralysie c\u00e9r\u00e9brale"),
        ("fente-palatine", "Fente palatine"),
        ("trisomie-21", "Trisomie 21"),
    ]

    ortho_links = ""
    for slug, label in ortho_troubles:
        ortho_links += (
            '                        <li><a href="' + prefix + 'orthophonie/' + slug + '.html" '
            'class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">'
            + label + '</a></li>\n'
        )

    # --- Psychologie trouble links ---
    psycho_troubles = [
        ("anxiete", "Anxi\u00e9t\u00e9"),
        ("depression", "D\u00e9pression"),
        ("tdah", "TDAH"),
        ("hpi", "Haut Potentiel (HPI)"),
        ("phobie-scolaire", "Phobie scolaire"),
        ("harcelement-scolaire", "Harc\u00e8lement scolaire"),
        ("tca", "TCA"),
        ("addictions-ecrans", "Addictions aux \u00e9crans"),
        ("troubles-sommeil", "Troubles du sommeil"),
        ("enuresie", "\u00c9nur\u00e9sie"),
        ("traumatismes-deuil", "Traumatismes & deuil"),
    ]

    psycho_links = ""
    for slug, label in psycho_troubles:
        psycho_links += (
            '                        <li><a href="' + prefix + 'psychologie/' + slug + '.html" '
            'class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">'
            + label + '</a></li>\n'
        )

    # --- Soutien scolaire subject links ---
    scolaire_subjects = [
        ("mathematiques", "Math\u00e9matiques"),
        ("francais", "Fran\u00e7ais"),
        ("anglais", "Anglais"),
        ("physique-chimie", "Physique-Chimie"),
        ("aide-aux-devoirs", "Aide aux devoirs"),
    ]

    scolaire_links = ""
    for slug, label in scolaire_subjects:
        scolaire_links += (
            '                        <li><a href="' + prefix + 'soutien-scolaire/' + slug + '/" '
            'class="text-sm font-medium text-gray-700 hover:text-primary transition-colors">'
            + label + '</a></li>\n'
        )

    # --- City links helper ---
    def city_links(section, label_prefix):
        cities = [
            ("paris", "Paris"),
            ("marseille", "Marseille"),
            ("lyon", "Lyon"),
            ("toulouse", "Toulouse"),
            ("nice", "Nice"),
        ]
        out = ""
        for slug, name in cities:
            out += (
                '                        <li><a href="' + prefix + section + '/villes/' + slug + '.html" '
                'class="text-sm font-medium text-gray-800 hover:text-primary">'
                + label_prefix + ' \u00e0 ' + name + '</a></li>\n'
            )
        return out

    ortho_city_links = city_links("orthophonie", "Orthophonie")
    psycho_city_links = city_links("psychologie", "Psychologie")
    scolaire_city_links = city_links("soutien-scolaire", "Soutien scolaire")

    return (
        '    <!-- NAVBAR -->\n'
        '    <nav class="bg-white shadow-sm sticky top-0 z-50 relative">\n'
        '        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">\n'
        '            <div class="flex justify-between items-center h-20">\n'
        '                <a href="' + prefix + 'index.html" class="flex items-center space-x-2 z-50">\n'
        '                    <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">\n'
        '                        <span class="text-white font-bold text-sm">L</span>\n'
        '                    </div>\n'
        '                    <span class="text-xl font-bold text-dark">Logopsi <span class="text-primary">Studios</span></span>\n'
        '                </a>\n'
        '\n'
        '                <div class="hidden lg:flex items-center space-x-1">\n'
        '                    <div class="relative" id="ortho-trigger" onmouseenter="openMegaMenu(\'ortho\')" onmouseleave="scheduleMegaClose(\'ortho\')">\n'
        '                        <button class="px-4 py-2 flex items-center gap-1 font-semibold text-[15px] text-gray-800 hover:text-primary transition-colors">\n'
        '                            Orthophonie <i data-lucide="chevron-down" class="w-4 h-4"></i>\n'
        '                        </button>\n'
        '                    </div>\n'
        '                    <div class="relative" id="psycho-trigger" onmouseenter="openMegaMenu(\'psycho\')" onmouseleave="scheduleMegaClose(\'psycho\')">\n'
        '                        <button class="px-4 py-2 flex items-center gap-1 font-semibold text-[15px] text-gray-800 hover:text-primary transition-colors">\n'
        '                            Psychologie <i data-lucide="chevron-down" class="w-4 h-4"></i>\n'
        '                        </button>\n'
        '                    </div>\n'
        '                    <div class="relative" id="scolaire-trigger" onmouseenter="openMegaMenu(\'scolaire\')" onmouseleave="scheduleMegaClose(\'scolaire\')">\n'
        '                        <button class="px-4 py-2 flex items-center gap-1 font-semibold text-[15px] text-gray-800 hover:text-primary transition-colors">\n'
        '                            Soutien Scolaire <i data-lucide="chevron-down" class="w-4 h-4"></i>\n'
        '                        </button>\n'
        '                    </div>\n'
        '                </div>\n'
        '\n'
        '                <div class="hidden lg:flex items-center gap-4">\n'
        '                    <a href="' + prefix + 'contact.html" class="bg-primary text-white font-semibold px-6 py-2.5 rounded-full hover:bg-primaryHover transition-colors shadow-md text-[15px]">\n'
        '                        Prendre rendez-vous\n'
        '                    </a>\n'
        '                </div>\n'
        '\n'
        '                <button class="lg:hidden p-2 text-gray-900 z-50" onclick="toggleMobileMenu()">\n'
        '                    <i data-lucide="menu" class="w-7 h-7"></i>\n'
        '                </button>\n'
        '            </div>\n'
        '        </div>\n'
        '\n'
        '        <!-- Orthophonie Mega Menu -->\n'
        '        <div id="ortho-mega" class="mega-menu absolute left-0 w-full bg-white shadow-xl border-t border-gray-100 z-50 mega-menu-enter" onmouseenter="cancelMegaClose(\'ortho\')" onmouseleave="scheduleMegaClose(\'ortho\')">\n'
        '            <div class="max-w-7xl mx-auto px-6 py-8 grid grid-cols-12 gap-8">\n'
        '                <div class="col-span-3 border-r border-gray-100 pr-6">\n'
        '                    <h3 class="text-lg font-bold text-gray-900 mb-2">Orthophonie en ligne</h3>\n'
        '                    <p class="text-sm text-gray-600 leading-relaxed">R\u00e9\u00e9ducation des troubles du langage, de la communication et des apprentissages.</p>\n'
        '                </div>\n'
        '                <div class="col-span-6 pr-6">\n'
        '                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Explorer par besoin</h4>\n'
        '                    <ul class="grid grid-cols-2 gap-x-6 gap-y-2.5">\n'
        + ortho_links +
        '                    </ul>\n'
        '                </div>\n'
        '                <div class="col-span-3 bg-light rounded-2xl p-5 border border-gray-100">\n'
        '                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Par ville</h4>\n'
        '                    <ul class="space-y-2.5">\n'
        + ortho_city_links +
        '                    </ul>\n'
        '                </div>\n'
        '            </div>\n'
        '        </div>\n'
        '\n'
        '        <!-- Psychologie Mega Menu -->\n'
        '        <div id="psycho-mega" class="mega-menu absolute left-0 w-full bg-white shadow-xl border-t border-gray-100 z-50 mega-menu-enter" onmouseenter="cancelMegaClose(\'psycho\')" onmouseleave="scheduleMegaClose(\'psycho\')">\n'
        '            <div class="max-w-7xl mx-auto px-6 py-8 grid grid-cols-12 gap-8">\n'
        '                <div class="col-span-3 border-r border-gray-100 pr-6">\n'
        '                    <h3 class="text-lg font-bold text-gray-900 mb-2">Psychologie en ligne</h3>\n'
        '                    <p class="text-sm text-gray-600 leading-relaxed">Accompagnement psychologique des enfants et adolescents, partout en France.</p>\n'
        '                </div>\n'
        '                <div class="col-span-6 pr-6">\n'
        '                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Explorer par besoin</h4>\n'
        '                    <ul class="grid grid-cols-2 gap-x-6 gap-y-2.5">\n'
        + psycho_links +
        '                    </ul>\n'
        '                </div>\n'
        '                <div class="col-span-3 bg-light rounded-2xl p-5 border border-gray-100">\n'
        '                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Par ville</h4>\n'
        '                    <ul class="space-y-2.5">\n'
        + psycho_city_links +
        '                    </ul>\n'
        '                </div>\n'
        '            </div>\n'
        '        </div>\n'
        '\n'
        '        <!-- Soutien Scolaire Mega Menu -->\n'
        '        <div id="scolaire-mega" class="mega-menu absolute left-0 w-full bg-white shadow-xl border-t border-gray-100 z-50 mega-menu-enter" onmouseenter="cancelMegaClose(\'scolaire\')" onmouseleave="scheduleMegaClose(\'scolaire\')">\n'
        '            <div class="max-w-7xl mx-auto px-6 py-8 grid grid-cols-12 gap-8">\n'
        '                <div class="col-span-3 border-r border-gray-100 pr-6">\n'
        '                    <h3 class="text-lg font-bold text-gray-900 mb-2">Soutien scolaire en ligne</h3>\n'
        '                    <p class="text-sm text-gray-600 leading-relaxed">Cours particuliers et aide aux devoirs avec des enseignants qualifi\u00e9s, du primaire au lyc\u00e9e.</p>\n'
        '                </div>\n'
        '                <div class="col-span-6 pr-6">\n'
        '                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Explorer par mati\u00e8re</h4>\n'
        '                    <ul class="grid grid-cols-2 gap-x-6 gap-y-2.5">\n'
        + scolaire_links +
        '                    </ul>\n'
        '                </div>\n'
        '                <div class="col-span-3 bg-light rounded-2xl p-5 border border-gray-100">\n'
        '                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Par ville</h4>\n'
        '                    <ul class="space-y-2.5">\n'
        + scolaire_city_links +
        '                    </ul>\n'
        '                </div>\n'
        '            </div>\n'
        '        </div>\n'
        '\n'
        '        <!-- Mobile Menu -->\n'
        '        <div id="mobile-menu" class="hidden lg:hidden bg-white border-t border-gray-100">\n'
        '            <div class="px-6 py-6 space-y-4">\n'
        '                <a href="' + prefix + 'orthophonie/" class="block text-gray-900 hover:text-primary font-semibold py-2">Orthophonie</a>\n'
        '                <a href="' + prefix + 'psychologie/" class="block text-gray-900 hover:text-primary font-semibold py-2">Psychologie</a>\n'
        '                <a href="' + prefix + 'soutien-scolaire/" class="block text-gray-900 hover:text-primary font-semibold py-2">Soutien Scolaire</a>\n'
        '                <a href="' + prefix + 'contact.html" class="w-full bg-primary text-white font-semibold py-3 rounded-full shadow-md mt-4 block text-center">Prendre rendez-vous</a>\n'
        '            </div>\n'
        '        </div>\n'
        '    </nav>\n'
    )


# ------------------------------------------------------------------
# 3. FOOTER
# ------------------------------------------------------------------

def get_footer(prefix):
    """Return the 4-column footer with legal links row."""

    return (
        '    <!-- FOOTER -->\n'
        '    <footer class="bg-dark py-16">\n'
        '        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">\n'
        '            <div class="grid md:grid-cols-4 gap-8 mb-12">\n'
        '                <div>\n'
        '                    <div class="flex items-center space-x-2 mb-4">\n'
        '                        <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">\n'
        '                            <span class="text-white font-bold text-sm">L</span>\n'
        '                        </div>\n'
        '                        <span class="text-xl font-bold text-white">Logopsi <span class="text-primary">Studios</span></span>\n'
        '                    </div>\n'
        '                    <p class="text-gray-400 text-sm">Orthophonie, psychologie et soutien scolaire en ligne. Des professionnels dipl\u00f4m\u00e9s, partout en France.</p>\n'
        '                </div>\n'
        '                <div>\n'
        '                    <h4 class="text-white font-semibold mb-4">Orthophonie</h4>\n'
        '                    <ul class="space-y-2">\n'
        '                        <li><a href="' + prefix + 'orthophonie/dyslexie.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Dyslexie</a></li>\n'
        '                        <li><a href="' + prefix + 'orthophonie/dysorthographie.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Dysorthographie</a></li>\n'
        '                        <li><a href="' + prefix + 'orthophonie/dyscalculie.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Dyscalculie</a></li>\n'
        '                        <li><a href="' + prefix + 'orthophonie/begaiement.html" class="text-gray-400 hover:text-primary text-sm transition-colors">B\u00e9gaiement</a></li>\n'
        '                        <li><a href="' + prefix + 'orthophonie/tsa.html" class="text-gray-400 hover:text-primary text-sm transition-colors">TSA</a></li>\n'
        '                    </ul>\n'
        '                </div>\n'
        '                <div>\n'
        '                    <h4 class="text-white font-semibold mb-4">Psychologie</h4>\n'
        '                    <ul class="space-y-2">\n'
        '                        <li><a href="' + prefix + 'psychologie/tdah.html" class="text-gray-400 hover:text-primary text-sm transition-colors">TDAH</a></li>\n'
        '                        <li><a href="' + prefix + 'psychologie/hpi.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Haut Potentiel</a></li>\n'
        '                        <li><a href="' + prefix + 'psychologie/phobie-scolaire.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Phobie scolaire</a></li>\n'
        '                        <li><a href="' + prefix + 'psychologie/anxiete.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Anxi\u00e9t\u00e9</a></li>\n'
        '                        <li><a href="' + prefix + 'psychologie/depression.html" class="text-gray-400 hover:text-primary text-sm transition-colors">D\u00e9pression</a></li>\n'
        '                    </ul>\n'
        '                </div>\n'
        '                <div>\n'
        '                    <h4 class="text-white font-semibold mb-4">Soutien Scolaire</h4>\n'
        '                    <ul class="space-y-2">\n'
        '                        <li><a href="' + prefix + 'soutien-scolaire/mathematiques/" class="text-gray-400 hover:text-primary text-sm transition-colors">Math\u00e9matiques</a></li>\n'
        '                        <li><a href="' + prefix + 'soutien-scolaire/francais/" class="text-gray-400 hover:text-primary text-sm transition-colors">Fran\u00e7ais</a></li>\n'
        '                        <li><a href="' + prefix + 'soutien-scolaire/anglais/" class="text-gray-400 hover:text-primary text-sm transition-colors">Anglais</a></li>\n'
        '                        <li><a href="' + prefix + 'soutien-scolaire/physique-chimie/" class="text-gray-400 hover:text-primary text-sm transition-colors">Physique-Chimie</a></li>\n'
        '                        <li><a href="' + prefix + 'soutien-scolaire/aide-aux-devoirs/" class="text-gray-400 hover:text-primary text-sm transition-colors">Aide aux devoirs</a></li>\n'
        '                    </ul>\n'
        '                </div>\n'
        '            </div>\n'
        '            <div class="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">\n'
        '                <p class="text-gray-500 text-sm">&copy; 2025 Logopsi Studios. Tous droits r\u00e9serv\u00e9s.</p>\n'
        '                <div class="flex space-x-6 mt-4 md:mt-0">\n'
        '                    <a href="' + prefix + 'mentions-legales.html" class="text-gray-500 hover:text-primary text-sm transition-colors">Mentions l\u00e9gales</a>\n'
        '                    <a href="' + prefix + 'contact.html" class="text-gray-500 hover:text-primary text-sm transition-colors">Contact</a>\n'
        '                    <a href="' + prefix + 'a-propos.html" class="text-gray-500 hover:text-primary text-sm transition-colors">\u00c0 propos</a>\n'
        '                </div>\n'
        '            </div>\n'
        '        </div>\n'
        '    </footer>\n'
    )


# ------------------------------------------------------------------
# 4. CTA SECTION
# ------------------------------------------------------------------

def get_cta_section(title, desc):
    """Return the green CTA banner section."""

    return (
        '    <!-- CTA -->\n'
        '    <section class="py-20">\n'
        '        <div class="max-w-4xl mx-auto px-6">\n'
        '            <div class="bg-primary rounded-3xl p-12 text-center text-white relative overflow-hidden">\n'
        '                <div class="absolute inset-0 opacity-10">\n'
        '                    <svg viewBox="0 0 100 100" preserveAspectRatio="none" class="w-full h-full">\n'
        '                        <path d="M0,20 Q25,0 50,20 T100,20 V100 H0 Z" fill="white"/>\n'
        '                    </svg>\n'
        '                </div>\n'
        '                <div class="relative z-10">\n'
        '                    <h2 class="text-3xl font-bold mb-4">' + title + '</h2>\n'
        '                    <p class="text-lg mb-8 text-green-50">' + desc + '</p>\n'
        '                    <a href="#" class="bg-white text-primary px-8 py-4 rounded-full font-bold hover:bg-green-50 transition text-lg inline-block shadow-lg">\n'
        '                        R\u00e9server mon bilan\n'
        '                    </a>\n'
        '                </div>\n'
        '            </div>\n'
        '        </div>\n'
        '    </section>\n'
    )


# ------------------------------------------------------------------
# 5. ABOUT SECTION
# ------------------------------------------------------------------

def get_about_section(practitioner, prefix):
    """Return the 'Pourquoi choisir Logopsi Studios' section.

    practitioner: "orthophoniste", "psychologue", or "enseignant"
    """

    practitioner_map = {
        "orthophoniste": "orthophonistes dipl\u00f4m\u00e9s d'\u00c9tat",
        "psychologue": "psychologues dipl\u00f4m\u00e9s d'\u00c9tat",
        "enseignant": "enseignants qualifi\u00e9s",
    }
    pro_label = practitioner_map.get(practitioner, "professionnels dipl\u00f4m\u00e9s")

    return (
        '    <!-- ABOUT SECTION -->\n'
        '    <section class="py-20 px-6 bg-light border-t border-gray-100">\n'
        '        <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center">\n'
        '            <div class="order-2 md:order-1 relative">\n'
        '                <div class="absolute -inset-4 bg-primary/10 rounded-3xl transform -rotate-3"></div>\n'
        '                <img src="https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="\u00c9quipe Logopsi Studios" class="relative rounded-2xl shadow-lg w-full object-cover h-[400px]">\n'
        '            </div>\n'
        '            <div class="order-1 md:order-2 space-y-6">\n'
        '                <div class="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold">\n'
        '                    <i data-lucide="award" class="w-4 h-4"></i> Professionnels dipl\u00f4m\u00e9s\n'
        '                </div>\n'
        '                <h2 class="text-3xl font-bold text-gray-900">Pourquoi choisir Logopsi Studios ?</h2>\n'
        '                <p class="text-gray-600 leading-relaxed">Chez Logopsi Studios, nous r\u00e9unissons des ' + pro_label + ', form\u00e9s aux derni\u00e8res avanc\u00e9es scientifiques. Notre plateforme vous connecte avec le bon professionnel en moins de 48h, partout en France.</p>\n'
        '                <div class="space-y-4">\n'
        '                    <div class="flex items-start gap-3">\n'
        '                        <div class="mt-1 bg-primary/10 text-primary rounded-full p-1"><i data-lucide="check" class="w-4 h-4"></i></div>\n'
        '                        <span class="text-gray-700"><strong>Rendez-vous sous 48h</strong> \u2014 Plus de listes d\'attente interminables</span>\n'
        '                    </div>\n'
        '                    <div class="flex items-start gap-3">\n'
        '                        <div class="mt-1 bg-primary/10 text-primary rounded-full p-1"><i data-lucide="check" class="w-4 h-4"></i></div>\n'
        '                        <span class="text-gray-700"><strong>S\u00e9ances remboursables</strong> \u2014 \u00c9ligible S\u00e9curit\u00e9 sociale et mutuelles</span>\n'
        '                    </div>\n'
        '                    <div class="flex items-start gap-3">\n'
        '                        <div class="mt-1 bg-primary/10 text-primary rounded-full p-1"><i data-lucide="check" class="w-4 h-4"></i></div>\n'
        '                        <span class="text-gray-700"><strong>100% en ligne</strong> \u2014 Depuis chez vous, sans d\u00e9placement</span>\n'
        '                    </div>\n'
        '                </div>\n'
        '            </div>\n'
        '        </div>\n'
        '    </section>\n'
    )


# ------------------------------------------------------------------
# 6. JAVASCRIPT
# ------------------------------------------------------------------

def get_js(include_faq=False):
    """Return the closing JS block (lucide, mega menus, mobile menu, optional FAQ)."""

    faq_js = ""
    if include_faq:
        faq_js = (
            '\n'
            '        // FAQ\n'
            '        function toggleFaq(btn) {\n'
            '            var content = btn.nextElementSibling;\n'
            '            var icon = btn.querySelector(\'.faq-icon\');\n'
            '            var isOpen = content.classList.contains(\'open\');\n'
            '            document.querySelectorAll(\'.faq-content\').forEach(function(c) { c.classList.remove(\'open\'); });\n'
            '            document.querySelectorAll(\'.faq-icon\').forEach(function(i) { i.style.transform = \'\'; });\n'
            '            if (!isOpen) {\n'
            '                content.classList.add(\'open\');\n'
            '                if (icon) icon.style.transform = \'rotate(45deg)\';\n'
            '            }\n'
            '        }\n'
        )

    return (
        '    <script>\n'
        '        lucide.createIcons();\n'
        '\n'
        '        // Mega Menu\n'
        '        var megaCloseTimers = { ortho: null, psycho: null, scolaire: null };\n'
        '        function openMegaMenu(menu) {\n'
        '            cancelMegaClose(menu);\n'
        '            var menus = { ortho: \'ortho-mega\', psycho: \'psycho-mega\', scolaire: \'scolaire-mega\' };\n'
        '            Object.keys(menus).forEach(function(key) {\n'
        '                var el = document.getElementById(menus[key]);\n'
        '                if (key === menu) { el.classList.add(\'active\'); }\n'
        '                else { el.classList.remove(\'active\'); clearTimeout(megaCloseTimers[key]); }\n'
        '            });\n'
        '        }\n'
        '        function scheduleMegaClose(menu) {\n'
        '            var menus = { ortho: \'ortho-mega\', psycho: \'psycho-mega\', scolaire: \'scolaire-mega\' };\n'
        '            megaCloseTimers[menu] = setTimeout(function() {\n'
        '                document.getElementById(menus[menu]).classList.remove(\'active\');\n'
        '            }, 200);\n'
        '        }\n'
        '        function cancelMegaClose(menu) { clearTimeout(megaCloseTimers[menu]); }\n'
        '        function toggleMobileMenu() { document.getElementById(\'mobile-menu\').classList.toggle(\'hidden\'); }\n'
        + faq_js +
        '    </script>\n'
        '</body>\n'
        '</html>\n'
    )


# ------------------------------------------------------------------
# 7. BREADCRUMB
# ------------------------------------------------------------------

def get_breadcrumb(crumbs):
    """Return a breadcrumb nav from a list of (label, url) tuples.

    The last tuple should have url=None (current page, displayed bold).
    Example: [("Accueil", "../index.html"), ("Psychologie", "../psychologie/"), ("Anxiete", None)]
    """

    parts = []
    for i, (label, url) in enumerate(crumbs):
        if url is not None:
            parts.append(
                '<a href="' + url + '" class="hover:text-primary transition-colors">' + label + '</a>'
            )
        else:
            parts.append(
                '<span class="text-gray-900 font-medium">' + label + '</span>'
            )
        if i < len(crumbs) - 1:
            parts.append('<i data-lucide="chevron-right" class="w-3.5 h-3.5"></i>')

    return (
        '            <div class="flex items-center gap-2 text-sm text-gray-500 mb-4">\n'
        '                ' + '\n                '.join(parts) + '\n'
        '            </div>\n'
    )
