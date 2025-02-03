from django.db import models
from django.core.exceptions import ValidationError

# Дни недели
WEEKDAYS = [
    ('mon', 'Понедельник'),
    ('tue', 'Вторник'),
    ('wed', 'Среда'),
    ('thu', 'Четверг'),
    ('fri', 'Пятница'),
    ('sat', 'Суббота'),
    ('sun', 'Воскресенье'),
]

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название группы")
    is_closed = models.BooleanField(default=False, verbose_name="Закрытая группа")
    is_online = models.BooleanField(default=False, verbose_name="Онлайн группа")
    is_individual = models.BooleanField(default=False, verbose_name="Индивидуальная группа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

class Teacher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"

class Classroom(models.Model):
    room_number = models.CharField(max_length=50, unique=True, verbose_name="Номер аудитории")

    def __str__(self):
        return self.room_number

    class Meta:
        verbose_name = "Аудитория"
        verbose_name_plural = "Аудитории"

class Schedule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Учитель")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Аудитория")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    repeat_weekly = models.BooleanField(default=True, verbose_name="Повторять еженедельно")
    weekday = models.CharField(max_length=3, choices=WEEKDAYS, verbose_name="День недели")

    def clean(self):
        if self.group.is_online or self.group.is_individual:
            self.classroom = None

        if self.classroom:
            overlapping_schedules = Schedule.objects.filter(
                classroom=self.classroom,
                weekday=self.weekday,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(id=self.id)

            if overlapping_schedules.exists():
                raise ValidationError("Аудитория занята в указанное время.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.group} - {self.teacher} - {self.weekday} ({self.start_time}-{self.end_time})"

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"

class ExtraLesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Учитель")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Аудитория")
    date = models.DateField(verbose_name="Дата урока")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    is_individual = models.CharField(verbose_name="Инициалы студента", max_length=200)
    is_online = models.BooleanField(default=False, verbose_name="Онлайн урок")

    def clean(self):
        if self.is_online:
            self.classroom = None

        if self.classroom:
            overlapping_lessons = Schedule.objects.filter(
                classroom=self.classroom,
                weekday=self.date.strftime('%a').lower(),
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )

            overlapping_extra_lessons = ExtraLesson.objects.filter(
                classroom=self.classroom,
                date=self.date,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(id=self.id)

            if overlapping_lessons.exists() or overlapping_extra_lessons.exists():
                raise ValidationError("Аудитория занята в указанное время.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        lesson_type = "Онлайн" if self.is_online else "Оффлайн"
        return f"Доп. урок ({lesson_type}) - {self.teacher} - {self.date} ({self.start_time}-{self.end_time})"

    class Meta:
        verbose_name = "Дополнительный урок"
        verbose_name_plural = "Дополнительные уроки"
