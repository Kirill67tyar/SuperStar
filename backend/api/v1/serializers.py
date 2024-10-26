from rest_framework import serializers
from django.db.models import OuterRef, Subquery
from django.db.models.functions import Coalesce


from trainings.models import (
    TrainigRequest,
    PositionRequirement,
    Level,
    Rating,
)
from skills.models import Competence, Skill
from employees.models import (
    Grade,
    Position,
    Team,
    Employee,
    Target,
)


class RatingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            'date',
            'score',
        )

class LevelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = (
            'skill',
            'date',
            'score',
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
    team = TeamModelSerializer(many=True, read_only=True)
    skills = serializers.SerializerMethodField(read_only=True)
    requests_by_employee = serializers.IntegerField(
        source='quantity_requests',
        read_only=True,
    )
    development_plan = serializers.SerializerMethodField(read_only=True)
    ratings = RatingModelSerializer(many=True, read_only=True,)

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
            'ratings',
            'skills',
        )

    def get_development_plan(self, obj):
        return hasattr(obj, 'development_requests')

    def get_skills(self, obj):
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
                scores['growth'] = level.latest_score > level.penultimate_score
                reqirement_score = (
                    requirement_data[obj.position.name][obj.grade.name]
                    .get(level.skill.name)
                )
                accordance = None
                if reqirement_score:
                    accordance = level.latest_score >= reqirement_score
                scores['accordance'] = accordance
                scores['reqirement_score'] = reqirement_score
                skills_data[skills_mapping[level.skill.competence.type]].append(
                    scores)
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



class FilterTeamModelSerializer(serializers.ModelSerializer):
    """Сериализатор фильтрации по командам."""
    class Meta:
        model = Team
        fields = (
            'id',
            'name',

        )

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



class ThinTeamModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = (
            'id',
            'name',

        )


class FilterEmployeeModelSerializer(serializers.ModelSerializer):
    """Сериализатор фильтрации по сотдрудникам."""
    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
        )


class FilterPositionModelSerializer(serializers.ModelSerializer):
    """Сериализатор фильтрации по должностям."""
    class Meta:
        model = Position
        fields = (
            'id',
            'name',
        )


class FilterGradeModelSerializer(serializers.ModelSerializer):
    """Сериализатор фильтрации по грейдам."""
    class Meta:
        model = Grade
        fields = (
            'id',
            'name',
        )


class FilterCompetenceModelSerializer(serializers.ModelSerializer):
    """Сериализатор фильтрации по компетенциям."""
    class Meta:
        model = Competence
        fields = (
            'id',
            'name',
        )


class FilterSkillModelSerializer(serializers.ModelSerializer):
    """Сериализатор фильтрации по компетенциям."""
    class Meta:
        model = Skill
        fields = (
            'id',
            'name',
        )


class FilterTrainigRequestModelSerializer(serializers.ModelSerializer):
    """Сериализатор фильтрации по календарю."""
    class Meta:
        model = TrainigRequest
        fields = (
            'id',
            'start_date',
            'end_date',
        )

        
class DateAverageScoreSerializer(serializers.Serializer):
    date = serializers.DateField()
    avg_score = serializers.FloatField()
