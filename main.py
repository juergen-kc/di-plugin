"""
main.py: A FastAPI app to create a ChatGPT plugin that queries with JC's Directory Insights.
"""

import httpx
from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    """
    A Pydantic model representing a query containing a question.
    """
    question: str

async def get_directory_insights_api_key() -> str:
    """
    Retrieve the API key for JumpCloud's Directory Insights API.
    
    Returns:
        str: The API key as a string.
    """
    # Replace this with the actual API key retrieval method
    return "YOUR_API_KEY"

@app.post("/chat")
async def chat(query: Query, api_key: str = Depends(get_directory_insights_api_key)):
    """
    Process a chat query by interacting with JumpCloud's Directory Insights API.

    Args:
        query (Query): A Pydantic model containing the question.
        api_key (str): The API key for JumpCloud's Directory Insights API.

    Returns:
        dict: The response from JumpCloud's Directory Insights API or an error message.
    """
    url = "https://api.jumpcloud.com/insights/directory/v1/events"
    headers = {"x-api-key": api_key}
    data = {
        "service": ["all"],
        "start_time": query.question
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        return {"error": "Unauthorized access to JumpCloud's Directory Insights API"}
    elif response.status_code == 403:
        return {"error": "Forbidden access to JumpCloud's Directory Insights API"}
    else:
        return {"error": f"Failed to fetch data from DI API (Status code: {response.status_code})"}

@app.get("/.well-known/ai-plugin.json")
async def serve_ai_plugin_json_get():
    """
    Serve the ai-plugin.json file located in the .well-known folder.

    Returns:
        FileResponse: The ai-plugin.json file as a FileResponse with media type application/json.
    """
    return FileResponse("./.well-known/ai-plugin.json", media_type="application/json")

@app.options("/.well-known/ai-plugin.json")
async def serve_ai_plugin_json_options():
    """
    Handle OPTIONS requests for the ai-plugin.json file.

    Returns:
        Response: An empty response with a 204 status code.
    """
    return Response(status_code=204)

@app.get("/.well-known/openapi.yaml")
async def serve_openapi_yaml_get():
    """
    Serve the openapi.yaml file located in the .well-known folder.

    Returns:
        FileResponse: The openapi.yaml file as a FileResponse with media type application/x-yaml.
    """
    return FileResponse("./.well-known/openapi.yaml", media_type="application/x-yaml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

