from fastapi import FastAPI, Depends, status, Request, HTTPException
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import http_exception_handler

from .routes import auth, error, genre, movie, person, reaction, reply, review, worker
from .services import shared

# set up app
app = FastAPI()
app.add_middleware(GZipMiddleware)
app.mount("/public", StaticFiles(directory="src/public"), name="public")

# redirect favicon.ico route
@app.get("/favicon.ico", response_class=RedirectResponse, status_code=status.HTTP_301_MOVED_PERMANENTLY)
def get_icon():
    return "/public/favicon.ico"

# add custom exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.headers.get('hx-request'):
        error = HTTPException(
            status_code=status.HTTP_200_OK,
            headers={'HX-Location': '/error/422'}
        )
        return await http_exception_handler(request, error)
    return shared.templates.TemplateResponse(request=request, name="error/422.jinja", status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)

@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    if request.headers.get('hx-request'):
        error = HTTPException(
            status_code=status.HTTP_200_OK,
            headers={'HX-Location': '/error/404'}
        )
        return await http_exception_handler(request, error)
    return shared.templates.TemplateResponse(request=request, name="error/404.jinja", status_code=status.HTTP_404_NOT_FOUND)

@app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
async def internal_server_error_exception_handler(request: Request, exc: HTTPException):
    if request.headers.get('hx-request'):
        error = HTTPException(
            status_code=status.HTTP_200_OK,
            headers={'HX-Location': '/error/500'}
        )
        return await http_exception_handler(request, error)
    return shared.templates.TemplateResponse(request=request, name="error/500.jinja", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# add routes
app.include_router(auth.router)
app.include_router(error.router)
app.include_router(genre.router, dependencies=[Depends(shared.get_current_person)])
app.include_router(movie.router, dependencies=[Depends(shared.get_current_person)])
app.include_router(person.router, dependencies=[Depends(shared.get_current_person)])
app.include_router(reaction.router, dependencies=[Depends(shared.get_current_person)])
app.include_router(reply.router, dependencies=[Depends(shared.get_current_person)])
app.include_router(review.router, dependencies=[Depends(shared.get_current_person)])
app.include_router(worker.router, dependencies=[Depends(shared.get_current_person)])