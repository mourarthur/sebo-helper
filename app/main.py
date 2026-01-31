from fastapi import FastAPI, UploadFile, File
import os
from app.services.ocr import extract_text
from app.services.persistence import save_extracted_titles, get_extracted_titles, clear_extracted_titles

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Process image with OCR
    raw_text = extract_text(file_path)
    
    # Split raw text into lines (potential titles)
    titles = [line.strip() for line in raw_text.split("\n") if line.strip()]
    
    # Save to persistence
    save_extracted_titles(titles)
    
    return {
        "filename": file.filename, 
        "titles_found": len(titles),
        "all_titles": get_extracted_titles()
    }

@app.get("/results")
def get_results():
    return {"titles": get_extracted_titles()}

@app.post("/clear")
def clear_results():
    clear_extracted_titles()
    return {"message": "Results cleared"}
