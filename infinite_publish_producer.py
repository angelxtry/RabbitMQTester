import sys
import time
import pika

def send_data():
    channel.exchange_declare(exchange='logs', type='fanout')

    message = ' '.join(sys.argv[1:]) or "info: Hello World"
    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print("[x] Sent %r" % message)

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    channel.close()
    try:
        while 1:
            for i in range(5):
                time.sleep(1)
                print('.')
                send_data()

    except KeyboardInterrupt:
        connection.close()
