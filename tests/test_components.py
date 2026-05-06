"""Smoke tests for shared_components. Run via `python3 tests/test_components.py`."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_components import get_booking_modal, get_booking_js, get_js
from shared_components import get_navbar


def test_modal_has_marker():
    assert "<!-- LOGOPSI_BOOKING_MODAL -->" in get_booking_modal()


def test_modal_has_price_and_delay():
    html = get_booking_modal()
    assert "150" in html
    assert "48h" in html or "48 h" in html


def test_modal_has_two_primary_ctas():
    html = get_booking_modal()
    assert "app.logopsiestudios.com/fr/login" in html
    assert "showCallbackForm" in html


def test_modal_has_callback_form():
    html = get_booking_modal()
    assert 'action="https://formsubmit.co/contact@logopsistudios.com"' in html
    assert 'name="phone"' in html or 'type="tel"' in html
    assert 'name="email"' in html
    assert 'name="name"' in html


def test_modal_has_aria_attributes():
    html = get_booking_modal()
    assert 'role="dialog"' in html
    assert 'aria-modal="true"' in html


def test_modal_has_member_login_link():
    html = get_booking_modal()
    assert "Se connecter" in html or "Déjà client" in html


def test_booking_js_exposes_open_close():
    js = get_booking_js()
    assert "function openBookingModal" in js
    assert "function closeBookingModal" in js
    assert "function showCallbackForm" in js
    assert "function showInfoView" in js


def test_booking_js_handles_escape():
    js = get_booking_js()
    assert "Escape" in js or "27" in js


def test_booking_js_handles_rappel_ok():
    js = get_booking_js()
    assert "rappel=ok" in js or "rappel" in js


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


if __name__ == "__main__":
    test_modal_has_marker()
    test_modal_has_price_and_delay()
    test_modal_has_two_primary_ctas()
    test_modal_has_callback_form()
    test_modal_has_aria_attributes()
    test_modal_has_member_login_link()
    test_booking_js_exposes_open_close()
    test_booking_js_handles_escape()
    test_booking_js_handles_rappel_ok()
    test_get_js_includes_booking_js()
    test_navbar_has_connexion_link_desktop()
    test_navbar_cta_opens_popup()
    test_navbar_keeps_prefix_for_other_links()
    print("test_components: OK")
