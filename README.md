# Reviewer

## Creating and Running the Project

For this project, I used a PostgreSQL database and a FastAPI server written in Python. The server serves HTML boosted by HTMX and stylized by Pico CSS. Therefore, there is a single server application with no client application.

In addition to PostgreSQL, FastAPI, Python and HTMX, this application uses the psycopg, pyjwt, pwdlib, pydantic, python-dotenv, Jinja2 and built-in libraries and Neon. The .env file is set up for a local reviewer database located at port 5432. However, the .env file provides a database URL for connecting to my Neon database. I primarily used the Neon database for development, but I finished development and tested with a local database.

Below are the instructions for creating and running my project on a Windows machine. However, the instructions should be similar for Linux and MacOS.

1. Install [Python](https://www.python.org/downloads/). I used version 3.12.6.

2. Install [PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads). I used version 17.6.

3. Create reviewer database.

4. Run 00-user.sql through 10-grants.sql files against reviewer database or just run sql_dump.sql. Below is the command to run sql_dump.sql.

```bash
psql -U postgres -d reviewer -f db/sql_dump.sql
```

5. Create virtual environment in python.

```bash
python -m venv DEV
```

6. Enter the new virtual environment.

```bash
.\DEV\Scripts\activate.bat
```

7. Upgrade pip.

```bash
python -m pip install --upgrade pip
```

8. Install fastapi, psycopg, pyjwt and pwdlib libraries. Below are the commands. These commands come from https://fastapi.tiangolo.com/tutorial/, https://www.psycopg.org/psycopg3/docs/basic/install.html, and https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ respectively.

```bash
pip install "fastapi[standard]"
pip install "psycopg[binary]"
pip install pyjwt
pip install "pwdlib[argon2]"
```

9. Start the server. FYI, this starts the server in development mode.

```bash
fastapi dev src/app.py
```

10. Navigate to http://127.0.0.1:8000 to get to the application.

Last thing to note is that you cannot create new users in the database. You can use the .env file to sign in as the different users in the database.
