import re
from django.shortcuts import render,redirect,reverse
from .models import Passport,Address
from books.enums import *
from books.models import Books
from django.http import JsonResponse
from utils.decorators import login_required
from order.models import OrderInfo,OrderGoods
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from bookstore import settings
from django.core.mail import send_mail
from users.tasks import send_active_email

# Create your views here.


@cache_page(60)
def index(request):
    python_new = Books.objects.get_books_by_type(PYTHON,limit=3,sort='new')
    python_hot = Books.objects.get_books_by_type(PYTHON,limit=4,sort='hot')
    javascript_new = Books.objects.get_books_by_type(JAVASCRIPT,limit=3,sort='new')
    javascript_hot = Books.objects.get_books_by_type(JAVASCRIPT,limit=4,sort='hot')
    algorithms_new = Books.objects.get_books_by_type(ALGORITHMS,limit=3,sort='new')
    algorithms_hot = Books.objects.get_books_by_type(ALGORITHMS,limit=4,sort='hot')    
    machinelearning_new = Books.objects.get_books_by_type(MACHINELEARNING,limit=3,sort='new')
    machinelearning_hot = Books.objects.get_books_by_type(MACHINELEARNING,limit=4,sort='hot')
    operationssysterm_new = Books.objects.get_books_by_type(OPERATIONSSYSTERM,limit=3,sort='new')
    operationssysterm_hot = Books.objects.get_books_by_type(OPERATIONSSYSTERM,limit=4,sort='hot')
    database_new = Books.objects.get_books_by_type(DATABASE,limit=3,sort='new')
    database_hot = Books.objects.get_books_by_type(DATABASE,limit=4,sort='hot')
    context = {
        'python_new':python_new,
        'python_hot':python_hot,
        'javascript_new':javascript_new,
        'javascript_hot':javascript_hot,
        'algorithms_new':algorithms_new,
        'algorithms_hot':algorithms_hot,
        'machinelearning_new':machinelearning_new,
        'machinelearning_hot':machinelearning_hot,
        'operationssysterm_new':operationssysterm_new,
        'operationssysterm_hot':operationssysterm_hot,
        'database_new':database_new,
        'database_hot':database_hot
    
    }
    return render(request,'index.html',context)


def user_register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if not all([username,password,email]):
            return render(request,'register.html',{'errmsg':'参数不能为空!'})
        if not re.match(r'^[a-z0-9][\w\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request,'register.html',{'errmsg':'邮箱不合法!'})

        
        p = Passport.objects.check_passport(username=username)
        if p:
            return render(request,'register.html',{'errmsg':'用户名已存在!'})
        passport_per = Passport.objects.add_one_passport(username=username,password=password,email=email)

        serializer = Serializer(settings.SECRET_KEY,3600)
        token = serializer.dumps({'confirm':passport_per.id})
        token = token.decode()

        # send_mail('我的书城用户激活','',settings.EMAIL_FROM,[email], html_message='<a href="http://127.0.0.1:8000/users/user_active/%s/">http://127.0.0.1:8000/users/user_active/</a>' % token)
        send_active_email.delay(token,username,email)        

        return redirect(reverse('index'))



def user_login(request):
    if request.method == 'GET':
        if request.COOKIES.get('username'):
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        context = {
            'username':username,
            'checked':checked
        }   
        return render(request,'login.html',context) 

    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        remember = request.POST.get('remember','')
        verifycode = request.POST.get('verifycode') 
        if not all([username,password,remember]):
            return JsonResponse({'res':2})


        if verifycode.upper() != request.session['verifycode']:
            return JsonResponse({'res': 2})
     
        passport = Passport.objects.get_one_passport(username=username,password=password)
    
        if passport:
            next_url = reverse('index')
            jres  = JsonResponse({'res':1,'next_url':next_url})
            if remember == 'true':
                jres.set_cookie('username',username,max_age=7*24*3600)
            else:
                jres.delete_cookie('username')
        
            request.session['islogin'] = True
            request.session['username'] = username
            request.session['passport_id'] = passport.id
            return jres
        else:
            return JsonResponse({'res':0})

                
def user_logout(request):
    request.session.flush()
    return redirect(reverse('index'))


@login_required
def user_center_info(request):
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)
    books_li = []
    context = {
        'addr':addr,
        'page':'user',  # 这里面是用来判断css跟随的
        'books_li':books_li
    }
    return render(request,'user_center_info.html',context)



@login_required
def user_address(request):
    passport_id = request.session.get('passport_id')
    
    if request.method == 'GET':
        addr = Address.objects.get_default_address(passport_id=passport_id)
        return render(request,'user_center_site.html',{'addr':addr,'page':'address'})
    else:
        recipient_name = request.POST.get('username')
        recipient_addr = request.POST.get('address')
        zip_code = request.POST.get('code')
        recipient_phone = request.POST.get('phone')

        if not all([recipient_name,recipient_addr,zip_code,recipient_phone]):
            return render(request,'user_center_site.html',{'errmsg':'参数不能为空'})
        Address.objects.add_one_address(
                    passport_id=passport_id,
                    recipient_name=recipient_name,
                    recipient_addr=recipient_addr,
                    zip_code=zip_code,
                    recipient_phone=recipient_phone)

        return redirect(reverse('users:user_address'))



@login_required
def user_order(request,page):
    passport_id = request.session.get('passport_id')
    order_li = OrderInfo.objects.filter(passport_id=passport_id)
    for order in order_li:
        order_id = order.order_id
        order_books_li = OrderGoods.objects.filter(order_id=order_id)
        for order_books in order_books_li:
            count = order_books.count
            price = order_books.price
            amount = count * price
            order_books.amount = amount
        
        order.order_books_li = order_books_li
    
    pa = Paginator(order_li,3)
    num_pages = pa.num_pages
    if not page:
        page = 1
    if page == '' or int(page) > num_pages:
        page = 1
    else:
        page = int(page)
    order_li = pa.page(page)
    if num_pages < 5:
        pages = range(1,num_pages + 1)
    elif page <= 3:
        pages = range(1,6)
    elif num_pages - page <=2:
        pages = range(num_pages-4,num_pages+1)
    else:
        pages = range(page -2 ,page + 3)
    context = {
        'order_li':order_li,
        'pages':pages,
    }

    return render(request,'user_center_order.html',context)



from django.http import HttpResponse
from django.conf import settings
import os
def verifycode(request):
    from PIL import Image, ImageDraw, ImageFont
    import random
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype(os.path.join(settings.BASE_DIR, "Ubuntu-RI.ttf"), 15)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    del draw
    request.session['verifycode'] = rand_str
    import io
    buf = io.BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')
