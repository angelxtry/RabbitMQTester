"""
Routing
multiple binding을 이용하여 worker들에게 선별적으로 메시지를 보낸다.

bindind은 exchange와 queue의 관계를 정의한다.
다시 말하자면 queue는 exchange로부터 나오는 message에 관심이 있다.
binding은 routing_key를 파라미터로 사용할 수 있다.
basic_publish의 파라미터와의 혼동을 피하기 위해 binding key 라고 부른다.
binding key는 exchange type에 따라 다르다.
fanout exchange는 binding key를 무시하기 때문에 유연하지않다.
그래서 fanout 대신 direct exchange를 사용한다.

direct exchange에서 메시지는
binding key가 메시지의 routing key와 일치하는 queue로 전달된다.
일치하지 않는 메시지는 무시한다.
동일한 binding key를 사용하여 다수의 queue에 binding 할 수 있다.
이 경우 fanout과 같이 동작한다.
"""
import sys
import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'
))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', type='direct')

severity = 'new'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

try:
    while 1:
        channel.basic_publish(exchange='direct_logs',
                              routing_key=severity,
                              body=message)
        print("[x] Sent %r:%r" % (severity, message))
        time.sleep(5)

except KeyboardInterrupt:
    connection.close()
