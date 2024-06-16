import openai
import os

def suggest_changes(message):
    print(os.environ['OPENAI_KEY'])
    openai.api_key=os.environ['OPENAI_KEY']

    messages = [ {"role": "system", "content":
                  "You are a code reviewer, reviewing code changes and suggesting changes as per best practices."} ]
    # message = input("User : ")
    message = "Can you suggest changes in the below code snippet? \n" + message
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k", messages=messages
        )
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})
