from rest_framework import serializers
from .models import Question, Category, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['title', 'isAnswer']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    class Meta:
            model = Question
            fields = ['question', 'choices']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True)
    class Meta:
            model = Category
            fields = ['name', 'grade', 'level', 'subject', 'questions']
