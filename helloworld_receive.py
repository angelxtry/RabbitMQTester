import pika

"""
RabbitMQ server에 접속한다.
이 코드는 helloworld_server.py 에서 사용한 것과 동일하다.
"""
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

"""
queue가 존재하는지 확인한다.
queue_declare를 사용하여 queue를 생성하는 것은 idempotent 하다.
queue_declare를 여러번 사용해도 queue는 하나만 생성된다.
queue가 이미 생성되어있다는 것을 확신할 수 있다면 queue_declare를 생략해도 된다.
하지만 server/client 중 어느 것이 먼저 실행될지는 확신할 수 없다.
그래서 두 프로그램에서 queue를 반복해서 선언하는 것은 좋은 습관이다.
참고로 RabbitMQ에 어떤 queue가 있는지 그리고 queue에 몇 개의 메시지가 존재하는지 보고 싶다면
rabbitmqctl list_queues 명령어를 이용하면 된다.
"""
channel.queue_declare(queue='hello')

"""
메시지를 받기 위해 callback 함수를 사용한다.
메시지를 받을 때마다 pika 라이브러리가 callback 함수를 호출한다.
"""
def callback(ch, method, properties, body):
    print("[x] Received %r" % body)

"""
RabbitMQ server에게 callback 함수가 hello queue의 메시지를 받을거라고 알려준다.
no_ack이 무엇인지는 나중에 설명한다.
"""
channel.basic_consume(callback, queue='hello', no_ack=True)

print('[*] Waiting for message. To exit press CTRL+C')
channel.start_consuming()
