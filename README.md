# Customer Support Chatbot

A simple LLM-powered customer support chatbot built with **Python, Streamlit, Google Gemini, and a JSON-based knowledge base**.

The chatbot is designed to answer common customer support questions, maintain conversation context, and generate natural responses using an LLM. The project is intentionally built with a simple architecture so that the underlying concepts can be understood before introducing more advanced techniques.

## Live Demo

[Customer Support Chatbot — Live Demo](https://customer-support-chatbot-nkac8usmzurksuqmeqncwj.streamlit.app/?utm_source=chatgpt.com)

---

## Project Goal

The goal of this project is to understand how an LLM-powered customer support application works from end to end.

The current application combines:

```text
Customer Question
        ↓
Streamlit Chat Interface
        ↓
Knowledge Base Search
        ↓
Relevant Company Information
        ↓
Conversation Context
        ↓
Prompt
        ↓
Google Gemini
        ↓
Natural Customer Support Response
```

The project currently uses a **local JSON knowledge base** instead of a database or document retrieval system. This keeps the implementation simple and makes the fundamental chatbot workflow easier to understand.

---

# Current Features

## 1. Interactive Chat Interface

The application uses Streamlit to provide a web-based chat interface.

Users can:

* Enter questions using the chat input.
* View previous messages.
* Continue the conversation.
* Clear the conversation.
* Use suggested questions from the sidebar.

---

## 2. Suggested Questions

The sidebar provides example questions so users can quickly test the chatbot.

Current categories include:

### Account

* Reset Password

### Orders

* Track Order
* Cancel Order
* Change Address

### Payments

* Payment Methods
* Payment Failed
* Refund Policy

### Shipping

* Shipping Time
* International Shipping

### Support

* Contact Support
* Human Agent

The suggested questions are directly connected to the current knowledge base so that the UI does not expose unsupported examples.

---

## 3. JSON Knowledge Base

The chatbot currently uses a local `knowledge_base.json` file.

Each entry contains:

```json
{
    "category": "Password Reset",
    "patterns": [
        "forgot password",
        "reset password",
        "password reset",
        "cannot login"
    ],
    "answer": "Go to Settings > Security > Reset Password."
}
```

The three important parts are:

### Category

Identifies the type of customer request.

Example:

```text
Password Reset
```

### Patterns

Contains phrases that can be used to identify the request.

Example:

```text
forgot password
reset password
cannot login
```

### Answer

Contains the official company information that can be given to the customer.

---

# Current Knowledge Base Categories

The current knowledge base contains information for:

* Greeting
* Farewell
* Password Reset
* Refund
* Shipping
* Order Tracking
* Order Cancellation
* Address Update
* Damaged Product
* Payment
* Payment Failed
* Account Registration
* International Shipping
* Contact Support

---

# 4. Simple Keyword-Based Retrieval

The chatbot currently uses a simple keyword matching approach.

The process is:

```text
User Question
      ↓
Convert question to lowercase
      ↓
Check knowledge base patterns
      ↓
Find matching pattern
      ↓
Return matching knowledge item
```

For example:

```text
User:
Where is my order?
```

The system checks the patterns:

```text
track order
where is my order
order status
track my package
```

The pattern:

```text
where is my order
```

matches the question.

The corresponding knowledge-base item is then passed to the next stage.

### Why simple keyword matching?

This was intentionally chosen instead of embeddings or vector databases.

It makes the retrieval process easy to understand and debug.

The current philosophy is:

> Keep the retrieval simple until there is a real reason to make it more advanced.

---

# 5. Conversation Context

The chatbot now maintains conversation history using Streamlit session state.

For example:

```text
User:
What is your refund policy?

Assistant:
Products can be returned within 7 days of delivery.

User:
How many days?

Assistant:
The return period is 7 days from the date of delivery.
```

Previously, the second question could fail because:

```text
"How many days?"
```

does not directly match the JSON knowledge base.

The current implementation handles this by checking the previous user question when the current question does not produce a direct match.

---

# Context-Aware Retrieval

The current retrieval flow is:

```text
Current Question
       ↓
Search JSON
       ↓
Match found?
   /          \
 Yes           No
 ↓             ↓
Use match    Check previous user question
                    ↓
               Search JSON
                    ↓
               Match found?
                 /     \
               Yes      No
                ↓        ↓
             Continue   Fallback
```

This is intentionally a basic form of conversational context.

It is not semantic memory or a vector search system.

---

# 6. Prompt Engineering

After retrieving relevant company information, the application builds a prompt for Gemini.

The prompt contains:

```text
Conversation History

Category

Company Information

Current Customer Question
```

The model is instructed to:

* Answer like a customer support executive.
* Keep responses short and clear.
* Use conversation history for follow-up questions.
* Avoid unnecessary greetings.
* Avoid repeating the customer's question.
* Avoid inventing information.
* Use only the supplied company information.

This separates the responsibilities of the application and the LLM.

---

# 7. Gemini Integration

Google Gemini is responsible for generating the final natural-language response.

The application sends a prompt using the Google GenAI Python SDK.

Conceptually:

```text
Retrieved Information
        +
Conversation Context
        +
Customer Question
        ↓
      Gemini
        ↓
Natural Language Response
```

The LLM is not treated as the source of company facts.

The JSON knowledge base provides the information, while Gemini is primarily responsible for turning that information into a natural customer-support response.

---

# 8. Fallback Handling

If the chatbot cannot find relevant information, it does not ask Gemini to guess.

Instead, it returns:

```text
Sorry, I couldn't find information related to your question.
```

For example:

```text
User:
Do you sell laptops?
```

Since the current knowledge base does not contain information about laptops, the chatbot does not invent an answer.

This is an important design decision because customer-support systems should prioritize **known information over hallucinated information**.

---

# Project Structure

The current project is intentionally small.

```text
Customer-Support-Chatbot/
│
├── app.py
├── chatbot.py
├── knowledge_base.json
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
└── .venv/
```

### `app.py`

Responsible for the user interface.

Main responsibilities:

* Streamlit configuration
* Page layout
* Sidebar
* Suggested questions
* Chat history
* User input
* Displaying chatbot responses

---

### `chatbot.py`

Contains the chatbot logic.

Main responsibilities:

* Loading environment variables
* Connecting to Gemini
* Loading the knowledge base
* Searching the knowledge base
* Building prompts
* Sending prompts to Gemini
* Handling conversation context
* Returning the final response

---

### `knowledge_base.json`

Contains the customer-support information used by the chatbot.

This is currently the chatbot's primary source of factual information.

---

### `.env`

Stores private configuration such as:

```text
GEMINI_API_KEY
MODEL_NAME
```

The `.env` file should never be committed to GitHub.

---

### `requirements.txt`

Contains the Python dependencies required to run the project.

---

# Technical Architecture

The current architecture is intentionally simple:

```text
                    ┌───────────────────┐
                    │     Customer      │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Streamlit UI    │
                    │      app.py       │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Chatbot Controller│
                    │    chatbot.py     │
                    └─────────┬─────────┘
                              │
                     Search Knowledge Base
                              │
                              ▼
                    ┌───────────────────┐
                    │ knowledge_base    │
                    │      .json        │
                    └─────────┬─────────┘
                              │
                     Relevant Information
                              │
                              ▼
                    ┌───────────────────┐
                    │   Prompt Builder  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Google Gemini   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Customer Response │
                    └───────────────────┘
```

---

# Important Design Principle

The current application follows a simple separation of responsibilities:

### Application Logic

Responsible for:

* Finding information.
* Managing conversation state.
* Controlling the workflow.
* Handling missing information.

### Knowledge Base

Responsible for:

* Providing company facts.
* Providing supported customer-support topics.

### Gemini

Responsible for:

* Understanding the supplied context.
* Producing natural language.
* Formatting the response conversationally.

This is preferable to simply sending every question directly to an LLM.

---

# Example Conversation

### Basic FAQ

```text
Customer:
What is your refund policy?

Assistant:
Products can be returned within 7 days of delivery.
```

### Follow-up Question

```text
Customer:
What is your refund policy?

Assistant:
Products can be returned within 7 days of delivery.

Customer:
How many days?

Assistant:
The return period is 7 days from the date of delivery.
```

### Unknown Question

```text
Customer:
Do you sell laptops?

Assistant:
Sorry, I couldn't find information related to your question.
```

---

# Running the Project Locally

## 1. Clone the repository

```bash
git clone <your-repository-url>
```

## 2. Open the project

```bash
cd Customer-Support-Chatbot
```

## 3. Create a virtual environment

```bash
python -m venv .venv
```

## 4. Activate the environment

Windows:

```bash
.venv\Scripts\activate
```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 6. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
MODEL_NAME=your_available_gemini_model
```

## 7. Run the application

```bash
streamlit run app.py
```

---

# Git Workflow Used During Development

The project is being developed incrementally.

The workflow is:

```text
Implement Feature
      ↓
Run Application
      ↓
Test Feature
      ↓
Fix Problems
      ↓
Commit Change
      ↓
Push to GitHub
      ↓
Start Next Feature
```

This keeps the Git history meaningful because each commit represents a specific development step.

Examples of commits include:

```text
Add conversation context to chatbot
Fix conversation context handling
```

This also makes it easier to understand how the application evolved.

---

# Current Limitations

The current implementation is intentionally limited.

### Retrieval

The chatbot uses basic keyword matching.

Therefore, different wording can sometimes fail to find the correct information.

For example:

```text
How can I track it?
```

may not directly match a pattern such as:

```text
track order
```

The current context fallback helps with some follow-up questions, but it is not a complete semantic retrieval system.

### Knowledge Base

The knowledge base is stored in a local JSON file.

There is currently:

* No database.
* No document ingestion.
* No vector database.
* No external company data source.

### Customer Operations

The chatbot currently provides information but does not perform real business operations.

It cannot currently:

* Retrieve a real order.
* Create a real support ticket.
* Modify an order.
* Process a refund.
* Contact a support representative.

### Conversation Memory

Conversation history currently exists only during the active Streamlit session.

It is not stored permanently.

---

# Future Work

The next improvements should be implemented gradually rather than all at once.

## 1. Order Tracking

Introduce a local `orders.json` file containing sample order information.

Example:

```json
{
    "order_id": "ORD1001",
    "status": "Shipped",
    "estimated_delivery": "2026-08-15"
}
```

The chatbot should be able to handle:

```text
Customer:
Where is my order?

Assistant:
Please provide your order ID.

Customer:
ORD1001

Assistant:
Your order ORD1001 has been shipped.
```

This will introduce the concept of **application logic + structured business data**.

---

## 2. Support Ticket Creation

Introduce a `tickets.json` file.

The chatbot could create a support ticket when an issue cannot be resolved through the knowledge base.

Example:

```text
Customer:
My product arrived damaged.

Assistant:
I can help you create a support ticket. Please provide your order ID.

Customer:
ORD1001

Assistant:
Your support ticket has been created.
```

This introduces a real business workflow.

---

## 3. Human Escalation

Allow the chatbot to recognize when a customer needs human assistance.

Possible workflow:

```text
Customer
   ↓
Chatbot
   ↓
Can chatbot resolve issue?
   ├── Yes → Answer
   │
   └── No → Offer support ticket
                    ↓
              Human Support
```

---

## 4. Better Retrieval

Improve the current keyword search without changing the rest of the application.

Possible progression:

```text
Keyword Matching
       ↓
Fuzzy Matching
       ↓
Semantic Similarity
       ↓
Embeddings
```

This will demonstrate why different retrieval techniques are useful.

---

## 5. Semantic Search

Introduce embeddings so that the chatbot can understand similar meanings.

For example:

```text
Where is my package?

Where can I see my shipment?

How do I track my delivery?
```

These questions should be recognized as related even when they do not share the same exact words.

---

## 6. Retrieval-Augmented Generation

After understanding basic retrieval, the knowledge source can be expanded beyond JSON.

Possible sources:

```text
Company FAQs
      +
Product Documentation
      +
Policies
      +
Help Articles
      ↓
Retriever
      ↓
Relevant Context
      ↓
Gemini
      ↓
Answer
```

This would introduce the fundamentals of **RAG**.

---

## 7. Database

The JSON files can eventually be replaced with a database.

For example:

```text
JSON
 ↓
SQLite
 ↓
PostgreSQL / MongoDB
```

This would allow the application to handle larger amounts of structured business data.

---

## 8. Backend API

The current application does not require a separate backend.

A future architecture could introduce:

```text
Streamlit / Web UI
        ↓
Backend API
        ↓
Business Logic
        ↓
Database
        ↓
LLM Services
```

This would make the application closer to a production-style system.

---

## 9. Authentication

A future version could support customer accounts.

Authentication could allow the system to securely access information such as:

```text
Customer Account
      ↓
Authenticated User
      ↓
Customer Orders
      ↓
Order Status
```

This should only be introduced once the basic business workflow is understood.

---

## 10. Production-Level Improvements

Longer-term improvements could include:

* API-based backend
* Database
* Authentication and authorization
* Logging
* Monitoring
* Rate limiting
* Error tracking
* Automated testing
* Conversation analytics
* Admin dashboard
* Human-agent handoff
* External support-system integration
* Secure handling of customer data

---

# Learning Roadmap

The project can be used to gradually learn modern LLM application development.

```text
Current
  │
  ├── Python
  ├── Streamlit
  ├── JSON
  ├── Gemini API
  ├── Prompt Engineering
  └── Basic Retrieval
       │
       ▼
Conversation Context
       │
       ▼
Structured Business Data
       │
       ▼
Order Tracking
       │
       ▼
Support Tickets
       │
       ▼
Fuzzy Retrieval
       │
       ▼
Embeddings
       │
       ▼
RAG
       │
       ▼
Database
       │
       ▼
Backend API
       │
       ▼
Production LLM Application
```

---

# Technologies

Current:

* Python
* Streamlit
* Google Gemini
* Google GenAI Python SDK
* JSON
* python-dotenv
* Git
* GitHub

Potential future technologies:

* RapidFuzz
* Embedding models
* Vector databases
* RAG frameworks
* SQLite/PostgreSQL/MongoDB
* FastAPI
* Authentication
* Cloud deployment
* Logging and monitoring

---

# What This Project Demonstrates

The current project demonstrates the fundamentals of building an LLM application rather than simply calling an AI API.

It covers:

* Building a chatbot UI
* Managing application state
* Structuring a knowledge base
* Basic information retrieval
* Prompt construction
* LLM integration
* Conversation context
* Fallback handling
* Separating application logic from LLM generation
* Deploying a Streamlit application
* Using Git and GitHub for incremental development

---

# Current Status

The chatbot currently has:

* [x] Streamlit chat interface
* [x] Gemini API integration
* [x] JSON knowledge base
* [x] Keyword-based retrieval
* [x] Prompt engineering
* [x] Conversation history
* [x] Context-aware follow-up retrieval
* [x] Suggested questions
* [x] Sidebar navigation
* [x] Clear conversation functionality
* [x] Unknown-question fallback
* [x] Streamlit deployment
* [x] GitHub-based incremental development

## Next Development Target

**Order Tracking with local structured order data.**

The next major concept will be moving from:

```text
Question
    ↓
FAQ
    ↓
Answer
```

to:

```text
Question
    ↓
Understand Request
    ↓
Retrieve Business Data
    ↓
Process Data
    ↓
Generate Response
```

This will be the first step toward making the chatbot perform practical customer-support tasks instead of only answering predefined FAQs.

---

## Author

Built as a learning project to understand **LLM-powered customer support systems, conversational AI, information retrieval, prompt engineering, and practical LLM application development**.
