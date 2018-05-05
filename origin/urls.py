"""origin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework_swagger.views import get_swagger_view
from rest_framework import documentation

from . import views as auth_views

schema_view = get_swagger_view(title='Hotel Lab API configuration')

# REST Swagger configuration
REST_SWAGGER_SETTINGS = {
    "title": "Origin Task List API",
    "description": "List of all API end points for all origin project",
    "public": False
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sign-in/$', auth_views.SignIn.as_view()),
    url(r'^registration/$', auth_views.Registration.as_view()),
    url(r'^task/', include('tasklist.urls')),
    # API Swagger documentation
    url(r'^swagger/doc/', schema_view),
    url(r'^rest/swagger/doc/', documentation.include_docs_urls(
        title=REST_SWAGGER_SETTINGS['title'],
        description=REST_SWAGGER_SETTINGS['description'],
        public=REST_SWAGGER_SETTINGS['public'])
        ),
]
