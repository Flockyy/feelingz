# backend/Dockerfile

FROM python:3.9

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8555

CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8555" , "--reload"]