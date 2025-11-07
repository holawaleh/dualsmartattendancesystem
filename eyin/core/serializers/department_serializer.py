from rest_framework import serializers
from core.models import Department, ProgramLevel, Course

class ProgramLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramLevel
        fields = ["id", "name", "order"]

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "code", "title", "credit_unit"]

class DepartmentSerializer(serializers.ModelSerializer):
    program_levels = ProgramLevelSerializer(many=True, read_only=True)
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "code", "description", "created_at", "program_levels", "courses"]
