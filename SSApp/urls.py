from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from .views import *

endpoint_API = [
    path('api/eng-dictionary/', API_views.EnglishDict_ViewSet.as_view(), 
         name='api-englist-dictionary'),
    path('api/irregular-verb/', API_views.IrregularVerb_ViewSet.as_view()),
    path('api/exam/', API_views.Exam_ViewSet.as_view()),
    path('api/chemical/', API_views.Chemical_ViewSet.as_view(), name="Chemical API")
]

urls_account = [
    path('login/', view=account_views.signIn, name='login'),
    path('register/', account_views.signUp, name='register'),
    path('logout/', view=account_views.logout_user, name="logout"),
    path('acount/<username>/', account_views.show_profile_user, name="acount"),
    path('social-auth/', include('social_django.urls', namespace='social')),
]

endpoint_site = [
    path('', views.home, name="home"),
    
    path('encode/', views.Encode, name="encode"),
    path('math/', views.Math, name="math"),
    path('physics/', views.Physics, name="physics"),
    path('chemical/', views.Chemical, name="chemical"),
    path('eng-dict/', views.EngDictionary_view, name="eng_dict"),
    path('conversion/', views.Conversions, name="conversion"),

    path('exam/', views.Exam_view, name="exam"),
    path('exam/<str:endpoint>/', views.Exam_view, name="path exam"),

    path('sschat/', views.SSChat, name="SSChat"),
    path('irregular/', views.IrregularVerb, name="irregular"),
    path('python/', views.Python, name="python"),
]


urlpatterns: list = endpoint_API + endpoint_site + urls_account