from django.shortcuts import render


def register_view(request) -> render:
    return render(request, 'authors/pages/author.html')
