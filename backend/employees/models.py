from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


class Grade(models.Model):
    """Модель грейда."""

    GRADE_CHOICES = [
        ('Junior', 'Junior'),
        ('Middle', 'Middle'),
        ('Senior', 'Senior'),
    ]
    name = models.CharField(
        max_length=20,
        choices=GRADE_CHOICES,
    )

    class Meta:
        verbose_name = 'Домен'
        verbose_name_plural = 'Домены'
        ordering = ('pk',)


class Position(models.Model):
    """Модель должности."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название',
    )

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ('pk',)


class Team(models.Model):
    """Модель команды."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название',
    )

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class Employee(models.Model):
    """Модель сотрудника."""
    name = models.CharField(
        max_length=100,
        verbose_name='Фамилия Имя',
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        # related_name='employees',
        verbose_name='Дожность',
    )
    bus_factor = models.BooleanField(
        default=False,
        verbose_name='Автобусный фактор',
    )
    grade = models.ForeignKey(
        Grade,
        # related_name='employees'
        on_delete=models.CASCADE,
        verbose_name='Грейд',
    )
    team = models.ManyToManyField(
        Team,
        # related_name='employees'
        verbose_name='Команды',
    )
    created = models.DateField(
        verbose_name='Добавлено',
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ('pk', )



class Competence(models.Model):
    """Модель Soft и Hard компетенций."""

    COMPETENCE_CHOICES = [
        ('Soft skills', 'Soft skills'),
        ('Hard skills', 'Hard skills'),
    ]
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название',
    )
    type = models.CharField(
        max_length=11,
        choices=COMPETENCE_CHOICES,
        verbose_name='Тип скилла',
    )

    class Meta:
        verbose_name = 'Компетенция'
        verbose_name_plural = 'Компетенции'
        ordering = ('pk',)


class Skill(models.Model):
    """Модель скилла."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название',
    )
    competence = models.ForeignKey(
        Competence,
        on_delete=models.CASCADE,
        related_name='skills',
        verbose_name='Компетенция',
    )

    class Meta:
        verbose_name = 'Скилл'
        verbose_name_plural = 'Скиллы'
        ordering = ('pk',)


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
            MaxValueValidator(
                1,
                message='Оценка не может быть меньше 1'
            ),
            MinValueValidator(
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
    # actual_hours = models.PositiveSmallIntegerField(
    #     verbose_name='Часов по факту',
    # )
    # planned_hours = models.PositiveSmallIntegerField(
    #     verbose_name='Запланированные часы',
    # )

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
        ordering = ('pk',)


class PositionRequirement(models.Model):
    """Модель требований для позиции (должности)."""

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        verbose_name='Должность',
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        verbose_name='Грейд',
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name='Скилл',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                1,
                message='Оценка не может быть меньше 1'
            ),
            MinValueValidator(
                5,
                message='Оценка не может быть больше 5'
            )
        ],
        verbose_name='Эталонная оценка',
    )

    class Meta:
        verbose_name = 'Требования к позиции'
        verbose_name_plural = 'Требования к позиции'


class Target(models.Model):
    """Модель карьерной цели сотрудника."""

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Сотрудник'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        verbose_name='Должность'
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        verbose_name='Грейд'
    )

    class Meta:
        verbose_name = 'Карьерная цель'
        verbose_name_plural = 'Карьерные цели'


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
            MaxValueValidator(
                1,
                message='Оценка не может быть меньше 1'
            ),
            MinValueValidator(
                5,
                message='Оценка не может быть больше 5'
            )
        ],
        verbose_name='Эталонная оценка',
    )
    name = models.CharField(
        max_length=20,
        choices=LEVEL_NAME_CHOICES,
        verbose_name='Оценка на словах',
    )
    accordance = models.CharField(
        max_length=20,
        choices=LEVEL_ACCORDANCE_CHOICES,
        verbose_name='Соответствие',
    )
