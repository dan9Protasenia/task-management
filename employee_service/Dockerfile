FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5002

RUN python -c "from app import db; db.create_all()"

EXPOSE 5002

CMD ["flask", "run", "--host", "0.0.0.0"]
