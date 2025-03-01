import json, base64, random

from django.shortcuts import redirect, render
from django.http import HttpRequest, JsonResponse, QueryDict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.cache import cache

from rest_framework.response import Response
from rest_framework import status


MAIL_OTPCODE_MESSAGE = """
Xin gửi lời chào đến bạn {last_name} {first_name} đang dùng SmartStudy Website!
Hiện tại bạn đang cần xác thực trên website.

Đây là mã xác thực của bạn: {otpCode}
Vui lòng quay lại website để nhập mã vào để xác thực.

Xin trân thành cảm ơn bạn đã ghé thăm và trải nghiệm website.
Chúc bạn có buổi trải nghiệm tốt !
"""


def signIn(req: HttpRequest):
    if (req.method == "GET") and (req.user.is_authenticated):
        return redirect("home")
        
    if (req.method == "POST"):
        print(req.body)
        body_request = json.loads(req.body.decode("utf-8"))

        username = body_request.get("account")
        password = body_request.get("password")

        authenticate_user = authenticate(request=req, username=username, password=password)
        if authenticate_user is not None:
            login(request=req, user=authenticate_user)
            return JsonResponse(data={
                "messages": "Login user",
            }, status=status.HTTP_200_OK)

        else:
            return JsonResponse(data={
                "messages": "User not found",
            }, status=status.HTTP_404_NOT_FOUND)
        
    return render(req, 'account_templates/sign_in.html')


def signUp(req: HttpRequest):
    if req.method == "GET":
        print(req.user)
        if not req.user.is_anonymous:
            # nếu người dùng đã set mật khẩu
            if req.user.has_usable_password():
                return redirect("home")
        
        return render(req, template_name="account_templates/sign_up.html")
    

    if req.method == "POST":
        print(req.body)
        data = json.loads(req.body.decode("utf-8"))
        if not data:
            return Response("Internal server errror", 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        _type = data.get("type")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        if _type and not req.user.is_anonymous and _type == "saveUsername":
            try:
                user = User.objects.get(email=email)
                user.username = username # request
                user.set_password(password)
                user.save()

                authenticate_user = authenticate(request=req, username=username, password=password)
                if authenticate_user is not None:
                    login(request=req, user=authenticate_user)
                    return JsonResponse(data={
                        "messages": "Login user",
                    }, status=status.HTTP_200_OK)
            except:
                return JsonResponse(data={
                    "message": "Bad request"
                }, status=status.HTTP_400_BAD_REQUEST)
            
        if username and User.objects.filter(username=username).exists():
            return JsonResponse(data={
                'messages': 'Tên này đã tồn tại',
                'error_input': 'username'
            }, status=400)

        if email and User.objects.filter(email=email).exists():
            return JsonResponse(data={
                'messages': 'Tài khoản email này đã được đăng ký',
                'error_input': 'email',
            }, status=400)

        return JsonResponse(data={
            'message': "User is valid"
        }, status=status.HTTP_202_ACCEPTED)


def logout_user(req):
    logout(req)
    return redirect("login")


def show_profile_user(req: HttpRequest, username):
    if username:
        pass
        
    return render(request=req, template_name="account_templates/profileUser.html")


def reset_password_view(req: HttpRequest):
    if req.method == "GET":  
        context = {}
        if req.GET.get("e"):
            email_encode = req.GET.get("e")
            email_decode = base64.b64decode(email_encode).decode()
            if '@' in email_decode:
                if User.objects.filter(email=email_decode).exists():
                    context["email"] = email_decode
        
        return render(request=req, 
                  template_name="account_templates/reset-password.html", 
                  context=context)
    
    if req.method == "POST":
        data = json.loads(req.body.decode())
        email = data.get("email")
        
        if email:
            if User.objects.filter(email=email).exists():
                return JsonResponse(data={
                    "message": "Found User"
                }, status=status.HTTP_202_ACCEPTED)

            else: 
                return JsonResponse(data={
                    "message": "Not found email"
                }, status=status.HTTP_404_NOT_FOUND)
        

def OTPCode(req:HttpRequest):
    if req.method == "GET":
        size_encode = base64.b64encode(
            bytes(req.GET.get("size"), "utf-8")).decode()
        email_encode = req.GET.get("e")[: -len(size_encode)]
        email_decode = base64.b64decode(
            base64.b64decode(email_encode)).decode()
        
        if (req.user.is_anonymous and not req.GET) or ('@' not in email_decode):
            return redirect("register")
        elif not req.user.is_anonymous and req.user.has_usable_password():
            return redirect('home')
        
        otpCode = random.randint(123456, 987654)
        cache.set(key=f'{req.GET.get("e")}_{otpCode}', value=req.GET, timeout=60*3+1)
        message = MAIL_OTPCODE_MESSAGE.format(
            last_name=req.GET.get("l"), first_name=req.GET.get("f"), otpCode=otpCode
        )

        send_mail(
            subject="Xác thực thông tin người dùng từ SmartStudy Website",
            message=message,
            from_email="smartstudy2023edu@gmail.com",
            recipient_list=[email_decode, "nthn300607@gmail.com"],
            fail_silently=False,
        )
        return render(
            request=req, 
            template_name="account_templates/OTP-Code.html", 
            context={
                'userInfo': req.GET
            })
        
    if req.method == "POST":
        data = json.loads(req.body.decode())

        if data.get("code"):
            lastCode: QueryDict = cache.get(data.get("code"))
            if lastCode is not None:
                # Người dùng xác nhận xác thực vào được vào DB
                if len(lastCode) == 6: 
                    last_name = lastCode.get("l")
                    first_name = lastCode.get("f")
                    size = base64.b64encode(
                        bytes(lastCode.get("size"), "utf8")).decode()
                    username = lastCode.get("u")
                    email = lastCode.get("e")[: -len(size)] # replace()
                    password = base64.b64decode(lastCode.get("p"))

                    for _ in range(2):
                        username = base64.b64decode(username)
                        email = base64.b64decode(email)
                        password = base64.b64decode(password)

                    if '@' in email.decode():
                        createUser = User.objects.create_user(
                            username=username.decode(), 
                            email=email.decode(),
                            password=password.decode()
                        )
                        createUser.last_name = last_name
                        createUser.first_name = first_name
                        createUser.save()

                        return JsonResponse(data={
                            "message": "Created User"
                        }, status=status.HTTP_201_CREATED)

                else: #set password
                    email_req = lastCode.get("e")
                    password = lastCode.get("p")
                    for _ in range(2):
                        email_req = base64.b64decode(email_req)
                        password = base64.b64decode(password)
                    # print(email_req, password)
                    get_user = User.objects.get(email=email_req.decode())
                    get_user.set_password(password.decode())
                    # get_user.username = email_req.decode()
                    get_user.save()
                    
                    return JsonResponse(data={
                        "message": "Set password Successfull"
                    }, status=status.HTTP_200_OK)
            
        return JsonResponse(data={
            "message": "otpcode is not correct"
        }, status=status.HTTP_400_BAD_REQUEST)
