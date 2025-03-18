FROM python:3.7-alpine

WORKDIR /app
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -U flask-cors
COPY . . 
CMD ["flask", "run"]

#CMD ["python", "run.py"]