import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Keyman")


@app.get("/")
async def root():
    return {"message": "Keyman is running!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
