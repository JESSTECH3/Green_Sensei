from django.shortcuts import render
from habits.models import Habit
from recommendations.models import Recommendation

def dashboard(request):
    # Habits for logged-in user
    habits = Habit.objects.filter(user=request.user).order_by('-date_logged')[:5]
    
    # Recommendations for logged-in user
    recommendations = Recommendation.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Stats (example: average impact score)
    avg_impact = habits.aggregate_avg('impact_score') if habits.exists() else None
    
    return render(request, 'dashboard/dashboard.html', {
        'habits': habits,
        'recommendations': recommendations,
        'avg_impact': avg_impact,
    })
