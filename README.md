# CV- ja portfoliosivusto

Djangolla toteutettu henkilökohtainen CV- ja portfoliosivusto. Sivusto esittelee
profiilin, osaamisen, työkokemuksen, koulutuksen, projektit ja yhteystiedot.
Sisältöä ylläpidetään Django-hallinnassa.

Ulkoasun teemana on Obsidian Gold: tumma tausta, kultaiset korostukset ja
vaalea teksti. Sivusto mukautuu myös pienille näytöille.

## Toiminnot

- Profiilikuva, esittely ja ladattava PDF-CV.
- Osaamiskortit ilman numeerisia taitotasoja.
- Työkokemukset tehtäväkuvauksineen.
- Tutkinnot ja kurssit: valmistumisvuosi sekä vapaaehtoinen kuukausi.
- Projektien kuvaukset, teknologiat sekä projekti- ja lähdekoodilinkit.
- Yhteystietolinkit ja sisältöjen näkyvyyden sekä järjestyksen hallinta.

## Teknologiat

Python, Django, SQLite, HTML ja CSS. Pillow käsittelee kuvatiedostojen
tukea ja python-dotenv lukee paikalliset ympäristöasetukset.
Riippuvuuksien tarkat versiot ovat `requirements.txt`-tiedostossa.
Projektia on kehitetty Windowsissa Python 3.14:llä.

## Paikallinen käyttöönotto (Windows / PowerShell)

Kloonaa tämä repositorio GitHubin **Code**-painikkeesta saatavalla osoitteella
ja siirry sen kansioon. Suorita seuraavat komennot projektin juuressa,
jossa `manage.py` sijaitsee.

### 1. Virtuaaliympäristö ja riippuvuudet

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Komennot käyttävät virtuaaliympäristön Pythonia suoraan, joten aktivointia
tai PowerShellin suorituskäytännön muuttamista ei tarvita.

### 2. Paikalliset asetukset

Kopioi asetuspohja ensimmäisellä käyttökerralla:

```powershell
Copy-Item .env.example .env
```

Jos `.env` on jo olemassa, säilytä se. Luo uusi avain:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(64))"
```

Lisää tulostettu arvo `.env`-tiedostossa rivin `DJANGO_SECRET_KEY=` perään.
Pidä avain salassa. `.env` jää Gitin ulkopuolelle, ja `.env.example` sisältää
vain tyhjän mallin. Järjestelmään asetettu ympäristömuuttuja on etusijalla
`.env`-tiedostoon nähden.

### 3. Tietokanta ja ylläpitäjä

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
```

### 4. Käynnistys

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

- Sivusto: http://127.0.0.1:8000/
- Hallinta: http://127.0.0.1:8000/admin/

Uusi asennus on sisällöltään tyhjä. Lisää hallinnassa yksi profiili sekä
osaamiset, työkokemukset, koulutukset, projektit ja yhteystietolinkit.
Kuvat ja PDF-CV ladataan profiilin kautta. Näkyvyys määräytyy sisältöjen
`Is active` -valinnan mukaan. Pienempi `Display order` näytetään ensin;
projekteissa myös `Is featured` nostaa projektin muiden edelle.

## Projektin rakenne

```text
cv_site/                  Django-asetukset ja pääreititys
portfolio/                Mallit, hallinta ja näkymät
  migrations/             Tietokannan rakenteen muutokset
  templates/portfolio/    HTML-sivupohjat
  static/portfolio/css/   Tyylitiedostot
media/                    Paikalliset ladatut tiedostot (ei Gitissä)
manage.py                 Djangon hallintakomennot
requirements.txt          Python-riippuvuudet
.env.example              Ympäristöasetusten malli
```

## Tarkistukset

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
git diff --check
```

## Sisällöt ja varmuuskopiot

Git sisältää lähdekoodin ja migraatiot. Paikallinen `db.sqlite3`, ladatut
kuvat ja PDF-tiedostot (`media/`), `.env` sekä `.venv/` eivät kuulu repositorioon.
Adminissa lisätyt sisällöt eivät siksi siirry GitHubiin lähdekoodin mukana.

Varmuuskopioi tietokanta ja `media/` erikseen. Käytä SQLite-varmuuskopiointia
tai pysäytä tietokantaan kirjoittavat prosessit ennen tietokantatiedoston
kopioimista. Säilytä varmuuskopiot projektin ulkopuolella.

## Projektin tila

Sisältöjen hallinta ja sivuston perustoiminnot on toteutettu. Ulkoasun
viimeistely ja tuotantoon julkaisu ovat seuraavia työvaiheita.
Nykyiset asetukset (`DEBUG=True`) ja `runserver` on tarkoitettu paikalliseen
kehitykseen. Tuotanto edellyttää erillisiä julkaisuasetuksia, kuten
isäntänimien, salaisen avaimen ja staattisten sekä mediatiedostojen palvelun
määrittämistä.
