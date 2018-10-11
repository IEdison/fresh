
from django.conf.urls import url

from home import views


urlpatterns = [
    # 首页地址
    url(r'^index/', views.index, name='index'),
]