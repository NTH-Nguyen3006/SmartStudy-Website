from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views

endpoint_API = [
    path('api/eng-dictionary/', views.EnglishDict_ViewSet.as_view(), 
         name='api-englist-dictionary'),
    path('api/irregular-verb/', views.IrregularVerb_ViewSet.as_view()),
    path('api/exam/', views.Exam_ViewSet.as_view()),
    path('api/chemical/', views.Chemical_ViewSet.as_view(), name="Chemical API")
]
endpoint_website = [
    path('', views.home, name="home"),
    path('login/', view=views.signIn, name='login'),
    path('register/', views.signUp, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('social-auth/', include('social_django.urls', namespace='social')),

    path('encode/', views.Encode, name="encode"),
    path('math/', views.Math, name="math"),
    path('physics/', views.Physics, name="physics"),
    path('chemical/', views.Chemical, name="chemical"),
    path('eng-dict/', views.EngDictionary_view, name="eng_dict"),
    path('conversion/', views.Conversions, name="conversion"),

    path('sschat/', views.SSChat, name="SSChat"),

    path('exam/', views.Exam_view, name="exam"),
    path('exam/<str:endpoint>/', views.Exam_view, name="path exam"),

    path('irregular/', views.IrregularVerb, name="irregular"),
    path('python/', views.Python, name="python"),
]


urlpatterns: list = endpoint_API + endpoint_website