from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name='home'),
    path("signup/",views.signup,name='signup'),
    path("tasks/",views.tasks,name='tasks'),
    path("logout/",views.signout,name='logout'),
    path("signin/",views.signin,name='signin'),
    path("tasks/create/",views.create_tasks,name='create_tasks'),
    path("tasks/completed/",views.tasksCompleted,name='tasksCompleted'),
    path("tasks/<int:tasks_id>/",views.tasks_detail,name='tasks_detail'),
    path("tasks/<int:tasks_id>/complete",views.completeTask,name='completeTask'),
    path("tasks/<int:tasks_id>/delete",views.completeTask,name='deleteTask'),
    path("tasks/<int:tasks_id>/update",views.updateTask,name='updateTask'),
    
]
