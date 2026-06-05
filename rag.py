import os
from dotenv import load_dotenv

load_dotenv()

from groq import Groq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

BOOKING_LINK = os.getenv("CAL_BOOKING_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=GROQ_API_KEY
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="./db",
    embedding_function=embeddings
)

retriever = db.as_retriever(search_kwargs={"k": 5})


def ask(question):

    booking_keywords = [
        "schedule",
        "interview",
        "book",
        "meeting",
        "availability",
        "call"
    ]

    if any(word in question.lower() for word in booking_keywords):
        return f"""
You can schedule an interview with Sujal using the following link:

{BOOKING_LINK}

Choose any available slot that works for you.
"""

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are Sujal Singh's AI representative.

Answer questions only from the provided context.

Rules:
1. Never hallucinate.
2. If the answer is not in the context, say:
"I don't know based on my available information."
3. Stay factual and concise.
4. Answer only using retrieved information.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content