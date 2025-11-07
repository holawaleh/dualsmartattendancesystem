from rest_framework import viewsets
from core.models import (
    Department, ProgramLevel, StudentProfile,
    Course, CourseEnrollment
)
from core.serializers import (
    DepartmentSerializer, ProgramLevelSerializer,
    StudentProfileSerializer, CourseSerializer,
    CourseEnrollmentSerializer
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ProgramLevelViewSet(viewsets.ModelViewSet):
    queryset = ProgramLevel.objects.all()
    serializer_class = ProgramLevelSerializer


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related('department', 'user', 'level')
    serializer_class = StudentProfileSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('department')
    serializer_class = CourseSerializer


class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = CourseEnrollment.objects.select_related('student', 'course')
    serializer_class = CourseEnrollmentSerializer
