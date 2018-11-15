from django.conf.urls import url
from .views import carts_add,carts_count

urlpatterns = [
    url(r'carts_add/$',carts_add,name='carts_add'),
    url(r'carts_count/$',carts_count,name='carts_count')    
]
