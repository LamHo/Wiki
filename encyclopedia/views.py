from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.conf.urls import handler404
from . import util
from django import forms
from . import urls
from django.shortcuts import redirect
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import loader
import random

class editForm(forms.Form):
    editted_content = forms.CharField(label = "", widget=forms.Textarea)


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request,'encyclopedia/error_404.html', data)

def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def load_entry(request, title):
    entry = util.get_entry(title)
    if (entry is not None):
        markdowner = Markdown()
        converted_content = markdowner.convert(entry)
        #print(converted_content)
        return render(request, "encyclopedia/entry_page.html",{
            "title": title,
            "content": converted_content
        })

    else:
        return render(request,'encyclopedia/error_404.html')
   
def search(request):
    if request.method == "GET":
        #print(request.GET['q'] in util.list_entries())
        if (request.GET['q'] == ""): #empty query
                result = []
                return render(request,"encyclopedia/search_results.html",{
                    "entries": result
                })
        else: #non_empty query
            if (request.GET['q'] in util.list_entries()): #the query matches the name of an encyclopedia entry
                return redirect(f"/wiki/{request.GET['q']}") #load_entry(request, request.GET['q'])
            else: 
                result = []
                list = util.list_entries()
                for entry in list:
                    if (request.GET['q']) in entry:
                        result += [entry]
                print(result)
                if (not result): #not find
                     return render(request,'encyclopedia/error_404.html')
                else: #displays a list of all encyclopedia entries that have the query as a substring
                    return render(request,"encyclopedia/search_results.html",{
                        "result": result
                    })
                                 
                    
def create(request):
    return render(request,"encyclopedia/create.html",{
            "exist": False
        })
        



def save(request):
    if request.method == "POST":        
        title = request.POST['in_title']
        if title in util.list_entries():
            
            return HttpResponse("<h1>Error: This entry's title already exists</h1>")
            
            """           
            return render(request,"encyclopedia/create.html",{
                "exist":  True
            })
            """
        content = request.POST['in_content']
        util.save_entry(title, content)
        return redirect(f"/wiki/{title}")
    else:
        return render(request,"encyclopedia/create.html")
        

def edit(request, title):
    if (request.method == "POST"):
        form = editForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["editted_content"]
            util.save_entry(title, content)
        return redirect(f"/wiki/{title}")
    else:
        form = editForm(initial={"editted_content": util.get_entry(title)})

        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "form": form
        })


def rand(request):
    #return HttpResponse("Hello World!")
    
    list = util.list_entries()
    choosen = random.choice(list)
    return redirect(f"/wiki/{choosen}")
    