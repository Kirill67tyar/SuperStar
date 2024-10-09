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
    
    def __str__(self):
        return self.name


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
    def __str__(self):
        return self.name

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

    def __str__(self):
            return self.name


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
        related_name='employees',
        verbose_name='Команды',
    )
    created = models.DateField(
        verbose_name='Добавлено',
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ('pk', )

    def __str__(self):
            return self.name


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

    def __str__(self):
        return str(self.pk)




