"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import user_register,user_login,user_logout,user_center_info,user_address,user_order,verifycode,user_active

urlpatterns = [
    url(r'user_register/$',user_register,name='user_register'),
    url(r'user_login/$',user_login,name='user_login'),
    url(r'user_logout/$',user_logout,name='user_logout'),
    url(r'user_center_info/$',user_center_info,name='user_center_info'),    
    url(r'user_address/$',user_address,name='user_address'),
    url(r'user_order/(?P<page>\d+)/$',user_order,name='user_order'),
    url(r'verifycode/$', verifycode, name='verifycode'),
    url(r'user_active/$',user_active,name='user_active')
]
