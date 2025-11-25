import os
from dotenv import load_dotenv
import logging
import psycopg
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi import Cookie, HTTPException, status
import jwt

# grab environment variables
load_dotenv()
database_url = os.getenv("DATABASE_URL")
jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_algorithm = os.getenv("JWT_ALGORITHM")
jwt_access_token_expire_minutes = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))

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

# set up security dependency
async def get_current_person(token: Annotated[str, Cookie()] = None):
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[jwt_algorithm])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={'Location': '/login'}
        )

    current_person_id = int(payload["sub"])
    if not current_person_id:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={'Location': '/login'}
        )
    else:
        return current_person_id