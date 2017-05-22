# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from opencv.video_analysis.shot_detect_RSV_ROG import detect_using_RSV_ROG
from django.core.files.storage import FileSystemStorage
import json
import os
from os import listdir
from os.path import isfile, join
import time


PATH_DATA_FOLDER = os.path.dirname(os.getcwd()) + '/data/'


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


def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # full_path = fs.base_location + '/' + filename
        # output_folder = ''
        # count = 0
        # while True:
        #     directory = fs.base_location + '/' + filename.split('.')[0] + '__result__' + str(count)
        #     if not os.path.exists(directory):
        #         os.makedirs(directory)
        #         output_folder = directory
        #         break
        #     count += 1
        # detect_using_RSV_ROG(video_uri=full_path, output_folder=output_folder)
        # get all frame in output folder
        directory_frame = '/home/huynhduc/PycharmProjects/OCN/media/vietnam__result__0'
        frame_list = [f for f in listdir(directory_frame) if isfile(join(directory_frame, f))]
        directory_shot = directory_frame + '/shot'
        shot_list = [f for f in listdir(directory_shot) if isfile(join(directory_shot, f))]
        # sort frame_list
        for i in range(0, len(frame_list) - 1):
            for j in range(i, len(frame_list)):
                frame_i = frame_list[i][5:-4]
                frame_j = frame_list[j][5:-4]
                if int(frame_i) > int(frame_j):
                    temp = frame_list[i]
                    frame_list[i] = frame_list[j]
                    frame_list[j] = temp
        # sort shot list
        for i in range(0, len(shot_list) - 1):
            for j in range(i, len(shot_list)):
                shot_i = shot_list[i][4:-4]
                shot_j = shot_list[j][4:-4]
                if int(shot_i) > int(shot_j):
                    temp = shot_list[i]
                    shot_list[i] = shot_list[j]
                    shot_list[j] = temp
        data = []
        for i in range(len(shot_list)):
            shot_frame = {
                str(i): [shot_list[i], frame_list[i]]
            }
            data.append(shot_frame)
        time.sleep(3)
        result = {
            'data': data,
            'directory': '/' + directory_frame.split('/')[5] + '/' + directory_frame.split('/')[6],
        }
        return HttpResponse(json.dumps(result), content_type='application/json')
    return HttpResponse(json.dumps({}), content_type='application/json')
