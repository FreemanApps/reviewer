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
                            WHERE UPPER(email_address) = UPPER(%s)
                        ''', (form_data.email_address,))
            current_person_details = cur.fetchone()

    # attempt to verify input password against hashed password
    try:
        verify = password_hash.verify(form_data.password, current_person_details["hashed_password"])
        if not verify:
            raise Exception("Passwords do not match")
        
        payload = {
            "sub": str(current_person_details["person_id"]),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=shared.jwt_access_token_expire_minutes)
        }
        token = jwt.encode(payload, shared.jwt_secret_key, algorithm=shared.jwt_algorithm)

        ## if verified, send to home page with token cookie 
        url = request.url_for("get_movies")
        response = RedirectResponse(url, status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="token", value=token)
        return response
    # otherwise, respond back with error details included
    except:
        error = {}
        error["form"] = 'Login details must be valid'
        return shared.templates.TemplateResponse(request=request, name="login.jinja", context={"form_data": form_data, "error":error})

@router.get("/logout")
async def logout(request: Request, response: Response):
    # send to home page with with no token cookie
    url = request.url_for("get_movies")
    response = RedirectResponse(url, status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="token")
    return response