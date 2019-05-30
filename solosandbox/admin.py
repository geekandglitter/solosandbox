# Register your models here.

from django.contrib import admin

from .models import blogurls  # import the class we just created

admin.site.register(blogurls)  # register on the actual admin site