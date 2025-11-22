import os
from dotenv import load_dotenv
import logging
import psycopg
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi import Cookie, HTTPException, status

# grab environment variables
load_dotenv()
database_url = os.getenv("DATABASE_URL")

# set up database logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger("psycopg").setLevel(logging.INFO)
class LoggingCursor(psycopg.ClientCursor):
    def execute(self, query, params = None, *, prepare = None, binary = None):
        if params:
            sql = self.mogrify(query, params)
        else:
            sql = query
        logging.info(sql)
        super().execute(query, params, prepare=prepare, binary=binary)

# set up templates
templates = Jinja2Templates(directory="src/templates", autoescape=False)

# set up security
async def get_current_person(current_person_id: Annotated[int, Cookie()] = None):
    if not current_person_id:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={'Location': '/login'}
        )
    else:
        return current_person_id