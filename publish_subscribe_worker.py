"""
publish/subscribe worker

publish/subscribe를 구현하기 위해 fanout exchange를 이용한다.
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'
))
channel = connection.channel()

channel.exchange_declare(exchange='logs', type='fanout')
"""
worker가 RabbitMQ에 접속할 때 마다 빈 queue를 새로 생성한다.
이렇게 만들어진 queue는 RabbitMQ가 임의로 이름을 부여한다.
queue_declare 함수에 queue='QUEUE_NAME' 를 넣지 않으면
임의로 이름이 부여된 빈 queue를 생성할 수 있다.
이렇게 만들어진 queue는 result.method.declare로 사용할 수 있다.
worker가 연결을 해제하면 임시로 생성했던 queue를 삭제하기위해
exclusive=True 플래그를 설정한다.
"""
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

"""
fanout exchange와 queue가 생성되었다면 둘을 연결해야한다. 이것은 바인딩이라고 한다.
"""
channel.queue_bind(exchange='logs', queue=queue_name)

print('[*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print("[x] %r" % body)
    connection.close()

channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()
