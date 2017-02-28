"""
다수의 worker에게 시간이 많이 드는 작업을 배포한다.

Work queue의 주요개념은 queue의 메시지를 한번에 다 보내는 것이 아니라
worker에서 메시지의 처리가 완료될 때까지 기다린다는 것이다.
대신 다음에 전달할 메시지를 예약한다.

Work queue를 사용하면 업무를 쉽게 병렬처리 할 수 있다.
"""
import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,
                      ))
print("[x] Sent %r" % message)
connection.close()

