# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.views.decorators.http import require_GET, require_POST


@require_GET
def index(request):
    return render_to_response('index.html')


@require_POST
def post(request):
    return redirect('/result')


@require_GET
def result(request):
    return render_to_response('result.html')
