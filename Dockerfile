FROM python:3.13.2

WORKDIR /app/server_knowledge_base

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "src/main.py"]