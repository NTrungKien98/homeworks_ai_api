from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer, CategorySerializer
from .models import Question, Category, Choice
from rest_framework.permissions import IsAuthenticated
from auth_firebase.authentication import FirebaseAuthentication
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate
from .forms import NewQuestionForm, NewCategoryForm, NewChoiceForm
from django.shortcuts import redirect
import openai
from .paginations import CustomPagination

from subprocess import Popen, PIPE
from rest_framework.decorators import action

openai.api_key = "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"

from auth_firebase.views_login.login import *
from auth_firebase.views_login.signup import *
from auth_firebase.views_data_manage import *
class QuestionAPIView(GenericAPIView):
       queryset = Question.objects.all()
       pagination_class = CustomPagination
       serializer_class = QuestionSerializer
       """This api will handle questions"""
       # permission_classes = [ IsAuthenticated ]
       """Here just add FirebaseAuthentication class in authentication_classes"""

       def get(self, request, id):
              self.pagination_class = CustomPagination
              queryset      = self.filter_queryset(self.queryset.filter(categories__id = id))
              page          = self.paginate_queryset(queryset)

              if page is not None:
                     serializer    = self.get_serializer(page, many=True)
                     return self.get_paginated_response(serializer.data)

              serializer    = self.get_serializer(queryset, many=True)

              return Response(serializer.data)


class CategoryAPIView(GenericAPIView):
       queryset = Category.objects.all()
       pagination_class = CustomPagination
       serializer_class = CategorySerializer

       def get(self, request, grade=None, subject=None, level=None):
              self.pagination_class = CustomPagination
              queryset      = self.filter_queryset(self.queryset.filter(     grade = grade,
                                                                             subject = subject,
                                                                             level = level
                                                                                    ))
              page          = self.paginate_queryset(queryset)

              if page is not None:
                     serializer    = self.get_serializer(page, many=True)
                     return self.get_paginated_response(serializer.data)

              serializer    = self.get_serializer(queryset, many=True)

              return Response(serializer.data)


@login_required(login_url='/login')
def home(request):
       categories    = Category.objects.all
       question      = Question.objects.all
       return render(request, 'home.html', {
              'question': question,
              'categories': categories
       })

@csrf_exempt
@login_required(login_url='/login')
def new_question(request):
       if request.user.is_authenticated:
              new_question_form = NewQuestionForm()
              # new_question_form.initial['user'] = request.user
              if request.method == "POST":
                     form = NewQuestionForm(request.POST)
                     if form.is_valid():
                            question = form.save()
                            return redirect('add_choices/' + str(question.id))
                     else:
                            return render(request, 'new_question.html', {'new_question_form': new_question_form})
              else:
                     return render(request, 'new_question.html', {'new_question_form': new_question_form})
       else:
              return redirect('/login')

def add_choices(request,id):
       question      = Question.objects.get(id = id)
       choices       = Choice.objects.filter(question_id = id)
       new_choice_form = NewChoiceForm()
       new_choice_form.initial['question'] = question
       if request.method == "POST":
              form = NewChoiceForm(request.POST)
              if form.is_valid():
                     form.save()
                     return redirect('/add_choices/' + str(id))
              else:
                     return render(request, 'add_choices.html', {'new_choice_form': new_choice_form, 'choices': choices})
       else:
              return render(request, 'add_choices.html', {'new_choice_form': new_choice_form, 'choices': choices})


@csrf_exempt
@login_required(login_url='/login')
def new_category(request):
       new_category_form = NewCategoryForm()
       if request.method == "POST":
              form = NewCategoryForm(request.POST)
              if form.is_valid():
                     form.save()
                     return redirect('/')
              else:
                     return render(request, 'new_category.html', {'new_category_form': new_category_form})
       else:
              return render(request, 'new_category.html', {'new_category_form': new_category_form})

@csrf_exempt
@login_required(login_url='/login')
def category_details(request, id):
       category = Category.objects.get(id= id)
       questions = category.questions
       return render(request, 'category_details.html', {'category': category, 'questions': questions})

@csrf_exempt
@login_required(login_url='/login')
def delete_question(request, id):
       if request.user.is_authenticated:
              Question.objects.filter(id=id).delete()
              return redirect('/')
       else:
              return redirect('/login')

@csrf_exempt
def chat(request):
       #        # Retrieve user input from the request
       # user_input = request.POST.get('message')
       # old_response = str(request.GET.get('reponse'))
       # # Call the ChatGPT API and get the model response
       # model_response = openai.Completion.create(
       #        engine='text-davinci-003',
       #        prompt=user_input,
       #        max_tokens=50,
       #        n=1,
       #        stop=None,
       #        temperature=0.7
       # )

       # # Extract the generated response from the model
       # response = model_response.choices[0].text.strip()
       # # response=''
       # # Return the response as JSON
       # # return JsonResponse({'response': response})
       # return render(request, 'chat.html', {'response': ( response)})
       return None
