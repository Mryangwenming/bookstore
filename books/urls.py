from django.conf.urls import url
from .views import book_list,book_detail

urlpatterns = [
    url(r'book_list/$',book_list,name='book_list'),
    url(r'book_detail/(\d+)/$',book_detail,name='book_detail'),
]
