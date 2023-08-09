### Установка
- В корневой директории(где docker-compose) создайте файл .env и перенесите туда все из .env.example
- Создайте виртуальное окружение: python -m venv venv
- Активируйте виртуальное окружение
- Установите зависимости: pip install -r requirements.dev.txt
- В postres_to_es/conf.py есть переменная SLEEP_TIME, ее стоит уменьшить до 1, чтобы данные быстрее загрузились
- Далее заходите в директорию с docker-compose файлом
- Далее нужно собрать сервисы: docker-compose -f docker-compose.dev.yml build
- Запускаем собранные сервисы: docker-compose -f docker-compose.dev.yml up
