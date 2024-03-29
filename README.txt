### Локальное развертывание
Сперва самое главное -- войти в переменное окружение `.\venv\Scripts\activate` из главной директории проекта.
Затем важно открыть три терминала: первый -- для запуска docker-контейнера, второй -- для запуска бота, третий -- для запуска сервера.
В каждом терминале необходимо находиться в переменном окружении! Для этого войдите в него в каждом терминале.
1) Установить зависимости `pip install -r requirements.txt` (1 терминал)
2) Запустить БД командой `docker run -p 5432:5432 -e POSTGRES_USER=social_bot -e POSTGRES_DB=social_bot -e POSTGRES_PASSWORD=social_bot --name social_bot_pg postgres` (1 терминал)
3) Применить все миграции командой `python manage.py migrate` (2 терминал)
4) Заполнить файл .env
5) Выполнить создание администратора и фондов командой `python manage.py start_project` (выполнить только если БД только создалась, иначе есть вероятность потерять прогресс фондов) (2 терминал)
6) Добавить актуальный токен своего бота полученного от @bot_father в .env файл
7) Для запуска бота использовать `python manage.py social_bot` (2 терминал)
8) Для запуска django-сервера использовать `python manage.py runserver` (3 терминал)
