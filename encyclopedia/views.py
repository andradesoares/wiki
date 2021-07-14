from django import forms
from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponse
import re
from . import util
import random


markdowner = Markdown()
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    request.session["entry"] = entry
    entry = util.get_entry(entry)
    
    if not entry:
        return render(request, "encyclopedia/error.html", {
        "message": "This entry does not exist."
        })
    else:
        response = markdowner.convert(entry)
        return render(request, "encyclopedia/entry.html", {
            "entry": response
        })
    

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            check = util.get_entry(title)
            if not check:
                (util.save_entry(title, content))
                entry = util.get_entry(title)
                request.session["entry"] = title
                response = markdowner.convert(entry)
                return render(request, "encyclopedia/entry.html", {
                    "entry": response
                })
            else:
                request.session["entry"] = title
                return render(request, "encyclopedia/entry.html", {
                    "entry": "Error this page already exists."
                })
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
        })

def edit(request):
    if request.method == "POST":
        form = (request.POST)
        content = form["updateEntry"]
        util.save_entry(request.session["entry"], content)
        entry = util.get_entry(request.session["entry"])
        response = markdowner.convert(entry)
        return render(request, "encyclopedia/entry.html", {
            "entry": response
        })
    else:
        entry = util.get_entry(request.session["entry"])
        return render(request, "encyclopedia/edit.html", {
            "entry": entry
        })


def search(request):
    form = (request.POST)
    searhTerm = form["q"]
    entry = util.get_entry(searhTerm)
    if entry:
        request.session["entry"] = entry
        response = markdowner.convert(entry)
        return render(request, "encyclopedia/entry.html", {
            "entry": response
        })
    else:
        entry = util.list_entries()
        pattern = re.compile(searhTerm)
        response = []
        for entries in entry:
            if pattern.search(entries):
                response.append(entries)
        return render(request, "encyclopedia/search.html", {
            "entries": response
        })

def random_page(request):
    entries = util.list_entries() # list of wikis
    selected_page = random.choice(entries)
    entry = util.get_entry(selected_page)
    response = markdowner.convert(entry)
    request.session["entry"] = selected_page
    return render(request, "encyclopedia/entry.html", {
        "entry": response
    })