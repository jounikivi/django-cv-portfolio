from django.shortcuts import render

from .models import Profile, Skill


def home(request):
    # Haetaan sivustolla näytettävä profiili.
    profile = Profile.objects.first()

    # Haetaan etusivulle vain näkyviksi merkityt taidot.
    skills = Skill.objects.filter(is_active=True)

    context = {
        "profile": profile,
        "skills": skills,
    }

    return render(request, "portfolio/home.html", context)
