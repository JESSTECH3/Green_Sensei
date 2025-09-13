import openai
from django.conf import settings
from users.models import CustomUser
from habits.models import Habit

def generate_recommendation(user: CustomUser) -> str:
    habits = Habit.objects.filter(user=user)
    if not habits.exists():
        return "No habits logged yet. Start tracking to get recommendations!"

    # Générer le prompt pour OpenAI
    prompt = "You are an eco-friendly coach. Provide personalized advice based on these habits:\n"
    for habit in habits:
        prompt += f"- Category: {habit.category}, Description: {habit.description}, Impact Score: {habit.impact_score}\n"

    # Appel à l'API OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        api_key=settings.OPENAI_API_KEY
    )

    return response.choices[0].message['content']
