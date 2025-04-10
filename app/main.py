from fastapi import FastAPI
from client.google_client import get_response
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = ["*","http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_llm_response/{message}")
def read_root(message: str):
    return get_response(message)    