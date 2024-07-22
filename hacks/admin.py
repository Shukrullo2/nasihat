from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Writer)
admin.site.register(Hack)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Report)