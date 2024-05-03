from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Classroom, Test, Question

class CustomUserCreationForm(UserCreationForm):

    ROLE_CHOICES = [
        ("student", "Student"),
        ("mentor", "Mentor"),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial="student")
    
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "role")

class CustomUserLoginForm(forms.Form):
    username = forms.CharField(max_length=40, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class CustomUserChangeForm(UserChangeForm):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("mentor", "Mentor"),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial="student")
    class Meta:
        model = CustomUser
        fields = ("email", "username","password", "role")
 
class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = "__all__"
        exclude = ['host','participants']

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'start_time', 'end_time']

class GenqForm(forms.Form):
    input_text = forms.CharField(widget=forms.Textarea)
    subject = forms.CharField()
    que_type = forms.ChoiceField(choices=[
        ('Objective', 'Objective'),
        ('Subjective', 'Subjective'),
        ('Numerical', 'Numerical')
    ])
    no_que = forms.IntegerField()

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
        time_taken = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)

class AnswerForm(forms.Form):
    option_selected = forms.ChoiceField(choices=[('option_a', 'Option A'), ('option_b', 'Option B'), ('option_c', 'Option C'), ('option_d', 'Option D')])
