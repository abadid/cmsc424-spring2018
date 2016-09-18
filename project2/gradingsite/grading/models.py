from __future__ import unicode_literals

from django.db import models

# Create your models here.
import datetime
from django.utils import timezone

class Instructor(models.Model):
	name = models.CharField(max_length=50)
	rank = models.CharField(max_length=50)
	def __str__(self):
		return self.name

class Course(models.Model):
	title = models.CharField(max_length=50)
    	instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
	credits = models.IntegerField()
	description = models.CharField(max_length=500)
	def __str__(self):
		return self.title

class Student(models.Model):
	name = models.CharField(max_length=50)
	courses = models.ManyToManyField(Course)
	def __str__(self):
		return self.name

class Assignment(models.Model):
	course = models.ForeignKey(Course)
	assignment_no = models.IntegerField()
	due_date = models.DateTimeField()
	def __str__(self):
		return "Course Title: {}, Assignment No.: {}, Due on: {}".format(self.course.title, self.assignment_no, self.due_date)

class Question(models.Model):
	assignment = models.ForeignKey(Assignment)
	question_no = models.IntegerField()
	question_text = models.CharField(max_length=500)
	trueorfalse = models.BooleanField()

class StudentAssignment(models.Model):
	assignment = models.ForeignKey(Assignment)
	student = models.ForeignKey(Student)
	answers = models.CharField(max_length=100)
	score = models.IntegerField()
	
