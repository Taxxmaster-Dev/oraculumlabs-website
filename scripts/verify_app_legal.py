#!/usr/bin/env python3
"""Source-only preflight for every localized ORACULUM legal webpage.

This verifies structural completeness and internal references. It is NOT a
professional legal translation review or a public HTTP availability check.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
LOCALES = (
    "en", "ar", "da", "de", "el", "es", "fr", "hi", "hu", "id",
    "it", "ja", "ko", "nb", "nl", "pl", "pt", "ro", "ru", "sv",
    "th", "tr", "vi", "zh-hans", "zh-hant",
)


class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html_lang = None
        self.links = []
        self.h1 = 0
        self.h2 = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.html_lang = attrs.get("lang")
        if tag == "h1":
            self.h1 += 1
        if tag == "h2":
            self.h2 += 1
        for name in ("href", "src"):
            if attrs.get(name):
                self.links.append(attrs[name])


def check(kind, locale):
    name = kind + ("" if locale == "en" else "-" + locale) + ".html"
    path = ROOT / "oraculum" / name
    assert path.is_file(), f"Missing {path}"
    content = path.read_text(encoding="utf-8")
    assert content.lstrip().lower().startswith("<!doctype html>"), path
    assert len(content) > 1800, f"Unexpectedly short legal page: {name}"
    assert "Oraculum Digital Labs Ltd" in content, name
    assert "HE 498123" in content, name
    assert "office@oraculumlabs.eu" in content, name
    assert "ORACULUM" in content, name
    assert "REVIEW DRAFT" not in content and "TODO" not in content, name
    assert f'https://oraculumlabs.eu/oraculum/{name}' in content, name
    parser = Extract()
    parser.feed(content)
    assert parser.html_lang == locale, f"Wrong lang in {name}: {parser.html_lang}"
    assert parser.h1 == 1 and parser.h2 >= 8, f"Incomplete headings in {name}"
    other = "terms" if kind == "privacy" else "privacy"
    sibling = other + ("" if locale == "en" else "-" + locale) + ".html"
    # Full canonical EN/HU notices cross-link directly; the other translated
    # editions are also independently reachable from the app and language index.
    assert (ROOT / "oraculum" / sibling).is_file(), f"Missing companion page: {sibling}"
    if locale in ("en", "hu"):
        assert f'href="{sibling}"' in content, f"Missing companion link: {name}"
    for value in parser.links:
        u = urlsplit(value)
        if u.scheme or u.netloc or value.startswith(("#", "//")):
            continue
        local = (ROOT / "oraculum" / unquote(u.path)).resolve()
        assert local.is_relative_to(ROOT) and local.is_file(), f"Broken local link {name}: {value}"
    if kind == "privacy":
        for provider in ("OpenAI", "Supabase", "Render", "Apple", "Google"):
            assert provider in content, f"Privacy notice {name} missing {provider}"
    if kind == "terms" and locale in ("en", "hu"):
        for text in ("Apple", "Google Play", "https://reportaproblem.apple.com/",
                     "https://support.google.com/googleplay/answer/15574897"):
            assert text in content, f"Store terms missing {text} in {name}"


def main():
    for kind in ("privacy", "terms"):
        existing = {p.name for p in (ROOT / "oraculum").glob(kind + "*.html")
                    if not p.name.endswith("-languages.html")}
        expected = {kind + ("" if l == "en" else "-" + l) + ".html" for l in LOCALES}
        assert existing == expected, f"{kind}: missing={expected-existing}, extra={existing-expected}"
        for locale in LOCALES:
            check(kind, locale)
    print(f"PASS: {len(LOCALES)} Privacy notices + {len(LOCALES)} Terms pages, internal links and store coverage")
    print("Scope: source/link structure only; translated legal content requires professional review.")


if __name__ == "__main__":
    main()
