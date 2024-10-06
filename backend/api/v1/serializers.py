from rest_framework import serializers
from django.db.models import OuterRef, Subquery
from django.db.models.functions import Coalesce


from employees.models import (
    Grade,
    Position,
    Team,
    Employee,
    Competence,
    Skill,
    TrainigRequest,
    PositionRequirement,
    Target,
)

"""
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
"""


class EmployeeModelSerializer(serializers.ModelSerializer):

    position = serializers.StringRelatedField(read_only=True)
    grade = serializers.StringRelatedField(read_only=True)
    team = serializers.StringRelatedField(many=True, read_only=True)
    skills = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Employee
        fields = (
            'name',
            'position',
            'bus_factor',
            'grade',
            'team',
            'created',
            'skills',
        )

    def get_skills(self, obj):
        skills_data = {}
        latest_scores = obj.levels.filter(
            skill=OuterRef('skill')
        ).order_by('-date').values('score')[:1]

        penultimate_scores = obj.levels.filter(
            skill=OuterRef('skill')
        ).order_by('-date').values('score')[1:2]

        skills_with_scores = (
            obj.levels
            # .values('skill__name')
            .annotate(
                latest_score=Subquery(latest_scores),
                penultimate_score=Coalesce(
                    Subquery(penultimate_scores), 5)
            )
            .distinct()
        )
        for skill in skills_with_scores:
            skills_data[skill['skill__name']] = {
                'score': skill['latest_score'],
                'growth': skill['latest_score'] > skill['penultimate_score']
            }
        return skills_data
