# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from icm.models import Type, Competition, Submission

import datetime

def only_user_type(usertype="A", failvalue=HttpResponseRedirect("/index/")):
    # Admin only decorator, similar to @login_required but requires the user to be an admin
    # Runs function if user is admin, otherwise returns failvalue
    def decorator(f):
        @login_required
        def wrapper(request, *args, **kwargs):
            # Check if user admin
            if request.user.type.usertype == usertype:
                # Run function
                return f(request, *args, **kwargs)
            else:
                # Return fail and add message
                messages.error(request, "Access denied")
                return failvalue
        return wrapper
    return decorator

def competition_active():
    # Check if competition still active and update it if it isn't
    # Returns False if no active competition or the competition if is it active
    # Should be called before anything is done to a competition
    # Get the competition marked as active
    competition = Competition.objects.filter(active=True)

    if competition.count() == 0:
        # No competition marked as active: return false
        return False

    # Compere the competition end time to the current time
    competition = competition[0]
    if competition.endtime.replace(tzinfo=None) > datetime.datetime.now():
        # competition still active
        return competition
    else:
        # Change competition active flag
        competition.active = False
        competition.save()
        return False

def competition_only(failvalue=HttpResponseRedirect("/index/")):
    # decorator which will only allow users to view the page if a competition is running
    # Will redirect them if they are not logged in, there is no competition running or
    # they are a competitior without the competition title in their model
    # Will also run function with an argument after request which is the model of the current competition
    def decorator(f):
        @login_required
        def wrapper(request, *args, **kwargs):
            # Get competition
            competition = competition_active()
            if competition:
                # Check if competitior
                if request.user.type.usertype == "C":
                    # Check if copetition name listed
                    if request.user.type.compname == competition.name:
                        # Run function
                        return f(request, competition, *args, **kwargs)
                    else:
                        # Return fail
                        messages.error(request, "Access denined")
                        return failvalue
                else:
                    # Run function
                    return f(request, competition, *args, **kwargs)
            else:
                # Return fail
                messages.error(request, "No competition running")
                return failvalue
        return wrapper
    return decorator

def get_score(user, competition):
    # Get the score of a given user in a given question

    # Get questions in the competition
    comp_questions = competition.questions

    score = 0

    # Check each question
    for question in comp_questions.all():
        # Get the scores by user for the question
        submissions = Submission.objects.filter(competition=competition).filter(user=user).filter(question=question)
        scores = map(lambda x: x.score, submissions)

        # Get the maximum score, an extra 0 is added to the list in the case of the user having no submissions
        score += max(scores + [0])

    return score
