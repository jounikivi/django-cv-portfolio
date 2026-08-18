from django.shortcuts import render

from .models import ContactLink, Education, Experience, Profile, Project, Skill


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
    }

    return render(request, "portfolio/home.html", context)
