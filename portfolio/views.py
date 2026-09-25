from django.shortcuts import render

from .models import ContactLink, Education, Experience, Profile, Project, Skill


def group_skills(skills):
    """Ryhmittele nykyiset taidot esitystä varten; säilytä myös uudet taidot."""
    categories = [
        ("IT-tuki ja käyttäjätuki", {
            "IT-tuki ja käyttäjäneuvonta", "Windows ja tekninen ongelmanratkaisu",
        }),
        ("Laitteistot ja testaus", {
            "Tietokoneiden kokoonpano ja testaus",
            "Ohjelmistojen ja käyttöliittymien testaus",
        }),
        ("Ohjelmistokehitys", {"Python- ja Django-kehitys", "React ja TypeScript"}),
        ("Tietokannat ja versionhallinta", {"SQL ja SQLite", "Git ja GitHub"}),
    ]
    groups = []
    assigned = set()
    for title, names in categories:
        members = [skill.name for skill in skills if skill.name in names]
        if members:
            groups.append({"title": title, "items": members})
            assigned.update(members)
    other = [skill.name for skill in skills if skill.name not in assigned]
    if other:
        groups.append({"title": "Muu osaaminen", "items": other})
    return groups


def home(request):
    # Haetaan sivustolla näytettävä profiili.
    profile = Profile.objects.first()

    # Haetaan etusivulle vain näkyviksi merkityt yhteystietolinkit.
    contact_links = ContactLink.objects.filter(is_active=True)

    # Haetaan etusivulle vain näkyviksi merkityt työkokemukset.
    experiences = Experience.objects.filter(is_active=True)

    # Haetaan etusivulle vain näkyviksi merkityt koulutukset.
    educations = Education.objects.filter(is_active=True)

    # Haetaan etusivulle vain näkyviksi merkityt projektit.
    projects = Project.objects.filter(is_active=True)

    # Haetaan etusivulle vain näkyviksi merkityt taidot.
    skills = Skill.objects.filter(is_active=True)

    context = {
        "contact_links": contact_links,
        "educations": educations,
        "experiences": experiences,
        "profile": profile,
        "projects": projects,
        "skills": skills,
        "skill_groups": group_skills(skills),
    }

    return render(request, "portfolio/home.html", context)
