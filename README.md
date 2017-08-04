# TorList demo
## Требования
* Python 3
* Redis
* Celery
## Установка
### Установка и запуск redis
```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
src/redis-server &
```
### Установка библиотек Python
```
sudo pip3 install -r requirements.txt
```
#### requirements.txt
```
Flask==0.12.2
Flask-Redis==0.3.0
celery==4.1.0
redis==2.10.5
```
## Запуск `Celery`-шедулера
```
celery -A torlist_scheduler.celery worker -B &
```
Шедулер выполняет `http` запрос на адрес `https://dan.me.uk/torlist/`, полученные данные помещаются в `redis`, в хранилище `1`, перед занесением данных в хранилище производится очистка хранилища с номером `1`. `Celery` так же использует `redis` в качестве брокера, свои данные он хранит и обрабатывает в хранилище с номером `0`. Периодичность обновления — 1 час.
## Запуск api-сервера
```
python3 torlist_server.py &
```
## API-методы
### Метод `/`
```
http://localhost:5000/
```
Ф-я возвращает имя сервера и перечень api-методов в формате `JSON`.
### Метод `get_last_update`
```
http://localhost:5000/get_last_update/
```
Ф-я возвращает информацию о том, когда в последний раз был обновлен перечень узлов `tor`.
* В случае успеха:
```JSON
{"result": result}
```
`result` — логическое значение [true/false]
* В случае недоступности данных:
```JSON
{"result": {"error": "Server is not ready yet"}}
```
### Метод `is_contains_ip/<ip_address>`
```
http://localhost:5000/is_contains_ip/127.0.0.1
```
Функция проверяет наличие записи в базе (списке нодов), с ключом, соответствующему ip-адресу узла.
* Возвращаемое значение:
```JSON
{"result": result}
```
`result` — логическое значение [true/false]
## Автотесты
Модули `test_scheduler.py` и `test_server.py` отвечают за тестирование основных ф-й сервера и шедулера.
### Запуск автотестов
```
python3 test_scheduler.py
python3 test_server.py
```