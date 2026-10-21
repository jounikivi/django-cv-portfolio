# Esittely- ja korttipäivityksen julkaisu

Päivitys lisää muokattavat esittelykentät, osaamiskuvaukset, kuvaavat
tehtäväotsikot ja projektityypit. Migraatio 0012 täyttää vain uudet tyhjät
kentät Jounin sivustolle. Nykyiset esittelyt, tehtävänimikkeet, kuvaukset,
kuvat ja CV säilyvät. Paikallista tietokantaa ei siirretä tuotantoon.

1. Tarkista paikallinen sivu. Tee GitHub Desktopissa commit ja Push origin.
2. Ota PythonAnywheren Bash-konsolissa tietokantavarmistus ennen päivitystä:

```bash
workon cv-portfolio
cd ~/django-cv-portfolio
python - <<'PY'
from pathlib import Path
from datetime import datetime
import sqlite3
folder = Path.home() / "cv-backups"
folder.mkdir(exist_ok=True)
target = folder / ("before-presentation-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".sqlite3")
with sqlite3.connect("db.sqlite3") as source, sqlite3.connect(target) as backup:
    source.backup(backup)
print(target)
PY
```

Lataa varmistus myös omalle koneelle Files-välilehdeltä.
Tämä päivitys ei muuta media-tiedostoja.

3. Aja seuraavat komennot yksi kerrallaan. Pysähdy virheeseen.

```bash
git pull --ff-only
python -m pip install -r requirements.txt
python manage.py migrate --settings=cv_site.settings_production
python manage.py collectstatic --noinput --settings=cv_site.settings_production
python manage.py check --deploy --settings=cv_site.settings_production
```

4. Paina Web → Reload. Tarkista etusivu, Minusta, osaamiset, projektit ja
   mobiilivalikko. HSTS-varoitus on odotettu, jos HTTPS:n jatkovarmennusta
   ja HSTS:n käyttöönottoa ei ole vielä tehty.

## Sisältöjen muokkaaminen jatkossa

- Profiles: etusivun pääotsikko, lyhyt aloitusteksti, Minusta-osion tekstit,
  kielitaito (yksi kieli per rivi) ja yhteydenoton esittelyteksti.
- Skills: Käytännön esimerkki näkyy taidon omassa osaamisryhmässä.
- Experiences: Kuvaava tehtäväotsikko on vapaaehtoinen. Tyhjänä käytetään
  alkuperäistä tehtävänimikettä.
- Projects: Projektin tyyppi ja pilkuilla erotellut teknologiat.

Tyhjä Minusta-teksti piilottaa koko osion ja sen navigaatiolinkin. Tyhjä
aloitusteksti käyttää alkuperäistä Bio-kenttää. Migraation tekstit ovat
aloitussisältöjä, joita voi muuttaa adminissa normaalisti.
