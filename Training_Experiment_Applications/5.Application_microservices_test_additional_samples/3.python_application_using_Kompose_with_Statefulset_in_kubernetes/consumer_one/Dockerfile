FROM python

WORKDIR /app

COPY ./consumer_one .
RUN pip install -r requirements.txt


CMD [ "python", "healthcheck.py" ]
