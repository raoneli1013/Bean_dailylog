from celery import shared_task
import openai
openai.api_key = "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"
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

    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=gpt_prompt)
    prompt = chat_completion['choices'][0]['message']['content']
    print(prompt)
    result = openai.Image.create(prompt=str(prompt), size="512x512")
    
    return result

# for test
@shared_task
def add(x, y):
    return x + y