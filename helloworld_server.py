"""
helloworld_server.py를 먼저 시작하면 [x] Sent 'Hello World!'를 출력하고 프로그램은 종료된다.
이 때 rabbitmqctl list_queues 명령어를 이용해 상태를 확인해보면
hello queue가 생성되었고 메시지 1개가 있음을 확인할 수 있다.
이 상태에서 helloworld_client.py를 실행하면 [x] Received b'Hello World!' 메시지가
queue로부터 수신되었음을 확인할 수 있다.
다시 rabbitmqctl list_queues 명령어로 확인해보면 hello queue는 존재하지만
queue에 존재하는 메시지는 0이 되었음을 알 수 있다.
"""
import pika

"""
RabbitMQ server에 connection을 연결
localhost에 연결했다.
다른 장비의 Server에 연결하려면 IP 또는 SERVER_NAME을 입력한다.
"""
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

"""
메시지를 보내기 전에 queue가 존재하는지 확인하는 과정이 필요하다.
존재하지 않는 queue에 메시지를 보내면 RabbitMQ는 그 메시지를 버린다.
hello 라는 queue를 만들었다. 이제 메시지를 보낼 준비가 끝났다.
"""
channel.queue_declare(queue='hello')

"""
RabbitMQ는 메시지를 queue에 직접 보내지 않고 exchange를 통해서 보낸다.
일단 exchange에 대해서는 신경쓰지 않는다.
이 예제에서는 빈 문자열로 설정한 default exchange를 사용한다.
exchange는 메시지가 어떤 queue로 가야하는지를 정확하게 구분해준다.
queue의 이름은 routing_key 파라미터에 설정한다.
"""
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print("[x] Sent 'Hello World!'")

connection.close()
