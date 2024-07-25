FROM python

WORKDIR /app
COPY ./consumer_four .
COPY ./repository .
COPY ./consumer_four/requirements.txt .
RUN pip install -r requirements.txt

CMD [ "python", "order_processing.py" ]
