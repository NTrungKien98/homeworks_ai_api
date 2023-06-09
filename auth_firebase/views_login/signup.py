from auth_firebase.views import *
from .login import *
@csrf_exempt
def sign_up_with_username(request):
       email = request.POST.get("email")
       password = request.POST.get("passswordsignup")
       re_password = request.POST.get("re_passswordsignup")
       username = request.POST.get("username")
       if re_password!=password:
              return HttpResponse("Passwords doesn't matched.")
       if not User.objects.filter(email=email).exists() and not User.objects.filter(username=username).exists():
              user = User.objects.create_user(username=username, email=email, password=password)
              user_one = User.objects.get(username=username)
              user_one.backend = 'django.contrib.auth.backends.ModelBackend'
              login(request,user_one)
              return HttpResponse("User Created.")
       elif User.objects.filter(username=username).exists():
              return HttpResponse("Username's taken.")
       else:
              return HttpResponse("Email's taken.")
