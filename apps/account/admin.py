from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.


admin.site.unregister(Group)
