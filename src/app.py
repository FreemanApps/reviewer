import os

from dotenv import load_dotenv
from fastapi import FastAPI
import psycopg

load_dotenv()
database_url = os.getenv("DATABASE_URL")

app = FastAPI()


@app.get("/")
def root():
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, value FROM public.playing_with_neon")
            for result in cur:
                print(result)
