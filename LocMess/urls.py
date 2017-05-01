"""LocMess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from users import views as user_views
from location import views as location_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/user/create', user_views.create_user),
    url(r'^api/user/test/login', user_views.test_login),
    url(r'^api/user/login', obtain_jwt_token),
    url(r'^api/location/create', location_views.create_location),
    url(r'^api/location/list', location_views.list_locations),
    url(r'^api/location/delete', location_views.delete_location),
]
