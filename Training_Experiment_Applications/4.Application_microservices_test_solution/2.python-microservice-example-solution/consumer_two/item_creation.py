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
channel.queue_declare(queue='create_item', durable=True)

# Callback function for item creation
def callback(ch, method, properties, body):
    logging.info('Item creation callback function is called!')
    data = json.loads(body)

    if not connection.is_closed:
        print("Item creation message received: ", data)
        logging.info('Item creation message received: %s', data)
        inventory = Inventory(sku=data['sku'], name=data['name'], 
            label=data['label'], price= data['price'], quantity=data['quantity'])
        db_session.add(inventory)
        db_session.commit()
    else:
        print("Item creation unsuccessful! Connection not found!")
        logging.error('Item creation unsuccessful! Connection not found!')

    return "Item creation is done!"

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='create_item', 
                      on_message_callback=callback, 
                      auto_ack=True)

print ('Starting consuming')
logging.info('Starting consuming')

channel.start_consuming()

channel.close() # close channel on exit