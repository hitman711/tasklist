""" List of urls of tasklist app

* task-list
* task-retrieve
"""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^list/$', views.TaskList.as_view(), name="task-list"),
    url(r'^(?P<task_id>[0-9]+)/$',
        views.TaskRetrieve.as_view(), name="task-retrieve"),
    url(r'^(?P<task_id>[0-9]+)/status/$',
        views.TaskStatus.as_view(), name="task-status"),
]
