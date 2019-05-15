"""solosandbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from solosandbox import views
from django.urls import path
from .views import ModelList # this is for the new class-based view

#The new django.urls.path() function allows a simpler, more readable URL routing syntax.
from solosandbox.models import blogurls

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^$', views.home, name='home'),
  url('error_page.html', views.errors),
  url('homepagesoup.html', views.homepagesoup),
  url('getfeedalpha.html', views.getfeedalpha),
  path('getfeedchron.html', views.getfeedchron),
  url('bloggerapigetalpha.html', views.bloggerapigetalpha),
  url('bloggerapigetchron.html', views.bloggerapigetchron),
  path('get_recipe_by_label.html', views.get_recipe_by_label),
  path('show_label_list.html', views.show_label_list),
  path('showallrecipeschosen.html', views.showallrecipeschosen),
  path('modelfun.html', views.modelfun),
  path('get_the_model_data.html', views.get_the_model_data),
  path('roto.html', views.roto),
  path('blogurls_list.html', ModelList.as_view(model=blogurls))



]





