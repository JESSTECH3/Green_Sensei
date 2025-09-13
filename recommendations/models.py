from django.db import models
from django.conf import settings
from habits.models import Habit

class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(default='')

    def __str__(self):
        return f"Recommendation for {self.habit.name}"