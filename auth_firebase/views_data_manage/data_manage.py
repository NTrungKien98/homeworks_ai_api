from auth_firebase.views import *


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
