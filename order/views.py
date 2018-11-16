from django.shortcuts import render
from utils.decorators import login_required
from django.db import transaction


@login_required
def order_place(request):
    books_ids = request.POST.getlist('books_ids')
    
    if not all(books_ids):
        return redirect(reverse('cart:carts_show'))

    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)

    books_li = []
    total_count = 0
    total_price = 0

    conn = get_redis_connection('default')
    cart_key = 'cart_%id' % passport_id

    for id in books_ids:
        books = Books.objects.get_books_by_id(books_id=id)
        count = conn.hget(cart_key,id)
        books.count = count
        amount = int(count) * books.price
        books.amount = amount
        books_li.append(books)

        total_count += int(count)
        total_price += books.amount

    transit_price = 10
    total_pay = total_price + transit_price

    books_ids = ','.join(books_ids)
    context = {
        'addr':addr,
        'books_li':books_li,
        'total_count':total_count,
        'total_price':total_price,
        'transit_price':transit_price,
        'total_pay':total_pay,
        'books_ids':books_ids,
    }

    return render(request,'place_order.html',context)



@transaction.atomic
def order_commit(request):
    if not request.session.has_key('islogin'):
        return JsonResponse({'res':0,'errmsg':'用户未登录'})
    
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    books_ids = request.POST.get('books_ids')
    
    if not all([addr_id,pay_method,books_ids]):
        return JsonResponse({'res':1,'errmsg':'数据不完整'})
    try:
        addr = Address.objects.get(id=addr_id) 
    except Exception as e :
        return JsonResponse({'res':2,'errmsg':'地址信息错误'})
    
    if int(pay_method) not in OrderInfo.PAY_METHODS_ENUM.values():
        return JsonResponse({'res':3,'errmsg':'不支持的支付方式'})
        
    passport_id = request.session.get('passport_id')
    order_id = datetime.now().strftime('%Y%m%d%')
