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
    requests_by_employee = serializers.IntegerField(
        source='quantity_requests',
        read_only=True,
    )
    development_plan = serializers.SerializerMethodField(read_only=True)

    # skills = LevelModelSerializer(
    #     many=True,
    #     read_only=True,
    #     source='levels',
    # )

    class Meta:
        model = Employee
        fields = (
            'id',
            'image',
            'name',
            'position',
            'bus_factor',
            'grade',
            'team',
            'created',
            'requests_by_employee',
            'development_plan',
            'skills',
        )

    def get_development_plan(self, obj):
        return hasattr(obj, 'development_requests')

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


class TrainigRequestReadSerializer(serializers.ModelSerializer):
    skill = serializers.SerializerMethodField()

    class Meta:
        model = TrainigRequest
        fields = (
            'id',
            'skill',
        )

    def get_skill(self, obj):
        skill_data = {
            'name': obj.skill.name,
            'competence': obj.skill.competence.name,
            'skill_course': f"Курс {obj.skill.name}",
            'time_of_training': f"{obj.start_date} - {obj.end_date or obj.start_date}",
            'test_data': {
                'competence': obj.skill.competence.pk,
                'skill': obj.skill.pk,
            }
        }

        employees = []
        for request in TrainigRequest.objects.filter(skill=obj.skill):
            employees.append({
                'name': request.employee.name,
                'image': request.employee.image.url if request.employee.image else None,
                'position': request.employee.position.name,
                'grade': request.employee.grade.name,
                'bus_factor': request.employee.bus_factor,
                'test_data': {
                    'employee': request.employee.pk,
                    'position': request.employee.position.pk,
                    'grade': request.employee.grade.pk,
                }
            })

        return {
            'competence': skill_data['competence'],
            'name': skill_data['name'],
            'skill_course': skill_data['skill_course'],
            'employees': employees if employees else []
        }

    # def get_skill(self, obj):
    #     """Запросы."""
    #     return {
    #         'competence': obj.skill.competence.name,
    #         'name': obj.skill.name,
    #         'skill_course': f"Курс {obj.skill.name}",
    #         'time_of_training': f"{obj.start_date} - {obj.start_date}",
    #         'test_data': {
    #             'competence': obj.skill.competence.pk,
    #             'skill': obj.skill.pk,
    #         },
    #         'employee': {
    #             'name': obj.employee.name,
    #             'position': obj.employee.position.name,
    #             'grade': obj.employee.grade.name,
    #             'bus_factor': obj.employee.bus_factor,
    #             'test_data': {
    #                 'employee': obj.employee.pk,
    #                 'position': obj.employee.position.pk,
    #                 'grade': obj.employee.grade.pk,
    #             }}
    #     }