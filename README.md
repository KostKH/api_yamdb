# Api_YaMDB

API для учебного проекта YaMDB - учебного проекта соц.сети, в котором пользователи могут размещать обзоры на произведения в разных категориях (фильмы, музыка, кино) и жанрах, после чего на основании оценок формируется рейтинг произведений. 

API позволяет: 
- зарегистрировать пользователя;
- управлять списком категорий, жанров, произведений;
- получать, размещать изменять и удалять отзывы, комментарии к ним;

В проекте:
- реализован REST API CRUD для основных моделей проекта; 
- для аутентификации используется токен Simple-JWT;
- настроено разграничение прав доступа к эндпойнтам API для разных групп пользователей;
- реализованы фильтрации, сортировки;
- реализован поиск по жанрам, категориям, именам пользователей;
- настроена пагинация ответов от API.

## Системные требования
- Python 3.7+
- Works on Linux, Windows, macOS

## Технологии:
- Python 3.7
- Django 2.2.6
- Django REST Framework
- Simple-JWT
- SQLite 3

## Как запустить проект:

- Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/KostKH/api_yamdb.git
cd api_yamdb
```

- Создать и активировать виртуальное окружение:
```
python -m venv venv
source venv/scripts/activate
python -m pip install --upgrade pip
```

- Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
- Выполнить миграции и запустить проект:
```
cd api_yamdb
python manage.py migrate
python manage.py runserver
```

## Документация по API
Документация доступна по эндпойнту /redoc/

## Примеры

#### Авторизация пользователей:
```
/api/v1/auth/signup/ - регистрация пользователя (POST)
/api/v1/auth/token/ - ввод полученного токена (POST)
```
#### Работа с категориями, жанрами:
```
/api/v1/categories/ - просмотр (GET), создание (POST) категорий 
/api/v1/categories/{slug}/ - удаление категории (DELETE)
/api/v1/genres/ - просмотр (GET), создание (POST) жанров
/api/v1/genres/{slug}/ - удаление категории (DELETE)
/api/v1/titles/ - просмотр (GET), создание (POST) записи о произведении
/api/v1/titles/{titles_id}/ - управление произведением (GET, PATCH, DELETE)
```
#### Работа с обзорами и комментариями:
```
/api/v1/titles/{title_id}/reviews/ - просмотр (GET), создание (POST) обзоров
/api/v1/titles/{title_id}/reviews/{review_id}/  - управление обзором (GET, PATCH, DELETE)
/api/v1/titles/{title_id}/reviews/{review_id}/comments/ - просмотр (GET), создание (POST) комментариев
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/  - управление комментарием (GET, PATCH, DELETE)
```
#### Работа с базой пользователей:
```
/api/v1/users/ - просмотр (GET), создание (POST) пользователей
/api/v1/users/{username}/ - управление пользователем (GET, PATCH, DELETE)
/api/v1/users/me/ - просмотр или изменение пользователем своих данных  (GET, PATCH)
```