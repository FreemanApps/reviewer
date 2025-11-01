import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import psycopg

load_dotenv()
database_url = os.getenv("DATABASE_URL")
app = FastAPI()
templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
async def get_movies(request: Request):
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, EXTRACT(year FROM release_date) AS release_year FROM reviewer.movie")
            movies = cur.fetchall()
    return templates.TemplateResponse(request=request, name="home.jinja", context={"movies": movies})

@app.get("/movie/{id}", response_class=HTMLResponse)
def get_movie(id: int):
    print(id)

@app.get("/crew/{id}", response_class=HTMLResponse)
def get_crew_member(id: int):
    print(id)

@app.get("/genre/{id}", response_class=HTMLResponse)
def get_genre(id: int):
    print(id)
