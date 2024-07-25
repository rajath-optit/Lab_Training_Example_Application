FROM python

WORKDIR /app

COPY ./consumer_two .
COPY ./repository .
RUN pip install -r requirements.txt

CMD [ "python", "item_creation.py" ]