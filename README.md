# Pipeline из двух звеньев
![Python](https://img.shields.io/badge/Python-3.10-green)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-0.2.0-green)
![Pika](https://img.shields.io/badge/Pika-1.3.1-green)
![docker](https://img.shields.io/badge/Docker-grey)<br>

## Оглавление:
- [Введение](#введение)
- [Инфраструктура](#инфраструктура)
- [Ограничения](#ограничения)
- [Инструкция по запуску](#инструкция-по-запуску)

----
### <anchor>Введение</anchor>
Приложение реализует pipeline из двух звеньев.
_Приложение А_ считывает информацию из файла, сохраняет их в базу данных и отправляет их в приложение B.
_Приложеие B_ принимает сообщение и формирует текущее состоние игры. Сохрянает текущее состояние в файл.
Формат текущего состояния:

<details>

**match_state**: {<br>

'status': 2,<br>
    'match_status': 3,<br>
    'match_time': '92:08'<br>
    }<br>
status (0-prematch, 1-live, 2-ended, 3-failed)
match_status (0-prematch, 1-first half, 2-second half, 3-ended)

**match_score**: {<br>
    “score”: {<br>
    “home_score”:1,<br>
    “away_score”:2<br>
},<br>
“period_scores”:[<br>
    {<br>
        “number”:1,<br>
        “home_score”:0,<br>
        “away_score”:1<br>
    },<br>
    {<br>
        “number”:2,<br>
        “home_score”:1,<br>
        “away_score”:1<br>
    }<br>
    ]<br>
}<br>
score - счет за весь период<br>
period_scores - счет по периодам,<br>
number - порядковый номер периода (1 - 1st half, 2 - 2nd
half)
</details>

Каждое обновление проверяется на валидность:
- Отностяся ли данные к текущему событию (event_id)
- Время и счет должны быть не меньше того, что в текущем состоянии.
В случае ошибки статус матча меняется на failed и игнорируются новые обновления
----
### <anchor>Инфраструктура</anchor>
**Python**
- Версия: _3.10_

**RabbitMQ Server**:
- Версия: _3.11.13-management_
- Версия выбрана для возможности просмотра интерфейса очередей через веб версию RabbitMQ<br>
Просмотр интерфеса очередей доступен после запуска `docker-compose` по адресу `http://localhost:15672/`

**Flake8**
- Для проверки соответствия кода PEP8
----
### <anchor>Ограничения</anchor>

- Для демонстрации функционала в качестве базы данных выбрана SQLite, также ее создание
и нахождение устроено в контейнер _producer_. При ноебходимости долговременного хранения
записанной инфорации, база данных должна быть организована в отдедльный контейнер с _volume_
- В базу данных записываются не все поля пришедшего сообщения. Сделано это для визульного уменьшения
"веса" синтексиса сохрарения в БД.
- Вывод _receiver_ выполнен через _print_ в терминал. При дополнительном требовании о формате выходных данны
можно поменять метод класса MatchLogger

----
### <anchor>Инструкция по запуску</anchor>
1. Клонируем репозиторий:
<br> `git clone git@github.com:Andrey-Kugubaev/BetTest.git`

2. Создаем файл *.env* и добавляем в него параметры:
<br>`DB_NAME = logs_fifa.db`
<br>`DB_TABLENAME = game`
<br>`RB_CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(host=RB_HOST))`
<br>`RB_HOST = rabbitmqServer`
<br>`QUEUE_NAME = fifa_logs_queue`
<br>`QUEUE_OPTS = {'durable':True}`
- файл *.env* необходимо добавить в директории _producer_ и _receiver_

4. Устанавливаем `Docker`

5. Собираем `docker-compose`
<br>`docker-compose up -d --build`

6. Останавливаем и удаляем контейнеры:
<br>`docker-compose down -v`

Автор: [https://github.com/Andrey-Kugubaev](https://github.com/Andrey-Kugubaev)
