from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomUserLoginForm, ClassroomForm, TestForm, QuestionForm, AnswerForm
from .models import CustomUser, Classroom, Topic, Message, Test, Question,TestScore, TestAttempt, TestAttemptQuestion
from django.contrib import messages
from django.db import models


# Very first page of the Website before login or sign up
def landing_page(request):
    return render(request,'landingpage.html')

# login or sign up page
def login_signup_page(request):
    return render(request,'login_signup.html')

# Login Page
def login_page(request):
    if request.user.is_authenticated:
        if request.user.role == 'mentor':
            classrooms = Classroom.objects.all()
            context = {'classrooms': classrooms}
            print(classrooms)
            return render(request, 'dashboard_mentor.html',context)
        elif request.user.role == 'student':
            return render(request, 'dashboard_student.html')

    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.role == 'mentor':
                    return redirect('dashboard_mentor')
                elif request.user.role == 'student':
                    return redirect('dashboard_student')
            else:
                form.add_error(None, 'Invalid login credentials. Please try again.')
    else:
        form = CustomUserLoginForm()
    return render(request, 'login.html', {'form': form})

# Signup Page or registration page
def registrationPage(request):
    if request.user.is_authenticated:
        if request.user.role == 'mentor':
            return render(request, 'dashboard_mentor.html')
        elif request.user.role == 'student':
            return render(request, 'dashboard_student.html')

    if request.method == 'POST':    
        form = CustomUserCreationForm(request.POST)    
        if form.is_valid():        
            user = form.save()        
            user = authenticate(request, username=user.username, password=request.POST['password1'])        
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if request.user.role == 'mentor':
                return redirect('dashboard_mentor')
            elif request.user.role == 'student':
                return redirect('dashboard_student')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})
 
# Dashboard   
@login_required(login_url='login')
def dashboard(request):
    classrooms = Classroom.objects.all()
    if request.user.role == 'mentor':
        print(classrooms)
        context = {'classrooms': classrooms}
        # loads mentor dashboard
        return render(request, 'dashboard_mentor.html',context)

    elif request.user.role == 'student':
        context = {'classrooms': classrooms}
        # load student dashboard
        return render(request, 'dashboard_student.html',context)

# Classrooms
@login_required(login_url='login')
def classroom(request, pk):
    classroom = Classroom.objects.get(id=pk)
    classroom_messages = classroom.message_set.all().order_by('created')
    tests = classroom.test_set.all().order_by('created')
    participants = classroom.participants.all()
    # questions = test.question_set.all().order_by('id')
    test_data = []

    for test in tests:
        num_questions = test.question_set.count()  # Count the number of questions in each test
        test_data.append({'test': test, 'num_questions': num_questions})

    context = {'classroom': classroom, 
               'classroom_messages': classroom_messages,
               'participants': participants,
               'test_data':test_data,
               }
    return render(request,'classroom.html',context)

@login_required(login_url='login')
def test(request,pk):
    classroom = Classroom.object.get(id=pk)

# Creating a test
@login_required(login_url='login')
def create_test(request, classroom_id):
    classrooms = Classroom.objects.all()
    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            test = test_form.save(commit=False)
            test.classroom_id = classroom_id
            test.save()

            for i in range(1, 11):
                question_form = QuestionForm(request.POST, prefix=f'question_{i}')
                if question_form.is_valid():
                    question = question_form.save(commit=False)
                    question.test = test
                    question.save()
                else:

                    pass
            context = {'classrooms': classrooms}
            return render(request, 'dashboard_mentor.html',context)
            # return redirect('classroom')  # Adjust the URL name as needed
    else:
        test_form = TestForm()
        question_forms = [QuestionForm(prefix=f'question_{i}') for i in range(1, 11)]

    return render(request, 'create_test.html', {'test_form': test_form, 'question_forms': question_forms})

# Classroom Details
@login_required(login_url='login')
def classroom_detail(request, classroom_id):

    classroom = Classroom.objects.get(id=classroom_id)
    classroom_messages = classroom.message_set.all().order_by('created')
    tests = classroom.test_set.all().order_by('created')
    participants = classroom.participants.all()
    test_data = []

    for test in tests:
        # counts the number questions in each test
        num_questions = test.question_set.count()
        test_data.append({'test': test, 'num_questions': num_questions})
    
    context = {'classroom': classroom, 
               'classroom_messages': classroom_messages,
               'participants': participants,
               'test_data':test_data}
    return render(request, 'classroom.html', context)

from .forms import AnswerForm

# @login_required(login_url='login')
# def take_test(request, pk, test_id, question_index=1):
#     # retrieve classroom, test, and questions
#     classroom = Classroom.objects.get(id=pk)
#     test = Test.objects.get(pk=test_id)
#     questions = test.question_set.all().order_by('id')
#     if request.method == 'POST':

#         # Create AnswerForm instance and populate with POST data
#         answer_form = AnswerForm(request.POST)
#         print(request.POST)

#         # Validate AnswerForm
#         if answer_form.is_valid():
#             # Process the submitted answer
#             option_selected = answer_form.cleaned_data['option_selected']
#             current_question_index = int(request.POST.get('current_question_index'))
#             time_taken_str = request.POST.get('time_taken')
#             time_taken = int(time_taken_str) if time_taken_str else 0

#             # Save the answer to the database or perform other actions as needed

#             # Determine the next question index
#             next_question_index = current_question_index + 1

#             # Redirect to the next question's URL if it exists
#             if next_question_index <= questions.count():
#                 return redirect('take_test', pk=pk, test_id=test_id, question_index=next_question_index)
#             else:
#                 # If it's the last question, redirect to the classroom or another desired URL
#                 return redirect('classroom', pk=pk)
#         else:
#             print("Answer form is invalid:", answer_form.errors)

#     else:
#         # Render the test-taking form for the current question
#         if question_index <= questions.count():
#             question = questions[question_index - 1]
#             time_limit = test.time_limit_per_question

#             return render(request, 'take_test.html', {
#                 'classroom': classroom,
#                 'test': test,
#                 'question': question,
#                 'time_limit': time_limit,
#                 'question_index': question_index,
#                 'answer_form': AnswerForm(),  # pass an instance of AnswerForm to the template
#             })

#     # If the request method is not POST or there are no more questions, render the classroom view
#     return render(request, 'classroom.html', {'classroom': classroom, 'tests': classroom.test_set.all().order_by('created')})

@login_required(login_url='login')
def take_test(request, pk, test_id, question_index=1):
    classroom = Classroom.objects.get(id=pk)
    test = Test.objects.get(pk=test_id)
    questions = test.question_set.all().order_by('id')

    if request.method == 'POST':
        option_selected = request.POST.get('option_selected')
        current_question_index = int(request.POST.get('current_question_index'))
        time_taken_str = request.POST.get('time_taken')
        time_taken = int(time_taken_str) if time_taken_str else 0

        if option_selected:
            test_attempt = TestAttempt.objects.create(
                student=request.user,
                test=test,
                start_time=datetime.fromisoformat(request.session['test_start_time']),
                end_time=timezone.now()
            )

            TestAttemptQuestion.objects.create(
                test_attempt=test_attempt,
                question=questions[current_question_index - 1], # Get the current question
                chosen_option=option_selected,
                time_taken=time_taken
            )

            next_question_index = current_question_index + 1
            if next_question_index <= questions.count():
                return redirect('take_test', pk=pk, test_id=test_id, question_index=next_question_index)
            else:
                test_score = calculate_and_redirect_score(request, test, request.user, classroom)
                messages.success(request, f'You have completed the test with a score of {test_score}!')
                return redirect('classroom', pk=pk)
        else:
            messages.error(request, 'Please select an option before submitting your answer.')

    else:
        if question_index <= questions.count():
            question = questions[question_index - 1]
            time_limit = test.time_limit_per_question
            request.session['test_start_time'] = timezone.now().isoformat()
            return render(request, 'take_test.html', {
                'classroom': classroom,
                'test': test,
                'question': question,
                'time_limit': time_limit,
                'question_index': question_index,
            })

    return render(request, 'classroom.html', {'classroom': classroom, 'tests': classroom.test_set.all().order_by('created')})

def calculate_and_redirect_score(request, test, student, classroom):
    try:
        test_score = TestScore.objects.get(student=request.user, test=test)
        messages.warning(request, 'You have already completed this test.')
    except TestScore.DoesNotExist:
        test_attempts = TestAttempt.objects.filter(test=test, student=request.user)
        total_questions = test.question_set.count()
        correct_answers = 0
        for attempt in test_attempts:
            questions_attempted = TestAttemptQuestion.objects.filter(test_attempt=attempt)
            for question_attempt in questions_attempted:
                if question_attempt.chosen_option == question_attempt.question.correct_option:
                    correct_answers += 1

        score = (correct_answers / total_questions) * 100
        TestScore.objects.create(
            student=request.user,
            test=test,
            score=score
        )
        messages.success(request, f'You have completed the test with a score of {score}!')
        return score

# def calculate_and_redirect_score(request, test, student, classroom):
#     test_attempts = TestAttempt.objects.filter(test=test, student=student)
#     total_questions = test_attempts.count()
#     correct_answers = 0
#     for attempt in test_attempts:
#         questions_attempted = TestAttemptQuestion.objects.filter(test_attempt=attempt)
#         for question_attempt in questions_attempted:
#             if question_attempt.chosen_option == question_attempt.question.correct_option:
#                 correct_answers += 1

#     score = (correct_answers / total_questions) * 100
#     TestScore.objects.create(
#         student=student,
#         test=test,
#         score=score
#     )
#     messages.success(request, f'You have completed the test with a score of {score}!')

# def calculate_score(test, student):
#     # Get all test attempts by the student for the given test
#     test_attempts = TestAttempt.objects.filter(test=test, student=student)

#     # Calculate the score based on correct and incorrect answers
#     total_questions = test_attempts.count()
#     # correct_answers = test_attempts.filter(selected_option=models.F('question__correct_option')).count()
#     correct_answers = test_attempts.filter(chosen_option=models.F('question__correct_option')).count()

#     score = (correct_answers / total_questions) * 100

#     # Save the score to the database
#     TestScore.objects.create(
#         student=student,
#         test=test,
#         score=score
#     )

#     return score


# To create a new classroom
@login_required(login_url='login')
def createClassroom(request):
    form = ClassroomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topics_name = request.POST.get('topic')
        topic,creates = Topic.objects.get_or_create(name = topics_name)
        Classroom.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('dashboard_mentor')
    context = {'form': form,'topics': topics}
    return render(request, 'classroom_form.html',context)

#  logout the user
def logout_page(request):
    logout(request)
    return render(request, 'logout.html')