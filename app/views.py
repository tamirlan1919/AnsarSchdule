from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Schedule, ExtraLesson
from .serializers import ScheduleSerializer, ExtraLessonSerializer
from datetime import datetime

from drf_spectacular.utils import extend_schema

class AvailableSlotsView(APIView):
    """Получить список доступных слотов"""

    @extend_schema(
        summary="Получить доступные слоты",
        description="Возвращает список всех доступных слотов для бронирования.",
        responses={
            200: ScheduleSerializer(many=True),
            400: "Ошибка запроса",
        },
    )
    def get(self, request):
        available_slots = Schedule.objects.filter(is_online=False)
        serializer = ScheduleSerializer(available_slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookSlotView(APIView):
    """Забронировать слот"""

    @extend_schema(
        summary="Забронировать слот",
        description="Позволяет забронировать слот по ID.",
        request={"type": "object", "properties": {"slot_id": {"type": "string"}}},
        responses={
            200: {"type": "object", "properties": {"success": {"type": "string"}}},
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
            404: {"type": "object", "properties": {"error": {"type": "string"}}},
        },
    )
    def post(self, request):
        slot_id = request.data.get("slot_id")
        if not slot_id:
            return Response({"error": "Не указан ID слота"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            slot = Schedule.objects.get(id=slot_id)
            return Response({"success": "Слот забронирован"}, status=status.HTTP_200_OK)
        except Schedule.DoesNotExist:
            return Response({"error": "Слот не найден"}, status=status.HTTP_404_NOT_FOUND)
