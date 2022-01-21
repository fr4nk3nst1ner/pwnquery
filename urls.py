from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
import leakedpasswords
import leakedpasswords.leaked_passwords_api
from leakedpasswords.leaked_passwords_api import LeakedPasswordViewset 
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from leakedpasswords import leaked_passwords_api

router = DefaultRouter()
router.register(r'leakedpasswords', leaked_passwords_api.LeakedPasswordViewset, basename='api')
#router.register(r'id', leaked_passwords_api.LeakedPasswordViewset, basename='id')
#router.register(r'username', leaked_passwords_api.LeakedPasswordViewset, basename='username')
#router.register(r'password', leaked_passwords_api.LeakedPasswordViewset, basename='password')
#router.register(r'domain', leaked_passwords_api.LeakedPasswordViewset, basename='domain')
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', include(router.urls)),
]
