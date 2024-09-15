import threading, requests, json, os
import urllib.parse as urlParse

from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from rest_framework import viewsets, status
from rest_framework.views import APIView 
from rest_framework.response import Response
from .utils import send_mail_to_user


# from .fbchat import listen
from .Handle import sschat
# from .SmartStudy import centre, Sundry
# from .SmartStudy.Plugin import EncodePython, Conversion
from .models import Irregular_Verb, Eng_Dictionary, Chemicals, Exam, Q
from .serializers import *

#create API
class EnglishDict_ViewSet(APIView): 
    def get(self, req):
        try:
            data = Eng_Dictionary.objects.all()
            if req.query_params.get('word'):
                word = req.query_params['word']
                data = data.get(word=word)
                return Response(
                    DictEnglish_Serializer(data, many=False).data,
                    status=status.HTTP_200_OK)
                
        except:
            return JsonResponse(
                {"message": "word does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST)
        

class IrregularVerb_ViewSet(APIView):
    def get(self, req):
        try:
            data = Irregular_Verb.objects.all()
            many = True
            if req.query_params.get('verb'):
                data = data.filter(
                    Q(verb1=req.query_params['verb']) | 
                    Q(verb2__icontains=req.query_params['verb']) | 
                    Q(verb3__icontains=req.query_params['verb'])
                )[0]
                many = False

            serializer = IrregularVerb_Serializer(data, many=many)
            return Response(
                serializer.data, 
                status=status.HTTP_200_OK)
            
        except:
            return Response(
                {"message": "word does not exists"},
                status=status.HTTP_400_BAD_REQUEST)


class Exam_ViewSet(APIView):
    def get(self, req):
        try:
            data_exam = Exam.objects.all()
            if len(req.data) > 0:
                args = ''
                for key, value in req.data.items():
                    if value.isdigit():
                        args += f'{key}={value}, '
                    else:
                        args += f'{key}__icontains="{value}", '
                
                data_exam = eval(f'data_exam.filter({args[:-2]})') 
                
            serializer = Exam_Serializer(data_exam, many=True, 
                                         context={'request': req})
            return Response(data=serializer.data, 
                            status=status.HTTP_200_OK)

        except Exception as e:
            # print(e)
            return Response({'message': "ValueError"},
                            status=status.HTTP_400_BAD_REQUEST)


class Chemical_ViewSet(APIView):
    def get(self, req):
        try:
            data = Chemicals.objects.all()
            if req.GET.get("element"):
                print(req.GET["element"])
                element = data.get(symbol_chemical=req.GET["element"].capitalize())
                seria = Chemical_Serializer(element, many=False)
                print(seria.data)

                return Response(data=seria.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': "ValueError"},
                            status=status.HTTP_400_BAD_REQUEST)


def home(req):
    if req.method == "GET":
        print(req.user)
        return render(req, 'home.html')
    

def signIn(req):
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")

    return render(req, 'sign_in.html')


def signUp(req: HttpRequest):
    if req.method == "GET":
        print(req.user)
        print(req.GET)
        if req.user.is_anonymous:
            redirect("register")
        else:
            context = {'is_register': False}
        
            if req.GET.get("register"):
                context = {'is_register': True}
        print(context)
        return render(req, template_name="sign_up.html")
    
    if req.method == "POST":
        print(req.GET)
        print(req.POST)

        print(req.body )
        data = json.loads(req.body.decode("utf-8"))

        username = data.get("username")
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")
        verify_password = data.get("verify_password")
        
    
        if User.objects.filter(username=username).exists():
            # messages.error(req, "Tên tài khoản này đã tồn tại!")
            return JsonResponse(data={
                'messages': 'Tên này đã được tồn tại',
                'error_input': 'username'
            }, status=400)

        if User.objects.filter(email=email).exists():
            # messages.error(req, "Tài khoản email này đã tồn tại.")
            return JsonResponse(data={
                'messages': 'Tài khoản email này đã được đăng ký',
                'error_input': 'email',
            }, status=400)
        
        if password != verify_password:
            return JsonResponse(data={
                'messages': 'Mật khẩu xác nhận không trùng khớp',
                'error_input': 'verify_password',
            }, status=400)
        
        if len(password) < 8 or len(password) > 20 :
            return JsonResponse(data={
                'messages': 'Mật khẩu chỉ được nằm trong phạm vi 8 đến 20 kí tự',
                'error_input': 'password',
            }, status=400)

        user = User.objects.create_user(
            username=username, email=email, password=password)
        
        user.first_name = first_name
        user.last_name = last_name
        

        user.save()
        
        # send_mail_to_user(email)
        messages.success(req, "Tạo tài khoản thành công")

        return redirect("login")
    # return render(req, "sign_up.html")




def SSChat(req):
    if req.method == "GET":
        return render(req, "Template/sschat.html")
    
    else: #Post
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
    
#     if req.method == "GET":
#         return render(req, 'Template/encode.html')
    
#     if req.method == "POST":
#         # config = Sundry.Json().load("SSApp/SmartStudy/Json/data.json")
#         try:
#             str_code = ''
#             if req.POST.get('textCode'):
#                 str_code = req.POST['textCode']

#             elif req.FILES.get('file'):
#                 _file = req.FILES['file']
#                 str_code = _file.read().decode('utf-8')

#             if str_code != ' ' or str_code :
#                 content = EncodePython(contentCodePython=str_code)
                
#                 #---------------------------api Github------------------------
#                 headers = {
#                     "Accept": "application/vnd.github+json",
#                     "Authorization": f"token {config['Token_Github']}",
#                     "X-GitHub-Api-Version": '2022-11-28'
#                 }
#                 payload = {
#                     "description": "Here is your code",
#                     "public": True,
#                     "files": {
#                         'encode.py': {
#                             "content": content
#                         }
#                     }
#                 }
#                 response = requests.post(
#                     "https://api.github.com/gists", json=payload, headers=headers)

#                 if response.status_code == 201:
#                     gist_id = response.json()["id"]
#                     url = f'https://gist.github.com/SmartStudy-ChatBot/{gist_id}'
                
#                 return render(req, 'Template/encode.html', context={'url': url})
#         except: 
#             raise HttpResponseBadRequest('Lỗi người dùng nhập vào!!!', status=422)
    pass


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
                data = data.get(word=_input.lower())
                context = {
                    "word": _input,
                    "mean": data.mean
                }
                return JsonResponse(data=context, status=200)
            return render(req, "Template/eng_dictionary.html")
        
        except Exception as e:
            print(e)
            return render(req, "Template/eng_dictionary.html", status=500)
            
    
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
