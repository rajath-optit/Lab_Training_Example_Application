# Microservice for healthcheck

import pika, json
import time
import logging

time.sleep(10)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the RabbitMQ connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='healthcheck', durable=True)

# Callback function for the healthcheck queue
def callback(ch, method, properties, body):
    logging.info('Healthcheck callback function is called!')
    data = json.loads(body)

    if not connection.is_closed:
        print("Healthcheck message received: ", data)
        logging.info('Healthcheck message received: %s', data)
    else:
        print("Healthcheck unsuccessful! Connection not found!")
        logging.error('Healthcheck unsuccessful! Connection not found!')

    # TOBEREMOVED ch.basic_ack(delivery_tag=method.delivery_tag)
    return "Healthcheck is done!"

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='healthcheck', 
                      on_message_callback=callback, 
                      auto_ack=True)

print ('Starting consuming')
logging.info('Starting consuming')

channel.start_consuming()

channel.close() # close channel on exit