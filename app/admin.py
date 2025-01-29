from django.contrib import admin
from .models import (
    Teacher,
    Course,
    Room,
    Student,
    Group,
    DayOfWeek,
    Schedule,
    ExtraLesson
)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "duration")
    search_fields = ("name", )

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity")
    search_fields = ("name", )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_individual")
    search_fields = ("name", "email")

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "course")
    search_fields = ("name", "course__name")

@admin.register(DayOfWeek)
class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ("day", )
    # Отдельный словарь/отображение можно сделать, если нужно вывести "Monday", "Tuesday" и т.д.

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    # Вместо 'date' в list_display укажем метод 'get_repeat_days'
    list_display = (
        "course",
        "teacher",
        "get_repeat_days",   # <- наше виртуальное поле
        "start_time",
        "end_time",
        "is_online",
        "room"
    )

    # Если дата всё же нужна, добавьте в конец:
    # "date",

    search_fields = ("course__name", "teacher__name")
    list_filter = ("is_online", "room", "repeat_days")

    def get_repeat_days(self, obj):
        """
        Возвращает строку из перечисленных дней недели,
        например: "Monday, Wednesday, Friday".
        """
        days = obj.repeat_days.all()  # М2М к DayOfWeek
        # Превращаем каждое DayOfWeek в человекочитаемую строку (__str__)
        day_names = [str(day) for day in days]
        return ", ".join(day_names)

    get_repeat_days.short_description = "Дни недели"
@admin.register(ExtraLesson)
class ExtraLessonAdmin(admin.ModelAdmin):
    list_display = ("groupe", "student", "date", "start_time", "end_time", 'room')
    search_fields = ("schedule__course__name", "student__name")
    list_filter = ("date", )
