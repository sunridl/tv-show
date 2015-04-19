# Сайт телепрограммы

## Исходная постановка задачи
Реализовать сайт телепрограммы, реализующий:
- управление (CRUD) каналами, передачами
- возможность ставить 1 передачу или фильм сразу по нескольким каналам, поиск каналов и программ
- избранные передачи, избранные каналы
- возможность создавать списки каналов.

## Функциональность
- администратор может создавать, изменять и удалять каналы и передачи;
- администратор может наполнять каналы передачами;
- канал обладает именем и содержит список пар <время показа, ссылка на передачу>;
- передача обладает именем и длительностью;
- для каналов и передач существует поиск по подстроке, фильтрующий отображаемую выборку;
- пользователь имеет список любимых каналов и список любимых передач;
- пользователь может добавлять и удалять канал/передачу из избранного;
- существуют списки каналов, общие для всех пользователей и редактируемые администраторами.

## Разворачивание
1. git clone git@github.com:sunridl/tv-show.git
2. Установить Python и связанные утилиты:
  1. sudo apt-get install python-setuptools python-dev build-essential
  2. sudo easy_install pip
  3. sudo pip install virtualenv
3. Перейти в директорию проекта (cd tv-show)
4. Создать виртуальное окружение: virtualenv env
5. Активировать виртуальное окружение: . env/bin/activate
6. Разрешить python-зависимости: pip install requirements.txt
7. Подготовить БД (ТОЛЬКО если файл app.db не существует или устарел!)
  1. Запустить python shell.py
  2. Командой db.create_all() создать БД
  3. Командой db_create_admin() создать пользователя-администратора
8. Запустить сервер: python server.py
9. Перейти в браузере по адресу http://localhost:5000/
10. Администратор -- (Admin, 123456). Обычный пользователь -- (kitten, 123456).
