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
    news = soup.find_all('article')

    # print(news)

    for article in news:
        main = article.find_all('a')[0]
        main_src = article.find_all('img')

        if main_src:
            src = main_src[0]['data-lazy-src']
            # print(src)

        link = main['href']  # good

        text = main.get_text()  # good
        # print(text)

        if link and len(text) > 10:
            print(text)
            print(len(text))
            new_headline = Headline()
            new_headline.title = text
            new_headline.image = src if src else None
            new_headline.save()

    return redirect("../")


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, "home.html", context)
