from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core import serializers

from main.forms import NewsForm
from main.models import News

# Create your views here.
def show_main(request):
    news_list = News.objects.all()
    context = {
        'npm': '2406353225',
        'name': 'Vincent Valentino Oei',
        'class': "PBP E",
        'news_list': news_list
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

def create_news(request):
    form = NewsForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')
    
    ctx = {
        'form': form
    }
    
    return render(request, 'create_news.html', context=ctx)
