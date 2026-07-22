from fastapi import FastAPI, Depends

app = FastAPI(title="Basic Todo App Server")


@app.get("/")
async def home():
    return {
        "status": True,
        "message": "Check service health on /health and docs on /docs",
    }
