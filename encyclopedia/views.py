from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import random


from . import util

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entryPage(request, TITLE):
    content = util.get_entry(TITLE)
    if content:
        return render(request, "encyclopedia/entryPage.html", {
            "content": markdown2.markdown(content),
            "title": TITLE
        })
    else:
        return render(request, "encyclopedia/entryPage.html", {
            "content": "<h1>Page not found</h1>"
        })


def search(request):
    keyword = request.GET["q"]
    entries = util.list_entries()
    isKeywordInEntries = keyword.lower() in (entry.lower()
                                             for entry in entries)
    if isKeywordInEntries:
        return HttpResponseRedirect(reverse("encyclopedia:entryPage", kwargs={'TITLE': keyword}))
    else:
        substrings = []
        for entry in entries:
            if keyword.lower() in entry.lower():
                substrings.append(entry)
        return render(request, "encyclopedia/searchResults.html", {
            "substrings": substrings
        })


def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newPage.html")

    title = request.POST["title"]
    content = request.POST["content"]
    entries = util.list_entries()
    isTitleInEntries = title.lower() in (entry.lower() for entry in entries)

    if isTitleInEntries:
        messages.add_message(request, messages.ERROR,
                             "The title already exists!")
        return render(request, "encyclopedia/newPage.html")

    util.save_entry(title, content)
    return HttpResponseRedirect(reverse("encyclopedia:entryPage", kwargs={'TITLE': title}))


def editPage(request):
    if request.method == "GET":
        title = request.GET['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "content": content
        })

    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("encyclopedia:entryPage", kwargs={'TITLE': title}))


def randomPage(request):
    entries = util.list_entries()
    randomTitle = random.choice(entries)
    return HttpResponseRedirect(reverse("encyclopedia:entryPage", kwargs={'TITLE': randomTitle}))
