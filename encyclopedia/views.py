import os
import random

from django import forms
from django.shortcuts import render
from django.forms import ModelForm, ValidationError
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
from django.db import models
from django.views.generic.edit import FormView

from . import util
from .models import Entry


class NewEntryForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        entry_title = cleaned_data.get("entry_title")
        entry_content = cleaned_data.get("entry_content")
        
        if entry_title in util.list_entries():
            raise ValidationError("Entry already exists in the wiki")
        
        return cleaned_data
        
    class Meta:
        model = Entry
        fields = ["entry_title", "entry_content"]

class NewEntryFormView(FormView):
    form_class = NewEntryForm
    success_url = '/'
    template_name = 'encyclopedia/new.html'
    def form_valid(self, form):
        entry_title = form.cleaned_data["entry_title"]
        entry_content = form.cleaned_data["entry_content"]
        os.chdir('entries')
        with open(f"{entry_title}.md","w+") as f:
            f.write(entry_content)
        os.chdir('..')
        
        return HttpResponseRedirect(self.success_url)

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
        
def new(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)

        if form.is_valid():
            #entry_title = form.cleaned_data["entry_title"]
            #entry_content = form.cleaned_data["entry_content"]
                
            return HttpResponseRedirect('')
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })
    
def rand(request):
    choice = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('encyclopedia:index') + f'wiki/{choice}')