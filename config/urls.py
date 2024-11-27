from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users'), name='users'),
    path('', include('main.urls', namespace='main'), name='main'),
    path('table-reservation/', include('table_rezerv.urls', namespace='table_rezerv'), name='table_rezerv'),
]
