import httpx
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

async def get_directory_insights_api_key() -> str:
    # Replace this with the actual API key retrieval method
    return "2223d06e74650b3201529ac99e2d023039f91e01"

@app.post("/chat")
async def chat(query: Query, api_key: str = Depends(get_directory_insights_api_key)):
    url = "https://console.jumpcloud.com/api/insights/directory"
    headers = {"x-api-key": api_key}
    response = await httpx.post(url, json=query.dict(), headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from JumpCloud's Directory Insights API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
