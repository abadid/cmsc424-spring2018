from django.conf.urls import url

from . import views
        
urlpatterns = [
        # ex: /grading/
        url(r'^$', views.mainindex, name='mainindex'),
        # ex: /grading/instructor/1
        url(r'^instructor/(?P<instructor_id>[0-9]+)/$', views.instructorindex, name='instructorindex'),
        # ex: /grading/instructor/1/course/2
        url(r'^instructor/(?P<instructor_id>[0-9]+)/course/(?P<course_id>[0-9]+)/$', views.instructorcourse, name='instructorcourse'),
        # ex: /grading/instructor/1/course/2/assignment/3
        url(r'^instructor/(?P<instructor_id>[0-9]+)/course/(?P<course_id>[0-9]+)/assignment/(?P<assignment_id>[0-9]+)/$', views.instructorassignment, name='instructorassignment'),
        # ex: /grading/instructor/1/course/2/create
        url(r'^instructor/(?P<instructor_id>[0-9]+)/course/(?P<course_id>[0-9]+)/create$', views.instructorcreate, name='instructorcreate'),
        # ex: /grading/instructor/1/course/2/assignment/3/student/4
        url(r'^instructor/(?P<instructor_id>[0-9]+)/course/(?P<course_id>[0-9]+)/assignment/(?P<assignment_id>[0-9]+)/student/(?P<student_id>[0-9]+)/$', views.instructorgradesubmission, name='instructorgradesubmission'),
        # ex: /grading/student/1
        url(r'^student/(?P<student_id>[0-9]+)/$', views.studentindex, name='studentindex'),
        # ex: /grading/student/1/assignment/2
        url(r'^student/(?P<student_id>[0-9]+)/assignment/(?P<assignment_id>[0-9]+)/$', views.studentassignment, name='studentassignment'),
        # ex: /grading/student/1/submitassignment/2
        url(r'^student/(?P<student_id>[0-9]+)/submitassignment/(?P<assignment_id>[0-9]+)/$', views.submitassignment, name='submitassignment'),
        # ex: /grading/student/1/submittedassignment/2
        url(r'^student/(?P<student_id>[0-9]+)/submittedassignment/(?P<assignment_id>[0-9]+)/$', views.submittedassignment, name='submittedassignment')
] 
