from django.conf.urls import url
from .views import order_place

urlpatterns = [
    url(r'order_place/$',order_place,name='order_place')
]
