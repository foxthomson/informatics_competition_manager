from django.conf.urls import url

from .base import views as base
from .question_setting import views as question_setting
from .admin_settings import views as admin_settings
from .competition import views as competition

urlpatterns = [
    url(r'^login/$', base.user_login, name='logon'),
    url(r'^(?:index|)/?$', base.index, name='index'),
    url(r'^logout/$', base.user_logout, name='logout'),
    url(r'^changepass/$', base.user_change_password, name='changepass'),
    url(r'^question/$', question_setting.question, name='question'),
    url(r'^questions/$', question_setting.user_question_list, name='userquestionlist'),
    url(r'^questions/([^/]+)/$', question_setting.user_edit_question, name='usereditquestion'),
    url(r'^questions/([^/]+)/testcases/$', question_setting.user_edit_testcases, name='useredittestcase'),
    url(r'^settings/$', admin_settings.admin_settings, name='adminsettings'),
    url(r'^settings/newuser/$', admin_settings.new_user, name='newuser'),
    url(r'^settings/users/$', admin_settings.user_list, name='userlist'),
    url(r'^settings/users/([a-zA-Z0-9_*+.-]+)/$', admin_settings.edit_user, name='edituser'),
    url(r'^settings/users/([a-zA-Z0-9_*+.-]+)/resetpass/$', admin_settings.reset_pass, name='resetpass'),
    url(r'^settings/users/([a-zA-Z0-9_*+.-]+)/submissions/$', admin_settings.pick_submissions, name='picksubmissions'),
    url(r'^settings/users/([a-zA-Z0-9_*+.-]+)/submissions/([a-zA-Z0-9_*+.-]+)/$', admin_settings.submissions, name='submissions'),
    url(r'^settings/users/([a-zA-Z0-9_*+.-]+)/submissions/([a-zA-Z0-9_*+.-]+)/(\d+)$', admin_settings.user_submission, name='usersubmission'),
    url(r'^settings/questions/$', admin_settings.quesiton_list, name='questionlist'),
    url(r'^settings/questions/([^/]+)/$', admin_settings.edit_question, name='editquestion'),
    url(r'^settings/questions/([^/]+)/testcases/$', admin_settings.testcases, name='testcases'),
    url(r'^settings/newcompetition/$', admin_settings.new_competition, name='newcompetition'),
    url(r'^scores/$', competition.score_list, name='scorelist'),
    url(r'^comp/$', competition.competition, name='competition'),
    url(r'^comp/([^/]+)/$', competition.comp_question_page, name='compquestion'),
    url(r'^comp/([^/]+)/results/$', competition.result, name='submission'),
]
