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

    user_words = set(user_question.lower().split())

    best_match = None
    highest_score = 0

    for item in knowledge_base:

        score = 0

        for pattern in item["patterns"]:

            pattern_words = set(pattern.lower().split())

            matched_words = pattern_words.intersection(user_words)

            score += len(matched_words)

        if score > highest_score:
            highest_score = score
            best_match = item

    # minimum score required
    if highest_score >= 2:
        return best_match

    return None


# build prompt
def build_prompt(user_question, company_info):

    prompt = f"""
You are a professional customer support executive for an online shopping platform.

Your responsibility is to answer customer questions using ONLY the company information provided below.

Guidelines:

- Answer naturally like a real customer support executive.
- Keep the response short (2-4 sentences).
- Do not repeat the customer's question.
- Do not start every answer with "Hello", "Certainly", or "Sure".
- Do not end every response with "Please let us know if you need further assistance."
- Never make up information.
- If the company information is not enough, say:
  "Sorry, I couldn't find information related to your question."

Category:
{company_info["category"]}

Company Information:
{company_info["answer"]}

Customer Question:
{user_question}
"""

    return prompt


# send prompt to gemini
def ask_gemini(prompt):

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()


# chatbot workflow
def get_response(user_question):

    company_info = find_best_answer(user_question)

    if company_info is None:
        return "Sorry, I couldn't find information related to your question."

    prompt = build_prompt(user_question, company_info)

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