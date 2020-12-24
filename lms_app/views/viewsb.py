from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Exists
from ..models import *
import bcrypt
import random

def index(request):
    return render(request, 'index.html')

# Login and Registration
def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user: 
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                # For future reference, we had to add the .id to the line above to make it work
                return redirect(f'/profile/{logged_user.id}')
            else:
                messages.error(request, "Incorrect password")
                request.session['type'] = "login"

        else:
            messages.error(request, "Email not found")
            request.session['type'] = "login"
    return redirect('/')


def signup(request):
    if request.method == "POST":

        errors = User.objects.basic_validator(request.POST)

        # Check to make sure email is not already in db
        duplicate = User.objects.filter(email=request.POST['email'])
        if duplicate:
            errors['registered'] = "A user account already exists with that email."

        if errors:
            for k, v in errors.items():
                messages.error(request, v)
            request.session['name'] = request.POST['name']
            request.session['email'] = request.POST['email']
            request.session['type'] = "signup"
            return redirect('/')

        #if no errors, add user to database
        pwdhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            password = pwdhash
        )
        # Remove entries from screen
        request.session.flush()
        request.session['user_id'] = User.objects.last().id
        return redirect(f'/profile/{request.session.user_id}')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

#profile test - feel free to delete
# def profile(request):
#     return render(request, 'profile.html')


# Quizzes
def take_quiz(request, course_id):
    if 'user_id' in request.session:
        # user submitted answers
        if request.method == "POST":
            # check answers on quiz and increment score
            score = 0
            # loop through questions/answers
            for num in range(1,6):
                # get correct answer id from question object in db
                # request.POST[qnum] is name of hidden tag in question
                # on form with value = {{question.id}}
                # access answer user chose: 'question_id':[chosen_answer_id]
                q_id = request.POST["q"+str(num)]
                this_question = Question.objects.get(id=q_id)

                # print("the id for the correct answer is " + str(this_question.correct_answer_id))
                correct_answer = this_question.correct_answer_id
                # print("what we get from POST is " + str(request.POST[f"{q_id}"]))

                # capture chosen answer for each question and save to session
                request.session[f"q" + str(num) + "chosen_answer"] = request.POST[f"{q_id}"]
                # save to session whether user selected correct or incorrect answer
                if str(request.POST[f"{q_id}"]) == str(correct_answer):
                    request.session[f'question'+str(num)] = "correct"
                    score += 1
                else:
                    request.session[f'question'+str(num)] = "wrong"

            # Create record of quiz results in database
            # print("at the end, score is " + str(score))
            this_record = User_Quiz_Record.objects.create(
                score = score,
            )
            this_record.course.add(course_id)
            this_record.users.add(request.session["user_id"])
            # print(this_record.__dict__)

            return redirect('/show_quiz_results')

        # GET request from course page
        else:
            this_course = Course.objects.get(id=course_id)
            # get and shuffle the five questions for this course
            # random.shuffle shuffles the list in place
            question_list = list(Question.objects.filter(course=this_course))
            random.shuffle(question_list)
            # create a list of dictionaries with questions and answers
            items = []
            # for each question, get and shuffle the answers
            q_num = 1
            for question in question_list:
                # create dictionary for that question 
                quiz_item = {
                    'q_num': q_num,
                    'q_num_key': 'q'+ str(q_num),
                    'q_id': question.id,
                    'q_content': question.content,
                }
                # add question to session for correct order retrieval on results page
                request.session[f'q'+str(q_num)] = question.id
                # get answers and shuffle them
                answer_list = list(Answer.objects.filter(question=question))
                random.shuffle(answer_list)
                # add answer choices to quiz item dictionary
                # add answer choices to session for correct order retrieval on results page
                count = 1
                for answer in answer_list:
                    quiz_item[f'answer'+str(count)+'_id'] = answer.id

                    request.session[f'q'+ str(q_num)+'ans'+ str(count)] = answer.id

                    # print("question = "+str(q_num)+"answer = "+str(count))

                    # print(request.session[f'q'+ str(q_num)+'ans'+ str(count)])

                    quiz_item[f'answer'+str(count)+'_content'] = answer.content
                    request.session[f'q'+ str(q_num)+'ans'+ str(count)+'_content'] = answer.content
                    # print("here is what the content looks like")
                    # print(request.session[f'q'+ str(q_num)+'ans'+ str(count)+'_content'])
                    count+=1
                items.append(quiz_item)
                q_num +=1
            # print("here is items")
            # print(items)
            context = {
                'course': this_course,
                'items': items,
            }
            return render(request, 'quiz_page.html', context)
    return redirect('/')

def show_quiz_results(request):
    # create a list of dictionaries with questions and answers
    # in order to recreate page in the same shuffled form
    items = []
    # for key, value in request.session.items():
        # print(key, value)
    # loop through questions/answers
    for num in range(1,6):
        # get question id from session
        this_question = Question.objects.get(id=request.session[f'q'+str(num)])
        # create dictionary for this quiz item
        quiz_item = {
            'q_num': num,
            'q_id': this_question.id,
            'q_content': this_question.content,
            'answer1': str(request.session[f'q'+ str(num)+'ans1']),
            'answer2': str(request.session[f'q'+ str(num)+'ans2']),
            'answer3': str(request.session[f'q'+ str(num)+'ans3']),
            'answer4': str(request.session[f'q'+ str(num)+'ans4']),
            'answer1content': request.session[f'q'+ str(num)+'ans1'+'_content'],
            'answer2content': request.session[f'q'+ str(num)+'ans2'+'_content'],
            'answer3content': request.session[f'q'+ str(num)+'ans3'+'_content'],
            'answer4content': request.session[f'q'+ str(num)+'ans4'+'_content'],
            'qchosenans': request.session[f'q' + str(num) + 'chosen_answer'],
            'evaluation': request.session[f'question'+str(num)]
        }
        # print(quiz_item["qchosenans"] +" "+ str(quiz_item["answer1"]))
        items.append(quiz_item)

    # get score
    this_user = User.objects.get(id=request.session["user_id"])
    this_quiz = this_question.course.records.filter(users=this_user).last()

    # print(this_quiz)
    # print(this_quiz.__dict__)
    # score = this_quiz.score
    context = {
        'items': items,
        'score': this_quiz.score
    }
    # print("the score is " + str(score))
    # print("here is the evaluation")
    # print(items[0]["evaluation"])

    return render(request, "quiz_results.html", context)

# Creating a quiz for the database for a specific course
# Questions and answers are random lorem ipsum
def create_random_quiz(request, course_id):
    # if request.method == "POST":
    # course_id = request.POST['course']
    questions = [
        "What lorem ipsum dolor sit amet, consectetur adipiscing elit?",
        "Who lorem ipsum dolor sit amet, consectetur adipiscing elit?",
        "Where lorem ipsum dolor sit amet, consectetur adipiscing elit?",
        "How lorem ipsum dolor sit amet, consectetur adipiscing elit?",
        "When lorem ipsum dolor sit amet, consectetur adipiscing elit?"
    ]
    random.shuffle(questions)
    # temporarily assign a correct_answer_id and then come back to update it
    for question in questions:
        item = Question(
            content = question,
            correct_answer_id = 2,
            course = Course.objects.get(id = course_id)
        )
        item.save()
        
        correct_answer_index = random.randint(1,4)
        a_num = 0
        for num in range(1,5):
            if num == correct_answer_index:
                correct_option = create_correct_answer()
                item.correct_answer_id = correct_option.id
                item.save()
            else:
                create_wrong_answer(a_num)
                a_num +=1
    return redirect(f"/take_quiz/{course_id}")
    # else:
    #     return render(request, "create_random_quiz.html", {"courses": Course.objects.all()})

def create_correct_answer():
    # Creating a correct answer
    correct_answers = [
        "Pick me!  I'm the right answer.",
        "Obviously the correct answer",
        "Pick me if you want to be right!",
        "I'm telling you: this is the correct answer.",
        "Hint: this is the correct answer!"
    ]

    correct_answer = Answer(
        content = random.choice(correct_answers),
        question = Question.objects.last()
    )
    correct_answer.save()
    # print(correct_answer.__dict__)
    return correct_answer

def create_wrong_answer(idx):
    # Creating a correct answer
    wrong_answers = [
        "An appealing but incorrect answer.",
        "Obviously NOT the correct answer",
        "Hint: this is an incorrect answer!"
    ]

    answer = Answer(
        content = wrong_answers[idx],
        question = Question.objects.last()
    )
    answer.save()
    # print(answer.__dict__)

    return answer

def create_quiz(request):
    # send list of courses that do not have quizzes yet
    # links to create random or real quizzes
    # need a way to edit quizzes at some point?

    # Get all questions from current quizzes
    questions = Question.objects.all()
    courses_with_questions = []
    # For each question, get the related course id and add to list
    for question in questions:
        if question.course.id not in courses_with_questions:
            courses_with_questions.append(question.course.id)

    # Query all courses and exclude those that have quizzes
    courses_without_quizzes = Course.objects.exclude(id__in=courses_with_questions)

    return render(request, "create_quiz.html", {"courses": courses_without_quizzes})

def create_real_quiz(request, course_id):
    # Submitted questions and answers to create a new quiz
    if request.method == "POST":
        # print(request.POST)
        for num in range(1,6):
            # create question; temporarily store fake correct answer id
            this_question = Question.objects.create(
                content = request.POST['q'+str(num)+'content'],
                correct_answer_id = 2,
                course = Course.objects.get(id=course_id)
            )

            # create answer objects
            # pick random answer to be correct (not always lowest id, for example)
            correct_answer_index = random.randint(1,4)
            # print("correct answer index" + str(correct_answer_index))
            a_num = 1
            for idx in range(1,5):
                # print(a_num)
                if idx == correct_answer_index:
                    # print("correct answer created")
                    # print('q'+str(num)+'correct')
                    correct_option = Answer.objects.create(
                        content = request.POST['q'+str(num)+'correct'],
                        question = this_question
                    )
                    # Fix question to have correct id for correct answer

                    this_question.correct_answer_id = correct_option.id
                    this_question.save()
                    # print("the correct answer id is now:")
                    # print(this_question.correct_answer_id)
                else:
                    # print("wrong answer created")
                    # print(request.POST['q'+str(num)+'wrong'+str(a_num)])
                    Answer.objects.create(
                        content = request.POST['q'+str(num)+'wrong'+str(a_num)],
                        question = this_question
                    )
                    a_num +=1
        return redirect(f"/take_quiz/{course_id}")

    # requested form for creating a new quiz
    else:
        context = {
            'question_numbers': [1,2,3,4,5],
            'course_id': course_id
        }
        return render(request, "create_real_quiz.html", context)

# def Lisa(request):
#     # this is for testing how f-strings, variables, and storing in session works

#     shuffled_question_list = [
#         {
#             'question.id': 1,
#             'question_content': "What do you think?"
#         },
#         {
#             'question.id': 2,
#             'question_content': "What do you know?"
#         },
#         {
#             'question.id': 3,
#             'question_content': "What do you want?"
#         }
#     ]
#     # create a list of dictionaries with questions and answers
#     questions = []
#     # for each question, get and shuffle the answers
#     q_num = 1
#     for question in shuffled_question_list:
#         # create dictionary for that question 
#         quiz_item = {
#             'question_num': q_num,
#             'question_id': question['question.id'],
#             'question_content': question['question_content'],
#         }
#         q_num +=1
#         # get answers and shuffle them
#         shuffled_answer_list = [
#             {
#                 'answer.id': 10,
#                 'answer_content': "this one is right!"
#             },
#                         {
#                 'answer.id': 11,
#                 'answer_content': "this one is not right!"
#             },
#                         {
#                 'answer.id': 12,
#                 'answer_content': "this one is wrong!"
#             }
#         ]
#         # add answer choices to quiz item dictionary 
#         count = 1
#         for answer in shuffled_answer_list:
#             quiz_item[f'answer'+str(count)+'_id'] = answer['answer.id'] 
#             request.session[f'q'+ str(q_num)+'ans'+ str(count)] = answer['answer.id']
#             quiz_item[f'answer'+str(count)+'content'] = answer['answer_content']
#             count+=1
#         questions.append(quiz_item)

#     print(questions)

#     context = {
#         'questions': questions,
#     }
#     return render(request, 'test.html', context)

# def grade(request):
#     print(request.POST)
#     for key, value in request.session.items():
#         print(key, request.session[key])
#     return redirect('/')