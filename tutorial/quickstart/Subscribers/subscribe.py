from django.core.cache import cache
from pubsub import pub


# ------------ create a listener ------------------

def preload_cache_sub(businessId, bookId):

    print(businessId, bookId)

    cache.set('id', 200, None)



# ------------ register listener ------------------

pub.subscribe(preload_cache_sub, 'updateCache')
