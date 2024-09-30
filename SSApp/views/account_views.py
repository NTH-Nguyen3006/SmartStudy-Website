import json, base64, random
import django.utils.timezone as timezone

from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.middleware.csrf import get_token, _unmask_cipher_token
from django.utils.crypto import constant_time_compare
from django.core.cache import cache

from requests import Response
from rest_framework import status


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
        last_codeAuthenticate = cache.get("123456")
        print(last_codeAuthenticate)
        if last_codeAuthenticate:
            print(timezone.now() - last_codeAuthenticate < timezone.timedelta(hours=1))
        if not req.user.is_anonymous:
            # nếu người dùng đã set mật khẩu
            if req.user.has_usable_password():
                return redirect("/")
        
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
            # messages.error(req, "Tên tài khoản này đã tồn tại!")
            return JsonResponse(data={
                'messages': 'Tên này đã được tồn tại',
                'error_input': 'username'
            }, status=400)

        if email and User.objects.filter(email=email).exists():
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

        if len(data) == 3:
            user_data = User.objects.get(username=req.user.get_username())
            user_data.username = username
            user_data.set_password(password)
            user_data.save()
            
        elif len(data) == 6:
            encode = base64.b64encode(req.body).decode('utf-8')
            urlSS = f"http://localhost:8000/register/?code={encode}"
            codeAuthenticate = random.randint(123456, 987654)
            cache.set(f"{codeAuthenticate}", timezone.now(), 60*3)

            message = f"""
Xin gửi lời chào đến người dùng SmartStudy Website!
Hiện tại bạn đang xác thực bạn là người dùng trên website. Bạn đã đăng ký với các thông tin sau:
- Tên đăng nhập: {username}
- Email của bạn : {email}
- Họ: {last_name}
- Tên: {first_name}
Xin vui lòng ấn vào url để xác thực: {urlSS}.
Đây là mã xác thực của bạn. {codeAuthenticate}

Xin trân thành cảm ơn bạn đã ghé thăm và trải nghiệm website lần đầu tiên.
Chúc bạn có buổi trải nghiệm tốt.
"""
            send_mail(
                subject="Xác thực thông tin người dùng từ SmartStudy Website",
                message=message,
                from_email="smartstudy2023edu@gmail.com",
                recipient_list=["nthn300607@gmail.com"],
                fail_silently=False,
            )

        return redirect("register")
    # return render(req, "sign_up.html")


def logout_user(req):
    logout(req)
    return redirect("login")


def show_profile_user(req: HttpRequest, username):
    if username:
        pass
        
    return render(request=req, template_name="Account_Template/profileUser.html")


def reset_password_view(req: HttpRequest):
    context = {}
    print(req.body)
    if req.method == "GET":        
        if req.GET.get("code"):
            code = req.GET.get("code")
            decode = base64.b64decode(code).decode()
            email = json.loads(decode).get("email")
            
            if User.objects.filter(email=email).exists():
                context["email"] = email
        
    if req.body and req.method == "POST":
        csrf_cookie = req.COOKIES.get('csrftoken')
        print(csrf_cookie)
        request = json.loads(req.body.decode())

        if request.get("email", None):
            try: 
                email = request.get("email")
                
                encode = base64.b64encode(req.body).decode()
                urlSS = f"http://localhost:8000/reset-password/?code={encode}"

                message = f"""
Xin chào người dùng đang trải nghiệm Smart-Study Website!!!
Hiện tại tôi thấy bạn đang có yêu cầu đặt lại mật khẩu cho tài khoản của bạn trên Smart-Study Website.
Truy cập vào URL: {urlSS}
"""             
                print('send_mail')
                send_mail(
                    subject="YÊU CẦU THAY ĐỔI MẬT KHẨU TÀI KHOẢN BẠN",
                    message=message,
                    from_email="smartstudy2023edu@gmail.com",
                    recipient_list=["nthn300607@gmail.com"],
                    fail_silently=False,
                )
                return JsonResponse(
                    {"message": "email sent successfully"}, 
                    status=status.HTTP_201_CREATED)

            except: 
                return JsonResponse(
                    {"message": "email sent fail"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if request.get("email", None) and request.get("password", None): 
            mail = request.get("password")
            password = request.get("password")
            print(email, password)
            user = User.objects.filter(email=mail).first()
            print(user)
            # user.set_password(password)
            # user.save()
            return JsonResponse(
                    {"message": "Set password successful !!"}, 
                    status=status.HTTP_205_RESET_CONTENT)

    return render(request=req, 
                  template_name="Account_Template/reset-password.html", 
                  context=context)