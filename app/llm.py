import requests


def generate_answer(question, context_chunks):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an enterprise document assistant.

Use ONLY the provided context.

Rules:
- Answer the user's question directly.
- If the question asks for a summary, summarize the main topic of the document.
- Do not focus on random details unless they are central to the document.
- Do not include copyright text, page numbers, headers, or footers.
- Do not make up information.
- If the context has related information, answer from it.
- Only say information is missing if the context has no relevant information.


Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"]