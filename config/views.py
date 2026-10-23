from django.shortcuts import render


def home_view(request):
    # Renders the public blank homepage.
    return render(request, "../templates/base.html")
