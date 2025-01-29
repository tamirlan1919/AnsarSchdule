from rest_framework import serializers
from .models import Schedule, ExtraLesson, Teacher, Course, Room

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']  # Добавь нужные поля

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']  # Добавь нужные поля

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity']  # Добавь нужные поля

class ScheduleSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)  # Вложенный сериализатор для преподавателя
    course = CourseSerializer(read_only=True)  # Вложенный сериализатор для курса
    room = RoomSerializer(read_only=True)  # Вложенный сериализатор для аудитории

    class Meta:
        model = Schedule
        fields = ['id', 'teacher', 'course', 'repeat_days', 'start_time', 'end_time', 'is_online', 'room']

class ExtraLessonSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)  # Вложенный сериализатор для аудитории

    class Meta:
        model = ExtraLesson
        fields = ['id', 'groupe', 'student', 'date', 'start_time', 'end_time', 'room', 'is_online']
