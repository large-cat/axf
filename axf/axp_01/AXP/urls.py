from AXP import views
from django.conf.urls import url

urlpatterns = [
    url(r'^hello/', views.hello, name='hello'),
    url(r'^home/', views.home, name='home'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^market/(?P<typeid>.*)/(?P<childtypeid>.*)/(?P<sort_num>\d)/', views.market, name='market'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^check_user/', views.check_user, name='check_user'),
    url(r'^login_out/', views.login_out, name='login_out'),
    url(r'^active/', views.active, name='active'),
    url(r'^do_active/', views.do_active, name='do_active'),
    url(r'^order_deal/', views.order_deal, name='order_deal'),
    url(r'^pay/', views.pay, name='pay'),
    url(r'^order_inquiry', views.order_inquiry, name='order_inquiry'),

]
