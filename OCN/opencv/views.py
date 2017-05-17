# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from opencv.video_analysis.shot_detect_RSV_ROG import detect_using_RSV_ROG
import json


# Create your views here.
def index(request):
    return render(request, 'base.html', {})


def analysis(request):
    result = {}
    if request.method == 'POST':
        video_uri = request.POST.get('video_uri', None)
        # TODO: create a folder to save all of keyframes
        output_folder = None
        detect_using_RSV_ROG(video_uri=video_uri, output_folder=output_folder)
    return HttpResponse(json.dumps(result), content_type='application/json')
