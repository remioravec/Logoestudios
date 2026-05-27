"""Smoke tests for shared_components. Run via `python3 tests/test_components.py`."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_components import get_booking_modal, get_booking_js, get_js
from shared_components import get_navbar, get_footer
from shared_components import get_cta_section


def test_modal_has_marker():
    assert "<!-- LOGOPSI_BOOKING_MODAL -->" in get_booking_modal()


def test_modal_has_price_and_delay():
    html = get_booking_modal()
    assert "150" in html
    assert "48h" in html or "48 h" in html


def test_modal_form_uses_ajax_class():
    html = get_booking_modal()
    # Modal form is intercepted via class hook (no third-party action attribute)
    assert "logopsi-contact-form" in html
    assert 'data-source="booking"' in html
    assert "formsubmit.co" not in html


def test_modal_has_callback_form():
    html = get_booking_modal()
    assert 'name="phone"' in html or 'type="tel"' in html
    assert 'name="email"' in html
    assert 'name="name"' in html
    # Honeypot for bots
    assert 'name="_hp"' in html


def test_modal_has_aria_attributes():
    html = get_booking_modal()
    assert 'role="dialog"' in html
    assert 'aria-modal="true"' in html


def test_booking_js_exposes_open_close():
    js = get_booking_js()
    assert "function openBookingModal" in js
    assert "function closeBookingModal" in js
    assert "function showCallbackForm" in js
    assert "function showInfoView" in js


def test_booking_js_handles_escape():
    js = get_booking_js()
    assert "Escape" in js or "27" in js


def test_booking_js_intercepts_form_ajax():
    js = get_booking_js()
    # AJAX interceptor — replaces formsubmit + ?rappel=ok mechanism
    assert "logopsi-contact-form" in js
    assert "logopsi_contact" in js  # AJAX action name
    assert "fetch(" in js
    assert "Merci" in js  # thank-you message rendered inline


def test_get_js_includes_booking_js():
    js = get_js()
    assert "openBookingModal" in js
    assert "closeBookingModal" in js


def test_navbar_has_connexion_link_desktop():
    html = get_navbar("./")
    assert "Connexion" in html
    assert "app.logopsiestudios.com/fr/login" in html
    # Desktop + mobile: link to login appears at least twice
    assert html.count("app.logopsiestudios.com/fr/login") >= 2


def test_navbar_cta_opens_popup():
    html = get_navbar("./")
    # The "Prendre rendez-vous" green button should call openBookingModal()
    assert "openBookingModal()" in html


def test_navbar_keeps_prefix_for_other_links():
    html = get_navbar("../")
    assert "../orthophonie/" in html


def test_footer_has_espace_membre_link():
    html = get_footer("./")
    assert "Espace membre" in html
    assert "app.logopsiestudios.com/fr/login" in html


def test_cta_section_uses_new_wording():
    html = get_cta_section("Prêt à commencer ?", "Réservez votre bilan en quelques clics.")
    assert "150" in html
    assert "48h" in html or "48 h" in html
    assert "openBookingModal()" in html
    # Old wording must be gone
    assert "tarifs sur demande" not in html


if __name__ == "__main__":
    test_modal_has_marker()
    test_modal_has_price_and_delay()
    test_modal_form_uses_ajax_class()
    test_modal_has_callback_form()
    test_modal_has_aria_attributes()
    test_booking_js_exposes_open_close()
    test_booking_js_handles_escape()
    test_booking_js_intercepts_form_ajax()
    test_get_js_includes_booking_js()
    test_navbar_has_connexion_link_desktop()
    test_navbar_cta_opens_popup()
    test_navbar_keeps_prefix_for_other_links()
    test_footer_has_espace_membre_link()
    test_cta_section_uses_new_wording()
    print("test_components: OK")
