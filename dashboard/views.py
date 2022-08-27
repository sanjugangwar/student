from re import search
from turtle import onclick
from django.shortcuts import render,redirect
from . forms import *
from django.contrib import messages
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request,'dashboard/home.html')


@login_required    
def notes(request):
    if(request.method=='POST'):
        form=Notesform(request.POST)
        if form.is_valid:
            notes=Note(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes added from {request.user.username} is successfully added")    
    else:        
     form=Notesform()
    note=Note.objects.filter(user=request.user)
    context={'notes':note,'form':form}
    return render(request,'dashboard/notes.html',context)



@login_required         
def delete_note(request,pk):
    Note.objects.get(id=pk).delete()
    return redirect("notes")
    


def notes_details(request,pk):
    note=Note.objects.get(id=pk)
    return render(request,'dashboard/notes_detail.html',{'note':note}) 


@login_required        
def homework(request):
    if(request.method=='POST'):
        form=Homeform(request.POST)
        if form.is_valid:
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                   finished=True
                else:
                   finished=False
            except:
                   finished=False     
            work=Homework(user=request.user,subject=request.POST['subject'],title=request.POST['title'],description=request.POST['description'],
            due=request.POST['due'],is_finished=finished)
            work.save()
            messages.success(request,f"Work added from {request.user.username} is successfully added")   
            return redirect("homework") 
    else:
        form=Homeform()        
    work=Homework.objects.filter(user=request.user)
    if len(work)==0:
       workdone=True
    else:
       workdone=False
    context={'work':work,'form':form,'workdone':workdone}
    return render(request,'dashboard/homework.html',context)  




@login_required     
def delete_work(request,pk):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")   




@login_required 
def update_homework(request,pk):
    work=Homework.objects.get(id=pk)
    print(work.is_finished)
    print("update")
    if work.is_finished==True:
       work.is_finished=False
    else:
        work.is_finished=True
    work.save()
    return redirect("homework")  




def youtube(request):
    if request.method=='POST':
        form=DashboardForm(request.POST)
        text=request.POST['text']
        video=VideosSearch(text,limit=10)
        result_list=[]
        for i in video.result()['result']:
            result_dict={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc+=j['text'] 
            result_dict['description']=desc
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)            
    else :
        form=DashboardForm()
    context={'form':form}
    return render(request,'dashboard/youtube.html',context)         




@login_required 
def todo(request):
    if(request.method=='POST'):
        form=TodoForm(request.POST)
        finished=request.POST.get('is_finished')
        if form.is_valid():
            try:
                if finished=='on':
                   finished=True
                else:
                    finished=False
            except:
                finished=False
        todo=Todo(user=request.user,title=request.POST['title'],is_finished=finished)
        todo.save() 
        messages.success(request,f"Todo added from {request.user.username} is successfully added!!") 
        return redirect("todo")
    else: 
         form=TodoForm()                                 
    todo=Todo.objects.filter(user=request.user)
    if len(todo)==0:
        done=True
    else:
        done=False 
    context={'done':done,'todo':todo,'form':form}        
    return render(request,'dashboard/todo.html',context)




@login_required 
def delete_todo(request,pk):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")




@login_required 
def update_todo(request,pk):
    todo=Todo.objects.get(id=pk)
    print(todo)
    if todo.is_finished==True:
        todo.is_finished=False
    else:
        todo.is_finished=True  
    todo.save()     
    return redirect("todo")     



def books(request):
    if request.method=='POST':
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html',context)            
    else :
        form=DashboardForm()
    context={'form':form}
    return render(request,'dashboard/books.html',context)  



def dictionary(request):
    if request.method=='POST':
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url="https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r=requests.get(url)
        answer=r.json()
        try:
            phonetics=answer[0]['phonetics'][0]['text']
            audio=answer[0]['phonetics'][0]['audio']
            definition=answer[0]['meanings'][0]['definitions'][0]['definition']
            example=answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms=answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context={
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context={
                'form':form,
                'input':''
            }
        return render(request,'dashboard/dictionary.html',context)
    else:          
        form=DashboardForm()
        context={'form':form}
        return render(request,'dashboard/dictionary.html',context)  




def wiki(request):
    if(request.method=='POST'):
        text=request.POST['text']
        form=DashboardForm(request.POST)
        search=wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'dashboard/wiki.html',context)
    else:
        form=DashboardForm()
        context={
            'form':form
        }
    return render(request,'dashboard/wiki.html',context)




def conversion(request):
   if request.method=="POST":
       form=ConversionForm(request.POST)
       if request.POST['measurement']=='length':
           measurement_form=ConversionlengthForm()
           context={
            'form':form,
            'm_form':measurement_form,
            'input':True
           }
           if 'input' in request.POST:
               first=request.POST['measure1']
               second=request.POST['measure2']
               input=request.POST['input']
               answer=''
               if input and int(input)>=0:
                  if first=='yard' and second=='foot':
                    answer=f'{input} yard={int(input)*3} foot'
                  if first=='foot' and second=='yard':
                    answer=f'{input} yard={int(input)/3} yard'
               context={
                'form':form,
                'm_form':measurement_form,
                'input':True,
                'answer':answer
               }     
       if request.POST['measurement']=='mass':
            measurement_form=ConversionMassForm()
            context={
               'form':form,
               'm_form':measurement_form,
               'input':True
            }
            if 'input' in request.POST:
               first=request.POST['measure1']
               second=request.POST['measure2']
               input=request.POST['input']
               answer=''
               if input and int(input)>=0:
                  if first=='pound' and second=='kilogram':
                    answer=f'{input} yard={int(input)*0.45392} kilogram'
                  if first=='kilogram' and second=='pound':
                    answer=f'{input} yard={int(input)/2.20462} pound'
               context={
                'form':form,
                'm_form':measurement_form,
                'input':True,
                'answer':answer
               }     
   else:
        form=ConversionForm()
        context={
            'form':form,
            'input':False
        }         
   return render(request,'dashboard/conversion.html',context)



def register(request):
    if request.method=='POST':
        form=UserReisteraionForm(request.POST)
        if form.is_valid:
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"Account Created For {username}!!")
            return redirect("login")
    else:
        form=UserReisteraionForm()  
    context={'form':form}
    return render(request,'dashboard/register.html',context) 


    
@login_required     
def profile(request):
    homeworks=Homework.objects.filter(is_finished=False,user=request.user)
    todos=Todo.objects.filter(is_finished=False,user=request.user)
    homework_done=False
    todos_done=False
    if len(homeworks)==0:
        homework_done=True
    if len(todos)==0:
        todos_done=True   
    context={
        'homework':homeworks,
        'todo':todos,
        'todo_done':todos_done,
        'homework_done':homework_done
    }         
    return render(request,'dashboard/profile.html',context)