from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'npm': '2406353225',
        'name': 'Vincent Valentino Oei',
        'class': "PBP E"
    }
    return render(request, "main.html", context)