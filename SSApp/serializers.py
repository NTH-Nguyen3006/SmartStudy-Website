from rest_framework.serializers import ModelSerializer
from .models import Eng_Dictionary, Irregular_Verb, Exam, Chemicals

class DictEnglish_Serializer(ModelSerializer):
    class Meta:
        model = Eng_Dictionary
        fields = ['word', 'mean']


class IrregularVerb_Serializer(ModelSerializer):
    class Meta:
        model = Irregular_Verb
        fields = ['verb1', 'verb2', 'verb3', 'mean']


class Exam_Serializer(ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class Chemical_Serializer(ModelSerializer):
    class Meta:
        model = Chemicals
        fields = '__all__'

