from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# -----------------------------
# App initialization
# -----------------------------
app = FastAPI()

# -----------------------------
# CORS (for frontend + extension)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # OK for hackathon / local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Data models
# -----------------------------
class TextInput(BaseModel):
    content: str
    source_url: str | None = None


class RepairResponse(BaseModel):
    original_text: str
    repaired_text: str
    repair_explanation: str


# -----------------------------
# Root endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "Credible.io backend is running"}


# -----------------------------
# Helper function
# -----------------------------
def generate_verification_suggestion(flags):
    if "Overconfident language" in flags:
        return "Check credible sources or studies that support this absolute claim."
    if "Insufficient context" in flags:
        return "Look for more detailed explanations or background information."
    return "Verify the claim using trusted academic or educational sources."


# =====================================================
# VERIFY ENDPOINT
# =====================================================
@app.post("/verify")
def verify_text(data: TextInput):
    """
    Explainable credibility verification (heuristic MVP).
    """
    try:
        text = data.content.lower()

        score = 80
        flags = []
        reasons = []

        # --- Linguistic risk checks ---
        if "definitely" in text or "always" in text:
            score -= 20
            flags.append("Overconfident language")
            reasons.append("Uses absolute terms without supporting evidence.")

        if len(text.split()) < 10:
            score -= 10
            flags.append("Insufficient context")
            reasons.append("Text is too short to verify reliably.")

        # --- Source authority boost ---
        authority_bonus = 0

        if data.source_url:
            if "wikipedia.org" in data.source_url:
                authority_bonus = 10
                reasons.append(
                    "Source is Wikipedia (community-reviewed reference platform)."
                )
            elif ".edu" in data.source_url or ".gov" in data.source_url:
                authority_bonus = 15
                reasons.append(
                    "Source is an educational or government domain."
                )

        score += authority_bonus
        score = min(score, 100)

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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# LIVE MISINFORMATION REPAIR ENDPOINT
# =====================================================
@app.post("/repair", response_model=RepairResponse)
def repair_text(data: TextInput):
    """
    Live Misinformation Repair (MVP)

    - Does NOT claim absolute truth
    - Rewrites only risky phrasing
    - Preserves original meaning
    - Fully explainable
    """
    try:
        original_text = data.content
        text_lower = original_text.lower()

        needs_repair = False
        reasons = []

        # --- Reuse same risk logic ---
        if "definitely" in text_lower or "always" in text_lower:
            needs_repair = True
            reasons.append(
                "Replaced absolute language with evidence-aware phrasing."
            )

        if len(original_text.split()) < 10:
            needs_repair = True
            reasons.append(
                "Clarified content due to insufficient context."
            )

        # --- If no repair needed ---
        if not needs_repair:
            return {
                "original_text": original_text,
                "repaired_text": original_text,
                "repair_explanation": (
                    "No risky or misleading claims detected. No repair required."
                )
            }

        # --- Conservative repair logic (MVP-safe) ---
        repaired_text = original_text

        if "definitely" in text_lower:
            repaired_text = repaired_text.replace(
                "definitely",
                "according to available evidence"
            )

        if "always" in text_lower:
            repaired_text = repaired_text.replace(
                "always",
                "in most documented cases"
            )

        explanation = " ".join(reasons)

        return {
            "original_text": original_text,
            "repaired_text": repaired_text,
            "repair_explanation": explanation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



