from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from django.forms import Form, fields
from django.core.mail import send_mail
from django.urls import reverse
from .models import *
from .models import buyer
import re
from django.contrib.auth.decorators import login_required
import random
from django.utils import timezone
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import login_form, AddForm, CommentForm, ImageFormBuyer, ImageFormSeller
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'index.html')


def homepage(request):
    if request.method == 'GET':
        goods_list = goods.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(goods_list, 5)
        try:
            good = paginator.page(page)
        except PageNotAnInteger:
            good = paginator.page(1)
        except EmptyPage:
            good = paginator.page(paginator.num_pages)
        return render(request, "homepage.html", {"good": good})
    else:
        good_name = request.POST.get('search')
        print(good_name)
        if goods.objects.filter(title=good_name).exists():
            good = goods.objects.filter(title=good_name)
            return render(request, "homepage.html", {"good": good})
        else:
            goods_list = goods.objects.all()
            page = request.GET.get('page', 1)
            paginator = Paginator(goods_list, 5)
            try:
                good = paginator.page(page)
            except PageNotAnInteger:
                good = paginator.page(1)
            except EmptyPage:
                good = paginator.page(paginator.num_pages)
            return render(request, "homepage.html", {"good": good, 'error': '找不到该商品！'})
        # if goods.objects.filter(title=good_name).exists():
        #     id = goods.objects.get(title=good_name)
        #     return redirect('/detail/{}/'.format(id))
        # else:
        #     goods_list = goods.objects.all()
        #     page = request.GET.get('page', 1)
        #     paginator = Paginator(goods_list, 5)
        #     try:
        #         good = paginator.page(page)
        #     except PageNotAnInteger:
        #         good = paginator.page(1)
        #     except EmptyPage:
        #         good = paginator.page(paginator.num_pages)
        # return render(request, "homepage.html", {"good": good, 'error': '找不到该商品'})


def message(request):
    return render(request, 'message.html')


def shopping_cart(request):
    if request.session.get('is_login', None):
        if request.method == 'GET':
            account = request.session.get('account')
            obj = shoppingCart.objects.filter(buyer=account)
            return render(request, 'shopping_cart.html', {'obj': obj})
        elif 'delete' in request.POST:
            id = request.POST.get('delete')
            shoppingCart.objects.filter(id=id).delete()
            account = request.session.get('account')
            obj = shoppingCart.objects.filter(buyer=account)
            return render(request, 'shopping_cart.html', {'obj': obj})
    return redirect('/login/')


def my(request):
    if request.session.get('is_login', None):
        if request.method == "GET":
            account = request.session.get('account')
            identity = request.session.get('identity')
            if identity == 'buyer':
                user = buyer.objects.get(account=account)
                return render(request, 'my.html', {'user': user})
            elif identity == 'seller':
                user = seller.objects.get(account=account)
                return render(request, 'my.html', {'user': user})
            return render(request, 'my.html')
        else:
            return render(request, 'my.html')
    return redirect('/login/')


def MyDetail(request):
    if request.session.get('is_login', None):
        account = request.session.get('account')
        addresses = Address.objects.filter(buyer=account)
        identity = request.session.get('identity')
        if identity == 'buyer':
            user = buyer.objects.get(account=account)
        elif identity == 'seller':
            user = seller.objects.get(account=account)
        return render(request, 'MyDetail.html', {'addresses': addresses, 'user': user})
    return redirect('/login/')


def EditData(request):
    if request.session.get('is_login', None):
        if request.method == 'GET':
            return render(request, 'EditData.html')
        else:
            print('welcome!')
            account = request.session.get('account')
            nickname = request.POST.get('nickname')
            sex = request.POST.get('sex')
            birth = request.POST.get('birth')
            error_info = {'error': ''}
            tmp_nickname = request.session.get('nickname')
            tmp_nickname0 = buyer.objects.filter(nickname=nickname)
            tmp_nickname1 = seller.objects.filter(nickname=nickname)
            if nickname and sex and birth:
                print('welcome')
                if not tmp_nickname0 or not tmp_nickname1 or nickname == tmp_nickname:
                    if seller.objects.filter(account=account).exists():
                        user = seller.objects.get(account=account)
                    elif buyer.objects.filter(account=account).exists():
                        user = buyer.objects.get(account=account)
                    user.nickname = nickname
                    user.sex = sex
                    user.birth = birth
                    user.save()
                    request.session['nickname'] = nickname
                    request.session['sex'] = sex
                    request.session['birth'] = birth
                    print('Correct')
                    return redirect('/my/MyDetail/')
                else:
                    error_info['error'] = '该昵称已存在！'
                    print('wrong')
                    return render(request, 'EditData.html', error_info)
            else:
                error_info['error'] = '不能为空'
                return render(request, "EditData.html", error_info)
    return redirect('/login/')


def EditEmail(request):
    if request.method == 'GET':
        return render(request, 'EditEmail.html')
    else:
        tmp_code = get_random_data()
        if 'register' in request.POST:
            account = request.session.get('account')
            email = request.POST.get('email')
            code = request.POST.get('code')
            error_info = {'error': ''}
            try:
                obj = EmailCode.objects.filter(email=email)[0]
                if obj:
                    tmp_code = obj.code
                    tmp_email = obj.email
            except:
                error_info['您还未发送验证码']
                return render(request, "EditEmail.html", error_info)
            if account and email:
                if not re.match('\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*', email):
                    error_info['error'] = '邮箱不符合规范！'
                    return render(request, 'EditEmail.html', error_info)
                elif code != tmp_code or email != tmp_email:
                    error_info['error'] = '邮箱验证码错误！'
                    return render(request, "EditEmail.html", error_info)
                else:
                    EmailCode.objects.filter(email=email).delete()
                    return redirect('/my/MyDetail/')
            else:
                error_info['error'] = '不能为空'
                return render(request, "EditEmail.html", error_info)
        elif 'email' in request.POST:
            email = request.POST.get('emails')
            try:
                EmailCode.objects.filter(email=email).delete()
            except:
                print('wrong')
            if email:
                messages.success(request, '发送成功')
                send_email(request, tmp_code)
                obj = EmailCode()
                obj.email = email
                obj.code = tmp_code
                obj.save()
            else:
                messages.error(request, '请先输入邮箱')
            # return redirect('/register/', messages)
            return render(request, "EditEmail.html")
        else:
            return render(request, "EditEmail.html")


def recharge(request):
    if request.session.get('is_login', None):
        if request.method == 'GET':
            return render(request, 'recharge.html')
        elif '6' in request.POST:
            account = request.session.get('account')
            tmp = buyer.objects.get(account=account)
            tmp.balance += 6
            tmp.save()
            request.session['balance'] = tmp.balance
            return redirect('/my/MyDetail/')
        elif '18' in request.POST:
            account = request.session.get('account')
            tmp = buyer.objects.get(account=account)
            tmp.balance += 18
            tmp.save()
            request.session['balance'] = tmp.balance
            return redirect('/my/MyDetail/')
        elif '68' in request.POST:
            account = request.session.get('account')
            tmp = buyer.objects.get(account=account)
            tmp.balance += 68
            tmp.save()
            request.session['balance'] = tmp.balance
            return redirect('/my/MyDetail/')
        elif '233' in request.POST:
            account = request.session.get('account')
            tmp = buyer.objects.get(account=account)
            tmp.balance += 233
            tmp.save()
            request.session['balance'] = tmp.balance
            return redirect('/my/MyDetail/')
        elif '648' in request.POST:
            account = request.session.get('account')
            tmp = buyer.objects.get(account=account)
            tmp.balance += 648
            tmp.save()
            request.session['balance'] = tmp.balance
            return redirect('/my/MyDetail/')
        elif '998' in request.POST:
            account = request.session.get('account')
            tmp = buyer.objects.get(account=account)
            tmp.balance += 998
            tmp.save()
            request.session['balance'] = tmp.balance
            return redirect('/my/MyDetail/')
        else:
            money = request.POST.get('money')
            account = request.session.get('account')
            error_info = {'error': ''}
            if not re.match('^\d{1,5}$', money):
                error_info['error'] = '金额不符合规范'
                return render(request, 'recharge.html', error_info)
            else:
                tmp = buyer.objects.get(account=account)
                tmp.balance += int(money)
                tmp.save()
                request.session['balance'] = tmp.balance
                return render(request, 'recharge.html')
    return redirect('/login/')


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        tmp_code = get_random_data()
        if 'register' in request.POST:
            account = request.POST.get('account')
            pwd0 = request.POST.get('pwd0')
            pwd1 = request.POST.get('pwd1')
            email = request.POST.get('emails')
            birth = request.POST.get('birth')
            nickname = request.POST.get('nickname')
            sex = request.POST.get('sex')
            identity = request.POST.get('identity')
            code = request.POST.get('code')
            error_info = {'error': ''}
            success_info = {'success': '注册成功，将返回登陆界面'}
            try:
                obj = EmailCode.objects.filter(email=email)[0]
                if obj:
                    tmp_code = obj.code
                    tmp_email = obj.email
            except:
                error_info['您还未发送验证码']
                return render(request, "register.html", error_info)
            tmp_account0 = buyer.objects.filter(account=account)
            tmp_account1 = seller.objects.filter(account=account)
            tmp_nickname0 = buyer.objects.filter(nickname=nickname)
            tmp_nickname1 = seller.objects.filter(nickname=nickname)
            if account and pwd0 and pwd1 and email and birth and nickname and sex:
                if pwd0 != pwd1:
                    error_info['前后密码不一致']
                    return render(request, "register.html", error_info)
                elif tmp_account0 or tmp_account1:
                    error_info['error'] = '该用户已存在！'
                    return render(request, 'register.html', error_info)
                elif tmp_nickname0 or tmp_nickname1:
                    error_info['error'] = '该昵称已存在！'
                    return render(request, 'register.html', error_info)
                elif not re.match('^\w{3,15}$', account):
                    error_info['error'] = '用户名不符合规范！'
                    return render(request, 'register.html', error_info)
                elif not re.match('^\w{6,20}$', pwd0):
                    error_info['error'] = '密码不符合规范！'
                    return render(request, 'register.html', error_info)
                elif not re.match('\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*', email):
                    error_info['error'] = '邮箱不符合规范！'
                    return render(request, 'register.html', error_info)
                elif code != tmp_code or email != tmp_email:
                    error_info['error'] = '邮箱验证码错误！'
                    return render(request, "register.html", error_info)
                else:
                    if identity == 'buyer':
                        users = buyer(account=account, pwd=pwd0, email=email, birth=birth,
                                      nickname=nickname, sex=sex)
                    elif identity == 'seller':
                        users = seller(account=account, pwd=pwd0, email=email, birth=birth,
                                       nickname=nickname, sex=sex)
                    users.save()
                    EmailCode.objects.filter(email=email).delete()
                    return redirect('/login/', success_info)
            else:
                error_info['error'] = '不能为空'
                return render(request, "register.html", error_info)
        elif 'email' in request.POST:
            email = request.POST.get('emails')
            try:
                EmailCode.objects.filter(email=email).delete()
                print('666')
            except:
                print('wrong')
            if email:
                messages.success(request, '发送成功')
                send_email(request, tmp_code)
                obj = EmailCode()
                obj.email = email
                obj.code = tmp_code
                obj.save()
            else:
                messages.error(request, '请先输入邮箱')
            # return redirect('/register/', messages)
            return render(request, "register.html")
        else:
            return render(request, "register.html")


def get_random_data():
    try:
        number = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        for i in range(0, 4):
            number = number + chars[random.randint(0, len(chars))]
        return number
    except:
        get_random_data()


def send_email(request, code):
    email = request.POST.get('emails')
    send_mail(
        subject='请验证您的辅助邮箱',
        message='Eshop\n收到了将 {} 用作 Eshop 帐号 辅助邮箱的请求\n请使用此验证码完成该辅助邮箱的设置：{}'.format(email, code),
        recipient_list=[email],
        fail_silently=False,
    )


def sex_choice(sex):
    if sex == 0:
        return '男'
    if sex == 1:
        return '女'


def login(request):
    if request.method == "GET":
        form = login_form(request.POST)
        return render(request, "login.html", context={'form': form})
    else:
        account = request.POST.get('account')
        password = request.POST.get('password')
        form = login_form(request.POST)
        obj = Form(request.POST)
        if account and password:
            if seller.objects.filter(account=account).exists():
                identity = 'seller'
                user = seller.objects.get(account=account)
            elif buyer.objects.filter(account=account).exists():
                identity = 'buyer'
                user = buyer.objects.get(account=account)
            else:
                return render(request, "login.html", {'error0': 'error0'})
            if not user.pwd == password:
                return render(request, "login.html", {'error1': 'error1'})
            # elif not form.is_valid():
            #     return render(request, "login.html", {'error2': 'error2'})
            else:
                request.session['is_login'] = True
                request.session['account'] = account
                request.session['id'] = user.id
                request.session['identity'] = identity
                request.session['nickname'] = user.nickname
                request.session['birth'] = user.birth.strftime('%Y-%m-%d')
                request.session['email'] = user.email
                request.session['sex'] = sex_choice(user.sex)
                request.session['balance'] = user.balance
                # request.session['headimg'] = user.headimg
                return render(request, "login.html")
        else:
            return render(request, "login.html")


def logout(request):
    if request.session.get('is_login', None):
        request.session.flush()
        return redirect('/')
    return redirect('/login/')


def detail(request, id):
    if request.session.get('is_login', None):
        if request.method == "GET":
            good = goods.objects.get(id=id)
            commentForm = CommentForm()
            obj = comments.objects.filter(title=id)
            return render(request, "detail.html", {"good": good, "obj": obj, 'commentForm': commentForm})
        elif 'buy' in request.POST:
            buyer = request.session.get('account')
            seller = goods.objects.get(id=id).seller
            price = goods.objects.get(id=id).price
            inventory = goods.objects.get(id=id).inventory
            title = goods.objects.get(id=id).title
            tmp = shoppingCart(good=id, buyer=buyer, seller=seller, price=price, inventory=inventory, title=title)
            tmp.save()
            return redirect('/order/')
        elif 'add' in request.POST:
            buyer = request.session.get('account')
            seller = goods.objects.get(id=id).seller
            price = goods.objects.get(id=id).price
            inventory = goods.objects.get(id=id).inventory
            title = goods.objects.get(id=id).title
            shoppingCart.objects.create(good=id, buyer=buyer, seller=seller, price=price, inventory=inventory,
                                        title=title)
            good = goods.objects.get(id=id)
            commentForm = CommentForm()
            obj = comments.objects.filter(title=id)
            return render(request, "detail.html", {"good": good, "obj": obj, 'commentForm': commentForm})
        elif 'comment' in request.POST:
            good = goods.objects.get(id=id)
            nickname = request.session.get('nickname')
            time = timezone.now()
            commentForm = CommentForm(request.POST)
            obj = comments.objects.filter(title=id)
            if commentForm.is_valid():
                comment = commentForm.save(commit=False)
                comment.author = request.user
                comment.owner = nickname
                comment.time = time
                comment.title = id
                comment.save()
            else:
                print('wrong')
            return render(request, 'detail.html', {'good': good, 'obj': obj, 'commentForm': commentForm})
    return redirect('/login/')


def order(request):
    if request.session.get('is_login', None):
        if request.method == "GET":
            account = request.session.get('account')
            good = shoppingCart.objects.filter(buyer=account)
            buyer = request.session.get('nickname')
            addresses = Address.objects.filter(buyer=account)
            return render(request, 'order.html', locals())
        elif 'pay' in request.POST:
            account = request.session.get('account')
            good_info = shoppingCart.objects.filter(buyer=account)
            buyers = request.session.get('account')
            time = timezone.now()
            addresses = Address.objects.filter(buyer=account)
            address = request.POST.get('address')
            orderID = createID()
            error_info = {'error': ''}
            for line in good_info:
                id = line.good
                title = line.title
                seller = line.seller
                price = line.price
                inventory = goods.objects.get(id=id).inventory
                number = int(request.POST.get('number'))
                print(number, '999999999999')
                if number:
                    if number <= inventory:
                        Order.objects.create(uid=orderID, seller=seller, buyer=buyers, time=time, number=number,
                                             price=price, receiving_address=address, goods=title)
                        inventory -= number
                        goods.objects.filter(title=title).update(inventory=inventory)
                        shoppingCart.objects.filter(buyer=account).delete()
                    else:
                        error_info['error'] = '库存不足！'
                        account = request.session.get('account')
                        good = shoppingCart.objects.filter(buyer=account)
                        buyer = request.session.get('nickname')
                        addresses = Address.objects.filter(buyer=account)
                        return render(request, 'order.html', locals())
                else:
                    error_info['error'] = '请输入购买数量！'
                    return render(request, 'order.html', locals())
            return redirect('/real_order/')
        elif 'delete' in request.POST:
            id = request.POST.get('delete')
            shoppingCart.objects.filter(id=id).delete()
            account = request.session.get('account')
            good = shoppingCart.objects.filter(buyer=account)
            buyer = request.session.get('nickname')
            addresses = Address.objects.filter(buyer=account)
            return render(request, 'order.html', locals())
    return redirect('/login/')


def comment(request):
    if request.session.get('is_login', None):
        if request.method == 'GET':
            commentForm = CommentForm()
            return render(request, 'comment.html', {'commentForm': commentForm})
        else:
            commentForm = CommentForm(request.POST)
            if commentForm.is_valid():
                comment = commentForm.save(commit=False)
                comment.author = request.user
                comment.save()
                comment.save_m2m()
                return HttpResponseRedirect(reverse("homepage/"))
            return render(request, 'comment.html', {'commentForm': commentForm})
    return redirect('/login/')


def add(request):
    if request.session.get('is_login', None):
        if request.method == "POST":
            af = AddForm(request.POST, request.FILES)
            account = request.session.get('account')
            if af.is_valid():
                if seller.objects.filter(account=account).exists():
                    # imageForm = ImageFormSeller(request.POST, request.FILES)
                    # imageForm.image = request.FILES.get('image', '')
                    # account = af.cleaned_data['account']
                    headimg = af.cleaned_data['headimg']
                    user = seller.objects.get(account=account)
                    user.headimg = headimg
                elif buyer.objects.filter(account=account).exists():
                    # imageForm = ImageFormBuyer(request.POST, request.FILES)
                    # imageForm.image = request.FILES.get('image', '')
                    # account = af.cleaned_data['account']
                    headimg = af.cleaned_data['headimg']
                    user = buyer.objects.get(account=account)
                    user.headimg = headimg
            else:
                print('wrong')
            user.save()
            return redirect('/my/')
        else:
            af = AddForm()
            return render(request, 'add.html', context={"af": af})
    return redirect('/login/')


def addGoods(request):
    if request.session.get('is_login', None):
        if request.method == "GET":
            labelChoices = Label.objects.all()
            af = AddForm(request.POST, request.FILES)
            return render(request, 'addGoods.html', locals())
            # return render(request, 'addGoods.html')
        else:
            title = request.POST.get('title')
            label = request.POST.get('label')
            number = request.POST.get('number')
            price = request.POST.get('price')
            detail = request.POST.get('detail')
            seller = request.session.get('account')
            af = AddForm(request.POST, request.FILES)
            img = af.cleaned_data['headimg']
            labelChoices = Label.objects.all()
            error_info = {'error': '', 'labelChoices': labelChoices}
            if title and label and number and price and detail:
                if not re.match("^[\u4E00-\u9FA5]{1,20}$", title):
                    error_info['error'] = '商品名称不规范'
                    return render(request, 'addGoods.html', locals())
                elif not re.match("^[\d]{1,4}$", number):
                    error_info['error'] = '数量超出范围'
                    return render(request, 'addGoods.html', locals())
                elif not re.match("^[\d]{1,9}$", price):
                    error_info['error'] = '价格超出范围'
                    return render(request, 'addGoods.html', locals())
                else:
                    goods.objects.create(seller=seller, title=title, Label=label, inventory=number, price=price,
                                         details=detail, img=img)
                    print(11111111)
                    return redirect('/my/')
            else:
                labelChoices = Label.objects.all()
                error_info['error'] = '不能为空'
                return render(request, 'addGoods.html', locals())
    return redirect('/login/')


def createID():
    number = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    for i in range(0, 12):
        number = number + chars[random.randint(0, len(chars))]
    return number


def AddAddress(request):
    if request.session.get('is_login', None):
        if request.method == "GET":
            return render(request, 'AddAddress.html')
        elif request.method == "POST":
            account = request.session.get('account')
            address = request.POST.get('address')
            Address.objects.create(buyer=account, address=address)
            return redirect('/my/MyDetail/')
    return redirect('/login/')


def real_order(request):
    if request.session.get('is_login', None):
        if request.method == "GET":
            account = request.session.get('account')
            if request.session.get('identity') == 'buyer':
                order = Order.objects.filter(buyer=account)
            elif request.session.get('identity') == 'seller':
                order = Order.objects.filter(seller=account)
            return render(request, 'real_order.html', {'order': order})
        else:
            account = request.session.get('account')
            order = Order.objects.filter(buyer=request.session.get('account'))
            Order.objects.filter(buyer=request.session.get('account')).update(state=1)
            if request.session.get('identity') == 'buyer':
                order = Order.objects.filter(buyer=account)
            elif request.session.get('identity') == 'seller':
                order = Order.objects.filter(seller=account)
            return render(request, 'real_order.html', {'order': order})
    return redirect('/login/')
