"""Tests for seo_titles mappings. Run via `python3 tests/test_seo_titles.py`."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seo_titles import (
    title_for_ortho_n2, title_for_ortho_n3, title_for_ortho_n4,
    title_for_psycho_n2, title_for_psycho_n3, title_for_psycho_n4,
    title_for_scolaire_n2, title_for_scolaire_n3, title_for_scolaire_n4,
    title_for_handwritten,
    meta_desc_for_ortho_n2, meta_desc_for_psycho_n2,
)


def test_ortho_n2_dyslexie():
    assert title_for_ortho_n2("dyslexie") == "Bilan dyslexie en ligne — Orthophoniste 150€/48h | Logopsi Studios"


def test_ortho_n2_oralite():
    assert title_for_ortho_n2("oralite") == "Bilan troubles de l'oralité — Orthophoniste 150€/48h | Logopsi Studios"


def test_ortho_n3_paris():
    assert title_for_ortho_n3("paris") == "Bilan orthophonique à Paris — 150€, sous 48h | Logopsi Studios"


def test_ortho_n4_dyslexie_paris():
    assert title_for_ortho_n4("dyslexie", "paris") == "Bilan dyslexie à Paris — Orthophoniste 150€/48h | Logopsi Studios"


def test_psycho_n2_tdah():
    assert title_for_psycho_n2("tdah") == "Bilan TDAH en ligne — Psychologue 150€/48h | Logopsi Studios"


def test_scolaire_n4():
    assert title_for_scolaire_n4("mathematiques", "3eme", "paris") == "Bilan mathématiques 3ème à Paris — 150€/48h | Logopsi Studios"


def test_all_titles_include_48h():
    for slug in ("dyslexie", "oralite", "paralysie-cerebrale"):
        assert "48h" in title_for_ortho_n2(slug), slug
    for slug in ("tdah", "hpi"):
        assert "48h" in title_for_psycho_n2(slug), slug
    assert "48h" in title_for_ortho_n4("dyslexie", "paris")
    assert "48h" in title_for_psycho_n4("tdah", "lyon")
    assert "48h" in title_for_scolaire_n2("mathematiques", "3eme")
    assert "48h" in title_for_scolaire_n4("mathematiques", "3eme", "paris")


def test_handwritten_index():
    assert title_for_handwritten("site/index.html") == "Bilan orthophonie, psychologie & soutien — 150€, 48h | Logopsi Studios"


def test_handwritten_contact_carries_brand():
    # Even admin pages now carry the 150€/48h positioning in the title.
    t = title_for_handwritten("site/contact.html")
    assert t is not None
    assert "150€/48h" in t and "Logopsi Studios" in t


def test_meta_desc_ortho_n2():
    desc = meta_desc_for_ortho_n2("dyslexie")
    assert "150" in desc
    assert "48h" in desc or "48 h" in desc


if __name__ == "__main__":
    test_ortho_n2_dyslexie()
    test_ortho_n2_oralite()
    test_ortho_n3_paris()
    test_ortho_n4_dyslexie_paris()
    test_psycho_n2_tdah()
    test_scolaire_n4()
    test_handwritten_index()
    test_handwritten_contact_carries_brand()
    test_meta_desc_ortho_n2()
    test_all_titles_include_48h()
    print("test_seo_titles: OK")
