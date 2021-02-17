from django.urls import path
from news.views import scrape, news_list, get_news_admin


urlpatterns = [
    path('scrape/', scrape, name="scrape"),
    path('', news_list, name="home"),
    path('home/', news_list, name="home"),
    path('get_news_admin/', get_news_admin, name="get_news_admin")
]
