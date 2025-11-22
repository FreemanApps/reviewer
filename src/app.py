from fastapi import FastAPI, Depends, status
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from .routes import auth, genre, movie, person, reaction, review, worker
from .services import shared

# set up app
app = FastAPI()
app.add_middleware(GZipMiddleware)
app.mount("/public", StaticFiles(directory="src/public"), name="public")

# redirect favicon.ico route
@app.get("/favicon.ico", response_class=RedirectResponse, status_code=status.HTTP_301_MOVED_PERMANENTLY)
def get_icon():
    return "/public/favicon.ico"

# add routes
app.include_router(auth.router)
app.include_router(genre.router, dependencies=[Depends(shared.get_current_person)])
app.include_router(movie.router, dependencies=[Depends(shared.get_current_person)])
app.include_router(person.router, dependencies=[Depends(shared.get_current_person)])
app.include_router(reaction.router, dependencies=[Depends(shared.get_current_person)])
app.include_router(review.router, dependencies=[Depends(shared.get_current_person)])
app.include_router(worker.router, dependencies=[Depends(shared.get_current_person)])