from django.contrib import admin
from .models import Recommendation

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "created_at", "is_seen")
    search_fields = ("user__username", "message")
    list_filter = ("is_seen", "created_at")
