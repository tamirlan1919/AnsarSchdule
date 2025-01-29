from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .views import OccupiedRoomsView, BookSlotView

urlpatterns = [
    path('slots/', OccupiedRoomsView.as_view(), name='available_slots'),
    path('slots/book/', BookSlotView.as_view(), name='book_slot'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
