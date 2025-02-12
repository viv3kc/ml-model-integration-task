# app/api/endpoints.py

import html

from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.core.config import settings
from app.core.manager import model_manager

router = APIRouter()


def render_html(code="", task="explain", provider=""):
    provider_display = provider or settings.default_model
    return f"""
    <html>
      <head>
        <title>Code Analysis Tool</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            margin: 0;
            padding: 20px;
          }}
          .container {{
            max-width: 800px;
            margin: auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
          }}
          textarea {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-family: monospace;
          }}
          input, select {{
            padding: 10px;
            margin-top: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 1em;
          }}
          input[type="submit"] {{
            background-color: #007BFF;
            color: white;
            border: none;
            cursor: pointer;
          }}
          input[type="submit"]:hover {{
            background-color: #0056b3;
          }}
          pre {{
            background: #eee;
            padding: 10px;
            border-radius: 4px;
            white-space: pre-wrap;
          }}
          /* Loading Spinner */
          #loading {{
            display: none;
            text-align: center;
            margin-top: 20px;
          }}
          .spinner {{
            border: 4px solid rgba(0, 0, 0, 0.1);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border-left-color: #09f;
            animation: spin 1s linear infinite;
            display: inline-block;
            vertical-align: middle;
          }}
          @keyframes spin {{
            to {{ transform: rotate(360deg); }}
          }}
          /* Markdown rendered content */
          #result-container {{
            margin-top: 20px;
          }}
          #error-container {{
            margin-top: 20px;
            color: red;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Code Analysis Tool</h1>
          <p>Current provider: {html.escape(provider_display)}</p>
          <form id="analysis-form">
            <label for="provider">Provider:</label><br>
            <input type="text" name="provider" value="{html.escape(provider_display)}"/><br>
            <label for="task">Task:</label><br>
            <select name="task">
              <option value="explain" {"selected" if task=="explain" else ""}>Explain</option>
              <option value="optimize" {"selected" if task=="optimize" else ""}>Optimize</option>
              <option value="security" {"selected" if task=="security" else ""}>Security</option>
              <option value="unit test" {"selected" if task=="unit test" else ""}>Unit Test</option>
            </select><br>
            <label for="code">Code:</label><br>
            <textarea name="code" rows="10" placeholder="Enter your code here...">{html.escape(code)}</textarea><br>
            <input type="submit" value="Analyze">
          </form>
          <div id="loading">
            <div class="spinner"></div>
            <p>Loading...</p>
          </div>
          <div id="result-container"></div>
          <div id="error-container"></div>
        </div>
        <!-- Include Marked.js for Markdown rendering -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/4.3.0/marked.min.js"></script>
        <script>
          document.getElementById('analysis-form').addEventListener('submit', async function(e) {{
            e.preventDefault();
            // Clear previous results and errors
            document.getElementById('result-container').innerHTML = "";
            document.getElementById('error-container').innerHTML = "";
            // Show loading spinner
            document.getElementById('loading').style.display = "block";

            const provider = document.getElementsByName('provider')[0].value;
            const task = document.getElementsByName('task')[0].value;
            const code = document.getElementsByName('code')[0].value;

            try {{
              const response = await fetch('/api/code/analyze', {{
                method: 'POST',
                headers: {{
                  'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ provider: provider, task: task, code: code }})
              }});
              const data = await response.json();
              if (!response.ok) {{
                throw new Error(data.detail || 'An error occurred');
              }}
              // Render the markdown response as HTML
              const renderedHTML = marked.parse(data.result);
              document.getElementById('result-container').innerHTML = renderedHTML;
            }} catch (error) {{
              document.getElementById('error-container').innerHTML = `<pre>${{error.message}}</pre>`;
            }} finally {{
              // Hide loading spinner
              document.getElementById('loading').style.display = "none";
            }}
          }});
        </script>
      </body>
    </html>
    """


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="HTML UI",
    description="Returns HTML interface for code analysis.",
)
async def get_ui():
    html_content = render_html()
    return HTMLResponse(content=html_content)


@router.post(
    "/analyze",
    response_class=HTMLResponse,
    summary="Analyze Code (HTML)",
    description="Analyzes code submitted via HTML form.",
)
async def analyze_ui(
    code: str = Form(...), task: str = Form("explain"), provider: str = Form("")
):
    provider_name = provider or settings.default_model
    try:
        prov = model_manager.get_provider(provider_name)
    except ValueError as e:
        html_content = render_html(
            code=code, task=task, provider=provider_name, error=str(e)
        )
        return HTMLResponse(content=html_content)
    try:
        result = await prov.analyze_code(code, task)
        html_content = render_html(
            code=code, task=task, provider=provider_name, result=result
        )
        return HTMLResponse(content=html_content)
    except Exception as e:
        html_content = render_html(
            code=code, task=task, provider=provider_name, error=str(e)
        )
        return HTMLResponse(content=html_content)


class CodePayload(BaseModel):
    code: str
    task: str = "explain"
    provider: str = None


@router.post(
    "/api/code/analyze",
    summary="Analyze Code (API)",
    description="Analyzes code via JSON payload with 'code', 'task', and optional 'provider'.",
)
async def code_analyze(payload: CodePayload):
    provider_name = payload.provider or settings.default_model
    try:
        provider = model_manager.get_provider(provider_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    try:
        result = await provider.analyze_code(payload.code, payload.task)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/api/models",
    summary="Supported Models",
    description="Returns supported models per provider. Optionally filter by provider.",
)
async def list_models(provider: str = None):
    if provider:
        try:
            p = model_manager.get_provider(provider)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {provider: p.supported_models}
    else:
        return {
            prov: model_manager.get_provider(prov).supported_models
            for prov in model_manager.list_providers()
        }


@router.get(
    "/api/llm_providers",
    summary="LLM Providers",
    description="Lists available LLM providers.",
)
async def list_providers():
    return {"llm_providers": model_manager.list_providers()}
