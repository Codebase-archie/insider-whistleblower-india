from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "🚀 FastAPI is working!"}

@app.get("/ping")
async def ping():
    return {"status": "ok"}
