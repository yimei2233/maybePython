"""
URL configuration for games4399 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('index/',views.index),
    path('login/',views.login),
    path('table_complete/',views.table_complete),
    path('add/',views.add),
    path('revise/',views.revise),
    path('register/',views.register),
    path('register/',views.register),
    path('table/',views.table),
    path('reinfo/',views.reinfo),
    path('tips/',views.tips),



    path('handle_login/',views.handle_login),
    path('handle_delete/',views.handle_delete),
    path('handle_deletes/',views.handle_deletes),
    path('handle_add/',views.handle_add),
    path('handle_revise/',views.handle_revise),
    path('handle_register/',views.handle_register),
    path('handle_reinfo/',views.handle_reinfo),


    # 可视化展示
    path('echart/',views.echart),
    path('handle_one/',views.handle_one),
    path('handle_two/',views.handle_two),
    path('handle_three/',views.handle_three),
    path('handle_four/',views.handle_four),
    path('handle_five/',views.handle_five),
]
