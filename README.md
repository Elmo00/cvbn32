# ufjt87
### Введение
!ВАЖНО! для работы с bootstrap и datetables я выкачал все пакеты, можно пользоваться CDN и не качать его!

						Debian +  Django + PostgreSQL + Gunicorn + Nginx
Запустить в VirtualBox(WMware) Linux (Debian 11+), можно скачать сразу готовый образ тут — [https://www.osboxes.org/ubuntu/](https://www.osboxes.org/ubuntu/)

### Установка пакетов из репозиториев Debian 11+

Сначала нужно обновить локальный `apt` :

```
sudo apt update
sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx git ufw curl
```

Установим инструмент для создания виртуальной среды Python, файлы разработки Python, необходимые для последующей сборки Gunicorn, систему базы данных Postgres и библиотеки, необходимые для взаимодействия с ней, веб-сервер Nginx, а также git для того чтобы забрать проект себе на виртуалку и ufw для открытия портов. 

### Создание базы данных PostgreSQL и пользователя

Теперь создадим базу данных и пользователя.
Во время установки Postgres был создан PostgreSQL админ `postgres`
Войдем в интерактивный сеанс Postgres, набрав:

```
sudo -u postgres psql
```

Создадим базу данных для проекта:

```
CREATE DATABASE *myproject;
```
*Меняем  

Далее создадим пользователя базы данных для проекта:

```
CREATE USER *myprojectuser WITH PASSWORD *'password';
```
*Меняем  

Установим кодировку символов по умолчанию на `UTF-8`, которую ожидает Django и часовой пояс. 
```
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
```

Теперь можем предоставить новому пользователю доступ для администрирования  базы данных:

```
GRANT ALL PRIVILEGES ON DATABASE *myproject TO *myprojectuser;
```
*Меняем 

выходим из командной строки PostgreSQL, набрав:

```
\q
```

Теперь Postgresql настроен так, что Django может подключаться к ней и управлять.

### Создание виртуальной среды Python

Создим и перейдем в каталог, в котором будет проект:

```
mkdir ~/*myprojectdir
cd ~/*myprojectdir
```
*Меняем 

Создаем виртуальную среду в каталоге проекта:
```
python3 -m venv *env
```
*Меняем 

Активируем виртуальную среду:
```
source *myprojectenv/bin/activate
```
*Меняем 
 должно появится (*myprojectenv)`
 
При активной виртуальной среде установите Django, Gunicorn и psycopg2 адаптер PostgreSQL :
```
pip install django gunicorn psycopg2-binary
```

Вроде все, забираем проект Django.

### Скачиваем и настраиваем проект Django

Скачиваем проект Django с гитхаба.

```
git clone ."ссылка на этот репозиторий"
```

### Настройка параметров проекта

Все будет уже изменено в репозитории, и скорее всего можно пропустить, но на всякий пожарный можно пробежать глазами, я делал после бурного выходного мог что-то пропустить))
Первое, что вы должны сделать с вашими вновь созданными файлами проекта, это настроить параметры. Откройте файл настроек в текстовом редакторе:

```
nano ~/myprojectdir/myproject/settings.py
```

Ищем  `ALLOWED_HOSTS` . Это список адресов серверов или доменных имен, которые могут использоваться для подключения к экземпляру Django.  
Обязательно добавить в конец `localhost` в качестве одного из параметров, поскольку мы будем проксировать соединения через локальный экземпляр Nginx.

```
Для примера:
# ALLOWED_HOSTS = [ 'example.com', '192.168.162.131(ip виртуальной машины)']
ALLOWED_HOSTS = ['your_server_domain_or_IP', 'second_domain_or_IP', . . ., 'localhost or 127.0.0.1']
```

Далее  раздел `DATABASES`.

```
. . .

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '*myproject',
        'USER': '*myprojectuser',
        'PASSWORD': '*password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

. . .
```

Параметр указывающий на  статические файлы. Это необходимо для того, чтобы Nginx мог обрабатывать запросы на эти элементы. 

```
. . .
STATIC_URL = 'static/'
import os # Это в самый вверх
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

Сохраните и закройте файл, когда закончите, в nano ctrl+x, yes если редактируете вимом я не знаю как из него выйти)

### Завершение первоначальной настройки проекта

Теперь зделаем миграцию в нашу базу данных PostgreSQL:

```
~/myprojectdir/manage.py makemigrations
~/myprojectdir/manage.py migrate
```

Соберем все статику в одну папку:

```
~/myprojectdir/manage.py collectstatic
```

Дальше для тестирования сервера,  разрешаем доступ к порту на котором он будет с помощью брандмауэра UFW.

Создадим исключение для стандартного порта 8000:

```
sudo ufw allow 8000
```

Протестируем проект, запустив сервер разработки Django:

```
~/myprojectdir/manage.py runserver 0.0.0.0:8000
```

В веб-браузере localhost:8000 или IP-адрес вашей виртуалки с основного компа:

Должна быть стандартная страница проекта, нажмите **CTRL-C** в окне терминала, чтобы выключить сервер разработки.

### Проверка работы Gunicorn

Последнее, что  нужно сделать, прежде чем покинуть виртуальную среду, это протестировать Gunicorn, чтобы убедиться, что он может работать с приложением. Можно сделать это, войдя в каталог проекта и используя `gunicorn` для загрузки модуля WSGI проекта:

```
cd ~/myprojectdir
gunicorn --bind 0.0.0.0:8000 myproject.wsgi
```

Это запустит Gunicorn на том же интерфейсе, на котором работал сервер разработки Django. можно опять глянуть в браузер там должна быть заставка Django.

Мы передали Gunicorn модуль, указав относительный путь к  `wsgi.py` файлу Django, который является точкой входа в ваше приложение. Внутри этого файла определена вызываемая функция `application`, которая используется для связи с приложением.

Выйдем из виртуальной среды, набрав:

```
deactivate
```

### Создание системных сокетов и служебных файлов для Gunicorn

Проверили, что Gunicorn может взаимодействовать с нашим приложением Django, но лучше реализовать более надежный способ запуска и остановки сервера приложений. Для этого создадим службу systemd и файлы сокетов.

Сокет Gunicorn будет создан при загрузке и будет прослушивать соединения. Когда происходит соединение, systemd автоматически запускает процесс Gunicorn для обработки соединения.

Начнем с создания и открытия файла сокета systemd:

```
sudo nano /etc/systemd/system/gunicorn.socket
```

Конфиг сокета:

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Затем создадим служебный файл systemd для Gunicorn . Имя файла службы должно совпадать с именем файла сокета, за исключением расширения:

```
sudo nano /etc/systemd/system/gunicorn.service
```

Конфиг демона:

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/myprojectdir
ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

`[Unit]` раздел, который используется для указания метаданных и зависимостей. 
`[Service]`раздел пользователя и групп, под которой  запускается процесс. 

Запустим сокет Gunicorn. Это создаст файл сокета  `/run/gunicorn.sock`:

```
sudo systemctl start gunicorn.socket
```

### Проверка файла сокета Gunicorn

Проверим статус процесса, чтобы узнать, удалось ли ему запуститься:

```
sudo systemctl status gunicorn.socket
```

Должно получиться примерно такой вывод:

```
Output● gunicorn.socket - gunicorn socket
     Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled; vendor preset: enabled)
     Active: active (listening) since Mon 2023-03-05 17:53:25 UTC; 5s ago
   Triggers: ● gunicorn.service
     Listen: /run/gunicorn.sock (Stream)
     CGroup: /system.slice/gunicorn.socket

Mart 05 17:53:25 django systemd[1]: Listening on gunicorn socket.
```

Проверим наличие файла `gunicorn.sock` в `/run` каталоге:

```
file /run/gunicorn.sock
Output/run/gunicorn.sock: socket
```

Если нету аутпута или вылезла ошибка. Смотрим журнал сокета Gunicorn, набрав:

```
sudo journalctl -u gunicorn.socket
```

### Тестирование активации сокета

Т.к сокет еще не получил никаких подключений `gunicorn.service` еще не будет активен. Проверим:
```
sudo systemctl status gunicorn

Output○ gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
     Active: inactive (dead)
TriggeredBy: ● gunicorn.socket
```

Нужно проверить механизм активации сокета,  отправим соединение с сокетом, набрав:
```
curl --unix-socket /run/gunicorn.sock localhost
```

 Gunicorn должен быть запущен и может обслуживать приложение Django. Можем убедиться, что служба Gunicorn запущена, набрав:

```
sudo systemctl status gunicorn
```

Если выходные данные `curl` или выходные данные `systemctl status` указывают на то, что возникла проблема, смотрим в журнал:

```
sudo journalctl -u gunicorn
```

Если вносим изменения в `/etc/systemd/system/gunicorn.service` файл, нужно перезагрузить демон и перезапустить процесс Gunicorn, набрав:

```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

### Nginx для Gunicorn

Теперь, когда Gunicorn настроен, вам нужно настроить Nginx.
Начнем с создания и открытия нового блока сервера в каталоге Nginx:

```
sudo nano /etc/nginx/sites-available/myproject
```

Внутри откроем новый серверный блок который  должен прослушивать обычный порт 80 и что он должен отвечать на доменное имя или IP-адрес вашего сервера:

```
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/sammy/myprojectdir;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Далее указываем Nginx игнорировать любые проблемы с поиском /favicon.ico. Также говорим ему, где найти статику.
`location / {}` блок, соответствующий всем другим запросам. Внутри этого места включаем стандартный `proxy_params` файл, включенный в установку Nginx, а затем передаем трафик непосредственно в сокет Gunicorn:

Теперь обзательно нужно его связать с `sites-enabled` каталогом:

```
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

Проверяем конфигурацию Nginx на наличие синтаксических ошибок:

```
sudo nginx -t
```

Если ошибок нету, перезапускаем Nginx:

```
sudo systemctl restart nginx
```

Нужно открыть брандмауэр для обычного трафика через порт 80. Поскольку нам вроде больше не нужен доступ к серверу разработки, также удалим правило для открытия порта 8000:

```
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```

Теперь сможем перейти к домену или IP-адресу нашего сервера, чтобы просмотреть приложение)
