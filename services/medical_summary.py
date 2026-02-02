from backend.models.medical_artifact import MedicalArtifact
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# -------------------------------------------------
# Load environment variables (.env) safely on Windows
# -------------------------------------------------
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# -------------------------------------------------
# Initialize Gemini client
# -------------------------------------------------
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def build_medical_context(artifacts: list[MedicalArtifact]) -> str:
    """
    Converts medical artifacts into a readable text context
    suitable for summarization.
    """
    if not artifacts:
        return "No medical records are available."

    lines = []

    for a in artifacts:
        line = f"- [{a.type.upper()}] {a.title}"

        if a.event_date:
            line += f" on {a.event_date.date()}"

        if isinstance(a.data, dict):
            details = ", ".join(f"{k}: {v}" for k, v in a.data.items())
            line += f" ({details})"

        lines.append(line)

    return "\n".join(lines)


def generate_summary_from_context(context: str) -> str:
    """
    Uses Gemini to generate a safe medical summary.
    Falls back gracefully if Gemini fails or quota is exceeded.
    """

    prompt = f"""
You are a medical record summarization assistant.

STRICT RULES:
- Do NOT diagnose
- Do NOT give medical advice
- Do NOT suggest treatments
- Do NOT speculate
- Only summarize provided facts
- Use neutral, factual language
- Write in bullet points

Medical records:
{context}

Output format:
Medical Summary:
• ...
• ...
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-pro-latest",
            contents=prompt
        )

        if not response or not response.text:
            return "Medical Summary:\n• No summary could be generated."

        return response.text.strip()

    except Exception as e:
        # IMPORTANT: Never crash the API because of LLM failures
        return (
            "Medical Summary:\n"
            "• Summary is temporarily unavailable due to AI service limits.\n"
            "• Please try again later."
        )
