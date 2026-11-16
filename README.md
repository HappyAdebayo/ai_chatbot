# AI Task Assistant

A Python-based AI task assistant built with Google's Gemini API. This project is a hands-on learning project focused on understanding the fundamentals of **LLM application engineering**.

The assistant interprets natural-language requests, converts them into structured outputs, executes task operations using Python and SQLite, and generates conversational responses.

It demonstrates how to build an LLM-powered application by combining language models with structured data, application logic, validation, and controlled execution.

## Features

### LLM Integration
- Integrates Google's Gemini API using the `google-genai` SDK.
- Uses a two-stage LLM workflow to interpret requests and generate conversational responses.
- Separates model interpretation from actual task execution.

### Prompt Engineering and System Instructions
- Uses system instructions to define the assistant's behaviour and responsibilities.
- Provides separate instructions for request interpretation and final response generation.
- Uses explicit instructions to reduce unsupported claims and improve response accuracy.

### Structured Outputs and Validation
- Uses Pydantic to define the expected structure of model responses.
- Requests structured JSON output from Gemini.
- Validates model-generated responses before executing application logic.
- Handles invalid or unexpected model responses.

### Task Execution
- Converts natural-language requests into predefined task actions.
- Uses a handler registry to map supported actions to Python functions.
- Executes task operations through application code rather than allowing the model to modify the database directly.
- Supports creating, listing, updating, completing, and deleting tasks.

### Conversation History
- Maintains conversation history across interactions.
- Uses message roles to distinguish user messages from assistant responses.
- Preserves conversational context between requests.

### Context-Window Management
- Tracks the token usage of conversation history and system instructions.
- Implements an application-level input token budget.
- Removes older conversation exchanges when the token budget is exceeded.
- Preserves the most recent conversation context where possible.

### Streaming Responses
- Streams Gemini-generated responses to the terminal.
- Displays response text as it is generated instead of waiting for the complete response.

### Token Usage Tracking
- Tracks input, output, and total token usage.
- Combines token usage from both Gemini requests.
- Helps monitor the token cost of individual interactions.

### Model Configuration
- Separates model settings from application logic.
- Configures generation parameters such as temperature and maximum output tokens.
- Makes model configuration easier to maintain and modify.

### Error Handling and Hallucination Safeguards
- Handles Gemini API errors.
- Handles invalid structured responses.
- Prevents the application from treating unsuccessful task operations as successful.
- Uses execution results as the source of truth when generating final responses.
- Instructs the model not to invent task details or claim actions were completed without confirmation from the application.

### Database
- Uses SQLite for local task persistence.
- Separates database operations from the assistant's conversational logic.

## Tech Stack

- **Python** – Application logic and task execution.
- **Google Gemini API** – Natural-language understanding and response generation.
- **google-genai** – Gemini Python SDK.
- **Pydantic** – Structured output validation.
- **SQLite** – Local task storage.
- **python-dotenv** – Environment variable management.

## Project Structure

```text
ai_chatbot/
│
├── main.py
├── assistant.py
├── config.py
├── prompts.py
├── schemas.py
├── task_manager.py
├── database.py
├── utils.py
├── requirements.txt
├── .env
└── README.md
```

### Main Components

- `main.py` – Application entry point and terminal interaction.
- `assistant.py` – Handles Gemini requests, conversation history, structured response processing, task execution, and streaming.
- `config.py` – Stores model configuration and generation parameters.
- `prompts.py` – Contains system instructions and response-generation instructions.
- `schemas.py` – Defines Pydantic models used to validate structured LLM outputs.
- `task_manager.py` – Contains task-related operations.
- `database.py` – Handles SQLite database setup and interaction.
- `utils.py` – Contains utility functions for token tracking and conversation context management.

## Getting Started

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd ai_chatbot
```

### 2. Create a Virtual Environment

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

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GENAI_API_KEY=your_gemini_api_key
```

Get your API key from [Google AI Studio](https://aistudio.google.com/).

Keep your `.env` file private. Do not commit API keys or other secrets to GitHub.

### 5. Run the Application

```bash
python main.py
```

## How It Works

The assistant follows a structured workflow:

1. **User Input:** The user enters a natural-language request through the terminal.
2. **Context Preparation:** The application adds the request to conversation history and checks the input token budget.
3. **LLM Interpretation:** Gemini processes the conversation and returns a structured JSON response following the Pydantic schema.
4. **Validation:** The application validates the model response before processing it.
5. **Action Execution:** The handler registry maps the requested action to the appropriate Python function.
6. **Response Generation:** The application sends the action result to Gemini to generate a natural-language response.
7. **Streaming:** The final response is streamed to the terminal.
8. **Token Tracking:** Token usage from both Gemini requests is combined and displayed.

This approach keeps language-model interpretation separate from application execution, allowing Python to control how operations are performed.

## Learning Objectives

This project is being developed as a practical introduction to LLM application engineering.

Topics covered:

- LLM API integration
- Prompt engineering and system instructions
- Message roles and conversation history
- Structured outputs and Pydantic validation
- LLM request and response workflows
- Python application logic and execution
- Handler registry pattern for action dispatching
- Streaming LLM responses
- Token counting and usage tracking
- Context-window management
- Model configuration
- API and application error handling
- Grounding responses in actual execution results
- Basic hallucination prevention techniques
