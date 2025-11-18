import os
from dotenv import load_dotenv
import logging
import psycopg
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated
from fastapi import Cookie, HTTPException, status
from psycopg.rows import class_row

# grab environment variables
load_dotenv()
database_url = os.getenv("DATABASE_URL")

# set up database logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
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
templates = Jinja2Templates(directory="src/templates")

# set up security
class Current_Person(BaseModel):
    person_id: int
    person_name: str

async def get_current_person(current_person_id: Annotated[str, Cookie()] = None):
    if not current_person_id:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={'Location': '/login'}
        )
    else:
        with psycopg.connect(database_url, cursor_factory=LoggingCursor) as conn:
            with conn.cursor(row_factory=class_row(Current_Person)) as cur:
                cur.execute('''
                                SELECT person_id, person_name
                                FROM reviewer.person
                                WHERE person_id = %s
                            ''', (current_person_id, ))
                current_person_details = cur.fetchone()
        return current_person_details