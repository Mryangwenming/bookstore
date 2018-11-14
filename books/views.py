from django.shortcuts import render,redirect,reverse
from .models import Books
from .enums import *

# Create your views here.

def book_list(request):
        
    return render(request,'list.html')


def book_detail(request,book_id):
    books = Books.objects.get_books_by_id(books_id=book_id)
    if books is None:
        return redirect(reverse('index'))
    books_li = Books.objects.get_books_by_type(type_id=books.type_id,limit=2,sort='new')
    type_title = BOOKS_TYPE[books.type_id]

    context = {'books':books,'books_li':books_li,'type_title':type_title}
    
    return render(request,'detail.html',context)
    
