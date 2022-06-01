from django.contrib import admin
from .models import Commnt, Post

admin.site.register([Post,Commnt])