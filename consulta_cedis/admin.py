from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.models import ContentType

# Register your models here.
admin.site.register(ContentType)
admin.site.register(Permission)