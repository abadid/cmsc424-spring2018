Summary of steps from: https://docs.djangoproject.com/en/1.10/intro/tutorial01/

- `django-admin startproject mysite`

- `python manage.py runserver 0.0.0.0:8888`: can load new python code automatically, but sometimes need to rerun it

- `python manage.py startapp polls`: start a new app called `polls`

- Edit `polls/views.py` to add a view to it:
```
from django.http import HttpResponse

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
    	# output = ', '.join([q.question_text for q in latest_question_list])
        # return HttpResponse(output)

	context = { 'latest_question_list': latest_question_list }

	# Following two lines is the long version
	# template = loader.get_template('polls/index.html')
	# return HttpResponse(template.render(context, request))

	return render(request, 'polls/index.html', context)


def detail(request, question_id):
    	# try:
        #    	question = Question.objects.get(pk=question_id)
	# except Question.DoesNotExist:
 	# raise Http404("Question does not exist")

	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	def vote(request, question_id):
		question = get_object_or_404(Question, pk=question_id)
		try:
			selected_choice = question.choice_set.get(pk=request.POST['choice'])
		except (KeyError, Choice.DoesNotExist):
			# Redisplay the question voting form.
			return render(request, 'polls/detail.html', {
					'question': question,
					'error_message': "You didn't select a choice.",
					})
		else:
			selected_choice.votes += 1
			selected_choice.save()
			# Always return an HttpResponseRedirect after successfully dealing
			# with POST data. This prevents data from being posted twice if a
			# user hits the Back button.
			return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```

- Add a new file: `polls/urls.py`, and add:
```
from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	# ex: /polls/5/
	url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
	# ex: /polls/5/results/
	url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
	# ex: /polls/5/vote/
	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
```

- Edit: `mysite/urls.py`
```
from django.conf.urls import include, url

from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
]

```

- Change: `mysite/settings.py` to use PostgreSQL, to change TimeZone to `US/Eastern`
- Change: `mysite/settings.py` to add to INSTALLED_APPS:     'polls.apps.PollsConfig',

- `python manage.py migrate`

- Edit `polls/models.py` -- this includes all the edits till the end
```
from __future__ import unicode_literals
from django.db import models
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
           return self.question_text
   def was_published_recently(self):
           return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
           return self.choice_text
```

- `python manage.py makemigrations polls`

- `python manage.py sqlmigrate polls 0001` shows the SQL it will run

- Steps to make changes to models:
    * Change your models (in models.py).
    * Run `python manage.py makemigrations` to create migrations for those changes
    * Run `python manage.py migrate` to apply those changes to the database.

- `python manage.py shell`
```
from polls.models import Question, Choice
Question.objects.all()
from django.utils import timezone
q = Question(question_text="What's new?", pub_date=timezone.now())
q.save()
q.question_text
Question.objects.filter(id=1)
Question.objects.filter(question_text__startswith='What')
q = Question.objects.get(pk=1)
q.choice_set.all()
q.choice_set.create(choice_text='Not much', votes=0)
q.choice_set.create(choice_text='The sky', votes=0)
c = q.choice_set.create(choice_text='Just hacking again', votes=0)
c.question
Choice.objects.filter(question__pub_date__year=current_year) # use double underscores
```

- `python manage.py createsuperuser` and go to: `http://localhost:8888/admin/`

- Edit `polls/admin.py`
```
from django.contrib import admin
from .models import Question
admin.site.register(Question)
```


- Edit: `polls/templates/polls/index.html`
```
{% if latest_question_list %}
<ul>
{% for question in latest_question_list %}
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
{% endfor %}
</ul>
{% else %}
<p>No polls are available.</p>
{% endif %}
```


- Edit: `polls/templates/polls/detail.html`
```
<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
<input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
<label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
{% endfor %}
<input type="submit" value="Vote" />
</form>
```

- Against hardcoding URLs. Instead of:
```
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
```
Use:
```
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
# refers to: url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail')
```

- Namespace Apps, by adding `app_name = 'polls'` to polls/url.py, and then using 'polls:detail' instead of 'detail' above.

- 'csrf_token' is about forgeries or something.

- New template: `polls/templates/polls/results.html`
```
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
<li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```
