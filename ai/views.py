from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import openai

@login_required
def coach_view(request):
    # Handle clear conversation request
    if request.GET.get('clear') == '1':
        request.session.pop('ai_conversation', None)
        return redirect('ai_coach')

    # Get or initialize conversation history
    conversation_history = request.session.get('ai_conversation', [])

    response_text = None
    user_input = None
    error_message = None

    if request.method == 'POST':
        user_input = request.POST.get('question')

        # Add user message to conversation history
        if user_input:
            conversation_history.append({"role": "user", "content": user_input})

        # Check if API key is configured
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_actual_openai_api_key_here":
            response_text = """🌱 **Welcome to Green Sensei AI Coach!**

I'm here to help you with eco-friendly living, but I need a valid OpenAI API key to provide personalized responses.

**To get started:**
1. Visit [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Create a new API key
3. Add it to your Django settings

**In the meantime, here are some quick eco-tips:**

🏠 **Home Energy Saving:**
- Unplug electronics when not in use
- Use LED bulbs and smart thermostats
- Seal windows and doors to prevent drafts

♻️ **Zero Waste Habits:**
- Carry reusable shopping bags
- Use a reusable water bottle
- Compost food waste

🍽️ **Sustainable Eating:**
- Eat more plant-based meals
- Buy local and seasonal produce
- Reduce food waste by planning meals

🚲 **Green Transportation:**
- Walk, bike, or use public transport
- Carpool when possible
- Maintain proper tire pressure

Visit the AI Coach again after setting up your API key for personalized advice! 🌍"""
            error_message = "api_key_missing"
        else:
            try:
                client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

                # Enhanced system prompt for eco-friendly advice
                system_prompt = """You are an AI Eco-Coach specializing in sustainable living and environmental conservation.
                Provide practical, actionable advice on eco-friendly habits, energy conservation, waste reduction,
                sustainable transportation, green fashion, and environmental impact reduction.

                Focus on:
                - Specific, implementable steps
                - Cost-effective solutions
                - Measurable environmental impact
                - Encouraging and positive tone
                - Local and global environmental benefits

                Keep responses informative and engaging. End with a question to continue the conversation."""

                # Prepare messages for API call
                messages = [{"role": "system", "content": system_prompt}]

                # Add conversation history (limit to last 10 exchanges to avoid token limits)
                recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
                messages.extend(recent_history)

                # Use the updated OpenAI API v1.0.0
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=400,
                    temperature=0.7
                )

                response_text = response.choices[0].message.content.strip()

                # Add AI response to conversation history
                conversation_history.append({"role": "assistant", "content": response_text})

            except openai.RateLimitError:
                response_text = """🌱 **API Quota Exceeded**

It looks like we've reached the OpenAI API usage limit. Here are some instant eco-tips while we wait:

**Quick Energy Savers:**
• Turn off lights when leaving a room
• Use a programmable thermostat
• Unplug chargers and electronics

**Waste Reduction:**
• Use reusable bags and containers
• Choose products with minimal packaging
• Compost organic waste

**Sustainable Transport:**
• Walk or bike for short trips
• Use public transportation
• Combine errands to reduce driving

Please check back later or consider upgrading your OpenAI plan for unlimited access! 🌍"""
                error_message = "quota_exceeded"

            except openai.AuthenticationError:
                response_text = """🔑 **API Key Issue**

There seems to be an issue with the OpenAI API key. Please check that it's correctly configured in your Django settings.

**Quick Eco Tips:**
• Reduce shower time to 5 minutes
• Use cold water for laundry when possible
• Air-dry clothes instead of using dryer
• Choose energy-efficient appliances

Contact your administrator to fix the API key configuration."""
                error_message = "auth_error"

            except Exception as e:
                response_text = f"""🤖 **Technical Issue**

I encountered an error while processing your request. Here's some general eco-advice:

**Daily Green Habits:**
• Bring your own reusable cup for coffee/tea
• Choose digital receipts over paper
• Use both sides of paper when printing
• Turn off tap while brushing teeth

**Environmental Impact:**
• One tree absorbs CO₂ from one car's emissions for 5 years
• Recycling one ton of paper saves 17 trees
• LED bulbs use 75% less energy than incandescent

Please try again later or contact support if the issue persists."""
                error_message = "general_error"

    # Store updated conversation history in session
    request.session['ai_conversation'] = conversation_history

    # Prepare conversation data for template
    conversation_data = []
    for i, msg in enumerate(conversation_history):
        if msg['role'] == 'user':
            conversation_data.append({
                'type': 'user',
                'message': msg['content'],
                'timestamp': None  # Could add timestamps if needed
            })
        elif msg['role'] == 'assistant':
            conversation_data.append({
                'type': 'ai',
                'message': msg['content'],
                'timestamp': None
            })

    return render(request, 'ai/coach.html', {
        'response': response_text,
        'user_input': user_input,
        'error_message': error_message,
        'conversation_history': conversation_data,
        'has_conversation': len(conversation_history) > 0
    })
