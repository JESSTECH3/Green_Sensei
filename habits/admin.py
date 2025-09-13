from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "impact_score", "date_logged")
    search_fields = ("category", "user__username")
    list_filter = ("category", "date_logged")
