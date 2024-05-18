from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TasksForm
from.models import Tasks
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.

#registrar usuarios
def signup(request):
    if request.method == 'GET':
        return render(request,"signup.html",{
        'from':UserCreationForm
        })
    else:
        # print("ya pues")
        # print(request.POST['password1'])
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('tasks')

            except IntegrityError:
                return render(request,"signup.html",{
                            'from':UserCreationForm,
                            'error':'el usuario ya existe'
                            })
        else:
            return render(request,"signup.html",{
                            'from':UserCreationForm,
                            'error':'la contraseña o coincide'
                            })

def home(request):
    return render(request,"home.html")


#presentar las tareas pendientes
@login_required
def tasks(request):
    tasks=Tasks.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,"tasks.html",{
        'tasks':tasks
    })


#Taras completadas
@login_required
def tasksCompleted(request):
    tasks=Tasks.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,"tasks.html",{
        'tasks':tasks
    })


#detalles de las tareas UI
@login_required
def tasks_detail(request,tasks_id):
    if request.method=='GET':
        task=get_object_or_404(Tasks,pk=tasks_id,user=request.user)
        form = TasksForm(instance=task)
        return render(request,'tasks_detail.html',
        {
            'task':task,
            'form':form
        })






#API para actualizar la tarea
@login_required
def updateTask(request,tasks_id):
    try:
        task=get_object_or_404(Tasks,pk=tasks_id,user=request.user)
        form = TasksForm(request.POST,instance=task)
        form.save()
        print(request.POST)
        return redirect('tasks')
    except ValueError:
        return render(request,'tasks_detail.html',
        {
            'task':task,
            'form':form,
            'error':'error actualizar tareas'
        })







#API para completar tarea
@login_required
def completeTask(request,tasks_id):
    Task=task=get_object_or_404(Tasks,pk=tasks_id,user=request.user)
    if request.method =='POST':
        task.datecompleted=timezone.now()
        task.save()
        return redirect('tasks')



#API para eliminar la tarea
@login_required
def deleteTask(request,tasks_id):
    Task=task=get_object_or_404(Tasks,pk=tasks_id,user=request.user)
    if request.method =='POST':
        task.delete()
        return redirect('tasks')
    
@login_required
def create_tasks(request):
    if request.method=='GET':
        return render(request,"create_task.html",{
            'form':TasksForm
        })
    else:
        try:
            form = TasksForm(request.POST)
            newtasks = form.save(commit=False)
            newtasks.user= request.user
            newtasks.save()
            return redirect('tasks')
        except ValueError:
            return render(request,"create_task.html",{
            'form':TasksForm,
            'error':'ingresa datos validos'
            })



@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method=='GET':
        return render(request,'signin.html',{
            'form':AuthenticationForm
        })
    else:
        user= authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
                'form':AuthenticationForm,
                'error':'el user o password es incorrecto'
            })
        else:
            login(request,user)
            return redirect("tasks")

