from pydantic import BaseModel
from fastapi import APIRouter, Request, Response, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated

from ..services import shared

class LoginFormData(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def get_login(request: Request):
    return shared.templates.TemplateResponse(request=request, name="login.jinja")

@router.post("/login", response_class=HTMLResponse)
async def login(response: Response, form_data: Annotated[LoginFormData, Form()]):
    # TODO: verify email and password, and set current_person_id
    print(form_data)

    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="current_person_id", value=form_data.email)
    return response