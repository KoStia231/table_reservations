from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main.apps import MainConfig
from main.views import (
    IndexView, AboutView
)

app_name = MainConfig.name

urlpatterns = [
                  path('', IndexView.as_view(), name='index'),
                  path('about/', AboutView.as_view(), name='about'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
