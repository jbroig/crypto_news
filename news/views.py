import requests
from django.shortcuts import render, redirect
from django.utils import timezone

from bs4 import BeautifulSoup as BSoup

from news.models import Headline

from datetime import datetime
import hashlib
import pytz


def scrape(request):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    # url = "https://www.theonion.com/"
    url = "https://www.criptonoticias.com/"

    content = session.get(url, verify=False).content
    soup = BSoup(content, "html.parser")
    news = soup.find_all('article')  # Finds ALL the articles. Good job, mate.

    for article in news:
        main = article.find_all('h3', class_='jeg_post_title')[0]
        main_a = main.find_all('a')[0]

        category_post_div = article.find_all('div', class_='jeg_post_category')
        if category_post_div:
            category_div = category_post_div[0]
            if category_div.find_all('a'):
                category = category_div.get_text()
            else:
                category = None
        else:
            category = None

        url_link = main_a['href']
        text = main_a.get_text()
        headline_id = int(hashlib.md5(text.encode('utf-8')).hexdigest(), 16)

        exists = Headline.objects.filter(headline_id=headline_id)
        if not exists:

            # todo: skip less than 10 characters titles.
            new_headline = Headline()
            new_headline.url = url_link
            new_headline.title = text
            new_headline.headline_id = headline_id
            new_headline.created_date = datetime.now(tz=timezone.utc)
            new_headline.category = category
            new_headline.web = "criptonoticias.com"

            date_div = article.find_all('div', class_='jeg_meta_date')
            if date_div:
                date = date_div[0].get_text()
                new_headline.publish_date = date

            image_div = article.find_all('div', class_='jeg_thumb')
            has_image = False
            if image_div:
                image_link = image_div[0].find_all('a')
                if image_link:
                    image = image_link[0].find_all('img')
                    if image:
                        has_image = True
                        new_headline.has_image = True
                        image_src = image[0]['data-lazy-src'] if image[0]['data-lazy-src'] else image[1]['src']
                        image_height = image[0]['height']
                        image_width = image[0]['width']
                        new_headline.image = image_src if image_src else None
                        new_headline.image_height = image_height if image_height else None
                        new_headline.image_width = image_width if image_width else None

            if has_image:
                if 360 <= int(image_width) < 750:
                    new_headline.intern_category = "Artículos Principales"
                if int(image_width) < 360:
                    new_headline.intern_category = "Noticias al Día"
            else:
                new_headline.intern_category = "La columna"

            new_headline.save()

    return redirect("../")


def news_list(request):
    headlines = Headline.objects.all()[::-1]

    main_headline = Headline.objects.filter(intern_category='Artículos Principales').order_by('created_date')[:1]
    last_news = Headline.objects.filter(intern_category='La columna').order_by('created_date')[:2]
    common_news = Headline.objects.filter(intern_category='Artículos Principales').order_by('created_date')[1:]
    #no_image_link = Headline.objects.filter(image_width__gte=80, image_width__lte=120).order_by('created_date')[:10]
    no_image_news = Headline.objects.filter(has_image=False)

    context = {
        'main_headline': main_headline,
        'last_news': last_news,
        'common_news': common_news,
        'no_image_link': no_image_news,
        # 'object_list': headlines,
    }
    return render(request, "home.html", context)


def get_news_admin(request):
    context = {}
    return render(request, "get_news_admin.html", context)
