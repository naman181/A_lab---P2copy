from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomUserLoginForm, ClassroomForm, TestForm, QuestionForm, AnswerForm
from .models import CustomUser, Classroom, Topic, Message, Test, Question,TestScore, TestAttempt, TestAttemptQuestion
from django.contrib import messages
from django.db import models
from django.db.models import Count, Sum, Avg
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
from time import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomUserLoginForm, ClassroomForm, TestForm, QuestionForm, GenqForm
from .models import CustomUser, Classroom, Topic, Message, Test, Question
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
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
from django.db.models import Count, Sum, Avg
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.template.loader import get_template
from django.template import Context
from xhtml2pdf import pisa
from .models import TestAttemptQuestion

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
 
#Contactus
def contact_page(request):
    return render(request,'contact.html')

#Faqs
def faqs_page(request):
    return render(request,'faqs.html')

#learnmore
def learnmore_page(request):
    return render(request,'learnmore.html')

#notification
def notification_page(request):
    return render(request,'notification.html')

#profile
def profile_page(request):
    return render(request,'profile.html')

#settings
def settings_page(request):
    return render(request,'settings.html')

#history
def history_page(request):
    return render(request,'history.html')

#calander
def calander_page(request):
    return render(request,'calander.html')



def qresult_page(request):
    return render(request,'result.html')

#genquestion
def genq_page(request):
    if request.method == "POST":
        form = GenqForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data.get('input_text')
            no_que = int(form.cleaned_data.get('no_que'))
            subject = form.cleaned_data.get('subject')
            que_type = form.cleaned_data.get('que_type')

            responses = get_lama_response(input_text, subject, no_que, que_type)

            return render(request, 'result.html', {'responses': responses})
    else:
        form = GenqForm()
    return render(request, 'gen.html', {'form': form})

def generate(request):
    input_text = request.form['input_text']
    no_que = int(request.form['no_que'])
    subject = request.form['subject']
    que_type = request.form['que_type']

    # Call the function to generate responses
    responses = get_lama_response(input_text, subject, no_que, que_type)

    # Save the generated questions to an Excel file
    # save_to_excel(responses)

    return render('result.html', responses=responses)


def get_lama_response(input_text, subject, no_que, que_type, max_token_length=512):
    llm = CTransformers(model='/Users/mohit/Documents/GitHub/ALAB/playground/model/llama-2-7b-chat.ggmlv3.q8_0.bin',
                        model_type='llama',
                        config={'max_new_tokens': 256, 'temperature': 0.1})

    template = """
        Generate {no_que} {que_type} questions and four options including correct answer on 
        subject/topic {subject} for the given topics: {input_text} in format
        question: Question?
        option a: ...
        option b: ...c
        option c: ...
        option d: ...
        correct Answer: ... 
        """

    prompt = PromptTemplate(input_variables=["no_que", "que_type", "subject", "input_text"],
                            template=template)

    # Split input text into chunks
    chunks = [input_text[i:i+max_token_length] for i in range(0, len(input_text), max_token_length)]

    responses = []
    for chunk in chunks:
        response = llm(prompt.format(no_que=no_que, que_type=que_type, subject=subject, input_text=chunk))
        responses.append(response)

    return responses

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
    test_scores = TestScore.objects.filter(student=request.user)
    # questions = test.question_set.all().order_by('id')
    test_data = []

    for test in tests:
        num_questions = test.question_set.count()  # Count the number of questions in each test
        test_data.append({'test': test, 'num_questions': num_questions})
        
    # calculate average score
    total_tests = test_scores.count()
    total_score = test_scores.aggregate(total=Sum('score'))['total'] or 0
    average_score = total_score / total_tests if total_tests > 0 else 0

    # calculating average time taken for a particular question
    average_time_per_question = TestAttemptQuestion.objects.filter(
        test_attempt__student=request.user
    ).aggregate(average_time=Avg('time_taken'))['average_time'] or 0

    print(average_time_per_question)

    # data visualization
    test_titles = [score.test.title for score in test_scores]
    test_scores_values = [score.score for score in test_scores]

    # pie chart
    # plt.figure(figsize=(8, 3))
    # # plt.legend(loc="upper center", bbox_to_anchor=(1, 0.5), title="Test Titles")
    # plt.pie(test_scores_values, labels=test_titles, autopct='%1.1f%%')
    # plt.title('Test Scores Distribution')
    # plt.axis('equal')


    # # convert plot to bytes and embed in HTML
    # buffer = BytesIO()
    # plt.savefig(buffer, format='png')
    # buffer.seek(0)
    # image_base64 = base64.b64encode(buffer.getvalue()).decode()
    # plt.close()

    # pie_chart = f'data:image/png;base64,{image_base64}'
    
    context = {'classroom': classroom, 
               'classroom_messages': classroom_messages,
               'participants': participants,
               'test_data':test_data,
               'tests': tests,
               'test_scores': test_scores,
               'average_score': average_score,
               'average_time_per_question': average_time_per_question,
            #    'pie_chart': pie_chart,
               }
    return render(request,'classroom.html',context)


# creating a test
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
    return render(request, 'classroomcopy.html', context)

@login_required(login_url='login')
def show_test(request, pk, test_id):
    classroom = Classroom.objects.get(id=pk)
    test = Test.objects.get(pk=test_id)
    
    if request.method == 'GET':
        test_data = [{'test': test, 'num_questions': test.question_set.count()}]
        return render(request, 'test_component.html', {'classroom': classroom, 'test_data': test_data})
    else:
        return redirect('classroom', pk=pk)


@login_required(login_url='login')
def take_test(request, pk, test_id, question_index):
    classroom = Classroom.objects.get(id=pk)
    test = Test.objects.get(pk=test_id)
    questions = test.question_set.all().order_by('id')

    if request.method == 'POST':
        option_selected = request.POST.get('option_selected')
        current_question_index = int(request.POST.get('current_question_index'))
        time_taken_str = request.POST.get('time_taken')
        time_taken = int(time_taken_str) if time_taken_str else 0

        if True:
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
            time_limit = 5
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

@login_required(login_url='login')
def student_report(request, classroom_id, student_id):

    print("hello1")
    student = User.objects.get(id=student_id)
    classroom = Classroom.objects.get(id=classroom_id)
    print("hello")
    test_scores = TestScore.objects.filter(student=student, test__classroom=classroom)

    # Extract test names and scores for plotting
    test_names = [score.test.title for score in test_scores]
    scores = [score.score for score in test_scores]

    # Generate pie chart
    # plt.figure(figsize=(8, 8))
    # plt.pie(scores, labels=test_names, autopct='%1.1f%%')
    # plt.title('Test Scores')
    # plt.savefig('test_scores_pie_chart.png')

    # # Generate bar chart
    # plt.figure(figsize=(10, 6))
    # plt.bar(test_names, scores, color='skyblue')
    # plt.xlabel('Tests')
    # plt.ylabel('Scores')
    # plt.title('Test Scores')
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.savefig('test_scores_bar_chart.png')

    context = {
        'student': student,
        'classroom': classroom,
        'test_scores': test_scores,
    }
    return render(request, 'student_report.html', context)


from django.db.models import Prefetch
from collections import defaultdict

def test_report(request, test_id):
    # Retrieve test details and questions
    print("View called")
    test = Test.objects.get(pk=test_id)
    questions = test.question_set.all().order_by('id')

    # Retrieve test attempt questions for the current user
    test_attempt_questions = TestAttemptQuestion.objects.filter(
        test_attempt__test=test,
        test_attempt__student=request.user
    ).prefetch_related(
        Prefetch('test_attempt', queryset=TestAttempt.objects.select_related('test'))
    )

    # Prepare data for template
    question_data = []
    for question in questions:
        attempts = test_attempt_questions.filter(question=question)
        if attempts:
            first_attempt = attempts.first()
            # Check if the chosen option matches the correct option
            is_correct = first_attempt.chosen_option == question.correct_option
            question_data.append({
                'question': question,
                'time_taken': first_attempt.time_taken,
                'chosen_option': first_attempt.chosen_option,
                'is_correct': is_correct, # Add this field to indicate correctness
            })
        else:
            question_data.append({
                'question': question,
                'time_taken': 'N/A',
                'chosen_option': 'N/A',
                'is_correct': False, # Assume incorrect if no attempt
            })

    # Generate context for template
    context = {
        'test': test,
        'question_data': question_data,
    }

    return render(request, 'test_report.html', context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def download_test_report_pdf(request, test_id):
    # Retrieve test details and questions
    test = Test.objects.get(pk=test_id)
    questions = test.question_set.all().order_by('id')

    # Retrieve test attempt questions for the current user
    test_attempt_questions = TestAttemptQuestion.objects.filter(
        test_attempt__test=test,
        test_attempt__student=request.user
    ).prefetch_related(
        Prefetch('test_attempt', queryset=TestAttempt.objects.select_related('test'))
    )

    # Prepare data for template
    question_data = []
    for question in questions:
        attempts = test_attempt_questions.filter(question=question)
        if attempts:
            first_attempt = attempts.first()
            # Check if the chosen option matches the correct option
            is_correct = first_attempt.chosen_option == question.correct_option
            question_data.append({
                'question': question,
                'time_taken': first_attempt.time_taken,
                'chosen_option': first_attempt.chosen_option,
                'is_correct': is_correct, # Add this field to indicate correctness
            })
        else:
            question_data.append({
                'question': question,
                'time_taken': 'N/A',
                'chosen_option': 'N/A',
                'is_correct': False, # Assume incorrect if no attempt
            })

    # Generate context for template
    context = {
        'test': test,
        'question_data': question_data,
    }

    # Render the PDF using the dedicated PDF template
    pdf = render_to_pdf('test_report_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f'test_report_{test_id}.pdf'
        content = f'attachment; filename="{filename}"'
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

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

