from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


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
            "content": markdown2.markdown(content)
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
