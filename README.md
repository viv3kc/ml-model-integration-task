# ML Model Integration Challenge

This FastAPI web app uses the OpenAI API to analyze code. It offers features like code explanation, performance optimization, security vulnerability detection, and unit test generation. The architecture is modular, allowing for future integration of additional ML providers such as Claude, Llama, etc.

> **Time Limit:** The solution was developed within a 2-hour timeframe, which influenced the prioritization of core functionalities.

> **User Interface:** The UI is basic, offering essential functionality with limited customization options.

## Features

- **Analysis Capabilities:**
  - **Code Explanation:** Clarify complex sections of code.
  - **Performance Optimization:** Suggest improvements for efficiency.
  - **Security Vulnerability Detection:** Identify potential security issues.
  - **Unit Test Generation:** Automatically generate unit tests.

## Implementation Overview

- **API Integration:** Utilizes the OpenAI API for code analysis.
- **Modular Architecture:** Designed to be easily extensible with additional ML models/providers.
- **Trade-offs:**
  - **API Dependency:** Requires an active internet connection and incurs API usage costs.
  - **Feature Scope:** Focused on core analysis functionalities with basic error handling.

## Prerequisites

- Python 3.8 or higher
- An active OpenAI API key (provided via email)
- Unix-like environment (for `run.sh`)
- Internet connection for API access

## Quick Start

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/viv3kc/ml-model-integration-task.git
   cd ml-model-integration-task
   ```

2. **Set Up Environment Variables:**

   Add your OpenAI API key in `.env` file:

   ```plaintext
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Run the Application:**

   Using the provided shell script:

   ```bash
   ./run.sh
   ```

   Alternatively, set up manually:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python main.py --port 8000
   ```

## API Documentation

### Web Interface

- **GET /**: Interactive web UI.
- **GET /docs**: Swagger documentation.

### REST API

- **POST /api/code/analyze**: Analyze code by providing a JSON payload:

  ```json
  {
    "code": "def example(): pass",
    "analysis_type": "explain|optimize|security|unit test"
  }
  ```

- **GET /api/models**: List available models.
- **GET /api/llm_providers**: List supported providers.

## Design Decisions & Trade-offs

- **Multi-Model Integration:**
  - **Pros:** Unified async interface that supports adding new ML providers easily.
  - **Cons:** Increased complexity and potential for higher latency and API costs.
- **FastAPI Infrastructure:**
  - **Pros:** High performance, quick prototyping, and built-in API documentation.
  - **Cons:** Basic error handling.
- **User Interface:**
  - **Pros:** Real-time markdown-rendered analysis.
  - **Cons:** Limited customization options.

## Future Improvements

- **Performance Enhancements:**
  - Implement history for LLM context.
  - Add request rate limiting and response validation.
- **Feature Enhancements:**
  - Integrate additional ML model providers.
  - Support analysis of files.
- **Development Enhancements:**
  - Comprehensive testing.
  - Detailed error logging and monitoring.

## Assumptions

- Designed for single-user or development environments.
- Intended for code snippets of moderate size.
- Assumes stable internet connectivity.
