# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, loader


def index(request, message):
    context = Context({
        'message': message,
    })

    return HttpResponse(loader.get_template('index.html').render(context))
