from django import forms
from .models import Question, Category, Choice

class NewChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['title', 'isAnswer', 'question']
        widgets = {
                    'question': forms.HiddenInput(),
                   }

class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        list_answers = ((1, 1), (2, 2), (3, 3), (4, 4))
        fields = ['question']
        widgets = {
                    # 'user': forms.HiddenInput(),
                #    'the_answer': forms.CheckboxSelectMultiple(choices=list_answers)
                   }
        # title           = forms.CharField(label = 'Title', max_length=500, required=True)
        # answer1         = forms.CharField(label = 'Answer 1', max_length=500, required=True)
        # answer2         = forms.CharField(label = 'Answer 2', max_length=500, required=True)
        # answer3         = forms.CharField(label = 'Answer 3', max_length=500, required=True)
        # answer4         = forms.CharField(label = 'Answer 4', max_length=500, required=True)
        # the_answer      = forms.IntegerField(label = 'Choose the answer from 1 - 4', max_length = 100, required=True)
        # your_name       = forms.CharField (label = 'Your name', max_length = 100, required=True)
class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, question):
        return "%s" % question.question

class NewCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'grade','level', 'subject', 'questions']
        questions = CustomMMCF(
                                                    queryset=Question.objects.all(),
                                                    widget=forms.CheckboxSelectMultiple()
                                                    )

