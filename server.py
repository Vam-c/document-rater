from fastapi import FastAPI, UploadFile, Form, Request, responses
from typing import Annotated
from comparator import AssignmentEvaluator
import sqlite3
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from utils import rows_to_dict, create_subject

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
conn = sqlite3.connect("assignment.db")

# Create table to store file names and marks.
create_assignment_table = """CREATE TABLE IF NOT EXISTS assignment(
subject VARCHAR(100) NOT NULL,
name VARCHAR(100) NOT NULL, 
path VARCHAR(300) UNIQUE NOT NULL,
marks VARCHAR(5),
FOREIGN KEY (subject) REFERENCES subject(name)
); 
"""
create_subject_table = """CREATE TABLE IF NOT EXISTS subject(
name VARCHAR(100) UNIQUE NOT NULL 
); 
"""
conn.cursor().execute(create_assignment_table)
conn.cursor().execute(create_subject_table)
conn.close()

# Return home page with subject list and upload files form.
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Fetch subjects and populate UI.
    conn = sqlite3.connect("assignment.db")
    result = conn.cursor().execute("SELECT name FROM subject;").fetchall()
    result = rows_to_dict(('name',), result)
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "subjects": result})

# fetch assignments from db
@app.get("/assignments")
def fetch_assignments():
    conn = sqlite3.connect("assignment.db")
    result = conn.cursor().execute("SELECT * FROM assignment;").fetchall()
    conn.close()
    return result

# Update marks of multiple assignments.
@app.post("/assignments/marks")
async def updateMarks(request: Request, subject: Annotated[str | None, Form()] = None):
    assignments = await request.form()
    conn = sqlite3.connect("assignment.db")
    for name, marks in assignments.items():
        # Convert empty strings to NULL values
        if marks == '':
            marks = None

        query = "UPDATE assignment SET marks = ? WHERE name = ? AND subject = ?;"
        conn.cursor().execute(query, (marks, name, subject))
        conn.commit()

    conn.close()
    return responses.RedirectResponse('/results?subject=' + subject, status_code=303)

@app.get("/results")
async def results(request: Request, subject: str | None = None):
    if not subject: return "Pass a subject as query params. (Ex: api/results?subject=OperatingSystem)"

    # Fetch assignments from db.
    conn = sqlite3.connect("assignment.db")
    data = conn.cursor().execute("SELECT name, path, marks FROM assignment WHERE subject = ?;", (subject,)).fetchall()
    # Convert the results into dictionary {path, marks}.
    assignments = rows_to_dict(("name", "path", "marks"), data)

    # Compute marks using model.
    model = AssignmentEvaluator();
    model.fit(assignments)

    for index in range(len(model.assignments)):
        assignments[index]["predicted_marks"] = round(model.compute_marks(index), 2)
    print(assignments)
    return templates.TemplateResponse("results.html", {"request": request, "assignments": assignments, "subject": subject})

# upload creates a new subject if new_subject is present 
# and uploads the files provided, if any into new_subject or subject.
@app.post("/upload")
async def store_files(
    request: Request, files: list[UploadFile | None] = None, 
    subject: Annotated[str | None, Form()] = None, 
    new_subject: Annotated[str | None, Form()] = None
):
    # we give more priority to new_subject, if it exists.
    # Create an entry for the new_subject and override the subject to new_subject.
    print(subject)
    if new_subject:
        create_subject(new_subject)
        subject = new_subject
    print(subject)

    # Create input directory if not exists to store files
    storage_dir = Path().cwd() / 'input' / subject
    storage_dir.mkdir(exist_ok=True)

    # Create a db connection.
    conn =  sqlite3.connect("assignment.db")
    print(len(files))
    # Store files on local machine and add file names, paths in db
    for file in files:
        # Strangely, empty files list has length = 1, 
        # the filename property is empty, so this is a walk around.
        if not file.filename: continue

        name = file.filename
        path = storage_dir / Path(f"{name}")
        content = file.file.read().decode("utf-8")

        # save file at path.
        with open(path, "w") as outputFile:
            outputFile.write(content)

        # store metadata in db.
        query = """
INSERT INTO assignment(name, path, subject) 
VALUES(?, ?, ?);
"""
        conn.cursor().execute(query, (name, str(path), subject))

        conn.commit()
    
    # Fetch all assignments belonging to the subject.
    assignments = conn.cursor().execute("SELECT name, path, marks FROM assignment WHERE subject = ?;", (subject,)).fetchall()
    assignments = rows_to_dict(('name', 'path', 'marks'), assignments)
    conn.close()

    return templates.TemplateResponse("marks-entry.html", {"request": request, "assignments": assignments, "subject": subject})
