from flask import Flask
import pika, json
import time
import logging
from sqlalchemy import select
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
channel.queue_declare(queue='order_processing', durable=True)

# function to convert DB query results to dictionary
def convertor(instance, exclude=[], force_array=False):
    if instance is None:
        return instance
    if type(instance) != list:
        instance = [instance]
        
    ret = []
    for i in instance:
        obj = dict()
        for key in i.__dict__:
            if key not in exclude and key != "_sa_instance_state":
                obj[key] = i.__dict__[key]
        ret.append(obj)
        
    if len(ret) == 1 and force_array == False:
        return ret[0]
    return ret

# Callback function for order processing
def callback(ch, method, properties, body):
    logging.info('Order Processing callback function is called!')
    data = json.loads(body)

    if not connection.is_closed:
        print("Order Processing message received: ", data)
        logging.info('Order Processing message received: %s', data)

        db_session.commit() # always fetch fresh data from database
        results = db_session.query(Inventory).all()
        results_dict = convertor(results, [], True)

        logging.info('Query returned: %s', results_dict)

        # send the query results as a response to producer
        ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                     body=json.dumps(results_dict))

    else:
        print("Order Processing unsuccessful! Connection not found!")
        logging.error('Order Processing unsuccessful! Connection not found!')
        return json.dumps(["message", "Order Processing failed!"])

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='order_processing', 
                      on_message_callback=callback, 
                      auto_ack=True)

print ('Starting consuming')
logging.info('Starting consuming')

channel.start_consuming()

channel.close() # close channel on exit
