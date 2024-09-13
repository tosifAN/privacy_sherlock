from groq import Groq
import os

def getResponse(task):
    client = Groq(
        api_key=os.environ['GROQ_API_KEY'],
    )

    chat_completion = client.chat.completions.create(
         messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        {
            "role": "user",
            "content": task,
        }
        ],
         model="mixtral-8x7b-32768",
         )
    return chat_completion.choices[0].message.content