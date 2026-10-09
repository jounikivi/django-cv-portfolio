"""Tuotantoasetusten tarkistus erillisessä prosessissa ilman oikeita salaisuuksia."""

import os
from pathlib import Path
import subprocess
import sys

from django.test import SimpleTestCase


class ProductionSettingsTests(SimpleTestCase):
    def run_production(self, code, **overrides):
        env = os.environ.copy()
        env.update({
            "DJANGO_SETTINGS_MODULE": "cv_site.settings_production",
            "DJANGO_SECRET_KEY": "test-only-0123456789abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "DJANGO_ALLOWED_HOSTS": "portfolio.example.com",
            "DJANGO_HSTS_SECONDS": "0",
        })
        env.update(overrides)
        return subprocess.run(
            [sys.executable, "-c", code], env=env,
            cwd=Path(__file__).resolve().parent.parent,
            capture_output=True, text=True, timeout=30,
        )

    def test_production_security_and_responses(self):
        result = self.run_production('''
import django
django.setup()
from django.conf import settings
from django.test import Client
assert settings.DEBUG is False
assert settings.SESSION_COOKIE_SECURE and settings.CSRF_COOKIE_SECURE
assert settings.STATIC_ROOT != settings.MEDIA_ROOT
client = Client(HTTP_HOST="portfolio.example.com")
response = client.get("/admin/login/")
assert response.status_code == 301
assert response["Location"] == "https://portfolio.example.com/admin/login/"
response = client.get("/missing-publication-test/", secure=True)
assert response.status_code == 404
assert b"Traceback" not in response.content
assert response["X-Content-Type-Options"] == "nosniff"
assert client.get("/admin/login/", secure=True, HTTP_HOST="unknown.example.com").status_code == 400
''')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_or_wildcard_host_is_rejected(self):
        for host in ("", "*", "https://example.com", ".example.com"):
            with self.subTest(host=host):
                result = self.run_production("import cv_site.settings_production", DJANGO_ALLOWED_HOSTS=host)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("ImproperlyConfigured", result.stderr)

    def test_insecure_secret_is_rejected(self):
        result = self.run_production("import cv_site.settings_production", DJANGO_SECRET_KEY="short")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ImproperlyConfigured", result.stderr)

    def test_hsts_after_https_verification(self):
        result = self.run_production('''
import django
django.setup()
from django.test import Client
response = Client(HTTP_HOST="portfolio.example.com").get("/missing/", secure=True)
assert response["Strict-Transport-Security"] == "max-age=3600"
''', DJANGO_HSTS_SECONDS="3600")
        self.assertEqual(result.returncode, 0, result.stderr)
