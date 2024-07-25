FROM python

WORKDIR /app

COPY ./producer .

RUN pip install -r requirements.txt

CMD [ "python", "producer.py" ]
