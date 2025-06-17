from django.shortcuts import render

def view_test (request):
    return render(
        request,
        'blog/pages/index.html'
    )
