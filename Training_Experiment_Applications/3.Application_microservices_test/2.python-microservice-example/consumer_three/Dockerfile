FROM python

WORKDIR /app

COPY ./consumer_three .
COPY ./repository .
RUN pip install -r requirements.txt


CMD [ "python", "stock_management.py" ]
