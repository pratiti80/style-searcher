from fastapi import FastAPI, UploadFile, File

app = FastAPI(
    title="Product Searcher API",
    description="Backend for identifying products from images",
    version="0.1.0",
)

@app.get("/")
def root():
    return {"status": "Backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/greet")
def greet(name: str):
    return {"greeting": f"Hello {name}"}


@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    return {
        "filename": image.filename,
        "content_type": image.content_type 
    }
