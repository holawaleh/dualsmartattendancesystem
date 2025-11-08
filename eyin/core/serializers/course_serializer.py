from rest_framework import serializers
from core.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "code", "title", "credit_unit", "description", "department"]
