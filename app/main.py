from fastapi import FastAPI, UploadFile, File, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import os
from app.services.ocr import extract_text
from app.services.persistence import save_extracted_titles, get_extracted_titles, clear_extracted_titles
from app.services.wishlist import save_wishlist, get_wishlist
from app.services.matching import is_match

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/pwa")
def pwa_app(request: Request):
    return templates.TemplateResponse(request, "pwa.html")

@app.get("/service-worker.js")
async def service_worker():
    return FileResponse("app/static/service-worker.js", media_type="application/javascript")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")

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
    
    wishlist = get_wishlist()
    results = [{"text": t, "is_match": is_match(t, wishlist)} for t in get_extracted_titles()]
    
    return {
        "filename": file.filename, 
        "titles_found": len(titles),
        "all_titles": results
    }

@app.get("/results")
def get_results():
    wishlist = get_wishlist()
    results = [{"text": t, "is_match": is_match(t, wishlist)} for t in get_extracted_titles()]
    return {"titles": results}

@app.post("/clear")
def clear_results():
    clear_extracted_titles()
    return {"message": "Results cleared"}

@app.get("/wishlist")
def get_wishlist_endpoint():
    """Retrieves the current wishlist."""
    return {"wishlist": get_wishlist()}

@app.post("/wishlist")
def save_wishlist_endpoint(items: list[str] = Body(embed=True)):
    """Updates the wishlist with the provided items."""
    save_wishlist(items)
    return {"message": "Wishlist updated"}
