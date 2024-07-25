import pika, json, uuid
from flask import Flask, jsonify, request
import time
import logging

time.sleep(12)

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the RabbitMQ connection without heartbeat, 
# as app is blocked on HTTP messages
connection = pika.BlockingConnection(
    pika.ConnectionParameters(heartbeat=0,
                              blocked_connection_timeout=300, 
                              host='rabbitmq'))
channel = connection.channel()


# API for haelthcheck end-point
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    channel.queue_declare(queue='healthcheck', durable=True)
    
    print("Sending Health chHealth check eck message")
    logging.info('Sending Health check message')

    channel.basic_publish (
        exchange='',
        routing_key='healthcheck',
        body=json.dumps(["message", "Healthcheck"]),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    return jsonify({
        'message': 'Health check message sent'
    })

# API for inventory item creation end-point
@app.route('/create_item', methods=['POST'])
def create_item():
    data = request.get_json()
    channel.queue_declare(queue='create_item', durable=True)

    print("Sending create item message %s", data)
    logging.info('Sending create item message %s', data)

    channel.basic_publish (
        exchange='',
        routing_key='create_item',
        body=json.dumps(data),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    return jsonify({
        'message': 'Create item message sent'
    })

# API for stock management (item delete) end-point
@app.route('/stock_management', methods=['POST'])
def stock_management():
    data = request.get_json() 
    channel.queue_declare(queue='stock_management', durable=True)

    print("Sending stock management (item delete) message %s", data)
    logging.info('Sending stock management (item delete) message %s', data)

    channel.basic_publish (
        exchange='',
        routing_key='stock_management',
        body=json.dumps(data),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    return jsonify({
        'message': 'Stock management (item delete) message sent'
    })

# order processing needs to handle response from the consumer, hence defining
# extra variables and callback function to handle response from consumer

response = None
corr_id = None

def on_response(ch, method, props, body):
        global response
        logging.info('on_response callback function called with msg body: %s', body)
        logging.info('Stored corr_id : %s, received corr_id %s', corr_id, props.correlation_id)
        if corr_id == props.correlation_id:
            response = body

# set up queue to receive the response, to be done outside the API function

result = channel.queue_declare(queue='amq.rabbitmq.reply-to', exclusive=True) # anonymous queue for receiving response
callback_queue = result.method.queue
channel.basic_consume(
            queue=callback_queue,
            on_message_callback=on_response,
            auto_ack=True)

# API for order processing (get inventory item list) end-point
@app.route('/order_processing', methods=['GET'])
def order_processing():    
    print("Sending order processing (get inventory item list) message")
    logging.info('Sending order processing (get inventory item list) message')

    global response
    global corr_id
    global callback_queue
    response = None
    corr_id = str(uuid.uuid4())

    channel.basic_publish(
            exchange='',
            routing_key='order_processing',
            properties=pika.BasicProperties(
                reply_to=callback_queue,
                correlation_id=corr_id,
            ),
            body=json.dumps(["message", "Order Processing"]))
    
    # connection.process_data_events(time_limit=None)
    while response is None:
        logging.info('Calling procss_data_events')
        connection.process_data_events(time_limit=10)

    logging.info('Received response %s', response)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    print("App getting terminated. Closing connection!")
    logging.info('App getting terminated. Closing connection!')
    connection.close()
