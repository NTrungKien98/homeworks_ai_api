from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer, CategorySerializer, UploadSerializer
from .models import Question, Category, Choice
from rest_framework.permissions import IsAuthenticated
from auth_firebase.authentication import FirebaseAuthentication
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate
from .forms import NewQuestionForm, NewCategoryForm, NewChoiceForm
from django.shortcuts import redirect
from .paginations import CustomPagination, CustomPaginationWithFile
from subprocess import Popen, PIPE
from rest_framework.decorators import action
from io import BytesIO

import requests
import json
import openai
openai.api_key = "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"

from auth_firebase.viewses.views_login.login import login_with_firebase, auth_firebase_login, login_with_username, check_firebase_response, proceed_to_login
from auth_firebase.viewses.views_login.signup import sign_up_with_username
from auth_firebase.viewses.views_data_manage.data_manage import home, add_choices, new_question, new_category, category_details, delete_question, chat

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
       serializer_classes = CategorySerializer

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

class FileUploadView(ViewSet, GenericAPIView):
       pagination_class = CustomPagination
       serializer_class = UploadSerializer

       def list(self, request):
              return Response("GET API")

       def create(self, request):
              file_uploaded = request.FILES.get('file_uploaded')
              f = BytesIO(file_uploaded.read())
              f = open(f, 'r')

              if file_uploaded is not None:
                     self.serializer_class = QuestionSerializer
                     self.queryset = Question.objects.all()
                     self.pagination_class = CustomPaginationWithFile
                     queryset      = self.filter_queryset(self.queryset.filter(categories__id = 1))
                     page          = self.paginate_queryset(queryset)

                     if page is not None:
                            serializer    = self.get_serializer(page, many=True)
                            self.serializer_class = UploadSerializer
                            return self.get_paginated_response(serializer.data)

                     serializer    = self.get_serializer(queryset, many=True)
                     self.serializer_class = UploadSerializer
                     return Response(serializer.data)

                     # content_type = file_uploaded.content_type
                     # response = "POST API and you have uploaded a {} file".format(content_type)
                     # return redirect('/api/questions/1')
              else:
                     response = "Not accepted files."
                     return Response(response)
