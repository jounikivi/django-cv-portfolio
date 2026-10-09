# Julkaisu PythonAnywhereen

Paikallinen sivusto käyttää `cv_site.settings`-asetuksia. Julkinen sivusto käyttää
`cv_site.settings_production`-asetuksia, joissa DEBUG on aina pois käytöstä.
Älä vaihda paikallista .env-tiedostoa tuotannon tiedostoksi.

## 1. Ennen siirtoa

- Tarkista sisältö, yhteystiedot ja julkiseen CV:hen sisältyvät henkilötiedot.
- Ota tuore varmuuskopio SQLite-tietokannasta ja media-kansiosta.
  Pysäytä paikallinen palvelin ja muut tietokantaan kirjoittavat ohjelmat ennen
  db.sqlite3-tiedoston kopioimista. Säilytä varmuuskopio projektin ulkopuolella.
- Tallenna ja lähetä tarkistetut koodimuutokset GitHubiin. Älä lähetä .env-tiedostoa,
  tietokantaa, varmuuskopioita tai media-kansiota GitHubiin.

## 2. Koodi ja virtuaaliympäristö

Luo ilmainen Beginner-tili. Avaa Consoles → Bash ja suorita:

```bash
git clone https://github.com/jounikivi/django-cv-portfolio.git
cd ~/django-cv-portfolio
```

Valitse Web-välilehden Manual configuration -vaihtoehdossa saatavilla oleva
projektin riippuvuuksien tukema Python-versio (vähintään 3.10). Käytä samaa
versiota virtuaaliympäristössä. Esimerkki, jos Python 3.13 on saatavilla:

```bash
mkvirtualenv cv-portfolio --python=/usr/bin/python3.13
python -m pip install -r requirements.txt
python -m pip check
```

Jos versio tai riippuvuuden asennus ei onnistu, pysähdy ja tarkista virhe.
Älä alenna riippuvuuksia summittaisesti. Windowsin .venv-kansiota ei siirretä.

## 3. Salaiset asetukset ja sisältö

Luo PythonAnywheren Files-välilehdellä tiedosto
`/home/KAYTTAJA/django-cv-portfolio/.env`. Korvaa KAYTTAJA omalla käyttäjänimelläsi.

```dotenv
DJANGO_SECRET_KEY=TÄHÄN_UUSI_SATUNNAINEN_AVAIN
DJANGO_ALLOWED_HOSTS=KAYTTAJA.pythonanywhere.com
DJANGO_HSTS_SECONDS=0
```

Käytä ALLOWED_HOSTS-arvona juuri Web-välilehdellä näkyvää isäntänimeä
(EU-palvelussa loppuosa voi olla eri). Ei jokerimerkkiä tai https://-alkua.
Luo avain Bash-konsolissa ja kopioi tulos vain palvelimen .env-tiedostoon:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
chmod 600 ~/django-cv-portfolio/.env
```

Siirrä varmuuskopiosta `db.sqlite3` projektin juureen ja koko `media/`-sisältö
projektin media-kansioon. Säilytä alikansiot ja tiedostonimet täsmälleen samoina.
Tee tämä ennen ensimmäistä migrate-komentoa. Älä ylikirjoita myöhemmin julkisen
sivuston tietokantaa paikallisella kopiolla: sivustolla tehdyt muutokset häviäisivät.
Tietokanta sisältää myös admin-käyttäjän ja salasanatiivisteen.

## 4. Tarkista ja kerää staattiset tiedostot

Projektin juuressa, cv-portfolio-virtuaaliympäristössä:

```bash
python manage.py migrate --settings=cv_site.settings_production
python manage.py collectstatic --noinput --settings=cv_site.settings_production
python manage.py check --deploy --settings=cv_site.settings_production
```

Ensimmäisellä kerralla HSTS-varoitus security.W004 on odotettu, koska sen arvo
on tarkoituksella 0. Muut varoitukset selvitetään ennen julkaisua.
Varmista ylläpitäjälle vahva, muualla käyttämätön salasana; tarvittaessa vaihda:

```bash
python manage.py changepassword OMA_ADMIN_TUNNUS --settings=cv_site.settings_production
```

## 5. Web-välilehti

Valitse Add a new web app → Manual configuration, ei uuden Django-projektin
automaattista luontia. Valitse sama Python-versio kuin virtuaaliympäristössä.

- Source code ja Working directory: `/home/KAYTTAJA/django-cv-portfolio`
- Virtualenv: `/home/KAYTTAJA/.virtualenvs/cv-portfolio`
- Avaa Web-välilehden WSGI configuration file -linkki ja korvaa sen sisältö:

```python
import os
import sys

path = "/home/KAYTTAJA/django-cv-portfolio"
if path not in sys.path:
    sys.path.insert(0, path)
os.environ["DJANGO_SETTINGS_MODULE"] = "cv_site.settings_production"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Korvaa KAYTTAJA myös tässä. Muokattava tiedosto on PythonAnywheren tarjoama
WSGI-tiedosto, ei projektin cv_site/wsgi.py. Älä käytä runserver-komentoa julkaisussa.

Lisää Web → Static files -kohdassa vain nämä hakemistot:

| URL | Directory |
| --- | --- |
| /static/ | /home/KAYTTAJA/django-cv-portfolio/staticfiles |
| /media/ | /home/KAYTTAJA/django-cv-portfolio/media |

Älä koskaan tarjoile projektin juurta: siellä ovat tietokanta ja salaiset asetukset.
Media-kansion sisältö on julkista. Säilytä siellä vain julkaistavat kuvat ja CV.
Paina Reload. Tarkista HTTPS-osoite ja kytke Security → Force HTTPS päälle,
jotta myös staattiset tiedostot ohjataan suojattuun yhteyteen.

## 6. Julkaisun hyväksymistesti

- Etusivu ja kaikki osiot näkyvät oikein puhelimella ja tietokoneella.
- Profiilikuva, ORAOwl-logo, ikonit sekä CSS ja JavaScript latautuvat.
- Mobiilivalikko aukeaa ja sulkeutuu; näppäimistön kohdistus näkyy.
- CV avautuu oikeana PDF:nä. Sähköposti-, puhelin- ja projektiosoitteet ovat oikein.
- Admin-kirjautuminen ja yhden sisällön tallentaminen onnistuvat HTTPS:llä.
- HTTP ohjautuu HTTPS:ään ilman uudelleenohjaussilmukkaa.
- Olematon osoite palauttaa 404:n ilman teknisiä virhetietoja.
- `/.env`, `/db.sqlite3` ja `/.git/config` eivät ole ladattavissa (404).
- Virhelokissa ei ole sovellusvirheitä. Älä jaa lokeja tarkistamatta salaisuuksia.

Kun HTTPS ja admin toimivat, muuta palvelimen .env:ssä `DJANGO_HSTS_SECONDS=3600`,
paina Reload ja aja check --deploy uudelleen. Aloita lyhyellä ajalla; älä aktivoi
preloadia tai kaikkia alidomaineja. Tarkista selaimesta myös HSTS-vastausotsake.
HSTS:n aktivoinnin jälkeen W005 ja W021 ovat tässä tarkoituksellisia huomautuksia:
emme vaadi HTTPS:ää kaikilta alidomaineilta emmekä ilmoita osoitetta selainten
pysyvään preload-listaan. Älä muuta näitä vain varoitusten poistamiseksi.

## 7. Päivitykset ja varmuuskopiot

Varmuuskopioi palvelimen tietokanta ja media ennen päivityksiä. SQLite-kannasta
ota turvallinen kopio SQLite backup -menetelmällä tai keskeytä kirjoitukset
kopioinnin ajaksi. Säilytä kopio myös muualla kuin PythonAnywheressa.

Bash-konsolissa projektin juuressa:

```bash
workon cv-portfolio
git pull --ff-only
python -m pip install -r requirements.txt
python manage.py migrate --settings=cv_site.settings_production
python manage.py collectstatic --noinput --settings=cv_site.settings_production
python manage.py check --deploy --settings=cv_site.settings_production
```

Paina lopuksi Web → Reload. Älä siirrä paikallista tietokantaa päivityksen mukana.
Jos päivitys epäonnistuu, älä jatka: säilytä lokit ja varmuuskopio palautusta varten.
Ilmaisella tilillä jatka sivuston voimassaoloa Web-välilehdellä ennen siellä
näkyvää määräpäivää (nykyisin kuukauden välein). Tarkkaile 512 MiB levytilarajaa.

## Palveluntarjoajan ohjeet

- https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/
- https://help.pythonanywhere.com/pages/DjangoStaticFiles/
- https://help.pythonanywhere.com/pages/ForcingHTTPS
- https://help.pythonanywhere.com/pages/FreeAccountsFeatures
