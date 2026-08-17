from django.shortcuts import render

from .models import Education, Experience, Profile, Skill


def home(request):
    # Haetaan sivustolla näytettävä profiili.
    profile = Profile.objects.first()

    # Haetaan etusivulle vain näkyviksi merkityt työkokemukset.
    experiences = Experience.objects.filter(is_active=True)

    # Haetaan etusivulle vain näkyviksi merkityt koulutukset.
    educations = Education.objects.filter(is_active=True)

    # Haetaan etusivulle vain näkyviksi merkityt taidot.
    skills = Skill.objects.filter(is_active=True)

    context = {
        "educations": educations,
        "experiences": experiences,
        "profile": profile,
        "skills": skills,
    }

    return render(request, "portfolio/home.html", context)
