# Reviewer

Sources
For each tool, documentation hosted on their websites
For HTML, Mozilla documentation

1. Install postgresql

2. Create reviewer database

3. Run 00-10 sql files against reviewer database or sql_dump.sql
   psql -U postgres -d reviewer -f db/sql_dump.sql

4. Create virtual environment in python
   python -m venv DEV

5. Enter virtual environment
   .\DEV\Scripts\activate.bat

6. Upgrade pip
   python -m pip install --upgrade pip

7. Install python libraries
   pip install "fastapi[standard]" - https://fastapi.tiangolo.com/tutorial/
   pip install "psycopg[binary]" - https://www.psycopg.org/psycopg3/docs/basic/install.html
   pip install pyjwt - https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
   pip install "pwdlib[argon2]" - https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

8. Start server
   fastapi dev src/app.py

9. Navigate to http://127.0.0.1:8000.
