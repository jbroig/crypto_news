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

            date_div = article.find_all('div', class_='jeg_meta_date')
            if date_div:
                date = date_div[0].get_text()
                new_headline.publish_date = date

            image_div = article.find_all('div', class_='jeg_thumb')
            if image_div:
                image_link = image_div[0].find_all('a')
                if image_link:
                    image = image_link[0].find_all('img')
                    if image:
                        image_src = image[0]['src']
                        image_height = image['height']
                        image_width = image['width']
                        new_headline.image = image_src if image_src else None
                        new_headline.image_height = image_height if image_height else None
                        new_headline.image_width = image_width if image_width else None

            new_headline.save()

    return redirect("../")


def news_list(request):
    headlines = Headline.objects.all()[::-1]

    main_headlines = Headline.objects.filter(image_width=360)[:10]
    no_image_link = Headline.objects.filter(image_width__gte=80, image_width__lte=120).order_by('created_date')[:10]

    context = {
        'main_headlines': main_headlines,
        'no_image_link': no_image_link,
        # 'object_list': headlines,
    }
    return render(request, "home.html", context)


def get_news_admin(request):
    context = {}
    return render(request, "get_news_admin.html", context)
