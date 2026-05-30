import requests
import os
from dotenv import load_dotenv

load_dotenv()

def evaluate_candidate(resume_text, role):

    prompt = f"""
You are an AI hiring assistant evaluating candidates for the role of {role}.

Your task is to analyze the resume and make a hiring decision based on relevance.

Evaluation Criteria:
1. Skills match with the role
2. Relevant work experience
3. Quality of projects
4. Overall role alignment

Scoring Guidelines:
- 80–100: Strong match → shortlisted
- 50–79: Partial match → review
- Below 50: Weak match → rejected

Instructions:
- Perform semantic understanding, not just keyword matching
- Be strict but fair in evaluation
- Avoid random or generic responses

Resume:
{resume_text}

Return ONLY valid JSON in this format:
{{
  "score": number (0-100),
  "decision": "shortlisted" or "rejected" or "review",
  "summary": "2-3 line professional evaluation",
  "skills_match": "percentage",
  "experience_match": "percentage"
}}
"""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
    )

    if response.status_code != 200:
        print(response.text)
        return "Error in AI response"

    result = response.json()

    try:
        return result["choices"][0]["message"]["content"]
    except:
        return "Error parsing AI response"


def generate_email(name, decision):

    if decision == "shortlisted":
        return f"""Hi {name},

Congratulations! You have been shortlisted for the next round.

We will contact you soon with interview details.

Best regards,
HR Team
"""

    elif decision == "rejected":
        return f"""Hi {name},

Thank you for applying.

We regret to inform you that you were not selected at this stage.

We wish you the best for future opportunities.

Best regards,
HR Team
"""

    else:
        return f"""Hi {name},

Thank you for your application.

Your profile is currently under review. We will get back to you shortly.

Best regards,
HR Team
"""