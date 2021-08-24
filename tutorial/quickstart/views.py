from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from pubsub import pub

from .Subscribers.subscribe import *


def preload_cache_init():

    cache.set('id', 100, None)


preload_cache_init()


class PredictAPI(APIView):

    def get(self, request, format=None):

        return Response(cache.get('id'))


class PublishAPI(APIView):

    def get(self, request, format=None):

        # ---------------- send a message ------------------

        pub.sendMessage('updateCache', businessId=1000, bookId=100)
            
        return Response("{'status':'model published'}")
