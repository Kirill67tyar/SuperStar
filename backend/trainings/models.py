from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from employees.models import Employee, Position, Grade
from skills.models import Skill


class Level(models.Model):
    """Модель текущего уровня сотрудника."""

    LEVEL_NAME_CHOICES = [
        ('Начинающий', 'Начинающий'),
        ('Базовый', 'Базовый'),
        ('Уверенный', 'Уверенный'),
        ('Экспертный', 'Экспертный'),
    ]
    LEVEL_ACCORDANCE_CHOICES = [
        ('Да', 'Да'),
        ('Нет', 'Нет'),
        ('Не требуется', 'Не требуется'),
    ]
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='levels',
        verbose_name='сотрудник',
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name='Скилл',
    )
    date = models.DateField(
        verbose_name='Добавлено',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Оценка не может быть меньше 1'
            ),
            MaxValueValidator(
                5,
                message='Оценка не может быть больше 5'
            )
        ],
        verbose_name='Эталонная оценка',
    )
    level_score = models.CharField(
        max_length=20,
        choices=LEVEL_NAME_CHOICES,
        verbose_name='Оценка на словах',
    )
    accordance = models.CharField(
        max_length=20,
        choices=LEVEL_ACCORDANCE_CHOICES,
        verbose_name='Соответствие',
    )

    def __str__(self):
        return str(self.pk)

class TrainigRequest(models.Model):
    """
    Модель отслеживания запросов,
     на повышение квалификации.
    """

    TICKET_CHOICES = [
        ('worker', 'Работник'),
        ('HR', 'HR'),
        ('regular', 'Регулярная'),
        ('manager', 'Руководитель'),
    ]
    STATUS_CHOICES = [
        ('on_discussion', 'на согласовании'),
        ('approved', 'одобрено'),
        ('cancellation', 'отмена'),
        ('denied', 'отказано'),
        ('in_process', 'в процессе'),
    ]
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Сотрудник',
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name='Навык',
    )
    desired_score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Оценка не может быть меньше 1'
            ),
            MaxValueValidator(
                5,
                message='Оценка не может быть больше 5'
            )
        ],
        verbose_name='Желаемая оценка сотрудника',
    )
    ticket_source = models.CharField(
        max_length=20, 
        choices=TICKET_CHOICES,
        verbose_name='Тикет откуда',
        )
    start_date = models.DateField(
        verbose_name='Дата начала обучения',
        )
    end_date = models.DateField(
        verbose_name='Дата окончания обучения',
        blank=True,
        null=True,
        )
    note = models.CharField(
        max_length=255,
        verbose_name='Заметка',
        )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        verbose_name='Статус',
        )
    actual_hours = models.PositiveSmallIntegerField(
        verbose_name='Часов по факту',
    )
    planned_hours = models.PositiveSmallIntegerField(
        verbose_name='Запланированные часы',
    )

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
        ordering = ('pk',)

    def __str__(self):
        return str(self.pk)

class Requirement(models.Model):
    """Модель требований для позиции (должности)."""

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        # on_delete=models.SET_NULL,
        related_name='requirements_position',
        verbose_name='Должность',
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        # on_delete=models.SET_NULL,
        related_name='requirements_grade',
        verbose_name='Грейд',
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        # on_delete=models.SET_NULL,
        related_name='requirements',
        verbose_name='Скилл',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Оценка не может быть меньше 1'
            ),
            MaxValueValidator(
                5,
                message='Оценка не может быть больше 5'
            )
        ],
        verbose_name='Эталонная оценка',
    )

    class Meta:
        verbose_name = 'Требования к позиции'
        verbose_name_plural = 'Требования к позиции'
        # db_table = 'lalala'

    def __str__(self):
        return str(self.pk)
