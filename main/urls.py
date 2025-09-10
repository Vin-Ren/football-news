from django.urls import path
from .views import create_news, show_json, show_json_by_id, show_main, show_news, show_xml, show_xml_by_id

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('news/<str:id>/', show_news, name='show_news'),
    path('xml/<str:news_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:news_id>/', show_json_by_id, name='show_json_by_id'),
    path('create-news/', create_news, name='create_news'),
]
