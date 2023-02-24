from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2

from . import util


def index(request):
    if 'q' in request.GET:
        query = request.GET['q']
        if query in util.list_entries():
            return HttpResponseRedirect(f'wiki/{query}')
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def entry(request, entry_title):
    if entry_title in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry_title,
            "entry_content": markdown2.markdown(util.get_entry(entry_title))
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "entry_title": entry_title,
        })