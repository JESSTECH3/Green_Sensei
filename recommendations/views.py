from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Recommendation
from .form import RecommendationForm

@login_required
def recommendation_list(request):
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.user = request.user
            rec.save()
            return redirect('recommendation_list')
    else:
        form = RecommendationForm()
    
    recommendations = Recommendation.objects.filter(user=request.user)
    return render(request, 'recommendations/recommendations_list.html', {
        'recommendations': recommendations,
        'form': form
    })
