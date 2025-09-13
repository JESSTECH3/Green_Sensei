from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Habit
from .form import HabitForm

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    total_habits = habits.count()
    habits_this_week = habits.filter(date_logged__gte=timezone.now() - timedelta(days=7)).count()
    avg_per_week = total_habits / 7 if total_habits > 0 else 0
    return render(request, 'habits/habit_list.html', {
        'habits': habits,
        'total_habits': total_habits,
        'habits_this_week': habits_this_week,
        'avg_per_week': avg_per_week,
    })

@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'habits/habit_create.html', {'form': form})
