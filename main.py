from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your domain later
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompareRequest(BaseModel):
    item1: str
    item2: str
    category: str  # player or team

@app.post("/compare")
def compare(req: CompareRequest):
    prompt = f"""
    Compare the following two {req.category}s in detail:

    {req.item1} VS {req.item2}

    Include:
    - Overview
    - Strengths
    - Weaknesses
    - Key statistics (general knowledge)
    - Final verdict
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "comparison": response.choices[0].message.content
}
