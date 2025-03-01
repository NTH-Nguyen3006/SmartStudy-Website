from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..plugin import sschat, encodePython
from ..models import Irregular_Verb, Eng_Dictionary, Chemicals, Exam, Q

# Views
def home(req):
    if req.method == "GET":
        return render(req, 'home.html')
    

def SSChat(req:HttpRequest, chatId=None):
    if req.method == "GET":
        if chatId:
            history = sschat.get_history_message(chatId=chat_id)
            
        return render(req, "template/sschat.html")
    
    if req.method == "POST": #Post
        if req.POST.get("message") or req.POST.get("base64_file"):
            message = req.POST.get("message", None)
            chat_id = req.POST.get("chat_id", None)
            base64_file = req.POST.get("file", None)
            mimeType = req.POST.get("mimetype", None)
            prompt = req.POST.get("prompt", None)
            history_chat = req.POST.get("history", None)
            username = None
            # print(req.POST.dict())

            if not req.user.is_anonymous: # đã đăng nhập
                username = req.user.username
            
            if prompt and history_chat:
                sschat.save_contentsGenAI_to_database(
                    username=req.user.username, history=history_chat)
             
            genAI_response = sschat.send_message(
                userMessage=message, kwargs=req.POST.dict()) # {"base64_file": "akljefwwkn vjwieuryoiuyakjdh"}
            return JsonResponse(
                {"reply": genAI_response},
            )


def Math(req):
    if req.method == 'GET':
        return render(req, "template/math.html")


def Physics(req):
    if req.method == 'GET':
        return render(req, "template/physics.html")
    

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
            return render(req, "template/eng_dictionary.html")
        
        except Exception as e:
            print(e)
            return render(req, "template/eng_dictionary.html", status=500)
            

def trac_nghiem_view(req, endpoint=None):
    template_path = "template/subject-test/" 
    if req.method == "GET":
        # if endpoint != None:
        #     templates = {
        #     #   endpoint: html
        #         "mon-hoc": "subject.html",
        #         'kiem-tra-15-phut': 'quiz.html',
        #         # 'kiem-tra-giua-hoc-ki-1': "midterm_exam.html",
        #         'kiem-tra-hoc-ki-1': 'final_exam_1.html',
        #         'danh-gia-nang-luc': 'competency_test.html',
        #         'danh-gia-tu-duy': 'thinking_test.html',
        #     } 

        #     return render(request=req, 
        #                 template_name=f"{template_path}{templates[endpoint]}")
    
        return render(request=req, 
                    template_name="template/subject-test/subject.html")

    
def Python(req):
    if req.method == 'GET':
        return render(req, "template/python.html")


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
        return render(req, "template/irregularVerb.html", context=context)
 

def Chemical(req):
    return render(req, "template/chemical.html")


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
                return render(req, "template/exams/showE.html", context=context)
            
            elif req.GET.get("search"):
                _input = req.GET['search']
                context['search'] = f'search={_input}'
                if _input.isdigit():
                    data_exam = Exam.objects.filter(id=_input)
                else:
                    data_exam = Exam.objects.filter(content__icontains=_input)
            else: 
                return render(req, r"template/exams/homeE.html", context=context)

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

        return render(req, "template/exams/exams.html", context=context)


def Encode(req):
    if req.method == "GET":
        return render(req, 'template/encode.html')
    
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
                
                return render(req, 'template/encode.html')
        except: 
            raise HttpResponseBadRequest('Lỗi người dùng nhập vào!!!', status=422)    

def conversions(req):
    context = {}
    if req.method == 'POST':
        if req.POST.get('selected') and req.POST.get('input'):
            print(req.POST)
            selected = req.POST['selected']
            data_input = req.POST['input']
            result = eval(f'conversion.{selected}("{data_input.strip()}")')
            context['result'] = result
            return JsonResponse(context)
    return render(req, "template/conversion.html", context=context)