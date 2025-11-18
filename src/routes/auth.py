from pydantic import BaseModel
from fastapi import APIRouter, Request, Response, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row

from ..services import shared

class LoginFormData(BaseModel):
    email_address: str
    password: str

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def get_login(request: Request):
    return shared.templates.TemplateResponse(request=request, name="login.jinja")

@router.post("/login", response_class=HTMLResponse)
async def login(response: Response, form_data: Annotated[LoginFormData, Form()]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT person_id, hashed_password
                            FROM reviewer.person
                            WHERE email_address = %s
                        ''', (form_data.email_address,))
            current_person_details = cur.fetchone()

    if form_data.password == current_person_details["hashed_password"]:
        response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="current_person_id", value=current_person_details["person_id"])
        return response