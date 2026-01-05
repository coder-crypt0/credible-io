from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# This defines what input we expect from the user
class TextInput(BaseModel):
    content: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Credible.io backend is running"}

def generate_verification_suggestion(flags):
    if "Overconfident language" in flags:
        return "Check credible sources or studies that support this absolute claim."
    if "Insufficient context" in flags:
        return "Look for more detailed explanations or background information."
    return "Verify the claim using trusted academic or educational sources."

@app.post("/verify")
def verify_text(data: TextInput):
    text = data.content.lower()

    score = 80
    reasons = []
    flags = []

    if "definitely" in text or "always" in text:
        score -= 20
        flags.append("Overconfident language")
        reasons.append("Uses absolute terms without evidence.")

    if len(text.split()) < 10:
        score -= 10
        flags.append("Insufficient context")
        reasons.append("Text is too short to verify reliably.")

    suggestion = None
    if score < 70:
        suggestion = generate_verification_suggestion(flags)

    return {
        "credibility_score": score,
        "flags_detected": flags,
        "explanation": reasons,
        "final_verdict": (
            "Likely Reliable" if score >= 70 else "Needs Verification"
        ),
        "verification_suggestion": suggestion
    }


