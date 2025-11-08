import uuid
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class ProgramLevel(models.Model):
    """
    Represents academic levels or stages within a department.
    Examples:
      - ND1, ND2, HND1, HND2
      - JSS1, JSS2, SSS1, SSS3
      - 100 Level, 200 Level, MSc, PhD
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(
        "core.Department",
        on_delete=models.CASCADE,
        related_name="program_levels"
    )
    name = models.CharField(max_length=50)  # e.g. 'ND1', 'SSS3', 'MSc'
    order = models.PositiveIntegerField(default=0)  # helps sorting (1,2,3,...)

    class Meta:
        unique_together = ("department", "name")
        verbose_name_plural = "Program Levels"
        ordering = ["department", "order"]  # Sort by dept, then order

    def __str__(self):
        return f"{self.name} ({self.department.code})"


class StudentProfile(models.Model):
    """
    Extends a User (role=STUDENT) with academic and biometric data.
    Each student belongs to exactly one department.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    department = models.ForeignKey(
        "core.Department", on_delete=models.PROTECT, related_name="students"
    )
    matric_no = models.CharField(max_length=30, unique=True)
    level = models.ForeignKey(
        ProgramLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )

    # Optional identifiers
    rfid_uid = models.CharField(max_length=100, unique=True, null=True, blank=True)
    fingerprint_template = models.BinaryField(null=True, blank=True)
    photo = models.ImageField(upload_to="student_photos/", null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Student Profiles"
        ordering = ["department", "matric_no"]

    def __str__(self):
        # Use first_name + last_name since full_name may not exist
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return f"{full_name} ({self.matric_no})"