from django.shortcuts import render,redirect,reverse
from .models import Books
from .enums import *
from django.core.paginator import Paginator
from rest_framework import viewsets,mixins
from .serializers import BooksSerializer
from django_redis import get_redis_connection



# Create your views here.

# 前后端分离部分的代码
class BooksViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer






def book_list(request,type_id,page):
    sort = request.GET.get('sort','default')
    if int(type_id) not in BOOKS_TYPE.keys():
        return redirect(reverse('index'))

    books_li = Books.objects.get_books_by_type(type_id=type_id,sort=sort)

    paginator = Paginator(books_li,1)
    num_pages = paginator.num_pages
    if page == '' or int(page)>num_pages:
        page = 1
    else:
        page = int(page)
    books_li = paginator.page(page)
    
    if num_pages < 5:
        pages = range(1,num_pages+1)
    elif page <=3:
        pages = range(1,6)
    elif num_pages - page <=2:
        pages = range(num_pages-4,num_pages+1)
    else:
        pages = range(page-2,page+3)

    books_new = Books.objects.get_books_by_type(type_id=type_id,limit=2,sort='new')
    type_title = BOOKS_TYPE[int(type_id)]
    context = {
        'books_li':books_li,
        'books_new':books_new,
        'type_id':type_id,
        'sort':sort,
        'type_title':type_title,
        'pages':pages
    } 
    
    return render(request,'list.html',context)
    

def book_detail(request,book_id):
    books = Books.objects.get_books_by_id(books_id=book_id)
    if books is None:
        return redirect(reverse('index'))
    books_li = Books.objects.get_books_by_type(type_id=books.type_id,limit=2,sort='new')

    if request.session.has_key('islogin'):
        conn = get_redis_connection('default')
        key = 'history_%d' % request.session.get('passport_id')
        conn.lrem(key,0,books.id)
        conn.lpush(key,books.id)
        conn.ltrim(key,0,4)
    

    type_title = BOOKS_TYPE[books.type_id]

    context = {'books':books,'books_li':books_li,'type_title':type_title}
    
    return render(request,'detail.html',context)
    
