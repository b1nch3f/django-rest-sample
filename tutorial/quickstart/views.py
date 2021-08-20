from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from pubsub import pub


cache = {}

def preload_cache_init():

    global cache

    cache['id'] = 100


preload_cache_init()


# ------------ create a listener ------------------

def preload_cache_sub():

    global cache

    cache['id'] = 200



# ------------ register listener ------------------

pub.subscribe(preload_cache_sub, 'updateCache')


class PredictAPI(APIView):
    def get(self, request, format=None):

        global cache

        #print(cache)
        
        # cache['id'] = 101
            
        return Response(cache)


class PublishAPI(APIView):
    def get(self, request, format=None):

        global cache

        # ---------------- send a message ------------------

        pub.sendMessage('updateCache')
            
        return Response("{'status':'model published'}")
