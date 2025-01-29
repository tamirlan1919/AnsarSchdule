from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .views import AvailableSlotsView, BookSlotView

urlpatterns = [
    path('api/slots/', AvailableSlotsView.as_view(), name='available_slots'),
    path('api/slots/book/', BookSlotView.as_view(), name='book_slot'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
