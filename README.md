### Описание проекта:

Проект yatube является абсолютно новой сетью, в которой вы можете делиться с миром новостями и событиями, комментировать события других пользователей и, конечно, подписываться и следить за людьми, которые вас интересуют!

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/yandex-praktikum/kittygram2plus.git
```

```
cd kittygram2plus
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Примеры запроса к API

Простой GET-запрос всех постов:

```
http://127.0.0.1:8000/api/v1/posts/
```

Создание комментария к записи:

```
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
Content-Type: application/json

{
    "text": "string",
}

Все детали о запросах см. в документации (http://127.0.0.1:8000/redoc/)