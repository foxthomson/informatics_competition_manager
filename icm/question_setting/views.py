# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages

# imports for user system
from django.contrib.auth.decorators import login_required

# local imports
from icm.models import Question, TestCase

# imports from standard libraries
import re

# Make qustion
@login_required
def question(request):
    if request.user.type.usertype == "C":
        # If user is a competitor (not question setter or admin) the redirect
        # them to the index with message saying they are not allowed to access the page
        messages.error(request, "Access denied")
        return HttpResponseRedirect("/index/")

    # POST or GET
    if request.method == "POST":
        # Get name, description and time to run
        questionname = request.POST["name"]
        description = request.POST["description"]
        timetorun = request.POST["time"]

        # Make question with name and description
        question = Question(name=questionname, description=description, timetorun=timetorun, author=request.user.username)
        question.save()

        # Work out number of testcases
        # Make list of keys in for inp then a number
        inp_re = re.compile(r'^inp(\d+)')
        inps = filter(inp_re.match, request.POST.keys())

        # Length of list is number of testcases
        for i in range(1, len(inps)+1):
            # For each testcase make a testcase object
            testinput = request.POST["inp" + str(i)]
            testoutput = request.POST["out" + str(i)]
            weighting = int(request.POST["weight" + str(i)])

            tc = TestCase(question=question, testinput=testinput,
                          testoutput=testoutput, weighting=weighting)
            tc.save()

        # Redirect to the index and add success message
        messages.success(request, "Question created")
        return HttpResponseRedirect("/index/")
    else:
        # GET: render question page
        return render(request, "question_setting/question.html", {})

# User qustion list
@login_required
def user_question_list(request):
    if request.user.type.usertype == "C":
        # If user is a competitor (not question setter or admin) the redirect
        # them to the index with message saying they are not allowed to access the page
        messages.error(request, "Access denied")
        return HttpResponseRedirect("/index/")

    # Get questions
    questions = Question.objects.filter(author=request.user.username)

    # Get the title of each question
    questions = map(lambda q: q.name, questions)

    # Render questions page with list of questions
    return render(request, "question_setting/questionlist.html", {"question_list": questions})

# User edit question
@login_required
def user_edit_question(request, title):
    if request.user.type.usertype == "C":
        # If user is a competitor (not question setter or admin) the redirect
        # them to the index with message saying they are not allowed to access the page
        messages.error(request, "Access denied")
        return HttpResponseRedirect("/index/")

    # Try to get question, if the question does not exist then return a 404 error
    question = get_object_or_404(Question.objects.all(), name=title)

    # Check if question is created by user
    if question.author != request.user.username:
        messages.error(request, "Access denied")
        return HttpResponseRedirect("/questions/")

    # POST or GET
    if request.method == "POST":
        # Get question data
        title = request.POST["title"]
        description = request.POST["description"]
        time = request.POST["time"]

        # Update database
        question.delete()
        question = Question()
        question.name = title
        question.description = description
        question.timetorun = time
        question.author = request.user.username
        question.save()

        messages.success(request, "Question saved")
        return HttpResponseRedirect("/questions/")
    else:
        context = {"title": title,
                   "question": question.description,
                   "time": question.timetorun}
        return render(request, "question_setting/editquestion.html", context)

# Edit testcases
@login_required
def user_edit_testcases(request, title):
    if request.user.type.usertype == "C":
        # If user is a competitor (not question setter or admin) the redirect
        # them to the index with message saying they are not allowed to access the page
        messages.error(request, "Access denied")
        return HttpResponseRedirect("/index/")

    # Try to get question, if the question does not exist then return a 404 error
    question = get_object_or_404(Question.objects.all(), name=title)

    # Check if question is created by user
    if question.author != request.user.username:
        messages.error(request, "Access denied")
        return HttpResponseRedirect("/questions/")

    # POST or GET
    if request.method == "POST":
        # Delete testcases
        for testcase in TestCase.objects.filter(question=question):
            testcase.delete()

        # Work out number of testcases
        # Make list of keys in for inp then a number
        inp_re = re.compile(r'^inp(\d+)')
        inps = filter(inp_re.match, request.POST.keys())

        # Length of list is number of testcases
        for i in range(1, len(inps)+1):
            # For each testcase make a testcase object
            testinput = request.POST["inp" + str(i)]
            testoutput = request.POST["out" + str(i)]
            weighting = int(request.POST["weight" + str(i)])

            tc = TestCase(question=question, testinput=testinput,
                          testoutput=testoutput, weighting=weighting)
            tc.save()

        messages.success(request, "Testcases saved")
        return HttpResponseRedirect("/questions")
    else:
        # Function to convert testcase
        f = lambda tc: (tc.testinput, tc.testoutput, tc.weighting)
        context = {"title": title,
                   "testcases": map(f, TestCase.objects.filter(question=question))}
        return render(request, "question_setting/testcases.html", context)
