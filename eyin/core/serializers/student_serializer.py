from rest_framework import serializers
from core.models import StudentProfile, ProgramLevel, Department
from django.contrib.auth import get_user_model

User = get_user_model()


class UserNestedSerializer(serializers.ModelSerializer):
    """Lightweight serializer to display student user info."""
    class Meta:
        model = User
        fields = ["id", "email", "full_name"]


class ProgramLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramLevel
        fields = ["id", "name", "order"]


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serialize full student profile with nested user and department info."""
    user = UserNestedSerializer(read_only=True)
    department = serializers.StringRelatedField()
    level = ProgramLevelSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "user",
            "matric_no",
            "department",
            "level",
            "rfid_uid",
            "fingerprint_template",
            "photo",
            "date_created",
        ]
