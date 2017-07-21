from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json
from .twitter_poller.poller import poll_twitter

import threading
import time

# Create your views here.
def index(request):
    template = loader.get_template('pollerapp/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def twitter_api(request):
    print(json.loads(request.body))
    # deserializing JSON string sent by AJAX that is, of course, a byte string available on request obeject to a Python object.
    tags_request = json.loads(request.body)

    if request.method == "POST":
        JSON_poll_data = poll_twitter(tags_request)
        if JSON_poll_data is not None:
            return HttpResponse(JSON_poll_data, content_type="application/json")
        else:
            return HttpResponse("None")

print(poll_twitter)
