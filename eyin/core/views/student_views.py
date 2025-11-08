from rest_framework import viewsets, permissions
from core.models import StudentProfile
from core.serializers import StudentProfileSerializer

class StudentProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing or editing student profiles.
    Accessible only to authenticated users (admins, staff, or department admins).
    """
    queryset = StudentProfile.objects.select_related("user", "department", "level")
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Limit what each user can see."""
        user = self.request.user

        # Superusers see everything
        if user.is_superuser:
            return self.queryset

        # Department Admins see students in their department
        from core.models import DepartmentAdmin
        dept_admin = DepartmentAdmin.objects.filter(user=user).first()
        if dept_admin:
            return self.queryset.filter(department=dept_admin.department)

        # Regular students only see themselves
        return self.queryset.filter(user=user)
