from fastapi import FastAPI, UploadFile, Form, Request
from typing import Annotated
from comparator import AssignmentEvaluator
import sqlite3
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
conn = sqlite3.connect("assignment.db")

# Create table to store file names and marks.
create_assignment_table = """CREATE TABLE IF NOT EXISTS assignment(
name VARCHAR(100) NOT NULL, 
path VARCHAR(300) NOT NULL,
marks VARCHAR(5)
); 
"""
conn.cursor().execute(create_assignment_table)
conn.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# fetch assignments from db
@app.get("/assignments")
def fetch_assignments():
    conn = sqlite3.connect("assignment.db")
    result = conn.cursor().execute("SELECT * FROM assignment;").fetchall()
    conn.close()
    return result

# Update marks of multiple assignments.
@app.post("/assignments/marks")
async def updateMarks(request: Request):
    assignments = await request.form()
    conn = sqlite3.connect("assignment.db")
    for name, marks in assignments.items():
        query = "UPDATE assignment SET marks = ? WHERE name = ?;"
        conn.cursor().execute(query, (marks, name))
        conn.commit()

    assignments = conn.cursor().execute("SELECT * FROM assignment;").fetchall()
    conn.close()
    return templates.TemplateResponse("results.html", {"request": request, "assignments": assignments})

@app.post("/upload")
async def store_files(files: list[UploadFile], request: Request):
    # Create input directory if not exists to store files
    storage_dir = Path().cwd() / 'input'
    storage_dir.mkdir(exist_ok=True)

    # Create a db connection.
    conn =  sqlite3.connect("assignment.db")

    # Store files on local machine and add file names, paths in db
    for file in files:
        name = file.filename
        path = storage_dir / Path(f"{name}")
        content = file.file.read().decode("utf-8")

        # save file at path.
        with open(path, "w") as outputFile:
            outputFile.write(content)

        # store metadata in db.
        query = """
INSERT INTO assignment(name, path) 
VALUES(?, ?);
"""
        conn.cursor().execute(query, (name, str(path)))
        assignments = conn.cursor().execute("SELECT * FROM assignment;").fetchall()

        conn.commit()
    
    conn.close()
    return templates.TemplateResponse("marks-entry.html", {"request": request, "assignments": assignments})