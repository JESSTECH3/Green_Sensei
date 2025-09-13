from django.db import models
from django.conf import settings

class Habit(models.Model):
    CATEGORY_CHOICES = [
        ('transport', 'Transport'),
        ('energy', 'Energy'),
        ('food', 'Food'),
        ('waste', 'Waste'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    date_logged = models.DateField(auto_now_add=True)
    impact_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.date_logged}"
