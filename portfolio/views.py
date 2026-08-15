from django.shortcuts import render

from .models import Skill


def home(request):
    # Haetaan etusivulle vain näkyviksi merkityt taidot.
    skills = Skill.objects.filter(is_active=True)

    context = {
        "skills": skills,
    }

    return render(request, "portfolio/home.html", context)
