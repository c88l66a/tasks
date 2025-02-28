FROM python:3.9.7-slim as builder

COPY . /bot
WORKDIR /bot

RUN pip install --no-cache-dir -r requirements.txt && mkdir /logs

CMD ["bash", "-c", "sleep 10 && python run_bot.py"]


