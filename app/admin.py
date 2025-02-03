from django.contrib import admin
from .models import Group, Teacher, Classroom, Schedule, ExtraLesson

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_closed', 'is_online', 'is_individual')
    list_filter = ('is_closed', 'is_online', 'is_individual')
    search_fields = ('name',)
    list_editable = ('is_closed', 'is_online', 'is_individual')
    list_per_page = 20

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')
    search_fields = ('name', 'surname')
    list_per_page = 20

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('room_number',)
    search_fields = ('room_number',)
    list_per_page = 20

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('group', 'teacher', 'classroom', 'start_time', 'end_time', 'repeat_weekly', 'weekday')
    list_filter = ('group', 'teacher', 'classroom', 'repeat_weekly', 'weekday')
    search_fields = ('group__name', 'teacher__name', 'teacher__surname', 'classroom__room_number')
    list_editable = ('repeat_weekly',)
    list_per_page = 20
    actions = ['make_repeat_weekly', 'remove_repeat_weekly']

    @admin.action(description="Сделать повторяемым еженедельно")
    def make_repeat_weekly(self, request, queryset):
        queryset.update(repeat_weekly=True)

    @admin.action(description="Убрать повторение еженедельно")
    def remove_repeat_weekly(self, request, queryset):
        queryset.update(repeat_weekly=False)

@admin.register(ExtraLesson)
class ExtraLessonAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'classroom', 'date', 'start_time', 'end_time', 'is_online')
    list_filter = ('is_online', 'date')
    search_fields = ('teacher__name', 'teacher__surname', 'classroom__room_number')
    date_hierarchy = 'date'
    list_per_page = 20
