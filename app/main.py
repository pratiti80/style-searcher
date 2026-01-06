from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import io 
import torch
import clip
from contextlib import asynccontextmanager

# app = FastAPI(
#     title="Product Searcher API",
#     description="Backend for identifying products from images",
#     version="0.1.0",
# )

model = None
preprocess = None

PRODUCT_TEXTS = [
    "a photo of sneakers",
    "a photo of a laptop",
    "a photo of a backpack",
    "a photo of headphones",
]

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, preprocess
    model, preprocess = clip.load("ViT-B/32")
    model.eval()
    print("model loaded")
    yield
    print("app shutting down")

app = FastAPI(
    title="Product Searcher API",
    description="Backend for identifying products from images",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/")
def root():
    return {"status": "Backend is running"}

@app.post("/search")
async def search_product(image: UploadFile = File(...)):
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image type")
    image_bytes = await image.read()
    try:
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    image_tensor = preprocess(pil_image).unsqueeze(0)
    text_tokens = clip.tokenize(PRODUCT_TEXTS)
    
    with torch.no_grad():
        image_features = model.encode_image(image_tensor)
        text_features = model.encode_text(text_tokens)
        similarity = (image_features @ text_features.T).squeeze(0)
    
    results = [
        {
            "product": PRODUCT_TEXTS[i],
            "score": float(similarity[i])
        }
        for i in range(len(PRODUCT_TEXTS))
    ]
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return {"results": results}
    
        

@app.get("/health")
def health_check():
    return {"status": "ok"}


#@app.post("/upload-image")
#async def upload_image(image: UploadFile = File(...)):
#    if image.content_type not in ALLOWED_CONTENT_TYPES:
#        raise HTTPException(
#            statuscode=400,
#            detail="Invalid file type. Please upload a JPG, PNG, or WEBP image."
#        )
#    
#    image_bytes = await image.read()
#    
#    try:
#        img = Image.open(io.BytesIO(image_bytes))
# #       img.verify()
#    except Exception:
#        raise HTTPException(
#            status_code=400,
#            detail="Uploaded file is not a valid image."
#        )
#    
#    return {
#        "filename": image.filename,
#        "content_type": image.content_type,
#        "status": "Image validated successfully."
#    }

