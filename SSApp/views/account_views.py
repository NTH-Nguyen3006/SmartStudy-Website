import json

from django.shortcuts import redirect, render
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from requests import Response
from rest_framework import status


def signIn(req: HttpRequest):
    if (req.method == "GET") and (req.user.is_authenticated):
        return redirect("home")
    
    if req.method == "POST":
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
        
    

    return render(req, 'sign_in.html')


def signUp(req: HttpRequest):
    if req.method == "GET":
        print(req.user)
        if not req.user.is_anonymous:
            if req.user.has_usable_password():
                return redirect("/")
        
        return render(req, template_name="sign_up.html")
    
    if req.method == "POST":
        print(req.body)
        data = json.loads(req.body.decode("utf-8"))
        if not data:
            return Response("Internal server errror", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            user_data = User.objects.create_user(
                username=username, email=email, password=password)
            
            user_data.first_name = first_name
            user_data.last_name = last_name
            user_data.save()
        
        # send_mail_to_user(email)

        return redirect("login")
    # return render(req, "sign_up.html")


def logout_user(req):
    logout(req)
    return redirect("login")


def show_profile_user(req: HttpRequest, username):
    if username:
        pass
        
    return render(request=req, template_name="profileUser.html")