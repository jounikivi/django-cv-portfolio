"""PythonAnywhere: käytä tätä asetustiedostoa WSGI:ssä ja hallintakomennoissa."""

from .settings import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = [
    host.strip() for host in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]
if not ALLOWED_HOSTS or any(
    "*" in host or "/" in host or ":" in host or host.startswith(".")
    for host in ALLOWED_HOSTS
):
    raise ImproperlyConfigured(
        "Aseta DJANGO_ALLOWED_HOSTS: tarkat isäntänimet ilman https://-alkua."
    )

if len(SECRET_KEY) < 50 or len(set(SECRET_KEY)) < 5 or SECRET_KEY.startswith("django-insecure-"):
    raise ImproperlyConfigured("Luo tuotantoon uusi pitkä satunnainen DJANGO_SECRET_KEY.")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Aktivoi vasta, kun julkinen HTTPS ja admin-kirjautuminen on testattu.
SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_HSTS_SECONDS", "0"))
if SECURE_HSTS_SECONDS < 0:
    raise ImproperlyConfigured("DJANGO_HSTS_SECONDS ei saa olla negatiivinen.")
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# PythonAnywheren tavallinen WSGI-julkaisu välittää HTTPS-tilan palvelimelta.
# Älä luota asiakkaan lähettämiin proxy-otsakkeisiin ilman alustakohtaista tarvetta.
