from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .secret import CLARIFAI_API_KEY

# View Functions for /image routes

# csrf added to handle POST request not related to FE Form
@csrf_exempt
def images(request):
    """
    Handles all requests for /image route, methods: GET, POST
    """
    if request.method == 'POST':
        # do stuff to return JSON response to clarifai
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        return JsonResponse({
            'message': 'Post Request Received!',
            'body': body
        })

    # otherwise return get request JSON
    elif request.method == 'GET':
        return JsonResponse({'message': 'GET Request Received!'})

    else:
        return JsonResponse({'message': 'Nothing to do!'})