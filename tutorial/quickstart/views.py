import sys
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from pubsub import pub
from memory_profiler import profile


from .Subscribers.subscribe import *
from .Profiler.profiler import *
from .Utils.util import *


def preload_cache_init():

    cache.set('id', 100, None)


preload_cache_init()


class PredictAPI(APIView):

    @profile
    # @profiler(sort_by='cumulative', lines_to_print=20, strip_dirs=True)
    def get(self, request, format=None):

        result = create_products(100000)

        result_sorted = product_counter_v1(result)

        return Response(cache.get('id'))


class PublishAPI(APIView):

    def get(self, request, format=None):

        # ---------------- send a message ------------------

        pub.sendMessage('updateCache', businessId=1000, bookId=100)
            
        return Response("{'status':'model published'}")
