from django.db import models
from django.forms import Form, fields
from ckeditor.fields import RichTextField


# Create your models here.

class buyer(models.Model):
    choice_sex = (
        (0, "男"),
        (1, "女"),
    )
    choice_state = (
        (0, "正常"),
        (1, "冻结"),
    )
    account = models.CharField(u'账号', max_length=15, unique=True, null=False)
    pwd = models.CharField(u'密码', max_length=20, null=False)
    birth = models.DateField(u'生日', default=None, null=True)
    email = models.EmailField(u'邮箱', default=None, null=True)
    nickname = models.CharField(u'昵称', max_length=16, null=True)
    sex = models.IntegerField(u'性别', choices=choice_sex, default=None, null=True)
    balance = models.IntegerField(u'余额', default=0, null=True)
    preference = models.CharField(u'偏好', 'Preference', max_length=1024, default=None, null=True)
    state = models.IntegerField(u'状态', choices=choice_state, default=None, null=True)
    address = models.TextField(u'地址', 'Address', default=None, null=True)
    headimg = models.ImageField(u'头像', upload_to='img/', null=True)


class seller(models.Model):
    choice_sex = (
        (0, "男"),
        (1, "女"),
    )
    choice_state = (
        (0, "正常"),
        (1, "冻结"),
    )
    account = models.CharField(u'账号', max_length=15, unique=True, null=False)
    pwd = models.CharField(u'密码', max_length=20, null=False)
    birth = models.DateField(u'生日', default=None, null=True)
    email = models.EmailField(u'邮箱', default=None, null=True)
    nickname = models.CharField(u'昵称', max_length=16, null=True)
    sex = models.IntegerField(u'性别', choices=choice_sex, default=None, null=True)
    balance = models.CharField(u'余额', max_length=16, default=0)
    preference = models.CharField(u'偏好', 'Preference', max_length=1024, default=None, null=True)
    state = models.IntegerField(u'状态', choices=choice_state, default=None, null=True)
    address = models.TextField(u'地址', default=None, null=True)
    headimg = models.ImageField(u'头像', upload_to='img/', null=True)


class goods(models.Model):
    title = models.CharField(u'商品名', default=None, null=True, max_length=128)
    label = models.CharField(u'标签', max_length=1024, default=None, null=True)
    inventory = models.IntegerField(u'库存', default=None, null=True)
    price = models.IntegerField(u'价格', default=None, null=True)
    details = models.TextField(u'详情', max_length=1024, default=None, null=True)
    seller = models.CharField(u'卖家', 'seller', max_length=1024, default=None, null=True)
    comments = models.CharField(u'评论', max_length=128, default=None, null=True)
    state = models.IntegerField(u'状态', default=0, null=True)
    img = models.ImageField(u'图片', upload_to='img/', default=None, null=True)


class Label(models.Model):
    label = models.CharField(u'标签', max_length=1024, default=None, null=True)


class shoppingCart(models.Model):
    good = models.CharField(u'商品', max_length=1024, default=None, null=True)
    good_info = models.ForeignKey(goods, on_delete=models.CASCADE, null=True)
    buyer = models.CharField(u'买家', max_length=1024, default=None, null=True)
    seller = models.CharField(u'卖家', max_length=1024, default=None, null=True)
    price = models.IntegerField(u'价格', default=None, null=True)
    inventory = models.CharField(u'库存', max_length=128, default=None, null=True)
    title = models.CharField(u'商品名', default=None, null=True, max_length=128)


class Address(models.Model):
    buyer = models.CharField(u'买家', max_length=1024, default=None, null=True)
    address = models.CharField(u'地址', max_length=1024, default=None, null=True)


class Order(models.Model):
    goods = models.CharField(u'商品', 'goods', max_length=1024, default=None, null=True)
    buyer = models.CharField(u'买家', 'buyer', max_length=1024, default=None, null=True)
    seller = models.CharField(u'卖家', 'seller', max_length=1024, default=None, null=True)
    receiving_address = models.CharField(u'收货地址', max_length=1024, default=None, null=True)
    number = models.IntegerField(u'数量', default=None, null=True)
    price = models.IntegerField(u'价格', default=None, null=True)
    time = models.DateField(u'下单时间', default=None, null=True)
    state = models.IntegerField(u'状态', default=0, null=True)
    uid = models.CharField(u'订单编号', max_length=128, null=True)


class comments(models.Model):
    owner = models.CharField(u'楼主', max_length=1024, default=None, null=True)
    title = models.CharField(u'标题', max_length=1024, default=None, null=True)
    details = models.TextField(u'详情', max_length=1024, default=None, null=True)
    time = models.DateField(u'下单时间', default=None, null=True)
    content = RichTextField(verbose_name='正文内容', config_name='default', null=True)


class EmailCode(models.Model):
    email = models.EmailField(u'邮箱', default=None, null=True)
    code = models.CharField(u'验证码', max_length=128, default=None, null=False)


class orderGoods(models.Model):
    goodsID = models.IntegerField(u"商品", null=True)
    orderID = models.IntegerField(u"订单", null=True)
