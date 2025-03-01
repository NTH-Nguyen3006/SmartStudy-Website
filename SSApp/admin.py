from django.contrib import admin
from .models import Exam

# Register your models here.
class Exam_AdminSite(admin.AdminSite):
    pass

admin.site.register(Exam)
