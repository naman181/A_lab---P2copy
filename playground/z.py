@login_required(login_url='login')
def take_test(request, pk, test_id, question_index=1):
    # retrieve classroom, test, and questions
    classroom = Classroom.objects.get(id=pk)
    test = Test.objects.get(pk=test_id)
    questions = test.question_set.all().order_by('id')

    if request.method == 'POST':

        # Create AnswerForm instance and populate with POST data
        answer_form = AnswerForm(request.POST)

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
    return render(request, 'classroom.html', {'classroom': classroom, 'tests': classroom.test_set.all().order_by('created')})



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

# @login_required(login_url='login')
# def test(equest, pk, test_id):
#     classroom = Classroom.object.get(id=pk)
#     test = Test.objects.get(pk=test_id)
#     if request.method == 'GET':
