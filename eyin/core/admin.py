from django.contrib import admin
from django.contrib.auth import get_user_model
from core.models import (
    Department,
    DepartmentAdmin,
    ProgramLevel,
    StudentProfile,
    Course,
    CourseEnrollment
)

User = get_user_model()


def get_user_department(user):
    """Return the department a department-admin user manages."""
    if user.is_superuser:
        return None
    dept_admin = DepartmentAdmin.objects.filter(user=user).first()
    return dept_admin.department if dept_admin else None


# ----------------------------
#  Inline relationships
# ----------------------------

class ProgramLevelInline(admin.TabularInline):
    model = ProgramLevel
    extra = 0
    show_change_link = True


class CourseInline(admin.TabularInline):
    model = Course
    extra = 0
    show_change_link = True


class DepartmentAdminInline(admin.TabularInline):
    model = DepartmentAdmin
    extra = 0
    show_change_link = True


# ----------------------------
#  Main model registrations
# ----------------------------

@admin.register(Department)
class DepartmentAdminPanel(admin.ModelAdmin):
    list_display = ("name", "code", "description", "created_at")
    search_fields = ("name", "code")
    ordering = ("name",)
    inlines = [ProgramLevelInline, CourseInline, DepartmentAdminInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        department = get_user_department(request.user)
        return qs.filter(id=department.id) if department else qs.none()


@admin.register(ProgramLevel)
class ProgramLevelAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "order")
    list_filter = ("department",)
    search_fields = ("name", "department__name")
    ordering = ("department", "order")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        department = get_user_department(request.user)
        return qs.filter(department=department) if department else qs.none()


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "matric_no", "department", "level", "rfid_uid")
    list_filter = ("department", "level")
    search_fields = ("user__first_name", "user__last_name", "matric_no", "rfid_uid")
    ordering = ("department", "matric_no")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        department = get_user_department(request.user)
        return qs.filter(department=department) if department else qs.none()


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "department", "credit_unit")
    list_filter = ("department",)
    search_fields = ("code", "title", "department__name")
    ordering = ("department", "code")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        department = get_user_department(request.user)
        return qs.filter(department=department) if department else qs.none()


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "is_borrowed",
        "approval_status",
        "approved_by",
        "requested_at",
    )
    list_filter = ("approval_status", "is_borrowed", "course__department")
    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "course__code",
        "course__title",
    )
    ordering = ("requested_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        department = get_user_department(request.user)
        return qs.filter(course__department=department) if department else qs.none()


# ----------------------------
#  Admin Branding
# ----------------------------
admin.site.site_header = "Smart Attendance Administration"
admin.site.site_title = "Smart Attendance Admin"
admin.site.index_title = "Management Dashboard"
