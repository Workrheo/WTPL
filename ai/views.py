from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from settings.models import websiteSetting
from ai.models import OpenAIChatRecord
import openai
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.decorators import admin_role_required, user_role_required, both_role_required


# AI Assistant Category
@login_required(login_url='signIn')
@both_role_required
def aiCategory(request):
    
    context = {
        'title' : 'AI Assistant',
    }
    
    return render(request, 'crm/main/ai/category.html', context)

# AI Generation History
@login_required(login_url='signIn')
@both_role_required
def aiHistory(request):
    records = OpenAIChatRecord.objects.all().order_by('-timestamp')
    
    context = {
        'title' : 'AI Assistant History',
        'records' : records
    }
    
    return render(request, 'crm/main/ai/records.html', context)

# AI Generation Delete
@login_required(login_url='signIn')
@admin_role_required
def aiHistoryDelete(request, id):
    record = get_object_or_404(OpenAIChatRecord, id=id)
    record.delete()
    messages.success(request, 'Deleted successfully!')
    return redirect('aiHistory')


# OpenAi Content Generation
@login_required(login_url='signIn')
@both_role_required
@csrf_exempt
def openAiContentGeneration(request, category):
    settings = websiteSetting.objects.first()
    openai.api_key = str(settings.openai_api)
    print(openai.api_key)

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        word_limit = request.POST.get('word_limit', None)

        prompts = {
            'blog': f"Generate a blog post about {user_input} with a word limit of {word_limit} words.",
            'review': f"Write a review for {user_input} with a word limit of {word_limit} words.",
            'reply': f"Craft a reply for a customer review or comment about {user_input} with a word limit of {word_limit} words.",
            'social-media-post': f"Create engaging social media post about {user_input} with a word limit of {word_limit} words.",
            'email': f"Write an email that impresses and gets replies about {user_input} with a word limit of {word_limit} words.",
            'facebook-ads': f"Generate a Facebook Ads title and content about {user_input} with a word limit of {word_limit} words.",
            'google-ads': f"Create a Google Ads title and content about {user_input} with a word limit of {word_limit} words.",
            'guide': f"Generate a step-by-step guide about {user_input} with a word limit of {word_limit} words.",
            'proposal': f"Create a catchy proposal for buyers about {user_input} with a word limit of {word_limit} words.",
        }

        prompt = prompts.get(category, f"Generate content about {user_input}.")

        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=int(settings.max_token)
            )
            print(response)
            print(prompt)

            generated_content = response['choices'][0]['text']

            record = OpenAIChatRecord(user=request.user, user_input=user_input, bot_response=generated_content,
                                      category=category)
            record.save()

            return JsonResponse({'generated_content': generated_content})

        except openai.OpenAIError as e:
            error_message = f"OpenAI API Error: {e}"
        return JsonResponse({'error_message': error_message}, status=500)

    return render(request, 'crm/main/ai/generator.html', {'category': category})

#########################
# For USER #
#########################

# AI Assistant Category
@login_required(login_url='signIn')
@user_role_required
def useraiCategory(request):
    settings = websiteSetting.objects.first()
    if settings.is_enabled_for_user:
        context = {
            'title' : 'AI Assistant',
        }
        
        return render(request, 'user/main/ai/category.html', context)
    else:
        return redirect('userDashboard')

# AI Generation History
@login_required(login_url='signIn')
@user_role_required
def useraiHistory(request):
    settings = websiteSetting.objects.first()
    if settings.is_enabled_for_user:  
        records = OpenAIChatRecord.objects.filter(user=request.user).order_by('-timestamp')
        
        context = {
            'title' : 'AI Assistant History',
            'records' : records
        }
        
        return render(request, 'user/main/ai/records.html', context)
    else:
        return redirect('userDashboard')

# AI Generation Delete
@login_required(login_url='signIn')
@user_role_required
def useraiHistoryDelete(request, id):
    settings = websiteSetting.objects.first()
    if settings.is_enabled_for_user:
        record = get_object_or_404(OpenAIChatRecord, id=id, user=request.user)
        record.delete()
        messages.success(request, 'Deleted successfully!')
        return redirect('useraiHistory')
    else:
        return redirect('userDashboard')


# OpenAi Content Generation
@login_required(login_url='signIn')
@user_role_required
@csrf_exempt
def useropenAiContentGeneration(request, category):
    settings = websiteSetting.objects.first()
    if settings.is_enabled_for_user:
        openai.api_key = str(settings.openai_api)
        print(openai.api_key)

        if request.method == 'POST':
            user_input = request.POST.get('user_input')
            word_limit = request.POST.get('word_limit')
            print(user_input)
            print(word_limit)

            prompts = {
                'blog': f"Generate a blog post about {user_input} with a word limit of {word_limit} words.",
                'review': f"Write a review for {user_input} with a word limit of {word_limit} words.",
                'reply': f"Craft a reply for a customer review or comment about {user_input} with a word limit of {word_limit} words.",
                'social-media-post': f"Create engaging social media post about {user_input} with a word limit of {word_limit} words.",
                'email': f"Write an email that impresses and gets replies about {user_input} with a word limit of {word_limit} words.",
                'facebook-ads': f"Generate a Facebook Ads title and content about {user_input} with a word limit of {word_limit} words.",
                'google-ads': f"Create a Google Ads title and content about {user_input} with a word limit of {word_limit} words.",
                'guide': f"Generate a step-by-step guide about {user_input} with a word limit of {word_limit} words.",
                'proposal': f"Create a catchy proposal for buyers about {user_input} with a word limit of {word_limit} words.",
            }

            prompt = prompts.get(category, f"Generate content about {user_input}.")

            try:
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=prompt,
                    max_tokens=int(settings.max_token)
                )
                print(response)
                print(prompt)

                generated_content = response['choices'][0]['text']

                record = OpenAIChatRecord(user=request.user, user_input=user_input, bot_response=generated_content,
                                        category=category)
                record.save()

                return JsonResponse({'generated_content': generated_content})

            except openai.OpenAIError as e:
                error_message = f"OpenAI API Error: {e}"
            return JsonResponse({'error_message': error_message}, status=500)

        return render(request, 'user/main/ai/generator.html', {'category': category})
    else:
        return redirect('userDashboard')
    

# ====================Error Page====================
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)

def error_500(request):
    return render(request, 'error/error_500.html', status=500)