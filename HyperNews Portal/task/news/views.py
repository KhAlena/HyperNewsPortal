import datetime
import itertools

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
import json


class PageView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as json_file:
            data = {}
            data_from_json = json.load(json_file)
            for link in data_from_json:
                data[str(link['link'])] = link
        if kwargs['link'] not in data:
            raise Http404
        news_post = data[kwargs['link']]
        context = {"created": news_post['created'], "text": news_post['text'], "title": news_post['title']}
        return render(request, 'news/index.html', context=context)


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as json_file:
            pre_data_from_json = json.load(json_file)
        data_from_json = []
        if request.GET.get('q'):
            for data in pre_data_from_json:
                if request.GET.get('q') in data['title']:
                    data_from_json.append(data)
        else:
            data_from_json = pre_data_from_json

        sorted_news = sorted(data_from_json, key=lambda i: i['created'], reverse=True)
        groupped_news = itertools.groupby(sorted_news, lambda i: i['created'][:10])
        groups = {}
        for k, g in groupped_news:
            groups[k] = list(g)  # Store group iterator as a list
        context = {"news": groups}
        return render(request, 'news/main.html', context=context)


def soon(request):
    return redirect('/news/')


class PostView(View):
    def get(self, request):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        text = request.POST.get('text')
        title = request.POST.get('title')
        created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        link = datetime.datetime.now().strftime("%y%m%d%H%M%S")
        add_to_json = {'created': created, 'text': text, 'title': title, 'link': link}
        with open(settings.NEWS_JSON_PATH, "r") as json_file:
            data_from_json = json.load(json_file)
        with open(settings.NEWS_JSON_PATH, "w") as json_file:
            data_from_json.append(add_to_json)
            json.dump(data_from_json, json_file)
        return redirect('/news/')
