
FROM python:3.11-slim


WORKDIR /app


COPY ./requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


COPY . /app

# ENV groq_api_key=GROQ_API_KEY

CMD ["fastapi", "run", "app.py", "--port", "8000"]