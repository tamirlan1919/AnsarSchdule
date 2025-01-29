from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

#
# 1) Универсальная функция для проверки занятости аудитории
#
def is_room_available(room, date, start_time, end_time, exclude_schedule_id=None, exclude_extra_id=None):
    """
    Проверяем, свободна ли аудитория 'room' в указанный день/время,
    учитывая и обычные занятия (Schedule), и дополнительные (ExtraLesson).

    exclude_schedule_id / exclude_extra_id -- позволяют исключить
    текущую запись (если мы её редактируем), чтобы не находить конфликт
    самой с собой.
    """
    # Проверка конфликтов с `Schedule`
    schedule_conflicts = Schedule.objects.filter(
        room=room,
        repeat_days__day=date.weekday(),
        start_time__lt=end_time,
        end_time__gt=start_time,
        is_online=False
    )
    if exclude_schedule_id:
        schedule_conflicts = schedule_conflicts.exclude(pk=exclude_schedule_id)

    if schedule_conflicts.exists():
        return False

    # Проверка конфликтов с `ExtraLesson`
    extra_conflicts = ExtraLesson.objects.filter(
        room=room,
        date=date,
        start_time__lt=end_time,
        end_time__gt=start_time,
        is_online=False
    )
    if exclude_extra_id:
        extra_conflicts = extra_conflicts.exclude(pk=exclude_extra_id)

    return not extra_conflicts.exists()

#
# 2) Модели
#
class Teacher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя преподавателя")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(blank=True, verbose_name="Описание курса")
    duration = models.DurationField(verbose_name="Продолжительность занятия")

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название аудитории")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость аудитории")

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя ученика")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")
    is_individual = models.BooleanField(default=False, verbose_name="Индивидуальное обучение")

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название группы")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    students = models.ManyToManyField(Student, blank=True, verbose_name="Ученики")

    def __str__(self):
        return self.name

class DayOfWeek(models.Model):
    DAYS = [
        (0, "Понедельник"),
        (1, "Вторник"),
        (2, "Среда"),
        (3, "Четверг"),
        (4, "Пятница"),
        (5, "Суббота"),
        (6, "Восрксенье"),
    ]

    day = models.IntegerField(choices=DAYS, unique=True, verbose_name="День недели")

    def __str__(self):
        return dict(self.DAYS)[self.day]

class Schedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Группа")
    repeat_days = models.ManyToManyField(DayOfWeek, blank=True, verbose_name="Повторяемые дни недели")
    start_date = models.DateField(verbose_name="Дата начала повторений", blank=True, null=True)
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    is_online = models.BooleanField(default=False, verbose_name="Онлайн")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Аудитория")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "start_date", "start_time"],
                name="unique_teacher_start_time"
            )
        ]

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("Время окончания не может быть раньше или равно времени начала.")

    def __str__(self):
        room_str = "Онлайн" if self.is_online else (self.room.name if self.room else "без аудитории")
        return f"{self.course.name} [{room_str}]"

class ExtraLesson(models.Model):
    student = models.CharField(max_length=200, blank=True, default=None)
    groupe = models.CharField(max_length=30, blank=True, default=None)
    date = models.DateField(verbose_name="Дата дополнительного занятия")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name='Аудитория',
        null=True,
        blank=True
    )
    is_online = models.BooleanField(
        default=False,
        verbose_name="Онлайн-формат"
    )

    class Meta:
        unique_together = ('groupe', 'date', 'start_time')
        verbose_name = "Дополнительное занятие"
        verbose_name_plural = "Дополнительные занятия"

    def clean(self):
        # Проверяем, что время окончания позже времени начала
        if self.end_time <= self.start_time:
            raise ValidationError("Время окончания не может быть раньше или равно времени начала.")

        # Если урок онлайн, пропускаем проверку аудитории
        if self.is_online:
            return

        # Проверяем наличие аудитории для оффлайн-уроков
        if not self.room:
            raise ValidationError("Для оффлайн-занятий необходимо указать аудиторию.")

        # Проверяем доступность аудитории
        if not is_room_available(
                room=self.room,
                date=self.date,
                start_time=self.start_time,
                end_time=self.end_time,
                exclude_extra_id=self.pk
        ):
            raise ValidationError("Аудитория занята в указанное время.")

    def __str__(self):

        return f"Доп. занятие для {self.student} — {self.date}"
