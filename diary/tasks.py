from celery import shared_task
import openai

@shared_task
def create_image_task(user_input):
    result = openai.Image.create(prompt=str(user_input), size="512x512")
    
    return result["data"][0]["url"]