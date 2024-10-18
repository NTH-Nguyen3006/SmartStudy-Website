import json, base64, random
import django.utils.timezone as timezone

from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, JsonResponse, QueryDict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.middleware.csrf import get_token, _unmask_cipher_token
from django.utils.crypto import constant_time_compare
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

        username = body_request["account"]
        password = body_request["password"]

        authenticate_user = authenticate(request=req, username=username, password=password)

        if authenticate_user is not None:
            login(request=req, user=authenticate_user)
            return JsonResponse(data={
                "messages": "Login successfull",
            }, status=status.HTTP_200_OK)

        else:
            return JsonResponse(data={
                "messages": "User not found",
            }, status=status.HTTP_404_NOT_FOUND)
        
    return render(req, 'Account_Template/sign_in.html')


def signUp(req: HttpRequest):
    if req.method == "GET":
        print(req.user)
        if not req.user.is_anonymous:
            # nếu người dùng đã set mật khẩu
            if req.user.has_usable_password():
                return redirect("home")
            
        last_codeAuthenticate = cache.get("123456")
        if last_codeAuthenticate:
            print(last_codeAuthenticate)
            print(timezone.now() - last_codeAuthenticate < timezone.timedelta(minutes=3))

        # Người dùng xác nhận xác thực vào được vào DB
        if req.GET.get("code"): 
            code = req.GET.get("code")
            decode = base64.b64decode(code).decode("utf-8")
            data = json.loads(decode)

            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            verify_password = data.get("verify_password")
            first_name = data.get("first_name")
            last_name = data.get("last_name")

            user_data = User.objects.create_user(
                username=username, email=email, password=password)
            
            user_data.first_name = first_name
            user_data.last_name = last_name
            user_data.save()
            return redirect("login")
        
        return render(req, template_name="Account_Template/sign_up.html")
    

    if req.method == "POST":
        print(req.body)
        data = json.loads(req.body.decode("utf-8"))
        if not data:
            return Response("Internal server errror", 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        verify_password = data.get("verify_password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        if User.objects.filter(username=username).exists():
            return JsonResponse(data={
                'messages': 'Tên này đã được tồn tại',
                'error_input': 'username'
            }, status=400)

        if email and User.objects.filter(email=email).exists():
            return JsonResponse(data={
                'messages': 'Tài khoản email này đã được đăng ký',
                'error_input': 'email',
            }, status=400)
        
        if password and verify_password:
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

        if len(data) == 3:
            user_data = User.objects.get(username=req.user.get_username())
            user_data.username = username
            user_data.set_password(password)
            user_data.save()
            
        elif len(data) == 6:
            otpCode = random.randint(123456, 987654)
            cache.set(key=f'{email} {otpCode}', value=data, timeout=60*3+1)
            
            message = MAIL_OTPCODE_MESSAGE.format(
                username=username, email=email, last_name=last_name,
                first_name=first_name, otpCode=otpCode
            )
            print('send email.')
            send_mail(
                subject="Xác thực thông tin người dùng từ SmartStudy Website",
                message=message,
                from_email="smartstudy2023edu@gmail.com",
                recipient_list=["nthn300607@gmail.com"],
                fail_silently=False,
            )
            print("data" ,data)
            return JsonResponse(data={
                "redirect": "otp-code",
                "user": str(data),
            }, status=status.HTTP_200_OK)
            
        if data.get("code"):
            lastCode_value = cache.get(key=f'{data["user"]["email"]} {data["code"]}')
            if lastCode_value is not None:
                user_data = User.objects.create_user(
                    username=lastCode_value["user"]['username'], 
                    email=lastCode_value["user"]['email'], 
                    password=lastCode_value["user"]['password']
                )
            
                user_data.first_name = lastCode_value["user"]['first_name']
                user_data.last_name = lastCode_value["user"]['last_name']
                user_data.save()

                return JsonResponse(data={
                    "redirect": "/",
                    "message": "Created User"
                }, status=status.HTTP_201_CREATED)
            else: 
                return JsonResponse(data={
                    "message": "Expired code !",
                    "user": lastCode_value["user"]
                }, status=status.HTTP_400_BAD_REQUEST)

        return redirect("home")


def logout_user(req):
    logout(req)
    return redirect("login")


def show_profile_user(req: HttpRequest, username):
    if username:
        pass
        
    return render(request=req, template_name="Account_Template/profileUser.html")


def reset_password_view(req: HttpRequest):
    if req.method == "GET":  
        context = {}
        if req.GET.get("e"):
            email_encode = req.GET.get("e")
            email_decode = base64.b64decode(email_encode).decode()
            if '@' in email_decode:
                if User.objects.filter(email=email_decode).exists():
                    context["email"] = email_decode
                    
                else: 
                    context["error"] = "User does not exists"
                    return render(request=req, 
                        template_name="Account_Template/reset-password.html", 
                        context=context)
        
        return render(request=req, 
                  template_name="Account_Template/reset-password.html", 
                  context=context)
        
    
def OTPCode(req:HttpRequest):
    if req.method == "GET":
        if req.user.is_anonymous and not req.GET:
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
            recipient_list=["nthn300607@gmail.com"],
            fail_silently=False,
        )
        return render(
            request=req, 
            template_name="Account_Template/OTP-Code.html", 
            context={
                'userInfo': req.GET
            })
        
    if req.method == "POST":
        data = json.loads(req.body.decode())

        if data.get("code"): #and data.get("user"):
            lastCode: QueryDict = cache.get(data.get("code"))
            print(lastCode)
            if lastCode is not None:
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
                    print(email_req, password)
                    get_user = User.objects.get(email=email_req.decode())
                    get_user.set_password(password.decode())
                    get_user.username = email_req.decode()
                    get_user.save()
                    
                    return JsonResponse(data={
                        "message": "Set password Successfull"
                    }, status=status.HTTP_200_OK)
            
        return JsonResponse(data={
            "message": "otpcode is not correct"
        }, status=status.HTTP_400_BAD_REQUEST)
