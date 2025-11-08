import uuid
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Department(models.Model):
    """
    Represents an academic or organizational department.
    The optional 'code' provides a concise machine-readable key.
    Example:
      - name: Computer Science
      - code: CSC
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        help_text="Short code like CSC, MEC, ACC (optional)"
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Departments"
        ordering = ["name"]

    def __str__(self):
        if self.code:
            return f"{self.name} ({self.code})"
        return self.name


class DepartmentAdmin(models.Model):
    """
    Connects department to its admin users.
    Allows multiple admins per department.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="admins"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="managed_departments"
    )

    class Meta:
        unique_together = ('department', 'user')
        verbose_name = "Department Admin"
        verbose_name_plural = "Department Admins"
        ordering = ["department__name", "user__email"]

    def __str__(self):
        return f"{self.user.email} → {self.department.name}"
