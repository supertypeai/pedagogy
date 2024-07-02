FROM python:3.12.4-slim-bookworm AS deploy

# RUN apt-get update && apt-get install -y -q build-essential
RUN apt-get update && apt-get install -y -q gcc

WORKDIR /pedagogy

COPY . .

RUN pip install -r requirements.txt

RUN pip install gunicorn==22.0.0

CMD [ "python3", "-m" , "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]