from rest_framework import serializers
from .models import Schedule, ExtraLesson, Teacher, Course, Room, DayOfWeek


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['name']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name']

class ScheduleSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    repeat_days = serializers.SerializerMethodField()

    def get_repeat_days(self, obj):
        """Преобразует repeat_days в список названий дней недели."""
        return [dict(DayOfWeek.DAYS)[day.day] for day in obj.repeat_days.all()]

    class Meta:
        model = Schedule
        fields = ['id', 'teacher', 'course', 'repeat_days', 'start_time', 'end_time', 'is_online', 'room']



class ExtraLessonSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    class Meta:
        model = ExtraLesson
        fields = ['id', 'groupe', 'student', 'date', 'start_time', 'end_time', 'room', 'is_online']
