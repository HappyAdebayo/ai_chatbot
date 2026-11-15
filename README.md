# AI Task Assistant

A Python-based AI task assistant built with Google's Gemini API. This project is a practical learning project focused on understanding LLM application engineering.

The assistant interprets natural-language requests, converts them into structured outputs, executes task operations using Python and SQLite, and generates conversational responses.

## Features

- **LLM Integration:** Uses Google's Gemini API to process natural-language requests.
- **System Instructions:** Uses system instructions to guide assistant behaviour.
- **Structured Outputs:** Uses Pydantic to validate structured responses from the model.
- **Conversation History:** Maintains conversation context across interactions.
- **Task Operations:** Supports creating, viewing, updating, completing, and deleting tasks.
- **SQLite Database:** Stores task information locally.
- **Streaming Responses:** Streams generated responses to the terminal.
- **Token Tracking:** Measures input and output token usage across both Gemini requests.

## Tech Stack

- Python
- Google Gemini API (`google-genai`)
- Pydantic
- SQLite
- python-dotenv

## Project Structure

```text
ai_chatbot/
│
├── main.py
├── assistant.py
├── prompts.py
├── schemas.py
├── task_manager.py
├── database.py
├── utils.py
├── requirements.txt
├── .env
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd ai_chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Linux/macOS**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GENAI_API_KEY=your_gemini_api_key
```

Get an API key from [Google AI Studio](https://aistudio.google.com/).

### 5. Run the application

```bash
python main.py
```

## Learning Objectives

This project is being developed as a practical introduction to LLM application engineering.

Topics covered so far:

- LLM API integration
- Prompt engineering and system instructions
- Message roles and conversation history
- Structured outputs and Pydantic validation
- Python application logic and execution
- Streaming LLM responses
- Token usage tracking

