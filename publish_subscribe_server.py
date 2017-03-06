"""
Publish/Subscribe
work queue는 각 작업이 정확히 하나의 worker에게 전달되기위해 사용한다.
여러 worker에게 동일한 메시지를 전달하기 위해서는 publish/subscribe 패턴을 사용한다.

사실 RabbitMQ에서 producer는 queue에 직접적으로 메시지를 보내지 않는다.
producer는 메시지가 어느 queue에 전달되는지 모른다.
대신 producer는 메시지를 exchange에 전달한다.
exchange는 메시지를 어떻게 처리해야 하는지 정확히 알아야한다.
메시지를 특정 queue에 보낼지, 여러 queue에 보낼지 아니면 폐기할지를 알고 있어야 한다.
이러한 규칙은 exchange type으로 정의한다.
exchange type은 direct, topic, header, fanout이 있다.
이번 예제에서는 fanout에 집중한다.

fanout은 수신한 모든 메시지를 모든 queue에 브로드캐스팅 하는 것을 의미한다.
RabbitMQ Server의 exchange를 확인하기 위해 rabbitmqctl list_exchanges 명령어를 사용한다.

이전 튜토리얼에서는 exchange에 대해 몰랐지만 queue에 메시지를 보낼 수 있었다.
지금까지는 빈 문자열로 정의한 default exchange를 사용한 것이다.
exchange 파라미터는 exchange의 이름이다.
default exchange를 사용하면 routing_key에 지정된 queue에 메시지를 보낸다.

이번 예제에서는 모든 message를 브로드캐스팅하고, 오래된 메시지가 아닌 현재 흘러가는 메시지를 수신할 것이다.
이것을 수행하기 위해 두 가지가 필요하다.

첫째, worker가 RabbitMQ에 접속할 때마다 새로만들어진 빈 queue가 필요하다.
이것을 위해 서버가 임의로 이름을 만든 queue를 생성한다.
queue_declare 함수에 파라미터를 넣지 않으면 이와 같은 queue를 만들 수 있다.
이렇게 만들어진 queue의 이름은 result.method.queue로 사용할 수 있다.

둘쨰, worker가 연결을 해제하면 queue를 삭제해야한다.
이것은 exclusive flag를 이용하여 처리한다.

fanout exchange와 queue가 생성되었다면 둘을 연결해야한다. 이것을 binding이라고 한다.
binding 목록은 rabbitmqctl list_bindings로 확인할 수 있다.

fanout exchange와 queue를 생성하고 둘을 binding했다면 메시지를 전달할 준비가 끝났다.
"""