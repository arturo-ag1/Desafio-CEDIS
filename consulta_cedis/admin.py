from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.models import ContentType
from .models import *

# Register your models here.
admin.site.register(ContentType)
admin.site.register(Permission)
admin.site.register(Consulta)