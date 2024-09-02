import re
from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init
from groq import Groq
from pydantic import BaseModel

from config import Settings

settings = Settings()
app = FastAPI(title="Keyman")
htmx_init(templates=Jinja2Templates(directory=Path(".") / "templates"))

client = Groq(api_key=settings.groq_api_key)

template = """<start_of_turn>user
You are a helpful recruiter Assistant. Extract only job relevant keywords I can use for my CV and return them as a Python list for this job description: {job_description}
Your response should be in the format: ["keyword1", "keyword2", "keyword3", ...]
<end_of_turn>
<start_of_turn>model
"""


class Input(BaseModel):
    job_description: str


@app.get("/", response_class=HTMLResponse)
@htmx("index", "index")
async def root(request: Request):
    return {"message": "Keyman is running!"}


@app.post("/extract", response_class=HTMLResponse)
@htmx("keywords", "keywords")
async def extract(request: Request, job_description: Annotated[str, Form()]):
    # print(job_description)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": template,
            },
            {
                "role": "user",
                "content": f"{template}\nJob description:\n{job_description}",
            },
        ],
        model="gemma2-9b-it",
    )
    # Extract the content from the response
    response_content = chat_completion.choices[0].message.content
    # Extract the content from the response
    response_content = chat_completion.choices[0].message.content

    # Use regex to find the list in the response
    match = re.search(r"\[.*?\]", response_content, re.DOTALL)

    if match:
        # Extract the list string and evaluate it as a Python list
        keywords_list = eval(match.group())

        return {"keywords": keywords_list}
    else:
        # print("No list found in the response. Raw output:")
        return {"raw_output": response_content}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
