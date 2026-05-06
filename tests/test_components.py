"""Smoke tests for shared_components. Run via `python3 tests/test_components.py`."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_components import get_booking_modal


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


if __name__ == "__main__":
    test_modal_has_marker()
    test_modal_has_price_and_delay()
    test_modal_has_two_primary_ctas()
    test_modal_has_callback_form()
    test_modal_has_aria_attributes()
    test_modal_has_member_login_link()
    print("test_components: OK")
