from django.shortcuts import render


def just_eating_home_view(request):
    return render(request, "just_eating_home.html")
