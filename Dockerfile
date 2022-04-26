FROM python:3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . .

RUN /usr/local/bin/python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

CMD [ "python3", "run.py"]
