from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls'), name='users'),
    path('', include('main.urls'), name='main'),
    path('reservation/', include('table_rezerv.urls'), name='table_rezerv'),
]
