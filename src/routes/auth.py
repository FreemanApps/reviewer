from pydantic import BaseModel
from pwdlib import PasswordHash
from fastapi import APIRouter, Request, Response, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row
from datetime import datetime, timedelta, timezone
import jwt

from ..services import shared

class LoginFormData(BaseModel):
    email_address: str
    password: str

password_hash = PasswordHash.recommended()

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def get_login(request: Request):
    return shared.templates.TemplateResponse(request=request, name="login.jinja")

@router.post("/login")
async def login(request: Request, response: Response, form_data: Annotated[LoginFormData, Form()]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT person_id, hashed_password
                            FROM reviewer.person
                            WHERE email_address = %s
                        ''', (form_data.email_address,))
            current_person_details = cur.fetchone()

    if password_hash.verify(form_data.password, current_person_details["hashed_password"]):
        payload = {
            "sub": str(current_person_details["person_id"]),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=shared.jwt_access_token_expire_minutes)
        }
        token = jwt.encode(payload, shared.jwt_secret_key, algorithm=shared.jwt_algorithm)

        url = request.url_for("get_movies")
        response = RedirectResponse(url, status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="token", value=token)
        return response

@router.get("/logout")
async def logout(request: Request, response: Response):
    url = request.url_for("get_movies")
    response = RedirectResponse(url, status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="token")
    return response