from django.db import migrations


def seed_presentation(apps, schema_editor):
    """Täytä vain uudet tyhjät kentät; älä korvaa ylläpitäjän sisältöjä."""
    alias = schema_editor.connection.alias
    Profile = apps.get_model("portfolio", "Profile")
    profiles = Profile.objects.using(alias).filter(full_name="Jouni Kiviperä")
    if not profiles.exists():
        return
    content = {
        "headline": "IT-osaaja, joka yhdistää käyttäjätuen ja käytännön kehitystyön",
        "intro": "Autan käyttäjiä, selvitän teknisiä ongelmia ja rakennan verkkosovelluksia Pythonilla ja Djangolla.",
        "about_heading": "Tekniikka toimii parhaiten, kun se auttaa ihmistä.",
        "about_text": "Olen Jouni Kiviperä, tietojenkäsittelyn tradenomi Turusta. Etsin tehtävää, jossa voin yhdistää käytännön IT-tuen ja ohjelmistokehityksen.\n\nTyöskentelen rauhallisesti ja selitän tekniset asiat ymmärrettävästi. Kun vastaan tulee uusi järjestelmä tai ongelma, selvitän asiaa, dokumentoin tarvittavan ja kysyn apua, kun sitä tarvitaan.",
        "languages": "Suomi – äidinkieli\nEnglanti – hyvä kirjallinen taito, suullinen taito kehittymässä",
        "contact_intro": "Etsin IT-tuen, käyttäjätuen ja ohjelmistokehityksen tehtäviä Turun seudulta. Keskustelen mielelläni siitä, miten voisin auttaa teidän tiimiänne.",
    }
    for field, value in content.items():
        profiles.filter(**{field: ""}).update(**{field: value})

    Skill = apps.get_model("portfolio", "Skill")
    descriptions = {
        "IT-tuki ja käyttäjäneuvonta": "Opastan ohjelmistojen käytössä ja selvitän käyttäjien laitteisto-ongelmia. Kerron ratkaisut ymmärrettävästi.",
        "Tietokoneiden kokoonpano ja testaus": "Kokoan tietokoneita ja testaan niiden toimintaa. Olen myös arvioinut käyttöliittymien käytettävyyttä ja tehnyt parannusehdotuksia.",
        "Python- ja Django-kehitys": "Olen kehittänyt Django-verkkopalveluja sekä toteuttanut työnhaun seurantasovelluksen Reactilla ja TypeScriptillä.",
        "SQL ja SQLite": "Olen toteuttanut tietojen tallennusta ja raportointia SQL-tietokannalla. Käytän Gitiä ja GitHubia koodin versionhallintaan.",
    }
    for name, description in descriptions.items():
        Skill.objects.using(alias).filter(name=name, description="").update(description=description)

    Experience = apps.get_model("portfolio", "Experience")
    for company, title in [
        ("Turun AMK / Futuristic Interactive Technologies", "Harjoittelija – käyttöliittymien suunnittelu ja testaus"),
        ("Jimm’s PC-Store Oy", "Harjoittelija – tietokoneiden kokoonpano ja testaus"),
    ]:
        Experience.objects.using(alias).filter(company=company, job_title="Harjoittelija", display_title="").update(display_title=title)

    Project = apps.get_model("portfolio", "Project")
    for title, category in [("ORAOwl", "Django-verkkosovellus"), ("IT Log Analyzer", "Python-työkalu"), ("JobTrack Lite", "React-verkkosovellus")]:
        Project.objects.using(alias).filter(title=title, category="").update(category=category)


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0011_portfolio_presentation_fields")]
    operations = [migrations.RunPython(seed_presentation, migrations.RunPython.noop)]
