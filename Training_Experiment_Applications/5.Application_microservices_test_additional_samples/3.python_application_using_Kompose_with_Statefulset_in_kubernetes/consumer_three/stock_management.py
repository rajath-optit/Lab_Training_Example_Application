from flask import Flask
import pika, json
import time
import logging
from database import db_session, init_db
from entity import Inventory

time.sleep(10)

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove() # close db_session while shutting down application

init_db()

# Set up the RabbitMQ connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='stock_management', durable=True)

# Callback function for stock management
def callback(ch, method, properties, body):
    logging.info('Stock Management callback function is called!')
    data = json.loads(body)

    if not connection.is_closed:
        print("Stock Management message received: ", data)
        logging.info('Stock Management message received: %s', data)
        db_session.query(Inventory).filter(Inventory.sku == data['sku']).delete(synchronize_session='evaluate')
        db_session.commit()
    else:
        print("Stock Management unsuccessful! Connection not found!")
        logging.error('Stock Management unsuccessful! Connection not found!')

    return "Stock Management is done!"

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='stock_management', 
                      on_message_callback=callback, 
                      auto_ack=True)

print ('Starting consuming')
logging.info('Starting consuming')

channel.start_consuming()

channel.close() # close channel on exit
