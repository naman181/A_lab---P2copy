from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomUserLoginForm, ClassroomForm, TestForm, QuestionForm, GenqForm
from .models import CustomUser, Classroom, Topic, Message, Test, Question
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

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

#calander
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
    llm = CTransformers(model='model\llama-2-7b-chat.ggmlv3.q8_0.bin',
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
    return render(request,'classroomcopy.html',context)

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
    return render(request, 'classroomcopy.html', context)

from .forms import AnswerForm

@login_required(login_url='login')
def take_test(request, pk, test_id, question_index=1):
    # retrieve classroom, test, and questions
    classroom = Classroom.objects.get(id=pk)
    test = Test.objects.get(pk=test_id)
    questions = test.question_set.all().order_by('id')
    if request.method == 'POST':

        # Create AnswerForm instance and populate with POST data
        answer_form = AnswerForm(request.POST)
        print(request.POST)

        # Validate AnswerForm
        if answer_form.is_valid():
            # Process the submitted answer
            option_selected = answer_form.cleaned_data['option_selected']
            current_question_index = int(request.POST.get('current_question_index'))
            time_taken_str = request.POST.get('time_taken')
            time_taken = int(time_taken_str) if time_taken_str else 0

            # Save the answer to the database or perform other actions as needed

            # Determine the next question index
            next_question_index = current_question_index + 1

            # Redirect to the next question's URL if it exists
            if next_question_index <= questions.count():
                return redirect('take_test', pk=pk, test_id=test_id, question_index=next_question_index)
            else:
                # If it's the last question, redirect to the classroom or another desired URL
                return redirect('classroom', pk=pk)
        else:
            print("Answer form is invalid:", answer_form.errors)

    else:
        # Render the test-taking form for the current question
        if question_index <= questions.count():
            question = questions[question_index - 1]
            time_limit = test.time_limit_per_question

            return render(request, 'take_test.html', {
                'classroom': classroom,
                'test': test,
                'question': question,
                'time_limit': time_limit,
                'question_index': question_index,
                'answer_form': AnswerForm(),  # pass an instance of AnswerForm to the template
            })

    # If the request method is not POST or there are no more questions, render the classroom view
    return render(request, 'classroomcopy.html', {'classroom': classroom, 'tests': classroom.test_set.all().order_by('created')})



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