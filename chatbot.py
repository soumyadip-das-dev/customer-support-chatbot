import json
import os

from dotenv import load_dotenv
from google import genai

# Load Environment Variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")
client = genai.Client(api_key=API_KEY)


# Load Knowledge Base
def load_knowledge_base():
    """
    Load all FAQs from the knowledge base.
    """
    with open("knowledge_base.json", "r", encoding="utf-8") as file:
        return json.load(file)


# Load once when the program starts
knowledge_base = load_knowledge_base()


# Search Knowledge Base

def find_best_answer(user_question):
    """
    Search the knowledge base using keyword matching.
    """
    user_question = user_question.lower()
    for item in knowledge_base:
        for pattern in item["patterns"]:
            if pattern.lower() in user_question:
                return item["answer"]
    return None



# Prompt Builder
def build_prompt(user_question, company_answer):

    prompt = f"""
You are a customer support assistant for an online shopping platform.

Your job is to answer using ONLY the company information provided.

Rules:
- Answer naturally like a human support executive.
- Keep responses short (2-4 sentences).
- Don't start every answer with "Hello" or "Certainly".
- Don't end every answer with "Please let us know if you need any further assistance."
- Only include additional help when it makes sense.
- Never make up information.
- If the company information is missing, say:
  "Sorry, I couldn't find information related to your question."

Company Information:
{company_answer}

Customer Question:
{user_question}
"""

    return prompt


# Gemini API
def ask_gemini(prompt):
    """
    Send the prompt to Gemini.
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text



# Main Chatbot Function
def get_response(user_question):
    """
    Complete chatbot workflow.
    """
    company_answer = find_best_answer(user_question)
    if company_answer is None:
        return "Sorry, I couldn't find information related to your question."
    prompt = build_prompt(user_question, company_answer)
    response = ask_gemini(prompt)
    return response


# Test
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