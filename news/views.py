import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline


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

        # todo: skip less than 10 characters titles.
        new_headline = Headline()
        new_headline.url = url_link
        new_headline.title = text

        image_div = article.find_all('div', class_='jeg_thumb')
        if image_div:
            image_link = image_div[0].find_all('a')
            if image_link:
                image = image_link[0].find_all('img')[0]
                image_src = image['data-lazy-src']
                image_height = image['height']
                image_width = image['width']
                new_headline.image = image_src if image_src else None
                new_headline.image_height = image_height if image_height else None
                new_headline.image_width = image_width if image_width else None

        new_headline.save()

    return redirect("../")

def news_list(request):
    headlines = Headline.objects.all()[::-1]

    main_headlines = Headline.objects.filter(image_width=360)
    no_image_link = Headline.objects.filter(image_width__gte=80, image_width__lte=120)

    context = {
        'main_headlines': main_headlines,
        'no_image_link': no_image_link,
        # 'object_list': headlines,
    }
    return render(request, "home.html", context)


def get_news_admin(request):
    context = {}
    return render(request, "get_news_admin.html", context)
