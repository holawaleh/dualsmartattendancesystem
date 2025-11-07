import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Course(models.Model):
    """
    Represents a single course belonging to a specific department.
    Example: CSC201 - Data Structures
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(
        "core.Department",
        on_delete=models.CASCADE,
        related_name="courses"
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Enter the course code manually, e.g. CSC201 or ECO102"
    )
    title = models.CharField(max_length=150)
    credit_unit = models.PositiveSmallIntegerField(default=3)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Courses"
        ordering = ["department", "code"]

    def __str__(self):
        return f"{self.code} - {self.title}"


class ApprovalStatus(models.TextChoices):
    PENDING = "PENDING", "Pending Approval"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"


class CourseEnrollment(models.Model):
    """
    Bridge table: connects a StudentProfile to a Course.
    Handles borrowed course logic and admin approval workflow.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        "core.StudentProfile",
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    is_borrowed = models.BooleanField(default=False)
    approval_status = models.CharField(
        max_length=10,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_enrollments",
        help_text="Admin who approved or rejected this borrowed course",
    )
    requested_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "course")
        verbose_name_plural = "Course Enrollments"
        ordering = ["student", "course"]

    def __str__(self):
        user = self.student.user
        full_name = f"{user.first_name} {user.last_name}".strip() or user.email
        return f"{full_name} → {self.course.code} ({self.get_approval_status_display()})"
