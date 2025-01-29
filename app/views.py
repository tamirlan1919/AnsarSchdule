from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Schedule, ExtraLesson
from .serializers import ScheduleSerializer, ExtraLessonSerializer
from datetime import datetime

from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .models import Schedule, ExtraLesson
from .serializers import ScheduleSerializer, ExtraLessonSerializer

class OccupiedRoomsView(APIView):
    """Получить список занятых помещений с расписанием и доп. уроками"""

    @extend_schema(
        summary="Получить занятые помещения",
        description="Возвращает список всех занятий, включая регулярное расписание и дополнительные уроки.",
        responses={
            200: ScheduleSerializer(many=True),
            400: "Ошибка запроса",
        },
    )
    def get(self, request):
        schedule_entries = Schedule.objects.all()
        extra_lessons = ExtraLesson.objects.all()

        schedule_data = ScheduleSerializer(schedule_entries, many=True).data
        extra_lesson_data = ExtraLessonSerializer(extra_lessons, many=True).data

        combined_data = schedule_data + extra_lesson_data

        return Response(combined_data, status=status.HTTP_200_OK)

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
