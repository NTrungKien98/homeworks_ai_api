from auth_firebase.views import *


def login_with_firebase(request):
       if not request.user.id:
              return render(request, "login_firebase.html")
       else:
              return redirect('/')

@csrf_exempt
def auth_firebase_login(request):
       email         = request.POST.get("email")
       provider      = request.POST.get("provider")
       username      = request.POST.get("username")
       token         = request.POST.get("token")
       firebase_res  = check_firebase_response(token)
       firebase_dict = json.loads(firebase_res)
       if "users" in firebase_dict:
              user   = firebase_dict["users"]
              if len(user)>0:
                     user_one = user[0]
                     if "phoneNumber" in user_one:
                            if user_one["phoneNumber"]==email:
                                   data = proceed_to_login(request, email, username, token, provider)
                                   return HttpResponse(data)
                            else:
                                   return HttpResponse("Invalid login request.")
                     else:
                            if email==user_one["email"]:
                                   provider1=user_one["providerUserInfo"][0]["providerId"]
                                   if user_one["emailVerified"]==1 or user_one["emailVerified"]==True or user_one["emailVerified"]=="True" or provider1=="facebook.com":
                                          data = proceed_to_login(request, email, username, token, provider)
                                          return HttpResponse(data)
                                   else:
                                          return HttpResponse("Please verify your email.")
                            else:
                                   return HttpResponse("Unknown Email User.")
       else:
              return HttpResponse("User not found")

@csrf_exempt
def login_with_username(request):
       email = request.POST.get("email")
       password = request.POST.get("password")
       users = User.objects.filter(email=email).exists()
       if users == True:
              username = User.objects.filter(email=email)[0].username
              users = authenticate(username=username, password=password)
              if users is not None:
                     user_one = User.objects.get(username=username)
                     user_one.backend='django.contrib.auth.backends.ModelBackend'
                     login(request, user_one)
                     return HttpResponse("Login Successfully.")
              else:
                     return HttpResponse("Wrong email or password.")
       else:
              return HttpResponse("There's no user using email: " + email)

def check_firebase_response(token):
       url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup"
       payload = 'key=AIzaSyCXVF7hzEkBASwk8F5LzjKhGAkEg_vxrw8&idToken='+token
       headers = {
              'Content-Type': 'application/x-www-form-urlencoded'
       }
       response = requests.request("POST", url, headers=headers, data=payload)
       return response.text

def proceed_to_login(request, email, username, token, provider):
       users = User.objects.filter(username=username).exists()

       if users == True:
              user_one = User.objects.get(username=username)
              user_one.backend='django.contrib.auth.backends.ModelBackend'
              login(request, user_one)
              return HttpResponse("Login Successfully.")
       else:
              user = User.objects.create_user(username=username, email=email, password=settings.SECRET_KEY)
              user_one = User.objects.get(username=username)
              user_one.backend = 'django.contrib.auth.backends.ModelBackend'
              login(request,user_one)
              return HttpResponse("User Created.")
