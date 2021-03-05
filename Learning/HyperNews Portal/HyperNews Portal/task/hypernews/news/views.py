from django.shortcuts import render
from django.conf import settings
from django.views import View
import json
from django.conf import settings
from django.views.generic.base import TemplateView
import datetime
from collections import defaultdict
from django.shortcuts import redirect
import random


json_path = 'C:\\Users\\ac5\\PycharmProjects\\HyperNews Portal\\HyperNews Portal\\task\\news.json'

with open(settings.NEWS_JSON_PATH, "r") as json_file:
    json_dict = json.load(json_file)

news_dict = [dict([key, datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').date() if key == 'created' else value]
                for key,value in dicts.items())
                for dicts in json_dict]

class MainView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/index.html',)

class NewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/news.html', context={'news_dict': news_dict})

class ArticleView(TemplateView):
    template_name = 'news/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_article = list(filter(lambda article: article['link'] == kwargs['n_article'], json_dict))[0]
        context['a_title'] = c_article['title']
        context['created'] = c_article['created']
        context['text'] = c_article['text']
        return context

class CreateArticle(View):
    articles = defaultdict(list)

    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html',)

    def post(self, request, *args, **kwargs):
        self.articles = dict()
        self.articles['created'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.articles['text'] = request.POST.get('text')
        self.articles['title'] = request.POST.get('title')
        self.articles['link'] = random.randint(100, 999)
        json_dict.append(self.articles)
        with open(settings.NEWS_JSON_PATH, "w") as json_file:
            json.dump(json_dict, json_file, indent=4)
        return redirect('/')



