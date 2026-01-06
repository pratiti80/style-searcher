from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import io 

app = FastAPI(
    title="Product Searcher API",
    description="Backend for identifying products from images",
    version="0.1.0",
)

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}

@app.get("/")
def root():
    return {"status": "Backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload-image")
async def upload_image(image: UploadFile = File(...)):
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            statuscode=400,
            detail="Invalid file type. Please upload a JPG, PNG, or WEBP image."
        )
    
    image_bytes = await image.read()
    
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid image."
        )
    
    return {
        "filename": image.filename,
        "content_type": image.content_type,
        "status": "Image validated successfully."
    }
    
