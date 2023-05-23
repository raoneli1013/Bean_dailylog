from celery import shared_task
import openai

@shared_task
def create_image_task(user_input):
    gpt_prompt = []
    gpt_prompt.append({
        "role": "system",
        "content": "Write a prompt to create an image as a series of words at the daily of the user."
    })

    gpt_prompt.append({
        "role": "user",
        "content": user_input
    })

    prompt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=gpt_prompt)
    
    result = openai.Image.create(prompt=prompt,size="512x512")
    return prompt

# for test
@shared_task
def add(x, y):
    return x + y