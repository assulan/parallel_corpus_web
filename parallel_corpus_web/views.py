-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q, Sum
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

import codecs
from django.shortcuts import render_to_response, redirect
from parallel_corpus_web.models import ParallelPage, MyUser
from parallel_corpus_web.signals import first_time
from django.contrib import messages
from parallel_corpus_web import settings
import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def index(request, template_name="index.html"):
    if request.method == "GET":
        return render_to_response(template_name, context_instance=RequestContext(request))
    username = request.POST['inputLogin']
    password = request.POST['inputPassword']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)                        
            first_time.send(sender=index, user=user)            
            messages.success(request,'Successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Account disabled.')
            return redirect('index')
    else:
        messages.error(request,'Invalid login.')
        return redirect('index')


@login_required
def home(request, template_name="home.html"):
    my_user = MyUser.objects.get(user=request.user)
    page_list = my_user.pages
    paginator = Paginator(page_list, 1)
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pages = paginator.page(paginator.num_pages)    
    return render_to_response(template_name, {'pages': pages}, context_instance=RequestContext(request))

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request,'Logged out.')
    return redirect('index')

@login_required
def correct(request, pk, page):
    parallel_sent = ParallelPage.objects.get(pk=pk)
    parallel_sent.correct_score += 1
    parallel_sent.save()
    messages.success(request,'Page is marked as correct. Thank you!')
    return redirect("/home/?page=%s" % str(int(page)))

@login_required
def incorrect(request, pk, page):
    parallel_sent = ParallelPage.objects.get(pk=pk)
    parallel_sent.incorrect_score += 1
    parallel_sent.save()
    messages.error(request, 'Page is marked as incorrect. Thank you!')
    return redirect("/home/?page=%s" % str(int(page)))


def about(request, template_name="about.html"):
    return render_to_response(template_name, context_instance=RequestContext(request))

@login_required(login_url='index')
def download(request, template_name="download.html"):
    static_path = os.path.join(settings.CURRENT_PATH, "static")
    download_path = os.path.join(static_path, 'downloads')                        
    pages = ParallelPage.objects.all()                   
    fname = "primeminister.output" 
    f_out = codecs.open(os.path.join(download_path, fname), "w", "utf-8")
    for page in pages:
        if page.correct_score == 1 and page.incorrect_score == 0:
            # verfied
            f_out.write("%s 1\n" % page.file_name) 
        elif page.incorrect_score == 1 and page.correct_score == 0:    
            f_out.write("%s 0\n" % page.file_name) 
    f_out.close()    
    links = {}
    links[fname] = os.path.join('/static/downloads', fname)
    return render_to_response(template_name, {'links': links}, context_instance=RequestContext(request))


def stats(request, template_name="stats.html"):    
    incorrect_dev = ParallelPage.objects.filter(is_dev=True, incorrect_score=1).count()
    correct_dev = ParallelPage.objects.filter(is_dev=True, correct_score=1).count()
    incorrect_test = ParallelPage.objects.filter(is_test=True, incorrect_score=1).count()
    correct_test = ParallelPage.objects.filter(is_test=True, correct_score=1).count()
    not_verified = ParallelPage.objects.filter(correct_score=0, incorrect_score=0).count()

    statistics = {
                    # 'dev.incorrect.{kz,en}': incorrect_dev,
                    # 'dev.correct.{kz,en}': correct_dev,
                    'test.incorrect.{kz,en}': incorrect_test,
                    'test.correct.{kz,en}': correct_test,
                    'not verified' : not_verified,
                    'verified': incorrect_dev + correct_dev + incorrect_test + correct_test,
                    'total': ParallelPage.objects.all().count()
                    }
    return render_to_response(template_name, {'stats': statistics},
                context_instance=RequestContext(request))
