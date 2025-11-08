from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views.department_views import DepartmentViewSet
from core.views.student_views import StudentProfileViewSet

# ✅ NEW IMPORT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet)
router.register(r"students", StudentProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),

    # ✅ JWT authentication endpoints
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
