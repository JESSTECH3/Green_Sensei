from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from habits.models import Habit
from recommendations.models import Recommendation

@login_required
def dashboard(request):
    # Habits for logged-in user
    habits = Habit.objects.filter(user=request.user).order_by('-date_logged')[:5]
    
    # Recommendations for logged-in user
    recommendations = Recommendation.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Stats (example: average impact score)
    avg_impact = habits.aggregate(avg_impact=Avg('impact_score'))['avg_impact'] if habits.exists() else None
    
    return render(request, 'dashboard/dashboard.html', {
        'habits': habits,
        'recommendations': recommendations,
        'avg_impact': avg_impact,
    })
