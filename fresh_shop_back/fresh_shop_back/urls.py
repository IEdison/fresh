"""fresh_shop_back URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import static

from fresh_shop_back import settings
from utils.upload_images import upload_image

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # homh模块
    url(r'^home/', include('home.urls', namespace='home')),
    # 商品模块
    url(r'^goods/', include('goods.urls', namespace='goods')),
    # 订单模块
    url(r'^orders/', include('orders.urls', namespace='orders')),
    # 编辑器中图片保存
    url(r'^util/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
]
# 访问media中的静态资源
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

