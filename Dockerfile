FROM python:3.11-alpine
RUN apk add curl

WORKDIR /reccy

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY /offlineplayer .

CMD ["python", "-O", "main.py"]