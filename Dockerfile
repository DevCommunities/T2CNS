
FROM python:3.8.6-slim-buster
RUN mkdir -p /usr/src/bot

WORKDIR /usr/src/bot

COPY ./bot .

# add env file
COPY ./bot/.env .env

# install requirements
RUN pip install -r requirements.txt
# Run the bot
CMD [ "python3", "main.py" ]