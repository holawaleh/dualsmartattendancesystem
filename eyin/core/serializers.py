from rest_framework import serializers
from core.models import (
    User, Department, DepartmentAdmin,
    ProgramLevel, StudentProfile, Course, CourseEnrollment
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'role', 'is_active']


class ProgramLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramLevel
        fields = ['id', 'name', 'order', 'department']


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    level = ProgramLevelSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'department', 'matric_no',
            'level', 'rfid_uid', 'photo'
        ]


class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'department', 'code', 'title', 'credit_unit', 'description']


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    student = StudentProfileSerializer(read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = [
            'id', 'student', 'course', 'is_borrowed',
            'approval_status', 'approved_by',
            'requested_at', 'updated_at'
        ]
