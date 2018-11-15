from django.conf.urls import url
from .views import carts_add,carts_count,carts_show

urlpatterns = [
    url(r'carts_add/$',carts_add,name='carts_add'),
    url(r'carts_count/$',carts_count,name='carts_count'),    
    url(r'carts_show/$',carts_show,name='carts_show'),
    url(r'carts_del/$',carts_del,name='carts_del'),
    url(r'carts_update/$',carts_update,name='carts_update')
]
