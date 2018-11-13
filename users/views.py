import re
from django.shortcuts import render,redirect,reverse
from .models import Passport

# Create your views here.

def index(request):
    python_new = Books.objects.get_books_by_type(PYTHON,limit=3,sort='new')
    python_hot = Books.objects.get_books_by_type(PYTHON,limit=4,sort='hot')
    javascript_new = Books.objects.get_books_by_type(JAVASCRIPT,limit=3,sort='new')
    javascript_hot = Books.objects.get_books_by_type(JAVASCRIPT,limit=4,sort='hot')
    algorithms_new = Books.objects.get_books_by_type(ALGORITHMS,3,sort='new')
    algotithms_hot = Books.objects.get_books_by_type(ALGORITHMS,4,sort='hot')    
    machinelearning_new = Books.objects.get_books_by_type(MACHINELEARNING,3,sort='new')
    machinelearning_hot = Books.objects.get_books_by_type(MACHINELEARNING,4,sort='hot')
    operationssysterm_new = Books.objects.get_books_by_type(OPRETIONSSYSTERM,3,sort='new')
    operationssysterm_hot = Books.objects.get_books_by_type(OPERATIONSSYSTERM,4,sort='hot')
    database_new = Books.objects.get_books_by_type(OPERATIONSSYSTERM,3,sort='new')
    database_hot = Books.objects.get_books_by_type(OPERATIONSSYSTERM,4,sort='hot')
    
    context = {
        'python_new':python_new,
        'python_hot':python_hot,
        'javascript_new':javascript_new,
        'javascript_hot':javascript_hot,
        'algorithms_new':algotithms_new,
        'algorithms_hot':algorithms_hot,
        'machinelearning_new':machinelearning_new,
        'machinelearning_hot':machinelearning_hot,
        'operationssysterm_new':operationssysterm_new,
        'operationssysterm_hot':operationssysterm_hot,
        'database_new':database_new,
        'database_hot':database_hot
    
    }

    return render(request,'index.html',content)


def user_register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if not all([username,password,email]):
            return render(request,'register.html',{'msg':'参数不能为空!'})
        if not re.match(r'^[a-z0-9][\w\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request,'register.html',{'msg':'邮箱不合法!'})
        try:
            Passport.objects.add_one_passport(username=username,password=password,email=email)
        except Exception as e:
            print(e)
            return render(request,'register.html',{'msg':'用户名已存在!'})
        
        return redirect(reverse('users:user_register'))
 
