import json
import os

from dotenv import load_dotenv
from google import genai

# load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

client = genai.Client(api_key=API_KEY)


# load knowledge base
def load_knowledge_base():
    with open("knowledge_base.json", "r", encoding="utf-8") as file:
        return json.load(file)


knowledge_base = load_knowledge_base()


# search for the best matching answer
def find_best_answer(user_question):

    user_question = user_question.lower()

    for item in knowledge_base:

        for pattern in item["patterns"]:

            if pattern.lower() in user_question:
                return item

    return None


# build prompt
def build_prompt(user_question, company_info, chat_history):

    history_text = ""

    for message in chat_history:
        history_text += f"{message['role']}: {message['content']}\n"

    return f"""
You are a professional customer support executive for an online shopping platform.

Your job is to answer customer questions using the company information provided below.

Guidelines:

- Answer naturally like a real customer support executive.
- Keep the response short and clear.
- Use the conversation history when the customer asks a follow-up question.
- Do not repeat the customer's question.
- Do not invent information.
- Only use information supported by the company information.
- If the information is not available, say:
  "Sorry, I couldn't find information related to your question."

Conversation History:
{history_text}

Category:
{company_info["category"]}

Company Information:
{company_info["answer"]}

Current Customer Question:
{user_question}
"""


# send prompt to gemini
def ask_gemini(prompt):

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()


# chatbot workflow
def get_response(user_question, chat_history=None):

    if chat_history is None:
        chat_history = []

    company_info = find_best_answer(user_question)

    if company_info is None:
        return "Sorry, I couldn't find information related to your question."

    prompt = build_prompt(
        user_question,
        company_info,
        chat_history
    )

    response = ask_gemini(prompt)

    return response

# terminal testing
if __name__ == "__main__":

    print("=" * 50)
    print(" Customer Support Chatbot ")
    print("=" * 50)

    while True:

        question = input("\nYou : ")

        if question.lower() in ["exit", "quit"]:
            print("\nChatbot : Thank you! Have a great day.")
            break

        response = get_response(question)

        print(f"\nChatbot : {response}")