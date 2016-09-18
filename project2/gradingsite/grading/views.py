from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from grading.models import Instructor, Course, Assignment, Student, StudentAssignment
from django.urls import reverse
import datetime
from django.utils import timezone


# Create your views here.

def mainindex(request):
        context = { 'instructor_list': Instructor.objects.all() }
        return render(request, 'grading/index.html', context)

def instructorindex(request, instructor_id):
        context = { 'course_list': Instructor.objects.get(pk=instructor_id).course_set.all() }
        return render(request, 'grading/instructorindex.html', context)

def instructorcourse(request, instructor_id, course_id):
	c = get_object_or_404(Course, pk=course_id)
	a_list = c.assignment_set.filter(due_date__gte=timezone.now())
	p_list = c.assignment_set.filter(due_date__lte=timezone.now())
	context = { 'instructor_id': instructor_id, 'course_id': course_id, 'course_title': c.title, 'active_assignment_list': a_list, 'past_assignment_list': p_list }
        return render(request, 'grading/instructorcourse.html', context)

def instructorassignment(request, instructor_id, course_id, assignment_id):
	# Should get a list of all submissions for this assignment, and set it in context
        context = { }
        return render(request, 'grading/instructorassignment.html', context)

def instructorcreate(request, instructor_id, course_id):
        context = { 'course_list': Instructor.objects.all() }
        return render(request, 'grading/instructorcreate.html', context)

def instructorgradesubmission(request, instructor_id, course_id, assignment_id, student_id):
	context = { }
        return render(request, 'grading/instructorgradesubmission.html', context)

def studentindex(request, student_id):
	context = { 'student_id': student_id, 'course_list': Student.objects.get(pk=student_id).courses.all() }
        return render(request, 'grading/studentindex.html', context)

def studentassignment(request, student_id, assignment_id):
	context = { 'assignment': Assignment.objects.get(pk=assignment_id), 'student': Student.objects.get(pk=student_id) }
        return render(request, 'grading/studentassignment.html', context)

def submitassignment(request, student_id, assignment_id):
	print request.POST
	answers = " ".join([request.POST["answer{}".format(i)] for i in range(1, 101) if "answer{}".format(i) in request.POST])
	sa = StudentAssignment(student=Student.objects.get(pk=student_id), assignment=Assignment.objects.get(pk=assignment_id), answers=answers, score=-1)
	sa.save()
	return HttpResponseRedirect(reverse('submittedassignment', args=(student_id,assignment_id,)))

def submittedassignment(request, student_id, assignment_id):
	context = { 'student_id': student_id, 'course_list': Student.objects.get(pk=student_id).courses.all() }
	return render(request, 'grading/studentindex.html', context)
