from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.
class Eng_Dictionary(models.Model):
    word = models.TextField()
    mean = models.TextField()


class VieWord(models.Model):
    word = models.CharField(max_length=40)
    def __str__(self):
        return self.word


class Irregular_Verb(models.Model):
    verb1 = models.CharField(max_length=20)
    verb2 = models.CharField(max_length=50)
    verb3 = models.CharField(max_length=50)
    mean = models.TextField()
    

class Chemicals(models.Model):
    discoverer = models.CharField(max_length=100, null=True, blank=True)
    name_of_chemical = models.CharField(max_length=100)
    symbol_chemical = models.CharField(max_length=5)
    plase = models.CharField(max_length=10)
    category = models.TextField()
    block = models.CharField(max_length=2)
    period = models.IntegerField()
    group = models.CharField(max_length=5)
    configuration = models.TextField()
    electronegativity = models.FloatField(null=False, blank=True)
    oxidation = models.TextField(null=True, blank=True)
    atomic_mass = models.FloatField()
    density = models.FloatField(null=True, blank=True)
    boil_K = models.FloatField(null=True, blank=True)
    melt_K = models.FloatField(null=True, blank=True)
    appearance = models.TextField(null=True, blank=True)
    summary = models.TextField()
    image_URL = models.TextField()
    classify = models.CharField(max_length=15)
    other_classification = models.CharField(max_length=20, null=True)


class Category(models.Model): 
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Exam(models.Model): # bản đề thi
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='', blank=True)
    exam_class = models.IntegerField()
    content = models.CharField(max_length=150)
    semester = models.CharField(max_length=100)
    path_render = models.TextField(default="")
    content_path = models.TextField(default="")

    URL_PDF = models.TextField(default="")
    URL_File_word = models.TextField(null=False, blank=True)
    URL_image = models.TextField(default="")

    def __str__(self):
        return self.content


class History_ChatBot(models.Model):
    chat_id = models.CharField(max_length=32, primary_key=True, null=False, blank=False)
    filename = models.CharField(max_length=20, blank=False)
    userId = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='', blank=True)

