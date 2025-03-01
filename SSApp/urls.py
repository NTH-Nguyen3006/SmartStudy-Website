from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from .views import *

endpoint_API = [
    path('api/eng-dictionary/', api_views.EnglishDict_ViewSet.as_view(), 
         name='api-englist-dictionary'),
    path('api/irregular-verb/', api_views.IrregularVerb_ViewSet.as_view()),
    path('api/exam/', api_views.Exam_ViewSet.as_view()),
    path('api/chemical/', api_views.Chemical_ViewSet.as_view(), name="Chemical API"),
]

endpoint_accounts = [
    path('login/', view=account_views.signIn, name='login'),
    path('register/', account_views.signUp, name='register'),
    path('logout/', view=account_views.logout_user, name="logout"),
    path('account/<username>/', account_views.show_profile_user, name="account-show"),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('reset-password/', account_views.reset_password_view, name="reset-password"),
    path('otp-code/', account_views.OTPCode, name="otp-code"),
]

endpoint_sites = [
    path('', views.home, name="home"),
    
    path('encode/', views.Encode, name="encode"),
    path('math/', views.Math, name="math"),
    path('physics/', views.Physics, name="physics"),
    path('chemical/', views.Chemical, name="chemical"),
    path('eng-dict/', views.EngDictionary_view, name="eng_dict"),
    
    path('trac-nghiem/', views.trac_nghiem_view, name="subject-test"),
    path('trac-nghiem/<str:endpoint>', views.trac_nghiem_view, name="subject-test endpoint"),

    path('conversion/', views.conversions, name="conversion"),

    path('exam/', views.Exam_view, name="exam"),
    path('exam/<str:endpoint>/', views.Exam_view, name="path exam"),

    path('sschat/', views.SSChat, name="SSChat"),
    path('sschat/<str:chatId>/', views.SSChat, name="SSChat"),

    path('irregular/', views.IrregularVerb, name="irregular"),
    path('python/', views.Python, name="python"),
]


urlpatterns: list = endpoint_API + endpoint_sites + endpoint_accounts