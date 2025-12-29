from fastapi import FastAPI

app = FastAPI(
    title="Visual Product Finder API",
    description="Backend for identifying products from images",
    version="0.1.0",
)

@app.get("/")
def root():
    return {"status": "Backend is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
