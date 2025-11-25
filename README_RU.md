# ActiveMQ Artemis Mock Server

Mock-сервер для разработки и тестирования взаимодействия с очередями ActiveMQ Artemis.

## Быстрый старт

```bash
make start
```

## Доступ

- **Web Console**: http://localhost:8161
  - Логин: `admin`
  - Пароль: `admin`

## Очереди

- `request.queue` - входящие запросы
- `response.queue` - исходящие ответы

## Команды

- `make start` - Запустить сервер
- `make stop` - Остановить сервер
- `make restart` - Перезапустить
- `make logs` - Показать логи
- `make clean` - Удалить всё

## Шаблоны

Добавляйте XML файлы в:
- `templates/requests/` - запросы
- `templates/responses/` - соответствующие ответы (с тем же именем)

Слушатель автоматически подхватит новые шаблоны после перезапуска.


d@linux:/var/www/artemis-mock-server$ make view-responses
docker exec artemis-mock /opt/activemq-artemis/bin/artemis queue stat --queueName response.queue --user admin --password admin
Connection brokerURL = tcp://localhost:61616
|NAME                 |ADDRESS              |CONSUMER|MESSAGE|MESSAGES|DELIVERING|MESSAGES|SCHEDULED|ROUTING|INTERNAL|
|                     |                     | COUNT  | COUNT | ADDED  |  COUNT   | ACKED  |  COUNT  | TYPE  |        |
|/queue/response.queue|/queue/response.queue|   0    |   6   |   12   |    0     |   0    |    0    |ANYCAST| false  |
d@linux:/var/www/artemis-mock-server$ 
