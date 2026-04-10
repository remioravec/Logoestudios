#!/usr/bin/env python3
"""
Update ALL pages in the site to have:
1. Consistent mega menu (Orthophonie, Psychologie, Soutien Scolaire)
2. Consistent footer with all sections
3. Replace "Familles Expatriées" card on homepage with "Soutien Scolaire"
"""

import os
import re
import glob

SITE_DIR = "/workspaces/Logoestudios/site"

# ── SHARED COMPONENTS ──

MEGA_MENU_CSS = """    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .mega-menu { display: none; opacity: 0; transition: opacity 0.2s ease; }
        .mega-menu.active { display: block; opacity: 1; }
        .mobile-menu { display: none; }
        .mobile-menu.active { display: block; }
        .mega-wrap { position: relative; }
    </style>"""

def get_navbar(prefix=""):
    """Generate the unified mega menu navbar. prefix adjusts relative paths."""
    p = prefix
    return f"""
    <!-- NAVBAR -->
    <nav class="bg-white shadow-sm sticky top-0 z-50 relative">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <a href="{p}index.html" class="flex items-center space-x-2">
                    <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                        <span class="text-white font-bold text-sm">L</span>
                    </div>
                    <span class="text-xl font-bold text-dark">Logopsi <span class="text-primary">Studios</span></span>
                </a>

                <div class="hidden lg:flex items-center space-x-8">
                    <div class="relative" id="ortho-trigger" onmouseenter="openMegaMenu('ortho')" onmouseleave="scheduleMegaClose('ortho')">
                        <button class="flex items-center space-x-1 text-dark hover:text-primary font-medium transition-colors py-5">
                            <span>Orthophonie</span>
                            <i data-lucide="chevron-down" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <div class="relative" id="psycho-trigger" onmouseenter="openMegaMenu('psycho')" onmouseleave="scheduleMegaClose('psycho')">
                        <button class="flex items-center space-x-1 text-dark hover:text-primary font-medium transition-colors py-5">
                            <span>Psychologie</span>
                            <i data-lucide="chevron-down" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <div class="relative" id="scolaire-trigger" onmouseenter="openMegaMenu('scolaire')" onmouseleave="scheduleMegaClose('scolaire')">
                        <button class="flex items-center space-x-1 text-dark hover:text-primary font-medium transition-colors py-5">
                            <span>Soutien Scolaire</span>
                            <i data-lucide="chevron-down" class="w-4 h-4"></i>
                        </button>
                    </div>
                </div>

                <div class="flex items-center space-x-4">
                    <a href="#contact" class="hidden sm:inline-flex bg-primary hover:bg-primaryHover text-white font-semibold px-5 py-2.5 rounded-full transition-colors">
                        Prendre RDV
                    </a>
                    <button class="lg:hidden" onclick="toggleMobileMenu()">
                        <i data-lucide="menu" class="w-6 h-6"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- Orthophonie Mega Menu -->
        <div id="ortho-mega" class="mega-menu absolute left-1/2 -translate-x-1/2 w-full max-w-4xl bg-white shadow-xl rounded-b-2xl border border-gray-100 z-50 mt-0" onmouseenter="cancelMegaClose('ortho')" onmouseleave="scheduleMegaClose('ortho')">
            <div class="p-8">
                <div class="grid grid-cols-3 gap-8">
                    <div>
                        <h3 class="font-bold text-dark mb-4 flex items-center"><i data-lucide="book-open" class="w-5 h-5 mr-2 text-primary"></i>Troubles pris en charge</h3>
                        <ul class="space-y-2">
                            <li><a href="{p}orthophonie/dyslexie.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Dyslexie</a></li>
                            <li><a href="{p}orthophonie/dysorthographie.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Dysorthographie</a></li>
                            <li><a href="{p}orthophonie/dyscalculie.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Dyscalculie</a></li>
                            <li><a href="{p}orthophonie/dysphasie.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Dysphasie</a></li>
                            <li><a href="{p}orthophonie/begaiement.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Bégaiement</a></li>
                            <li><a href="{p}orthophonie/tsa.html" class="text-gray-600 hover:text-primary transition-colors text-sm">TSA</a></li>
                            <li><a href="{p}orthophonie/oralite.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Troubles de l'oralité</a></li>
                            <li><a href="{p}orthophonie/surdite.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Surdité</a></li>
                            <li><a href="{p}orthophonie/paralysie-cerebrale.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Paralysie cérébrale</a></li>
                            <li><a href="{p}orthophonie/fente-palatine.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Fente palatine</a></li>
                            <li><a href="{p}orthophonie/trisomie-21.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Trisomie 21</a></li>
                        </ul>
                    </div>
                    <div>
                        <h3 class="font-bold text-dark mb-4 flex items-center"><i data-lucide="map-pin" class="w-5 h-5 mr-2 text-primary"></i>Par ville</h3>
                        <ul class="space-y-2">
                            <li><a href="{p}orthophonie/villes/paris.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Paris</a></li>
                            <li><a href="{p}orthophonie/villes/marseille.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Marseille</a></li>
                            <li><a href="{p}orthophonie/villes/lyon.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Lyon</a></li>
                            <li><a href="{p}orthophonie/villes/toulouse.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Toulouse</a></li>
                            <li><a href="{p}orthophonie/villes/nice.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Nice</a></li>
                        </ul>
                    </div>
                    <div class="bg-green-50 rounded-2xl p-6 flex flex-col justify-center">
                        <h3 class="font-bold text-dark text-lg mb-2">Besoin d'un orthophoniste ?</h3>
                        <p class="text-gray-600 text-sm mb-4">Nos orthophonistes diplômés sont disponibles en ligne, partout en France.</p>
                        <a href="#contact" class="bg-primary hover:bg-primaryHover text-white font-semibold px-5 py-2.5 rounded-full transition-colors text-center text-sm">Prendre rendez-vous</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Psychologie Mega Menu -->
        <div id="psycho-mega" class="mega-menu absolute left-1/2 -translate-x-1/2 w-full max-w-4xl bg-white shadow-xl rounded-b-2xl border border-gray-100 z-50 mt-0" onmouseenter="cancelMegaClose('psycho')" onmouseleave="scheduleMegaClose('psycho')">
            <div class="p-8">
                <div class="grid grid-cols-3 gap-8">
                    <div>
                        <h3 class="font-bold text-dark mb-4 flex items-center"><i data-lucide="brain" class="w-5 h-5 mr-2 text-primary"></i>Troubles pris en charge</h3>
                        <ul class="space-y-2">
                            <li><a href="{p}psychologie/tdah.html" class="text-gray-600 hover:text-primary transition-colors text-sm">TDAH</a></li>
                            <li><a href="{p}psychologie/hpi.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Haut Potentiel (HPI)</a></li>
                            <li><a href="{p}psychologie/phobie-scolaire.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Phobie scolaire</a></li>
                            <li><a href="{p}psychologie/harcelement-scolaire.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Harcèlement scolaire</a></li>
                            <li><a href="{p}psychologie/anxiete.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Anxiété</a></li>
                            <li><a href="{p}psychologie/depression.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Dépression</a></li>
                            <li><a href="{p}psychologie/tca.html" class="text-gray-600 hover:text-primary transition-colors text-sm">TCA</a></li>
                            <li><a href="{p}psychologie/addictions-ecrans.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Addictions aux écrans</a></li>
                            <li><a href="{p}psychologie/troubles-sommeil.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Troubles du sommeil</a></li>
                            <li><a href="{p}psychologie/enuresie.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Énurésie</a></li>
                            <li><a href="{p}psychologie/traumatismes-deuil.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Traumatismes & deuil</a></li>
                        </ul>
                    </div>
                    <div>
                        <h3 class="font-bold text-dark mb-4 flex items-center"><i data-lucide="map-pin" class="w-5 h-5 mr-2 text-primary"></i>Par ville</h3>
                        <ul class="space-y-2">
                            <li><a href="{p}psychologie/villes/paris.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Paris</a></li>
                            <li><a href="{p}psychologie/villes/marseille.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Marseille</a></li>
                            <li><a href="{p}psychologie/villes/lyon.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Lyon</a></li>
                            <li><a href="{p}psychologie/villes/toulouse.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Toulouse</a></li>
                            <li><a href="{p}psychologie/villes/nice.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Nice</a></li>
                        </ul>
                    </div>
                    <div class="bg-green-50 rounded-2xl p-6 flex flex-col justify-center">
                        <h3 class="font-bold text-dark text-lg mb-2">Besoin d'un psychologue ?</h3>
                        <p class="text-gray-600 text-sm mb-4">Nos psychologues diplômés accompagnent votre enfant en ligne.</p>
                        <a href="#contact" class="bg-primary hover:bg-primaryHover text-white font-semibold px-5 py-2.5 rounded-full transition-colors text-center text-sm">Prendre rendez-vous</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Soutien Scolaire Mega Menu -->
        <div id="scolaire-mega" class="mega-menu absolute left-1/2 -translate-x-1/2 w-full max-w-4xl bg-white shadow-xl rounded-b-2xl border border-gray-100 z-50 mt-0" onmouseenter="cancelMegaClose('scolaire')" onmouseleave="scheduleMegaClose('scolaire')">
            <div class="p-8">
                <div class="grid grid-cols-3 gap-8">
                    <div>
                        <h3 class="font-bold text-dark mb-4 flex items-center"><i data-lucide="graduation-cap" class="w-5 h-5 mr-2 text-primary"></i>Matières</h3>
                        <ul class="space-y-2">
                            <li><a href="{p}soutien-scolaire/mathematiques/" class="text-gray-600 hover:text-primary transition-colors text-sm">Mathématiques</a></li>
                            <li><a href="{p}soutien-scolaire/francais/" class="text-gray-600 hover:text-primary transition-colors text-sm">Français</a></li>
                            <li><a href="{p}soutien-scolaire/anglais/" class="text-gray-600 hover:text-primary transition-colors text-sm">Anglais</a></li>
                            <li><a href="{p}soutien-scolaire/physique-chimie/" class="text-gray-600 hover:text-primary transition-colors text-sm">Physique-Chimie</a></li>
                            <li><a href="{p}soutien-scolaire/aide-aux-devoirs/" class="text-gray-600 hover:text-primary transition-colors text-sm">Aide aux devoirs</a></li>
                        </ul>
                    </div>
                    <div>
                        <h3 class="font-bold text-dark mb-4 flex items-center"><i data-lucide="map-pin" class="w-5 h-5 mr-2 text-primary"></i>Par ville</h3>
                        <ul class="space-y-2">
                            <li><a href="{p}soutien-scolaire/villes/paris.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Paris</a></li>
                            <li><a href="{p}soutien-scolaire/villes/marseille.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Marseille</a></li>
                            <li><a href="{p}soutien-scolaire/villes/lyon.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Lyon</a></li>
                            <li><a href="{p}soutien-scolaire/villes/toulouse.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Toulouse</a></li>
                            <li><a href="{p}soutien-scolaire/villes/nice.html" class="text-gray-600 hover:text-primary transition-colors text-sm">Nice</a></li>
                        </ul>
                    </div>
                    <div class="bg-green-50 rounded-2xl p-6 flex flex-col justify-center">
                        <h3 class="font-bold text-dark text-lg mb-2">Besoin de soutien scolaire ?</h3>
                        <p class="text-gray-600 text-sm mb-4">Enseignants qualifiés, cours en ligne du CP à la Terminale.</p>
                        <a href="#contact" class="bg-primary hover:bg-primaryHover text-white font-semibold px-5 py-2.5 rounded-full transition-colors text-center text-sm">Prendre rendez-vous</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Mobile Menu -->
        <div id="mobile-menu" class="mobile-menu lg:hidden bg-white border-t">
            <div class="px-4 py-4 space-y-3">
                <a href="{p}orthophonie/" class="block text-dark hover:text-primary font-medium py-2">Orthophonie</a>
                <a href="{p}psychologie/" class="block text-dark hover:text-primary font-medium py-2">Psychologie</a>
                <a href="{p}soutien-scolaire/" class="block text-dark hover:text-primary font-medium py-2">Soutien Scolaire</a>
                <a href="#contact" class="block bg-primary hover:bg-primaryHover text-white font-semibold px-5 py-2.5 rounded-full transition-colors text-center">Prendre RDV</a>
            </div>
        </div>
    </nav>"""


def get_footer(prefix=""):
    p = prefix
    return f"""
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
                        <li><a href="{p}orthophonie/dyslexie.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Dyslexie</a></li>
                        <li><a href="{p}orthophonie/dysorthographie.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Dysorthographie</a></li>
                        <li><a href="{p}orthophonie/dyscalculie.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Dyscalculie</a></li>
                        <li><a href="{p}orthophonie/begaiement.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Bégaiement</a></li>
                        <li><a href="{p}orthophonie/tsa.html" class="text-gray-400 hover:text-primary text-sm transition-colors">TSA</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-white font-semibold mb-4">Psychologie</h4>
                    <ul class="space-y-2">
                        <li><a href="{p}psychologie/tdah.html" class="text-gray-400 hover:text-primary text-sm transition-colors">TDAH</a></li>
                        <li><a href="{p}psychologie/hpi.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Haut Potentiel</a></li>
                        <li><a href="{p}psychologie/phobie-scolaire.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Phobie scolaire</a></li>
                        <li><a href="{p}psychologie/anxiete.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Anxiété</a></li>
                        <li><a href="{p}psychologie/depression.html" class="text-gray-400 hover:text-primary text-sm transition-colors">Dépression</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-white font-semibold mb-4">Soutien Scolaire</h4>
                    <ul class="space-y-2">
                        <li><a href="{p}soutien-scolaire/mathematiques/" class="text-gray-400 hover:text-primary text-sm transition-colors">Mathématiques</a></li>
                        <li><a href="{p}soutien-scolaire/francais/" class="text-gray-400 hover:text-primary text-sm transition-colors">Français</a></li>
                        <li><a href="{p}soutien-scolaire/anglais/" class="text-gray-400 hover:text-primary text-sm transition-colors">Anglais</a></li>
                        <li><a href="{p}soutien-scolaire/physique-chimie/" class="text-gray-400 hover:text-primary text-sm transition-colors">Physique-Chimie</a></li>
                        <li><a href="{p}soutien-scolaire/aide-aux-devoirs/" class="text-gray-400 hover:text-primary text-sm transition-colors">Aide aux devoirs</a></li>
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
    </footer>"""


def get_mega_menu_js():
    return """
    <script>
        lucide.createIcons();

        var megaCloseTimers = { ortho: null, psycho: null, scolaire: null };

        function openMegaMenu(menu) {
            cancelMegaClose(menu);
            var menus = { ortho: 'ortho-mega', psycho: 'psycho-mega', scolaire: 'scolaire-mega' };
            Object.keys(menus).forEach(function(key) {
                var el = document.getElementById(menus[key]);
                if (key === menu) {
                    el.classList.add('active');
                } else {
                    el.classList.remove('active');
                    clearTimeout(megaCloseTimers[key]);
                }
            });
        }

        function scheduleMegaClose(menu) {
            megaCloseTimers[menu] = setTimeout(function() {
                var id = menu === 'ortho' ? 'ortho-mega' : menu === 'psycho' ? 'psycho-mega' : 'scolaire-mega';
                document.getElementById(id).classList.remove('active');
            }, 150);
        }

        function cancelMegaClose(menu) {
            clearTimeout(megaCloseTimers[menu]);
        }

        function toggleMobileMenu() {
            document.getElementById('mobile-menu').classList.toggle('active');
        }
    </script>"""


def compute_prefix(filepath):
    """Compute the relative prefix from a file to the site root."""
    rel = os.path.relpath(SITE_DIR, os.path.dirname(filepath))
    if rel == ".":
        return "./"
    return rel + "/"


def update_page(filepath):
    """Replace nav and footer in a page with the unified versions."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    prefix = compute_prefix(filepath)

    # ── Replace everything from <nav to </nav> (the entire nav block, potentially including mega menus)
    # We need to find the nav and all its mega menu sub-divs
    # Strategy: replace from first <nav or <!-- NAVBAR --> or <!-- Navbar --> to the closing </nav>

    # Find the start of the nav section
    nav_start_patterns = [
        r'\s*<!-- NAVBAR -->\s*\n\s*<nav',
        r'\s*<!-- Navbar -->\s*\n\s*<nav',
        r'\s*<nav class="bg-white'
    ]

    nav_start = -1
    for pattern in nav_start_patterns:
        match = re.search(pattern, content)
        if match:
            nav_start = match.start()
            break

    if nav_start == -1:
        print(f"  WARNING: No nav found in {filepath}")
        return False

    # Find the LAST </nav> that closes the main nav (could include mega menus)
    # The mega menus are inside the nav, so we need the last </nav>
    # Actually, look for all </nav> tags and find the right one
    # The nav structure includes sub-<nav> for breadcrumb, so be careful

    # Strategy: find the closing </nav> that matches our opening <nav>
    # Count opening and closing nav tags from nav_start
    pos = nav_start
    depth = 0
    nav_end = -1
    while pos < len(content):
        open_match = re.search(r'<nav[\s>]', content[pos:])
        close_match = re.search(r'</nav>', content[pos:])

        if open_match is None and close_match is None:
            break

        open_pos = open_match.start() + pos if open_match else float('inf')
        close_pos = close_match.start() + pos if close_match else float('inf')

        if open_pos < close_pos:
            depth += 1
            pos = open_pos + 1
        else:
            depth -= 1
            if depth == 0:
                nav_end = close_pos + len('</nav>')
                break
            pos = close_pos + 1

    if nav_end == -1:
        print(f"  WARNING: Could not find closing </nav> in {filepath}")
        return False

    new_navbar = get_navbar(prefix)

    # Replace the nav section
    new_content = content[:nav_start] + new_navbar + content[nav_end:]

    # ── Replace footer ──
    # Find <footer and </footer>
    footer_start_match = re.search(r'\s*(?:<!-- FOOTER -->\s*\n\s*)?<footer', new_content)
    if footer_start_match:
        footer_start = footer_start_match.start()
        footer_end_match = re.search(r'</footer>', new_content[footer_start:])
        if footer_end_match:
            footer_end = footer_start + footer_end_match.start() + len('</footer>')
            new_footer = get_footer(prefix)
            new_content = new_content[:footer_start] + new_footer + new_content[footer_end:]

    # ── Replace the JS at the end ──
    # Remove existing lucide.createIcons() and mega menu JS, replace with unified version
    # Remove old script blocks before </body>
    new_content = re.sub(
        r'\s*<script>\s*lucide\.createIcons\(\);\s*</script>',
        '',
        new_content
    )
    # Remove old mega menu JS blocks
    new_content = re.sub(
        r'\s*<script>\s*//\s*Initialize Lucide.*?</script>',
        '',
        new_content,
        flags=re.DOTALL
    )
    # Remove old inline JS that might conflict
    new_content = re.sub(
        r'\s*<!-- JavaScript -->\s*\n\s*<script>.*?</script>',
        '',
        new_content,
        flags=re.DOTALL
    )

    # Add mega menu JS before </body>
    js = get_mega_menu_js()
    new_content = new_content.replace('</body>', f'{js}\n</body>')

    # ── Ensure mega menu CSS is in <head> ──
    if '.mega-menu' not in new_content.split('</head>')[0]:
        # Add CSS before </head>
        # Remove old style blocks first if any
        new_content = new_content.replace('</head>', f'{MEGA_MENU_CSS}\n</head>')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def update_homepage():
    """Special handling for the homepage - replace Expatriés card with Soutien Scolaire."""
    filepath = os.path.join(SITE_DIR, "index.html")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the Expatriés card with Soutien Scolaire
    old_card = """                <!-- Expatriés Card -->
                <div class="group bg-light rounded-3xl p-8 hover:shadow-xl transition-all duration-300 border border-transparent hover:border-primary">
                    <div class="bg-green-100 rounded-2xl w-14 h-14 flex items-center justify-center mb-6 group-hover:bg-primary transition-colors">
                        <i data-lucide="plane" class="w-7 h-7 text-primary group-hover:text-white"></i>
                    </div>
                    <h3 class="text-xl font-bold text-dark mb-3">Familles Expatriées</h3>
                    <p class="text-gray-600 mb-4">Un suivi en français, où que vous soyez dans le monde. Fuseaux horaires adaptés et approche interculturelle.</p>
                    <a href="#contact" class="text-primary font-semibold flex items-center">
                        Nous contacter <i data-lucide="arrow-right" class="w-4 h-4 ml-2"></i>
                    </a>
                </div>"""

    new_card = """                <!-- Soutien Scolaire Card -->
                <a href="./soutien-scolaire/" class="group bg-light rounded-3xl p-8 hover:shadow-xl transition-all duration-300 border border-transparent hover:border-primary">
                    <div class="bg-green-100 rounded-2xl w-14 h-14 flex items-center justify-center mb-6 group-hover:bg-primary transition-colors">
                        <i data-lucide="graduation-cap" class="w-7 h-7 text-primary group-hover:text-white"></i>
                    </div>
                    <h3 class="text-xl font-bold text-dark mb-3">Soutien Scolaire</h3>
                    <p class="text-gray-600 mb-4">Cours particuliers en ligne du CP à la Terminale. Maths, français, anglais, physique-chimie et aide aux devoirs.</p>
                    <span class="text-primary font-semibold flex items-center">
                        En savoir plus <i data-lucide="arrow-right" class="w-4 h-4 ml-2"></i>
                    </span>
                </a>"""

    content = content.replace(old_card, new_card)

    # Also update the meta description
    content = content.replace(
        'Des professionnels diplômés, disponibles partout en France et pour les expatriés.',
        'Des professionnels diplômés et du soutien scolaire en ligne, disponibles partout en France.'
    )

    # Update the badge in hero
    content = content.replace(
        'Orthophonie & Psychologie en ligne',
        'Orthophonie, Psychologie & Soutien Scolaire'
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print("  Homepage: replaced Expatriés card with Soutien Scolaire")


def main():
    # Step 1: Update homepage specific content
    print("=== Step 1: Update homepage content ===")
    update_homepage()

    # Step 2: Update ALL pages with unified nav + footer
    print("\n=== Step 2: Update nav + footer on all pages ===")
    all_html = glob.glob(os.path.join(SITE_DIR, "**/*.html"), recursive=True)
    all_html.sort()

    success = 0
    failed = 0
    for filepath in all_html:
        rel = os.path.relpath(filepath, SITE_DIR)
        result = update_page(filepath)
        if result:
            success += 1
        else:
            failed += 1
            print(f"  FAILED: {rel}")

    print(f"\nDone! Updated {success} pages, {failed} failures out of {len(all_html)} total.")


if __name__ == "__main__":
    main()
