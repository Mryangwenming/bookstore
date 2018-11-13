from django.conf.urls import url
from .views import book_list

urlpatterns = [
    url(r'book_list/$',book_list,name='book_list')
]
