from pydantic import BaseModel
from pwdlib import PasswordHash
from fastapi import FastAPI, Request, Response, Form, Cookie, Depends, HTTPException, status
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
import psycopg
from typing import Annotated

#from dependencies import
from .services import shared
from .routes import genre, movie, person, review, worker

class LoginFormData(BaseModel):
    email: str
    password: str

password_hash = PasswordHash.recommended()

async def get_current_person(person_id: str = Cookie(None)):
    if not person_id:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={'Location': '/login'}
        )
    else:
        return person_id

# set up app
app = FastAPI()
app.add_middleware(GZipMiddleware)
app.mount("/public", StaticFiles(directory="src/public"), name="public")

@app.get("/favicon.ico", response_class=RedirectResponse, status_code=301)
def get_icon():
    return "/public/favicon.ico"

@app.get("/login", response_class=HTMLResponse)
def get_login(request: Request):
    return shared.templates.TemplateResponse(request=request, name="login.jinja")

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, response: Response, form_data: Annotated[LoginFormData, Form()]):
    # TODO: verify user and password
    print(form_data)

    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="person_id", value=form_data.email)
    return response

@app.get("/", response_class=HTMLResponse)
async def get_movies(current_person: Annotated[str, Depends(get_current_person)], request: Request):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT movie_id, movie_name, EXTRACT(year FROM release_date) AS release_year
                            FROM reviewer.movie
                            ORDER BY movie_name, release_date
                        ''')
            movies = cur.fetchall()
    return shared.templates.TemplateResponse(request=request, name="home.jinja", context={"movies": movies})

app.include_router(genre.router)
app.include_router(movie.router)
app.include_router(person.router)
app.include_router(review.router)
app.include_router(worker.router)