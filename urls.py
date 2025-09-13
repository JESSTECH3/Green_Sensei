from django.contrib import admin
from django.urls import path, include
from . import views   # 👈 import views from the project folder

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ai/", include("ai.urls")),
    path("dashboard/", views.dashboard, name="dashboard"),  # 👈 new
]
