FROM python

WORKDIR /app

COPY ./consumer_three .
COPY ./consumer_three/requirements.txt .
COPY ./repository .
RUN pip install -r requirements.txt


CMD [ "python", "stock_management.py" ]
