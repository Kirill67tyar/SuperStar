from rest_framework import serializers
from django.db.models import OuterRef, Subquery
from django.db.models.functions import Coalesce


from trainings.models import (
    TrainigRequest,
    PositionRequirement,
    Level,
)
from skills.models import Competence, Skill
from employees.models import (
    Grade,
    Position,
    Team,
    Employee,
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


class LevelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = (
            'skill',
            'date',
            'score',
            # 'latest_score',
        )


class TeamModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            'id',
            'name',
        )


class EmployeeModelSerializer(serializers.ModelSerializer):

    position = serializers.StringRelatedField(read_only=True)
    grade = serializers.StringRelatedField(read_only=True)
    # team = serializers.StringRelatedField(many=True, read_only=True)
    team = TeamModelSerializer(many=True, read_only=True)
    skills = serializers.SerializerMethodField(read_only=True)
    # skills = LevelModelSerializer(
    #     many=True,
    #     read_only=True,
    #     source='levels',
    # )

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'position',
            'bus_factor',
            'grade',
            'team',
            'created',
            'skills',
        )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     requirements_for_position = Requirement.objects.select_related(
    #         'position',
    #         'grade',
    #         'skill',
    #     ).values(
    #         'position__name',
    #         'grade__name',
    #         'skill__name',
    #         'score'
    #     )
    #     requirement_data = {}

    #     for p in requirements_for_position:

    #         requirement_data[p['position__name']] = (
    #             requirement_data
    #             .get(p['position__name'], {})
    #         )
    #         requirement_data[p['position__name']][p['grade__name']] = (
    #             requirement_data
    #             [p['position__name']]
    #             .get(p['grade__name'], {})
    #         )
    #         (requirement_data
    #          [p['position__name']]
    #          [p['grade__name']]
    #          .update({p['skill__name']: p['score']}))
    #     self.requirement_data = requirement_data

    def get_skills(self, obj):
        """
        skills: [
            {
                name: string;
                score: number;
                id: number;
                growth: boolean;
                accordance: boolean;
                hard_skills: boolean;
            },
            {
                name: string;
                score: number;
                id: number;
                growth: boolean;
                accordance: boolean;
                hard_skills: boolean;
            },
            ...
    ]       
        или так:
        skills: {
            hard_skills: [
                    {
                        name: string;
                        score: number;
                        id: number;
                        growth: boolean;
                        accordance: boolean;
                    },
                    ...
            ],
            soft_skills: [
                ...
            ]

        """
        skills_mapping = {
            'Hard skills': 'hard_skills',
            'Soft skills': 'soft_skills',
        }
        skills_data = {
            'hard_skills': [],
            'soft_skills': [],
        }
        score_ids = set()
        requirement_data = self.context['requirement_data']
        for level in obj.filtered_levels:
            scores = {}
            if level.skill.pk not in score_ids:
                score_ids.add(level.skill.pk)
                scores['id'] = level.skill.pk
                scores['name'] = level.skill.name
                if level.latest_score:  # is not None
                    scores['score'] = level.latest_score
                if level.penultimate_score:  # is not None
                    scores['penultimate_score'] = level.penultimate_score
                scores['growth'] = level.latest_score > level.penultimate_score
                reqirement_score = (
                    requirement_data[obj.position.name][obj.grade.name]
                    .get(level.skill.name)
                )
                accordance = None
                if reqirement_score:
                    accordance = level.latest_score >= reqirement_score
                scores['accordance'] = accordance
                skills_data[skills_mapping[level.skill.competence.type]].append(
                    scores)
        return skills_data

        # # ? =-=-=-=-=-=-=-=-=-=-=-= новый вариант:
        # skills_data = {
        #     'hard_skills': [],
        #     'soft_skills': [],
        # }
        # for level in obj.levels.all():
        #     if level.skill.competence.type == 'Hard skills':
        #         pass
        #     else:
        #         pass

        # ! =-=-=-=-=-=-=-=-=-=-=-= старый вариант:
        # skills_data = {}
        # for level in obj.levels.all():
        #     competence_type = level.skill.competence.type
        #     if competence_type in skills_data:
        #         if level.skill.name not in skills_data[competence_type]:
        #             level_dict = {level.skill.name: {
        #                 'score': level.latest_score,
        #                 'growth': level.latest_score > level.penultimate_score,
        #             }}

        #             reqirement_score = self.requirement_data[obj.position.name][obj.grade.name].get(
        #                     level.skill.name)
        #             accordance = None
        #             if reqirement_score:
        #                 accordance = level.latest_score >= reqirement_score
        #             level_dict[level.skill.name].update(
        #                 {
        #                     'accordance': accordance,
        #                 }
        #             )

        #             skills_data[competence_type].update(level_dict)
        #     else:
        #         skills_data[competence_type] = {}
        # return skills_data


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


class TeamGroupedSerializer(serializers.Serializer):
    name = serializers.CharField()
    # team_members = serializers.SerializerMethodField()
    team_members = EmployeeModelSerializer(
        many=True,
        read_only=True,
        source='employees',
    )

    # def get_team_members(self, obj):
    #     # Используем предварительно загруженные данные сотрудников через related менеджер
    #     employees = [employee for employee in self.context['employees'] if obj in employee.team.all()]
    #     return EmployeeModelSerializer(employees, many=True).data
