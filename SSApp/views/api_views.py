import requests, datetime, base64

from django.http import HttpRequest, JsonResponse

from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.response import Response

from SSApp.models import Chemicals, Eng_Dictionary, Exam, Irregular_Verb
from SSApp.serializers import *
from ..models import Irregular_Verb, Eng_Dictionary, Chemicals, Exam, Q


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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def post(self, req):
        try:
            # code to try
            data = Eng_Dictionary.objects.all()
            if req.data.get("word"):
                word = req.data['word']
                data = data.get(word=word)
                return Response(
                    DictEnglish_Serializer(data, many=False).data,
                    status=status.HTTP_200_OK)
        
        except:
            return JsonResponse(
                {"message": "word does not exists"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
                
        


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

    def post(self, req: HttpRequest):
        seria = Exam_Serializer()
        print(req.POST)
        print(req.FILES)
        _file = req.FILES.get("file", None)
        image = req.FILES.get("image", None)
        content = req.POST.get("content", None)
        _class = req.POST.get("content", None)

        if _file and image:
            if (_file.content_type == "application/pdf" and 
                image.content_type.startswith == "image"):
                
                pass
        
        # if seria.is_valid():
        #     # seria.save()
        #     print(seria)
        #     return Response(seria.data, status=status.HTTP_201_CREATED)

        return Response("ok", status=status.HTTP_400_BAD_REQUEST)


class Chemical_ViewSet(APIView):
    def get(self, req):
        try:
            data = Chemicals.objects.all()
            if req.GET.get("element"):
                element = data.get(symbol_chemical=req.GET["element"].capitalize())
                seria = Chemical_Serializer(element, many=False)

                return Response(data=seria.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': "ValueError"},
                            status=status.HTTP_400_BAD_REQUEST)
        

