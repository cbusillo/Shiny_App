"""django_poetry_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import logging

from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.views.generic import RedirectView
from pwa import urls as pwa_urls

urlpatterns = [
    path("", include(pwa_urls)),
    path("", RedirectView.as_view(url="label_printer/"), name="home"),
    path("admin/", admin.site.urls, name="admin"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("favicon.ico/", RedirectView.as_view(url="/static/favicons/favicon.ico")),
]

for app in settings.SHINY_INSTALLED_APPS:
    app_name = app.split(".")[-1]
    urlpatterns.append(path(app_name + "/", include((app + ".urls", app_name), namespace=app_name)))
    logging.info("app: %s", app)
