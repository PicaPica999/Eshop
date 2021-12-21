from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('homepage/', views.homepage, name='homepage'),
    path('message/', views.message, name='message'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('my/', views.my, name='my'),
    path('my/addGoods/', views.addGoods, name='addGoods'),
    path('my/MyDetail/', views.MyDetail, name='MyDetail'),
    path('my/MyDetail/EditEmail/', views.EditEmail, name='EditEmail'),
    path('my/MyDetail/recharge/', views.recharge, name='recharge'),
    path('my/MyDetail/EditData/', views.EditData, name='EditData'),
    path('my/MyDetail/AddAddress/', views.AddAddress, name='AddAddress'),
    path('homepage/detail/<int:id>/', views.detail, name='detail'),
    path('comment/', views.comment, name='comment'),
    path('add/', views.add, name='add'),
    path('logout/', views.logout, name='logout'),
    path('order/', views.order, name='order'),
    path('real_order/',views.real_order, name='real_order'),
]
