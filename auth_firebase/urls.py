from django.urls import path
from .views import *
urlpatterns = [
    path("api/questions", QuestionAPIView.as_view()),
    path("api/categories/<int:grade>/<int:subject>/<int:level>", CategoryAPIView.as_view()),
    path("login/", login_with_firebase, name="login_firebase"),
    path("auth_firebase_login", auth_firebase_login),
    path("login_with_username", login_with_username),
    path("", home),
    path("new_question", new_question, name='new_question'),
    path("add_choices/<int:id>", add_choices, name='add_choices'),
    path("new_category", new_category, name='new_category'),
    path("category_details/<int:id>", category_details, name='category_details'),
    path("delete_question/<int:id>", delete_question, name='delete_question'),
    path('chat/', chat, name='chat'),
    path('sign_up_with_username', sign_up_with_username),
  ]
