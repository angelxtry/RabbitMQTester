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

"""
ack을 이용하면 consumer가 죽더라도 메시지 손실을 막을 수 있다.
하지만 RabbitMQ server에 문제가 생긴다면 여전히 메시지가 손실될 가능성이 있다.
그러므로 queue와 메시지 두 가지 모두를 내구성있게 만들어야 한다.

먼저 queue를 내구성있게 만들기 위해 durable=True로 선언한다.
기존에 이미 선언되었던 queue는 변경할 수 없다.
durable=True는 producer와 consumer에 모두 필요하다.

그리고 delivery_mode=2를 정의하여 메시지를 영구적으로 표시한다.(?)
-> 이거 무슨 의미인지 잘 모르겠다.
"""
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

