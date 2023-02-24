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
from django.views.generic.edit import UpdateView

from . import util
from .models import Entry


class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label="Entry Title", required=True, widget=forms.TextInput)
    entry_content = forms.CharField(label="Content: ", required=True, widget= forms.Textarea)

class EditEntryForm(forms.Form):
    entry_content = forms.CharField(label="Content: ", widget=forms.Textarea)
    
def index(request):
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
                
            entry_title = form.cleaned_data["entry_title"]
            entry_content = form.cleaned_data["entry_content"]


            all_entries = util.list_entries()
            for filename in all_entries:
                if entry_title.lower()== filename.lower():
                    error_message="Page exists with the title '%s'. \n please try again with different title!" %filename
                    return render(request, "encyclopedia/new.html",{
                        "form":form,
                        "error":error_message
                    })

            util.save_entry(entry_title, entry_content)
            return HttpResponseRedirect(reverse('encyclopedia:index') + f'wiki/{entry_title}')
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

def edit(request, entry_title):
    entry_content = util.get_entry(entry_title)
    form = EditEntryForm(initial={
        "entry_content": entry_content
    })
    if request.method == 'POST':
        form = EditEntryForm(request.POST, initial={
            "entry_content": entry_content
        })
        if form.is_valid():
            entry_content = form.cleaned_data["entry_content"]

            util.save_entry(entry_title, entry_content)
            return HttpResponseRedirect(reverse('encyclopedia:index') + f'wiki/{entry_title}')
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "entry_title": entry_title
            })
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "entry_title": entry_title
        })
        
def search(request):
    query = request.GET['q']
    for entry in util.list_entries():
        if entry.lower() == query.lower():
            return HttpResponseRedirect(reverse('encyclopedia:index') + f'wiki/{entry}')
    
    # No exact match
    results = []
    for entry in util.list_entries():
        if query.lower() in entry.lower():
            results.append(entry)
    return render(request, "encyclopedia/search_results.html", {
        "results": results,
        "query": query
    })