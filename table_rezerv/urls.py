from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from table_rezerv.apps import TableRezervConfig
#from table_rezerv.views import ()

app_name = TableRezervConfig.name

urlpatterns = [
                  #path('', index, name='index'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)