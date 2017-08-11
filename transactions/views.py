from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.http import HttpRequest, HttpResponseRedirect
from django_ajax.decorators import ajax

from multiprocessing import Process

from .models import User
from django.db import connection

from pprint import pprint

def index(request: HttpRequest):
    return render(request, 'transactions/index.html', {'users': User.objects.all()})

class ResultsView(generic.TemplateView):
    template_name = 'transactions/results.html'

def run_transaction(isolation_level: str, query: str):
    set_level = "SET TRANSACTION ISOLATION LEVEL " + isolation_level + ";"
    with connection.cursor() as cursor:
        cursor.execute(set_level + query)

@ajax
def run(request: HttpRequest):
    isolation_level = request.POST.get("isolation_level")
    q1 = request.POST.get("sql1")
    q2 = request.POST.get("sql2")

    p1 = Process(target=run_transaction, args=(isolation_level, q1,))
    p2 = Process(target=run_transaction, args=(isolation_level, q2,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    return render(request, 'transactions/table.html', {'users': User.objects.all()})