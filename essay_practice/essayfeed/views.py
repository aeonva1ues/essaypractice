from django.shortcuts import render


def essay_feed(request):
    template_name = 'essay_feed/feed.html'
    return render(request, template_name)
