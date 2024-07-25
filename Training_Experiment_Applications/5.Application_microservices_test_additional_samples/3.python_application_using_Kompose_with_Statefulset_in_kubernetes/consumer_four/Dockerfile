FROM python

WORKDIR /app
COPY ./consumer_four .
COPY ./repository .
RUN pip install -r requirements.txt

CMD [ "python", "order_processing.py" ]
