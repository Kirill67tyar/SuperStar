from django.db import models


class GradeTable(models.Model):
    """Модель чего?."""

    GRADE_CHOICES = [
        ('Junior', 'Джун'),
        ('Middle', 'Мидл'),
        ('Senior', 'Синьор'),
    ]
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)

    class Meta:
        verbose_name_plural = 'ljlel'


class PositionTable(models.Model):
    """Модель чего?."""

    name = models.CharField(
        max_length=100,
        verbose_name='Название',
    )

    class Meta:
        verbose_name_plural = 'ljlel'


class EmployeeTable(models.Model):
    """Модель сотрудника."""

    last_name = models.CharField(
        max_length=50,
        verbose_name='Имя',
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
    )
    position = models.ForeignKey(
        PositionTable,
        on_delete=models.CASCADE,
    )
    bus_factor = models.BooleanField()
    grade = models.ForeignKey(
        GradeTable,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'ljlel'


class CompetenceTable(models.Model):
    """Модель Soft и Hard компетенций."""

    COMPETENCE_CHOICES = [
        ('Soft skills', 'Софт скилы'),
        ('Hard skills', 'Хард скилы'),
    ]
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
    )
    type = models.CharField(max_length=20, choices=COMPETENCE_CHOICES)

    class Meta:
        verbose_name_plural = 'ljlel'


class SkillTable(models.Model):
    """Модель чего?."""

    name = models.CharField(
        max_length=100,
        verbose_name='Название',
    )
    competence = models.ForeignKey(
        CompetenceTable,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'ljlel'


class TrackingRequestsTable(models.Model):
    """Модель отслеживания запросов."""

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
        EmployeeTable,
        on_delete=models.CASCADE,
    )
    skill = models.ForeignKey(
        SkillTable,
        on_delete=models.CASCADE,
    )
    desired_score = models.SmallIntegerField()
    ticket_source = models.CharField(max_length=20, choices=TICKET_CHOICES)
    start_date = models.DateTimeField('Добавлено', auto_now_add=True)
    end_date = models.DateTimeField('Добавлено', auto_now_add=True)
    notes = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        verbose_name_plural = 'ljlel'


class TeamTable(models.Model):
    """Модель чего?. """

    name = models.CharField(
        max_length=100,
        verbose_name='Название',
    )

    class Meta:
        verbose_name_plural = 'ljlel'


class EmployeeTeamTable(models.Model):
    """Модель команды сотрудников."""

    employee = models.ForeignKey(
        EmployeeTable,
        on_delete=models.CASCADE,)
    team = models.ForeignKey(
        TeamTable,
        on_delete=models.CASCADE,)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'team'],
                name='unique_employee_team'
            )
        ]

class PositionRequirementsTable(models.Model):

    """Модель чего?."""
    position = models.ForeignKey(
        PositionTable,
        on_delete=models.CASCADE,
    )
    grade = models.ForeignKey(
        GradeTable,
        on_delete=models.CASCADE,
    )
    skill = models.ForeignKey(
        SkillTable,
        on_delete=models.CASCADE,
    )
    score = models.SmallIntegerField(verbose_name='Эталонная оценка',)

    class Meta:
        verbose_name_plural = 'ljlel'


class TargetTable(models.Model):
    """Модель чего?"""

    employee = models.OneToOneField(EmployeeTable, on_delete=models.CASCADE,)
    position = models.ForeignKey(
        PositionTable,
        on_delete=models.CASCADE,
    )
    bus_factor = models.BooleanField()
    grade = models.ForeignKey(
        GradeTable,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'ljlel'


class LevelTable(models.Model):
    """Модель чего?"""

    LEVEL_NAME_CHOICES = [
        ('Начинающий', 'Начинающий'),
        ('Базовый', 'Базовый'),
        ('Уверенный', 'Уверенный'),
        ('Экспертный', 'Экспертный'),
    ]
    LEVEL_ACCORDANCE_CHOICES = [
        ('Да', 'Начинающий'),
        ('Нет', 'Базовый'),
        ('Не требуется', 'Уверенный'),
    ]
    employee = models.ForeignKey(
        EmployeeTable,
        on_delete=models.CASCADE,)
    skill = models.ForeignKey(
        SkillTable,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField('Добавлено', auto_now_add=True)
    score = models.SmallIntegerField(verbose_name='Эталонная оценка',)
    name = models.CharField(max_length=20, choices=LEVEL_NAME_CHOICES)
    accordance = models.CharField(max_length=20, choices=LEVEL_ACCORDANCE_CHOICES)
