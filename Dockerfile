FROM python:3.10.0

RUN pip install --upgrade pip \
    && mkdir /app

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD python /app/anime_bot.py