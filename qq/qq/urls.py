"""qq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # TODO: test
    path('get_test/', views.get_test),  # 响应get文本请求
    path('post_test/', views.post_test),  # 响应post文本请求
    path('post_file_test/', views.upload_file),  # 响应get文件请求
    path('test_file/',views.test_file),

    # TODO: chat
    path('', include('chat.urls'))
]
