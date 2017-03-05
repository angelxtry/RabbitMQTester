
import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print('[*] Waiting for message. To exit press CTRL+C')

"""
수행하는데 몇 초가 걸릴 정도의 긴 작업이 있다고 가정하자.
RabbitMQ가 consumer에게 메시지를 전달하고 바로 메모리에서 지워버린다면
consumer가 이 작업을 수행하다가 죽어버렸을 때 이 메시지는 손실된다.
하지만 우리는 어떤 메시지도 손실되는 것을 원하지 않는다.
consumer가 죽어버리면 다른 consumer에게 메시지를 다시 전달하기를 원한다.
이를 위해 RabbitMQ는 Message Acknowledgement를 지원한다.
consumer가 ack을 발송하여 RabbitMQ에게 특정 메시지가 수신되고 처리되었음을 알린다.
RabbitMQ가 ack을 받지 못하면 메시지가 완전하게 처리되지 않았다고 판단하고
메시지를 다시 다른 consumer에게 재전송한다.

Message Acknowlegement는 명시하지 않아도 기본적으로 설정된다.
이것을 설정하지 않으려면 no_ack=True로 설정해야한다.

basic_ack을 놓치는 것은 흔한 실수다.
하지만 누적된다면 RabbitMQ는 사용하지 않은 메시지를 릴리즈 할 수 없으므로
점점 더 많은 메모리가 사용된다.
이런 실수를 확인하기 위해서 rabbitmqctl을 사용하여 message_unacknowledged를 확인한다.
$ rabbitmqctl list_queues name message_ready message_unacknowledged
"""
def callback(ch, method, properties, body):
    print("[x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print('[x] Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)

"""
basic_qos(prefetch_count=1) 이라고 설정하면 RabbitMQ는 worker가 메시지를 하나의 메시지를
다 처리하였음을 확인하기 전까지는 새 메시지를 보내지 않는다.
대신 다른 worker에게 메시지를 보낸다.
"""
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')

channel.start_consuming()
