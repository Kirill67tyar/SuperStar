from django.db import models

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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name
