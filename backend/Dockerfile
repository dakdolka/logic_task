FROM python:3.12.9-slim

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install cryptography

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
