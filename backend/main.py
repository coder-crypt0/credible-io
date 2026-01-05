from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# This defines what input we expect from the user
class TextInput(BaseModel):
    content: str

@app.get("/")
def root():
    return {"message": "Credible.io backend is running"}

@app.post("/verify")
def verify_text(data: TextInput):
    text = data.content

    # VERY SIMPLE credibility logic (for MVP)
    score = 80
    explanation = "Content appears factual and well-structured."

    # If text sounds too confident but gives no evidence
    if "definitely" in text.lower() or "always" in text.lower():
        score -= 20
        explanation = "Overconfident language detected without supporting evidence."

    return {
        "credibility_score": score,
        "explanation": explanation
    }
