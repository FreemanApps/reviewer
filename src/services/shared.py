import os
from dotenv import load_dotenv
import logging
import psycopg
from fastapi.templating import Jinja2Templates

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