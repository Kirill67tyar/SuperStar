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
        # ! =-=-=-=-=-=-=-= старый вариант
        # for level in obj.levels.all():
        #     if level.skill.name not in skills_data:
        #         skills_data[level.skill.name] = {
        #             # 'competence': level.skill.competence.type,
        #             'score': level.latest_score,
        #             'growth': level.latest_score > level.penultimate_score
        #         }
        # ! =-=-=-=-=-=-=-= старый вариант
        # ? =-=-=-=-=-=-=-= последний вариант
        for level in obj.levels.all():
            competence_type = level.skill.competence.type
            if competence_type in skills_data:
                if level.skill.name not in skills_data[competence_type]:
                    level_dict = {level.skill.name: {
                        'score': level.latest_score,
                        'growth': level.latest_score > level.penultimate_score,
                        # 'accordance': level.score >= level.penultimate_score,
                    }}
                    skills_data[competence_type].update(level_dict)
            else:
                skills_data[competence_type] = {}

        # ? =-=-=-=-=-=-=-= последний вариант
        return skills_data


class TeamModelSerializer(serializers.ModelSerializer):
    team_members = EmployeeModelSerializer(
        many=True,
        read_only=True,
        source='employees',
    )

    class Meta:
        model = Team
        fields = (
            'name',
            'team_members',
        )
