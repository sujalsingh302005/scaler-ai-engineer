from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from rag import ask

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CAL_BOOKING_URL = os.getenv("CAL_BOOKING_URL")


class Query(BaseModel):
    question: str


class VoiceQuery(BaseModel):
    query: str


@app.get("/")
def home():
    return {
        "status": "running"
    }


@app.get("/booking")
def booking():
    return {
        "booking_url": CAL_BOOKING_URL
    }


@app.post("/chat")
def chat(query: Query):

    answer = ask(query.question)

    return {
        "answer": answer
    }


@app.post("/voice-rag")
def voice_rag(payload: VoiceQuery):

    answer = ask(payload.query)

    return {
        "answer": answer
    }