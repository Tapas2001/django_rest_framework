from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def students(request):
    students = [
        {'id': 1, 'name': 'John Leo', 'age': 32}
    ]

    return HttpResponse(students)
    # return HttpResponse('<h2>Hello</h2>')

