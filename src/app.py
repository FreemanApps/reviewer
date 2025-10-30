import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import psycopg

load_dotenv()
database_url = os.getenv("DATABASE_URL")

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def get_movies():
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM reviewer.movie")
            for result in cur:
                print(result)

@app.get("/movie/{id}", response_class=HTMLResponse)
def get_movie(id: int):
    print(id)

@app.get("/crew", response_class=HTMLResponse)
def get_crew_members():
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM reviewer.crew")
            for result in cur:
                print(result)

@app.get("/crew/{id}", response_class=HTMLResponse)
def get_crew_member(id: int):
    print(id)

@app.get("/genre", response_class=HTMLResponse)
def get_genres():
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM reviewer.genre")
            for result in cur:
                print(result)

@app.get("/crew/{id}", response_class=HTMLResponse)
def get_genre(id: int):
    print(id)
