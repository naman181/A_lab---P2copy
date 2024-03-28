


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

<!-- <script>
 var startTime = new Date().getTime();
 var timer = setInterval(function () {
    var currentTime = new Date().getTime();
    var timeElapsed = Math.floor((currentTime - startTime) / 1000);
    var timeRemaining = {{ time_limit }} - timeElapsed;
    document.getElementById('time_remaining').innerText = timeRemaining;
    document.getElementById('time_taken').value = timeElapsed; // Update the time_taken value

    if (timeRemaining <= 0) {
      clearInterval(timer);
      document.forms[0].submit(); // Auto-submit the form when time runs out
    }
 }, 1000);
</script> -->