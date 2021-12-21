from django.contrib import admin

# Register your models here.
admin.site.site_header = 'Eshop管理后台'  # 设置header
admin.site.site_title = 'Eshop管理后台'  # 设置title
admin.site.index_title = 'Eshop管理后台'

from .models import *

admin.site.register(goods)
admin.site.register(Order)
admin.site.register(buyer)
admin.site.register(seller)
