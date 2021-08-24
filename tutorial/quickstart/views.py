import sys
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from pubsub import pub
from memory_profiler import profile

from .Subscribers.subscribe import *
from .profile import *

import random


random.seed(20)


###

def create_products(num):
    """Create a list of random products with 3-letter alphanumeric name."""
    return [''.join(random.choices('ABCDEFG123', k=3)) for _ in range(num)]

def product_counter_v1(products):
    """Get count of products in descending order."""
    counter_dict = create_counter(products)
    sorted_p = sort_counter(counter_dict)
    return sorted_p

def create_counter(products):
    counter_dict = {}
    for p in products:
        if p not in counter_dict:
            counter_dict[p] = 0
        counter_dict[p] += 1
    return counter_dict

def sort_counter(counter_dict):
    return {k: v for k, v in sorted(counter_dict.items(),
                                    key=lambda x: x[1],
                                    reverse=True)}

###


def preload_cache_init():

    cache.set('id', 100, None)


preload_cache_init()


class PredictAPI(APIView):

    # @profile
    @profiler(sort_by='cumulative', lines_to_print=20, strip_dirs=True)
    def get(self, request, format=None):

        result = create_products(100000)

        result_sorted = product_counter_v1(result)

        return Response(cache.get('id'))


class PublishAPI(APIView):

    def get(self, request, format=None):

        # ---------------- send a message ------------------

        pub.sendMessage('updateCache', businessId=1000, bookId=100)
            
        return Response("{'status':'model published'}")
