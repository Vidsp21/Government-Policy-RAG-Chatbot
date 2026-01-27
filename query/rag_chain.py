import ollama
from config import LLM_MODEL

SYSTEM_PROMPT = """
You are a government policy assistant.
Answer strictly using the provided context.
If the answer is not present, say:
"The information is not available in the provided policy documents."
"""

def generate_answer(context, question):
    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
