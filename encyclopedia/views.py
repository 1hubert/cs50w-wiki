from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_title):
    return render(request, "encyclopedia/entry.html", {
        "entry_title": entry_title,
        "entry_content": markdown2.markdown(util.get_entry(entry_title))
    })