from fastapi import FastAPI, UploadFile, Response
from comparator import Comparator

app = FastAPI()

@app.get("/")
def start():
    return {"Hello": "World"}

@app.post("/pdfs")
async def store_files(files: list[UploadFile], response: Response):
    for file in files:
        content = file.file.read().decode("utf-8")
        with open("./input/" + file.filename, "w") as outputFile:
            outputFile.write(content)

    marks = Comparator().compute_marks_of_document(1)
    return marks