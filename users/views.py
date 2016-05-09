import random
import re
import urllib
import json as m_json

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from bs4 import BeautifulSoup
from google import search

from models import UserProfile, Question, AttendedCourse, CourseQuestion
# Create your views here.


def home(request):
    try:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            gender = request.POST.get('gender-radio')
            password1 = request.POST.get('password1')
            user = User.objects.create_user(username=email, first_name=first_name,
                                            last_name=last_name, email=email,
                                            password=password1)
            user_profile = UserProfile(user=user, phone_number=phone_number, gender=gender)
            user_profile.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, "users/home.html")
    except Exception, e:
        print e.message


def log_in(request):
    try:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username=email, password=password)
            if user:
                request.session['start_question'] = {}
                request.session['start_question']['id_count'] = []
                request.session['start_question']['black_list'] = []
                request.session.modified = True
                login(request, user)
            return HttpResponseRedirect('/')
    except Exception, e:
        print e.message


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


def start_question(request):
    request.session['start_question'] = {}
    request.session['start_question']['id_count'] = []
    request.session.modified = True
    return render(request, "users/ground.html")


@csrf_exempt
def first_attempt(request):
    try:
        data = {}
        if request.method == "POST":
            question = CourseQuestion.objects.all()[0]
            data['question'] = question.question
            data['question_id'] = question.id
            request.session['start_question']['id_count'].append(question.id)
            request.session.modified = True
            return HttpResponse(m_json.dumps(data), content_type="application/json")
    except Exception, e:
        print e.message


@csrf_exempt
def get_question(request):
    try:
        if request.method == "POST":
            question = CourseQuestion.objects.get(id=request.POST.get('id'))
            answered, created = AttendedCourse.objects.get_or_create(user=request.user, course=question.course)
            if question.answer == request.POST.get('answer'):
                answered.weight += question.weight
            else:
                if question.weight == 2:
                    request.session['start_question']['black_list'].append(question.id)
                    request.session.modified = True
            answered.save()
        setter = CourseQuestion.objects.all().exclude(id__in=request.session['start_question']['id_count'])
        if setter:
            data = {}
            k = random.choice(setter)
            request.session['start_question']['id_count'].append(k.id)
            request.session.modified = True
            data['question'] = k.question
            data['id'] = k.id
            return HttpResponse(m_json.dumps(data), content_type="application/json")
        else:
            lists = []
            ac = AttendedCourse.objects.filter(user=request.user).aggregate(Max('weight'))
            best_courses = AttendedCourse.objects.filter(user=request.user, weight=ac['weight__max'])
            course_list = []
            for course in best_courses:
                for q in course.course.coursequestion_set.all():
                    if q.weight == 2:
                        if q.id not in request.session['start_question']['black_list']:
                            course_list.append(course)
            for i in course_list:
                data = {'name': i.course.name}
                lists.append(data)
            request.session['start_question']['id_count'] = []
            request.session['start_question']['black_list'] = []
            request.session.modified = True
            return HttpResponse(m_json.dumps(lists), content_type="application/json")
    except Exception, e:
        print e.message


@csrf_exempt
def ask_question(request):
    try:
        if request.method == "POST":
            data = {}
            query = request.POST.get('question')
            question, created = Question.objects.get_or_create(question=query)
            if not created:
                data['answer'] = question.answer
                return HttpResponse(m_json.dumps(data), content_type="application/json")
            # if 'how' in query.lower():
            #     query += " wikihow english"
            # elif 'who' or 'what' in query.lower():
            # 	query += " wikipedia english"
            # query = urllib.urlencode({'q': query})
            # response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query).read()
            # json = m_json.loads(response)
            # results = json['responseData']['results']
            for result in search(query, tld='es', lang='es', stop=20):
                print result
            for result in search(query, tld='es', lang='es', stop=20):
                if 'wikipedia' in result:
                    new_url = result
                    print new_url
                    r = urllib.urlopen(new_url).read()
                    soup = BeautifulSoup(r, "html.parser")
                    result = soup.find("div", {"id": "mw-content-text"})
                    pre = result.find_all("p")
                    ans = re.sub(r'\([^)]*\)', '', pre[0].text)
                    data['answer'] = ans
                    break
                elif 'wikihow' in result:
                    new_url = result
                    r = urllib.urlopen(new_url).read()
                    soup = BeautifulSoup(r, "html.parser")
                    result = soup.findAll("div", {"class": "step"})
                    data['answer'] = result[0].text
                    break
                else:
                    data['answer'] = 'not found'
            question.answer = data['answer']
            question.save()
            return HttpResponse(m_json.dumps(data), content_type="application/json")
        return render(request, "users/ask_question.html")
    except Exception, e:
        print e.message
