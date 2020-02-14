# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages

# imports for user system
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# local imports
from icm.models import Submission, Question
from informatics_competition_manager import settings
from icm.helper_functions import competition_active, only_user_type, competition_only, get_score

# imports from standard libraries
import os
import shutil
import subprocess
import time

# Veiw scores
@only_user_type()
@competition_only()
def score_list(request, competition):
    # Get users and questions in the competition
    comp_users = User.objects.filter(type__compname=competition.name)
    comp_questions = competition.questions

    # Get the name and score of each user
    users = []
    for user in comp_users:
        users.append((user.username, get_score(user, competition)))

    # Sort users (negitive key so it is sored in decending)
    users = sorted(users, key=lambda x: -x[1])

    return render(request, "competition/scores.html", {"users":users, "competition":competition})

# Competition page function for when users are granted acces to the page
def competition_page(request, competition):
    # Get questions and question data
    questions = competition.questions.all()
    f = lambda q: q.name
    questions = sorted(map(f, questions))

    # Render with questions and compeition title
    if request.user.type.usertype == "C":
        return render(request, "competition/competition.html", {"compname":competition.name, "questions":questions, "score": get_score(request.user, competition), "competitor": True})
    else:
        return render(request, "competition/competition.html", {"compname":competition.name, "questions":questions})

# Main competition page
@login_required
def competition(request):
    # Check competition running
    competition = competition_active()
    if competition:
        # POST or GET
        if request.method == "POST":
            # Get user data
            compname = request.POST["compname"]

            # Check if correct competition name
            if compname.replace(" ", "") == competition.name.replace(" ", ""):
                # Update user model
                request.user.type.compname = compname
                request.user.type.save()

                # Return competition page with success message
                messages.success(request, "Correct competition name")
                return competition_page(request, competition)
            else:
                # Return enter competition page with error message
                return render(request, "competition/entercomp.html", {"error": "Incorrect competition name"})
        else:
            # Check usertype
            if request.user.type.usertype == "C":
                # Check if competition name is correct
                if request.user.type.compname == competition.name:
                    # Return competition page
                    return competition_page(request, competition)
                else:
                    # Render enter competition page
                    return render(request, "competition/entercomp.html")
            else:
                # Return competition page
                return competition_page(request, competition)
    else:
        # Redirect to index
        return HttpResponseRedirect("/index/")

# Competition question page
@competition_only()
def comp_question_page(request, competition, title):
    # Get question
    question = get_object_or_404(Question.objects.all(), name=title)

    # Check if question is part of competition
    if question not in competition.questions.all():
        return HttpResponseRedirect("/comp/")

    # Get context
    context = {}
    context["compname"] = competition.name
    context["title"] = title
    context["description"] = question.description
    context["usertype"] = request.user.type.usertype
    context["score"] = get_score(request.user, competition)

    # render page
    return render(request, "competition/compquestion.html", context=context)

def run_code(code, testcases, scoreing_method, testcase_time):
    # Get testcase information
    inps = testcases[0]
    outs = testcases[1]
    weights = testcases[2]

    # Check if cpp file
    if code.name[-4:] != ".cpp":
        return "Not .cpp file, upload file with .cpp extention"

    # Copy file to runcode directory
    oldfilepath = os.path.join(settings.BASE_DIR, code.name)
    filepath = os.path.join(settings.BASE_DIR, "runcode\\program.cpp")
    shutil.copy(oldfilepath, filepath)

    # Compile code
    try:
        subprocess.check_output("g++ -o program program.cpp --std=c++11", cwd=os.path.join(settings.BASE_DIR, "runcode"), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        return "Compiler error:\n" + e.output

    scores = []
    numberPassed = 0

    # test each test case
    for i in range(len(inps)):
        # setup input file and output file
        inpfile = open(os.path.join(settings.BASE_DIR, "runcode\\input.txt"), "w")
        inpfile.write(inps[i])
        inpfile.close()

        prog_out_file = open(os.path.join(settings.BASE_DIR, "runcode\\input.txt"), "r")

        outfile = open(os.path.join(settings.BASE_DIR, "runcode\\output.txt"), "w")
        outfile.close()

        # Run the code
        runningcode = subprocess.Popen(os.path.join(settings.BASE_DIR, "runcode\\program.exe"), cwd=os.path.join(settings.BASE_DIR, "runcode"))
        time.sleep(testcase_time)

        if runningcode.poll() is None:
            # Code took too long
            runningcode.kill()
            scores.append(0)
            continue

        # Get user output
        prog_out_file = open(os.path.join(settings.BASE_DIR, "runcode\\output.txt"), "r")
        prog_out = prog_out_file.read()

        # Compare output with expected
        if prog_out == outs[i]:
            scores.append(weights[i])
            numberPassed += 1
        else:
            scores.append(0)

    # Sum scores based on scoreing method
    if scoreing_method == "=":
        return sum(scores), numberPassed, sum(weights)
    elif scoreing_method == "%":
        maxscore = sum(weights)
        return int(100 * (sum(scores) / float(maxscore))), numberPassed, 100
    elif scoreing_method == "s":
        score = sum(scores)
        return score * score, numberPassed, sum(weights)*sum(weights)
    elif scoreing_method == "S":
        maxscore = sum(weights)
        score = int(100 * (sum(scores) / float(maxscore)))
        return score*score, numberPassed, 10000
    else:
        return int(maxscore == sum(scores)), numberPassed, 1

# Results for submission
@only_user_type("C", HttpResponseRedirect("/comp/"))
@competition_only()
def result(request, competition, title):
    # Get submission data
    user = request.user
    question = get_object_or_404(Question, name=title)
    submission = request.FILES["upload"]

    # Make submission object to save file
    s = Submission()
    s.user = user
    s.competition = competition
    s.question = question
    s.score = 0
    s.submission = submission
    s.save()

    # get testcase details
    testcases = question.testcase_set.all()
    outputs = map(lambda tc: tc.testoutput, testcases)
    inputs = map(lambda tc: tc.testinput, testcases)
    weightings = map(lambda tc: tc.weighting, testcases)
    scoreing_method = competition.scoringtype
    timetorun = question.timetorun

    # Run code
    code = s.submission
    graded = run_code(code, (inputs, outputs, weightings), scoreing_method, timetorun)

    # Get context
    context = {"questiontitle": title}

    # Check if error
    if type(graded) == unicode:
        # add error message to context
        context["error"] = graded
    else:
        # Add score
        context["success"] = True
        context["passed"] = graded[1]
        context["numtestcases"] = len(inputs)
        context["score"] = graded[0]
        context["maxmarks"] = graded[2]

        # Update submission
        s.score = graded[0]
        s.save()

    # Add score to context
    context["totalscore"] = get_score(user, competition)

    # render
    return render(request, "competition/result.html", context)
