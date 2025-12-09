from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..services import shared

router = APIRouter()

@router.get("/error/422", response_class=HTMLResponse)
async def get_error_422(request: Request):
    return shared.templates.TemplateResponse(request=request, name="error/422.jinja")

@router.get("/error/404", response_class=HTMLResponse)
async def get_error_404(request: Request):
    return shared.templates.TemplateResponse(request=request, name="error/404.jinja")

@router.get("/error/500", response_class=HTMLResponse)
async def get_error_500(request: Request):
    return shared.templates.TemplateResponse(request=request, name="error/500.jinja")