from django.shortcuts import render

# Näytetään CV-sivuston etusivu HTML-templaten avulla.
def home(request):
    # Etsitään template ja palautetaan valmis HTML-vastaus selaimelle.
    return render(request, "portfolio/home.html")
