import requests, json, os, threading
# import urllib.parse as urlParse

from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from ..Plugin import sschat, encodePython, Conversion
from ..models import Irregular_Verb, Eng_Dictionary, Chemicals, Exam, Q
from ..serializers import *

from django.core.mail import send_mail

# send_mail(
#     "Subject here",
#     '[link=http://localhost:8000/]Liên hệ với chúng tôi[/link]',
#     "smartstudy2023edu@gmail.com",
#     ["nthn300607@gmail.com"],
#     fail_silently=False,
# )

# Views
def home(req):
    if req.method == "GET":
        print(req.user)
        return render(req, 'home.html')
    

def SSChat(req):
    if req.method == "GET":
        return render(req, "Template/sschat.html")
    
    if req.method == "POST": #Post
        if req.POST.get("message"):
            message = req.POST["message"]
            resultResponse = sschat.generateResponse(message)
            if resultResponse:
                result_text = ""
                for part in resultResponse['candidates'][0]["content"]["parts"]:
                    result_text += part["text"]
                return JsonResponse({'reply': result_text})
            return JsonResponse({"message": "request failed !!"})
        

def Encode(req):
    if req.method == "GET":
        return render(req, 'Template/encode.html')
    
    if req.method == "POST":
        # config = Sundry.Json().load("SSApp/SmartStudy/Json/data.json")
        try:
            str_code = ''
            if req.POST.get('textCode'):
                str_code = req.POST['textCode']

            elif req.FILES.get('file'):
                _file = req.FILES['file']
                str_code = _file.read().decode('utf-8')

            if str_code != ' ' or str_code :
                content = encodePython(contentCodePython=str_code)
                
                #---------------------------api Github------------------------
                # headers = {
                #     "Accept": "application/vnd.github+json",
                #     "Authorization": f"token {config['Token_Github']}",
                #     "X-GitHub-Api-Version": '2022-11-28'
                # }
                # payload = {
                #     "description": "Here is your code",
                #     "public": True,
                #     "files": {
                #         'encode.py': {
                #             "content": content
                #         }
                #     }
                # }
                # response = requests.post(
                #     "https://api.github.com/gists", json=payload, headers=headers)

                # if response.status_code == 201:
                #     gist_id = response.json()["id"]
                #     url = f'https://gist.github.com/SmartStudy-ChatBot/{gist_id}'
                
                return render(req, 'Template/encode.html')
        except: 
            raise HttpResponseBadRequest('Lỗi người dùng nhập vào!!!', status=422)


def Math(req):
    if req.method == 'GET':
        return render(req, "Template/maintenance.html")


def Physics(req):
    if req.method == 'GET':
        return render(req, "Template/maintenance.html")
    

def EngDictionary_view(req):
    if req.method == 'GET':
        try:
            data = Eng_Dictionary.objects.all()
            if req.GET.get('word'):
                _input = req.GET['word']
                data = data.filter(word=_input.lower()).first()
                context = {
                    "word": _input,
                    "mean": data.mean
                }
                return JsonResponse(data=context, status=200)
            return render(req, "Template/eng_dictionary.html")
        
        except Exception as e:
            print(e)
            return render(req, "Template/eng_dictionary.html", status=500)
            

def trac_nghiem_view(req, endpoint=None):
    template_path = "Template/Subject-Test/" 
    if req.method == "GET":
        if endpoint != None:
            templates = {
            #   endpoint: html
                "mon-hoc": "subject.html",
                'kiem-tra-15-phut': 'quiz.html',
                # 'kiem-tra-giua-hoc-ki-1': "midterm_exam.html",
                'kiem-tra-hoc-ki-1': 'final_exam_1.html',
                'danh-gia-nang-luc': 'competency_test.html',
                'danh-gia-tu-duy': 'thinking_test.html',
            } 

            return render(request=req, 
                        template_name=f"{template_path}{templates[endpoint]}")
    
    return render(request=req, 
                  template_name=f"{template_path}subject_test.html")


    
def Python(req):
    if req.method == 'GET':
        return render(req, "Template/python.html")
    

def IrregularVerb(req):
    if req.method == 'GET':
        data = Irregular_Verb.objects.all()
        
        if req.GET.get('search'):
            _input = req.GET['search']

            # docs tại https://docs.djangoproject.com/en/5.0/topics/db/queries/
            data = Irregular_Verb.objects.filter(
                Q(verb1__contains=_input) | Q(verb2__contains=_input) |
                Q(verb3__contains=_input) | Q(mean__contains=_input)
            )
        context = {'words': data}
        return render(req, "Template/irregularVerb.html", context=context)


def Conversions(req):
    context = {}
    if req.method == 'POST':
        if req.POST.get('selected') and req.POST.get('input'):
            print(req.POST)
            selected = req.POST['selected']
            data_input = req.POST['input']
            result = eval(f'Conversion.{selected}("{data_input.strip()}")')
            context['result'] = result
            return JsonResponse(context)
    return render(req, "Template/conversion.html", context=context)
    

def Chemical(req):
    return render(req, "Template/chemical.html")


def Exam_view(req, endpoint=None, page=1):
    context = {}
    if req.method == 'GET':
        
        if not endpoint:
            if req.GET.get("show"): # người dùng ấn vào 1 đề thi bất kì
                data_exam = Exam.objects.get(content_path=req.GET["show"])
                context["exam"] = data_exam
                context["orther_article"] = Exam.objects.filter(
                    Q(path_render=data_exam.path_render)
                ).order_by('?')[:10] # lấy 10 đề thi liên quan
                return render(req, "Template\Exams\showE.html", context=context)
            
            elif req.GET.get("search"):
                _input = req.GET['search']
                context['search'] = f'search={_input}'
                if _input.isdigit():
                    data_exam = Exam.objects.filter(id=_input)
                else:
                    data_exam = Exam.objects.filter(content__icontains=_input)
            else: 
                return render(req, "Template\Exams\homeE.html", context=context)

        else:
            data_exam = Exam.objects.filter(path_render=endpoint)
        paginator = Paginator(data_exam, 20) #show mỗi page là 20 item
        page_number = req.GET.get("page") 
        try:
            pages = paginator.page(page_number)
        except PageNotAnInteger:
            # Nếu page_number không thuộc kiểu integer, trả về page đầu tiên
            pages = paginator.page(1)
        except EmptyPage:
            # Nếu page không có item nào, trả về page cuối cùng
            pages = paginator.page(paginator.num_pages)

        context['pages'] = pages

        return render(req, "Template\Exams\exam.html", context=context)
