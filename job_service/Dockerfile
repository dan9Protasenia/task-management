FROM python:3.9

WORKDIR /job

COPY requirements.txt /job/
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=job.py
ENV FLASK_RUN_PORT=5005
ENV FLASK_RUN_HOST=0.0.0.0

RUN flask db upgrade

CMD ["flask", "run"]
