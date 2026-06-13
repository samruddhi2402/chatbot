import google.generativeai as genai

from config import GEMINI_API_KEY
from prompts import SYSTEM_PROMPT

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.4,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4096,
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT,
    generation_config=generation_config,
)


def get_response(user_input, uploaded_code=None):

    explain_keywords = [
        "explain",
        "describe",
        "how",
        "why",
        "working",
        "algorithm",
        "detail",
        "deep",
    ]

    detailed = any(
        word in user_input.lower()
        for word in explain_keywords
    )

    if uploaded_code:

        final_prompt = f"""
You are an expert software development assistant.

Uploaded Code:

{uploaded_code}

User Question:

{user_input}

If the question is about the uploaded code:

- Explain purpose
- Explain every function
- Explain important variables
- Explain execution flow
- Mention time complexity
- Mention space complexity
- Suggest improvements

If the question is unrelated to the uploaded code, ignore the uploaded code completely and answer normally.

Use headings and bullet points.
"""

    else:

        final_prompt = user_input

    if detailed:

        final_prompt += """

Give a detailed explanation including:

- Definition
- Working
- Step-by-step explanation
- Example
- Code example
- Time Complexity
- Space Complexity
- Advantages
- Disadvantages
- Real-world applications

Use simple language.
"""

    try:

        response = model.generate_content(final_prompt)

        answer = ""

        if hasattr(response, "candidates"):

            for candidate in response.candidates:

                if hasattr(candidate, "content"):

                    for part in candidate.content.parts:

                        if hasattr(part, "text"):
                            answer += part.text

        if answer.strip():
            return answer

        return "⚠️ No response generated."

    except Exception as e:

        return f"⚠️ Error: {str(e)}"