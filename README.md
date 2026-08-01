# Customer Support Chatbot

A simple **LLM-powered Customer Support Chatbot** built with **Python, Streamlit, and Google Gemini**. This project demonstrates how a customer support assistant can answer user queries using a predefined knowledge base and generate natural, human-like responses with an LLM.

The primary goal of this project is **learning**. The chatbot is intentionally built with a simple architecture so that each component can be understood before moving to more advanced concepts like semantic search, embeddings, and Retrieval-Augmented Generation (RAG).

---

## Features

* Customer support chatbot interface
* Interactive chat UI built with Streamlit
* Google Gemini API integration
* JSON-based knowledge base
* Keyword-based information retrieval
* Context-aware prompt engineering
* Chat history during the session
* Suggested questions in the sidebar
* Clean and modular project structure
* Beginner-friendly implementation

---

## Tech Stack

| Category              | Technology    |
| --------------------- | ------------- |
| Language              | Python        |
| UI                    | Streamlit     |
| LLM                   | Google Gemini |
| Data Storage          | JSON          |
| Environment Variables | python-dotenv |

---

## Project Structure

```text
Customer-Support-Chatbot/
│
├── app.py                  # Streamlit UI
├── chatbot.py              # Chatbot logic
├── knowledge_base.json     # Company FAQs
├── requirements.txt
├── .env
├── README.md
```

---

## Workflow

```text
User
   │
   ▼
Streamlit UI
   │
   ▼
User Question
   │
   ▼
Search Knowledge Base (JSON)
   │
   ▼
Retrieve Matching Information
   │
   ▼
Build Prompt
   │
   ▼
Google Gemini
   │
   ▼
Generate Natural Response
   │
   ▼
Display Response
```

---

## How It Works

### 1. User asks a question

Example:

> How do I reset my password?

---

### 2. Search the Knowledge Base

The chatbot searches the local JSON file using simple keyword matching.

Example:

```json
{
    "category": "Password Reset",
    "patterns": [
        "forgot password",
        "reset password",
        "cannot login"
    ],
    "answer": "Go to Settings > Security > Reset Password."
}
```

---

### 3. Build Prompt

The retrieved company information is combined with the user's question.

Example:

```text
Category:
Password Reset

Company Information:
Go to Settings > Security > Reset Password.

Customer Question:
How do I reset my password?
```

---

### 4. Gemini Generates the Response

Gemini rewrites the retrieved information into a professional customer support response while staying within the provided company information.

---

## Supported Categories

* Greeting
* Farewell
* Password Reset
* Refund
* Shipping
* Order Tracking
* Order Cancellation
* Address Update
* Damaged Product
* Payment Methods
* Payment Failed
* Account Registration
* International Shipping
* Contact Support

---

## Installation

Clone the repository

```bash
git clone https://github.com/your-username/customer-support-chatbot.git
```

Move into the project

```bash
cd customer-support-chatbot
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_API_KEY
MODEL_NAME=gemini-3.5-flash
```

---

## Run the Application

```bash
streamlit run app.py
```

---

## Example Questions

Account

* How do I reset my password?

Orders

* Where is my order?
* Can I cancel my order?

Payments

* What payment methods are accepted?
* My payment failed.

Shipping

* How long does shipping take?

Support

* How can I contact customer support?
* Can I talk to a human agent?

---

## Current Limitations

This project is intentionally simple.

Current limitations include:

* Uses keyword matching instead of semantic search.
* Knowledge base is stored locally in a JSON file.
* No authentication.
* No database.
* No conversation memory across sessions.
* No integration with real customer support systems.
* No ticket creation or order lookup.

These choices keep the project easy to understand and suitable for learning.

---

# What I Learned

This project helped me understand:

* Structuring a chatbot application
* Prompt engineering fundamentals
* Integrating Google Gemini API
* Building interactive applications with Streamlit
* Organizing a project into reusable modules
* Managing environment variables securely
* Using a structured knowledge base for information retrieval
* Separating retrieval logic from response generation

---

# Future Learning Roadmap

This project is designed to evolve gradually. Future improvements will focus on learning more advanced AI concepts while keeping the architecture modular.

### Stage 1 – Better Search

* Fuzzy matching
* Improved keyword ranking
* Better retrieval accuracy

---

### Stage 2 – Semantic Search

* Sentence embeddings
* Vector similarity
* Understanding user intent beyond exact keywords

---

### Stage 3 – Retrieval-Augmented Generation (RAG)

* PDF document support
* Company documentation
* Dynamic knowledge retrieval
* Larger knowledge bases

---

### Stage 4 – Production Features

* Database integration
* User authentication
* Order tracking APIs
* Ticket creation
* Multi-turn conversation memory
* Admin dashboard
* Analytics
* Deployment on cloud platforms

---

## Skills Demonstrated

* Python Programming
* Streamlit
* Google Gemini API
* Prompt Engineering
* JSON Data Handling
* Modular Programming
* Customer Support Chatbot Development
* LLM Application Development

---

## Acknowledgements

This project was built as a learning project to understand how modern LLM-powered customer support systems work by combining a structured knowledge base with a Large Language Model. It serves as a foundation for exploring more advanced conversational AI techniques in future iterations.
