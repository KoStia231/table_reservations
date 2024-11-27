from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from table_rezerv.apps import TableRezervConfig
from table_rezerv.views import (
    TableView, ReservationCreateView,
    ReservationConfirmView, ReservationCancelView,
    ReservationChangeView
)

app_name = TableRezervConfig.name

urlpatterns = [
                  path('', TableView.as_view(), name='index'),
                  path('reservation-create/<int:table_pk>', ReservationCreateView.as_view(), name='reservation_create'),
                  path('reservation-change/<int:pk>', ReservationChangeView.as_view(), name='reservation_change'),

                  path('reservation-confirm/<int:pk>', ReservationConfirmView.as_view(), name='reservation_confirm'),
                  path('reservation-cancel/<int:pk>', ReservationCancelView.as_view(), name='reservation_cancel'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
