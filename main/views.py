import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core import serializers

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse


from main.forms import NewsForm
from main.models import News

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    filters = request.GET.get('filter', 'all')
    news_list = News.objects.all() if filters == 'all' else News.objects.filter(user=request.user)
    context = {
        'npm': '2406353225',
        'name': 'Vincent Valentino Oei',
        'class': "PBP E",
        'news_list': news_list,
        'last_login': request.COOKIES.get('last_login')
    }
    return render(request, "main.html", context)

def show_xml(request):
    news_list = News.objects.all()
    data = serializers.serialize("xml", news_list)
    return HttpResponse(data, content_type="application/xml")

def show_json(request):
    news_list = News.objects.all()
    data = serializers.serialize("json", news_list)
    return HttpResponse(data, content_type="application/json")

def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()
    ctx = {
        'news': news
    }
    return render(request, "news_detail.html", context=ctx)

def show_xml_by_id(request, news_id):
    try:
        news_item = News.objects.filter(pk=news_id)
        xml_data = serializers.serialize("xml", news_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except News.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, news_id):
    try:
        news_item = News.objects.filter(pk=news_id)
        json_data = serializers.serialize("json", news_item)
        return HttpResponse(json_data, content_type="application/json")
    except News.DoesNotExist:
        return HttpResponse(status=404)

@login_required(login_url='/login')
def create_news(request: HttpRequest):
    form = NewsForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        news = form.save(commit=False)
        news.user = request.user
        news.save()
        return redirect('main:show_main')
    
    ctx = {
        'form': form
    }
    
    return render(request, 'create_news.html', context=ctx)

def register(request: HttpRequest):
    form = UserCreationForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        form.save()
        messages.success(request, 'Your account has been successfully created!')
        return redirect('main:login')
    ctx = {
        'form': form
    }
    return render(request, 'register.html', context=ctx)

def login_user(request: HttpRequest):
    
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST or None)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse('main:show_main'))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    context = {
        'form': form
    }
    return render(request, 'login.html', context=context)

def logout_user(request: HttpRequest):
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('last_login')
    return response
