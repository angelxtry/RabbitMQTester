
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'
))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severity = 'new'

channel.queue_bind(exchange='direct_logs',
                   queue=queue_name,
                   routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    connection.close()

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    connection.close()
