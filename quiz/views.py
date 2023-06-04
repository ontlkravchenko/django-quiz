from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import User, Quiz, Answers, UserHistory
import random
import json
import re
# Create your views here.


def generate_quiz(request):
    """
    Checks if user have not answered questions, if user answered all
    return error message with empty div.
    If user have unanswered questions, make it JSON format
    and give it to user
    """

    """
    TODO:
    Query all quiz and place their id's inside arrray
    then get random index from that array
    in theory problem is solved.
    """
    # Create array of questions ID
    quizArray = Quiz.objects.all()
    idsArr = []
    for index in quizArray:
        idsArr.append(index.id)
    # Create array of answered questions ID
    answeredArray = UserHistory.objects.get(user=request.user)
    answeredArray = answeredArray.answered.all()
    idsAnswered = []
    for answer in answeredArray:
        idsAnswered.append(answer.id)
    if len(idsAnswered) == len(idsArr):
        return JsonResponse({"error": "You answered all questions."})
    filteredArr = [x for x in idsArr if x not in idsAnswered]
    randomQuiz = filteredArr[random.choice(range(len(filteredArr)))]
    randomQuiz = Quiz.objects.get(id=randomQuiz)
    answers = Answers.objects.filter(quiz=randomQuiz)
    answers_json = []
    for i in range(answers.__len__()):
        answers_json.append({
            'answer': answers[i].answer,
            'is_correct': answers[i].is_correct,
            'id': answers[i].id
        })
    quiz_json = {
        "question": randomQuiz.question,
        "id": randomQuiz.id,
        "score": request.user.score,
        "answers": answers_json
    }
    data = {
        'quiz': quiz_json
    }
    return JsonResponse(data)


@login_required(login_url="login")
def index(request):
    return render(request, "quiz/index.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            return render(request, "quiz/login.html", {
                "message": "Invalid username or password"
            })
    return render(request, "quiz/login.html")


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if "" in (username, email, password, confirmation):
            return render(request, "quiz/register.html", {
                "message": "Do not change HTML of this page."
            })
        if password != confirmation:
            return render(request, "quiz/register.html", {
                "message": "Please check your passwords."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            history = UserHistory()
            history.user = user
            history.save()
            return redirect(login_view)
        except IntegrityError:
            return render(request, "quiz/register.html", {
                "message": "User is already exist."
            })
    return render(request, "quiz/register.html")


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect(login_view)


@login_required(login_url="login")
def create_quiz(request):
    return render(request, "quiz/create_quiz.html")


def check_answer(request):
    """
    Checks if answer is correct and give json response.
    """
    if request.method == 'PUT':
        data = json.loads(request.body)
        quizId = data['quizId']
        answerId = data['answerId']
        answer = Answers.objects.get(id=answerId)
        if answer.is_correct == True:
            return JsonResponse({"succes": "Answer is correct."})
        else:
            return JsonResponse({"message": "Answer is wrong."})


def change_score(request):
    """
    Takes true or false as argument from request
    and changes score to +1 or -1 respectively.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        is_correct = data['is_correct']
        quizId = data['quizId']
        print(f"FDSAKJFHASDKJFH {quizId}")
        user = User.objects.get(id=request.user.id)
        if is_correct:
            score = user.score + 1
            user.score = score
            user.save()
            history = UserHistory.objects.get(user=request.user)
            history.answered.add(Quiz.objects.get(id=quizId))
            history.save()
            return redirect(index)
        else:
            score = user.score - 1
            user.score = score
            user.save()
            return JsonResponse({
                "message": "Your score is changed.",
                "score": score,
            })


def create_quiz_api(request):
    if request.method == 'PUT':
        user = User.objects.get(id=request.user.id)
        data = json.loads(request.body)
        answers_json = data['answers']
        correctId = data['correct']
        quiz = Quiz()
        quiz.question = data['question']
        quiz.user = user
        quiz.save()
        # Creating answers
        for answer in answers_json:
            newAnswer = Answers()
            quizId = Quiz.objects.get(question=data['question'])
            newAnswer.quiz = quizId
            newAnswer.answer = answer
            if answers_json.index(answer) + 1 == correctId:
                newAnswer.is_correct = True
            newAnswer.save()
        return JsonResponse({
            "message": "Hey"
        })


def leaderboard(request):
    users = User.objects.all()
    context = {
        "users": users
    }
    return render(request, "quiz/leaderboard.html", context)


def profile_page(request, userId):
    try:
        user = User.objects.get(id=userId)
        questions = Quiz.objects.filter(user=user)
    except:
        return render(request, "quiz/404.html")
    context = {
        "user": user,
        "questions": questions
    }
    return render(request, "quiz/profile_page.html", context)
