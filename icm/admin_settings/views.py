# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages

# imports for user system
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# local imports
from icm.models import Type, Question, TestCase, Competition, Submission
from icm.helper_functions import competition_active, only_user_type

# imports from standard libraries
import re
import datetime

# Admin settings
@only_user_type()
def admin_settings(request):
    # Render admin settings page
    return render(request, "admin/admin.html", {})

# New user
@only_user_type()
def new_user(request):
    # POST or GET
    if request.method == "POST":
        # Get data from request
        username = request.POST["username"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        usertype = request.POST["usertype"]

        # Error checking
        # Check if valid username
        if len(username) > 150:
            return render(request, "admin/newuser.html", {"error": "Usernames must be 150 characters or fewer"})
        if not re.match(r'[a-zA-Z0-9_@+.-]+$', username):
            return render(request, "admin/newuser.html", {"error": "Usernames may only contain alphanumeric, _, @, +, . and - characters"})

        # Check if username already exists
        if User.objects.filter(username=username).count() == 1:
            return render(request, "admin/newuser.html", {"error": "Username exists"})

        # Check if passwords match
        if pass1 != pass2:
            return render(request, "admin/newuser.html", {"error": "Passwords don't match"})

        # Check if password entered
        if pass1 == "":
            return render(request, "admin/newuser.html", {"error": "No password entered"})

        # Make new user and usertype
        user = User.objects.create_user(username, password=pass1)
        user.save()

        ut = Type(usertype=usertype, user=user)
        ut.save()

        messages.success(request, "User created")
        return HttpResponseRedirect("/settings/")
    else:
        # Render make user page
        return render(request, "admin/newuser.html", {})

# User list
@only_user_type()
def user_list(request):
    # Get users
    users = User.objects.all()

    # Function to convert user object to tuple of values needed each row
    # Which is then run on each user
    conv = {'A': "Admin",
            'Q': "Question setter",
            'C': "Competitior"}
    f = lambda user: (user.username, conv[user.type.usertype], user.username.replace('@', '*'))
    users = sorted(map(f, users), key=lambda x: x[0])

    # Render users page with list of users
    return render(request, "admin/users.html", {"user_list": users})

# Edit user
@only_user_type()
def edit_user(request, username):
    # Try to get user, if the user does not exist then return a 404 error
    user = get_object_or_404(User.objects.all(), username=username.replace('*', '@'))

    # POST or GET
    if request.method == "POST":
        # Get user data
        usertype = request.POST["usertype"]
        newusername = request.POST["username"]

        # Update database
        user.username = newusername
        user.type.usertype = usertype
        user.type.save()
        user.save()

        messages.success(request, "User details saved")
        return HttpResponseRedirect("/settings/users")
    else:
        context = {"usertype": user.type.usertype,
                   "username": user.username,
                   "url": username}
        return render(request, "admin/edituser.html", context)

# Reset password
@only_user_type()
def reset_pass(request, username):
    # Try to get user, if the user does not exist then return a 404 error
    user = get_object_or_404(User.objects.all(), username=username.replace('*', '@'))

    # POST or GET
    if request.method == "POST":
        # Get user data
        pass1 = request.POST["newpass1"]
        pass2 = request.POST["newpass2"]

        # Check if passwords match
        if pass1 != pass2:
            # Render with error
            return render(request, "admin/resetpass.html", {"no_match": True, "username": user.username, "url": username})

        # update and redirect
        user.set_password(pass1)
        user.save()
        messages.success(request, "Password reset")
        return HttpResponseRedirect("/settings/users/{}".format(username))
    else:
        context = {"username": user.username,
                   "url": username}
        return render(request, "admin/resetpass.html", context)

# Question list
@only_user_type()
def quesiton_list(request):
    # Get questions
    questions = Question.objects.all()

    # Get the title of each question
    questions = map(lambda q: q.name, questions)

    # Render questions page with list of questions
    return render(request, "admin/questions.html", {"question_list": questions})

# Edit user
@only_user_type()
def edit_question(request, title):
    # Try to get question, if the question does not exist then return a 404 error
    question = get_object_or_404(Question.objects.all(), name=title)

    # POST or GET
    if request.method == "POST":
        # Get question data
        title = request.POST["title"]
        description = request.POST["description"]
        time = request.POST["time"]

        # Update database
        author = question.author
        question.delete()
        question = Question()
        question.name = title
        question.description = description
        question.timetorun = time
        question.author = author
        question.save()

        messages.success(request, "Question saved")
        return HttpResponseRedirect("/settings/questions")
    else:
        context = {"title": title,
                   "question": question.description,
                   "time": question.timetorun}
        return render(request, "admin/editquestion.html", context)

# Edit testcases
@only_user_type()
def testcases(request, title):
    # Try to get question, if the question does not exist then return a 404 error
    question = get_object_or_404(Question.objects.all(), name=title)

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
        return HttpResponseRedirect("/settings/questions")
    else:
        # Function to convert testcase
        f = lambda tc: (tc.testinput, tc.testoutput, tc.weighting)
        context = {"title": title,
                   "testcases": map(f, TestCase.objects.filter(question=question))}
        return render(request, "admin/testcases.html", context)

# New competition
@only_user_type()
def new_competition(request):
    # POST or GET
    if request.method == "POST":
        # Check if active competition
        if competition_active():
            # Get questions title and id
            f = lambda q: (q.name, q.qid)
            questions = map(f, Question.objects.all())
            return render(request, "admin/makecompetition.html", {"questions": questions, "error": "Competition cannot be started when another competition is running"})

        # Get user data
        title = request.POST["title"]
        endtime = request.POST["endtime"]
        enddate = request.POST["enddate"]
        scoringtype = request.POST["scoringtype"]

        # convert endtime to a datetime object
        endtime = datetime.datetime(*map(int, re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})', enddate + "T" + endtime).group(1, 2, 3, 4, 5)))

        # Make the competition
        competition = Competition(name=title, endtime=endtime, scoringtype=scoringtype, active=True)
        competition.save()

        # Add questions
        q_re = re.compile(r'^q(\d+)')
        qids = filter(None, map(q_re.match, request.POST.keys()))
        for qid in qids:
            competition.questions.add(Question.objects.all().get(qid=int(qid.group(1))))

        # Save the model
        competition.save()

        # Redirect
        messages.success(request, "Competition started")
        return HttpResponseRedirect("/settings")
    else:
        # Get questions title and id
        f = lambda q: (q.name, q.qid)
        questions = sorted(map(f, Question.objects.all()), key=lambda x: x[0])
        return render(request, "admin/makecompetition.html", {"questions": questions})

# Pick competition for submissions page
@only_user_type()
def pick_submissions(request, username):
    user = get_object_or_404(User, username=username)

    # Get the names of the competitions the user has submitted solutions to
    competitions = []
    for c in Competition.objects.all():
        for q in c.questions.all():
            if Submission.objects.filter(competition=c).filter(user=user).filter(question=q):
                competitions.append(c.name)
                break

    return render(request, "admin/pickcompetition.html", {"url": username, "competitions": competitions})

# Submissions page
@only_user_type()
def submissions(request, username, competition):
    user = get_object_or_404(User, username=username)
    competition = get_object_or_404(Competition, name=competition)
    compname = competition.name

    # Get users submissions
    submissions = Submission.objects.filter(competition=competition).filter(user=user)

    if len(submissions) == 0:
        # No submissions by the user, most likly not in competition
        return render(request, "admin/pickcompetition.html", {"url": username, "error": "No submissions from {} in that competition".format(username)})

    # Get data about each question
    question_data = []
    comp_questions = competition.questions
    for question in comp_questions.all():
        # Get the scores by user for the question
        questionsubmissions = submissions.filter(question=question)
        scores = map(lambda x: x.score, questionsubmissions)

        # Get the maximum score, an extra 0 is added to the list in the case of the user having no submissions
        score = max(scores + [0])

        # Add question data
        question_data.append((question.name, score, len(questionsubmissions), map(lambda x: x.id, questionsubmissions)))

    # Calculate score, number attempted
    score = sum(map(lambda x: x[1], question_data))
    numberattempted = len(filter(lambda x: x[2], question_data))

    # Calculate mean score, mean attempted
    meanscore = score/float(len(comp_questions.all()))
    meanattempted = score/float(numberattempted)

    # Calculate number of attempts
    totalattempts = sum(map(lambda x: x[2], question_data))

    # Return submissions page
    context = {
        "username": username,
        "competition": compname,
        "totalscore": score,
        "meanscore": meanscore,
        "numattempted": numberattempted,
        "meanattempted": meanattempted,
        "totalattempts": totalattempts,
        "questions": question_data
    }
    return render(request, "admin/submissions.html", context=context)

# User submission
@only_user_type()
def user_submission(request, username, competition, submissionid):
    # Get submission
    submission = get_object_or_404(Submission, id=int(submissionid))

    # Get code as string
    usercodefile = submission.submission
    usercodefile.open()
    usercode = usercodefile.read()
    usercodefile.close()

    # Make context and render
    context = {
        "username": submission.user.username,
        "question": submission.question.name,
        "competition": submission.competition.name,
        "code": usercode
    }
    return render(request, "admin/submission.html", context=context)
