from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2

from . import util


def index(request):
    if 'q' in request.GET:
        query = request.GET['q']
        for entry in util.list_entries():
            if entry.lower() == query.lower():
                return HttpResponseRedirect(f'wiki/{entry}')
        
        # No exact match
        results = []
        for entry in util.list_entries():
            if query.lower() in entry.lower():
                results.append(entry)
        return render(request, "encyclopedia/search_results.html", {
            "results": results,
            "query": query
        })
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