from rest_framework.decorators import api_view
import json
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse



class VideoCallAccountCreate(APIView):

    """ Here we call node js video calling account create api."""

    def post(self, request, *args, **kwargs):
        # call another api for POST
        url = 'https://c24vconfapi.accelx.net/api/v1/account/'
        f = requests.Session()
        headers = {'content-type': 'application/json'}
        payload = request.data
        api_call = f.post(
            url, 
            data=json.dumps(payload),
            timeout=30, headers=headers, 
            verify=False)

        return Response(api_call)





class UpdateVideoCallAccount(APIView):

    """ Here we call node js video calling account update api."""

    def put(self, request, token, *args, **kwargs):
        # call another api for PUT
        url = 'https://c24vconfapi.accelx.net/api/v1/account/'
        auth_token= token
        f = requests.Session()
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + str(auth_token)}
        payload = request.data
        api_call = f.put(
            url, 
            data=json.dumps(payload),
            timeout=30, headers=headers, 
            verify=False)

        return Response(api_call)




class VideoCallCreateMeeting(APIView):

    """ Here we call node js video calling account create api."""

    def post(self, request, token, *args, **kwargs):
        # call another api for POST
        url = 'https://c24vconfapi.accelx.net/api/v1/meeting/'
        auth_token= token
        f = requests.Session()
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + str(auth_token)}
        payload = request.data
        print('Payload', payload)  # post data
        api_call = f.post(
            url, 
            data=json.dumps(payload),
            timeout=30, headers=headers, 
            verify=False)

        return Response(api_call)



class VideoCallCreateDemoMeeting(APIView):

    """ Here we call node js video calling account create api."""

    def post(self, request, token, *args, **kwargs):
        # call another api for POST
        url = 'https://c24vconfapi.accelx.net/api/v1/demo/'
        auth_token= token
        f = requests.Session()
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + str(auth_token)}
        payload = request.data
        print('Payload', payload) 
        api_call = f.post(
            url, 
            data=json.dumps(payload),
            timeout=30, headers=headers, 
            verify=False)

        return Response(api_call)




class VideoCallGetMeetingInfo(APIView):

    """ Here we call node js video calling account create api."""

    def get(self, request, token, meetingId,  *args, **kwargs):
        # call another api for POST
        url = 'https://c24vconfapi.accelx.net/api/v1/:meetingId'
        auth_token= token
        f = requests.Session()
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + str(auth_token)}
        payload = request.data
        print('Payload', payload) 
        api_call = f.get(
            url, 
            data=json.dumps(payload),
            timeout=30, headers=headers, 
            verify=False)

        return Response(api_call)



class VideoCallUpdateMeetingInfo(APIView):

    """ Here we call node js video calling account create api."""

    def put(self, request, token, meetingId,  *args, **kwargs):
        # call another api for POST
        url = 'https://c24vconfapi.accelx.net/api/v1/:meetingId'
        auth_token= token
        f = requests.Session()
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + str(auth_token)}
        payload = request.data
        print('Payload', payload) 
        api_call = f.put(
            url, 
            data=json.dumps(payload),
            timeout=30, headers=headers, 
            verify=False)

        return Response(api_call)



class VideoCallDeleteMeetingInfo(APIView):

    """ Here we call node js video calling account create api."""

    def delete(self, request, token, meetingId,  *args, **kwargs):
        # call another api for POST
        url = 'https://c24vconfapi.accelx.net/api/v1/:meetingId'
        auth_token= token
        f = requests.Session()
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + str(auth_token)}
        payload = request.data
        print('Payload', payload) 
        api_call = f.delete(
            url, 
            data=json.dumps(payload),
            timeout=30, headers=headers, 
            verify=False)

        return Response(api_call)


