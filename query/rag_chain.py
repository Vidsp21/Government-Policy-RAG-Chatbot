import ollama
from config import LLM_MODEL

SYSTEM_PROMPT = """
You are a government policy assistant.
Answer strictly using the provided context.
If the answer is not present, say:
"The information is not available in the provided policy documents."

When answering follow-up questions:
- Refer back to previous questions and answers in the conversation
- Use pronouns and context from earlier messages
- Maintain consistency with previous responses
"""

# def generate_answer(context, question):
#     """Generate answer without conversation history """
#     prompt = f"""
# {SYSTEM_PROMPT}

# Context:
# {context}

# Question:
# {question}
# """

#     response = ollama.chat(
#         model=LLM_MODEL,
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )

#     return response["message"]["content"]

def generate_answer_with_history(context, question, conversation_history):
    """Generate answer with conversation history for follow-up questions"""
    
    # Build messages list with system prompt and history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add conversation history (limited to avoid token overflow)
    for entry in conversation_history:
        messages.append(entry)
    
    # Add current context and question
    current_prompt = f"""
Context from policy documents:
{context}

Current question:
{question}
"""
    
    messages.append({"role": "user", "content": current_prompt})
    
    # Generate response
    response = ollama.chat(
        model=LLM_MODEL,
        messages=messages
    )

    return response["message"]["content"]
