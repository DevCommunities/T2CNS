
FROM python:3.8.6-slim-buster
RUN mkdir -p /usr/src/bot

WORKDIR /usr/src/bot

COPY ./bot .

# install requirements
RUN pip install -r requirements.txt
# rm venv folder
RUN rm -rf venv
# Run the bot
CMD [ "python3", "main.py" ]