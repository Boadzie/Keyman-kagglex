from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init

app = FastAPI(title="Keyman")
htmx_init(templates=Jinja2Templates(directory=Path(".") / "templates"))


@app.get("/", response_class=HTMLResponse)
@htmx("index", "index")
async def root(request: Request):
    return {"message": "Keyman is running!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
