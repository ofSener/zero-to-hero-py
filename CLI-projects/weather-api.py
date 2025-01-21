import os
from openai import OpenAI

#read the api key from the .env file
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Sen bir hava durumu asistanısın. Türkiye'deki hava durumu hakkında bilgi verirsin."
        },
        {
            "role": "user",
            "content": "İstanbul'da bugün hava nasıl olacak?"
        }
    ],
    model="gpt-3.5-turbo",  # veya "gpt-3.5-turbo" kullanabilirsiniz
)
print(chat_completion.choices[0].message.content)