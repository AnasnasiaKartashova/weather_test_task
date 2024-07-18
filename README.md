# Weather Application

## Что выполнено

- Вывод данных (прогноза погоды) в удобно читаемом формате
- Написаны тесты
- Docker контейнеры
- Статистика по количеству просмотров городов

## Запуск

1. Создайте и активируйте виртуальное окружение:

    ```bash
    python3 -m venv venv
    ```

    - Для Linux: `source venv/bin/activate`
    - Для Windows: `venv\Scripts\activate.bat`

2. Создайте файл `.env` с переменными:

    - `SECRET_KEY` — секретный ключ Django
    - `OWM_TOKEN` — токен для использования погодного API [OpenWeatherMap](https://openweathermap.org/)

    Для `SECRET_KEY` вставьте любое значение. Для `OWM_TOKEN` можете использовать этот: `796dac1f61592a0fb08b39b72038dd01` или свой.

3. Запуск приложения:

    ```bash
    docker compose up --build
    ```

    URL для просмотра: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

    ИЛИ

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    python3 manage.py makemigrations
    python3.manage.py migrate
    python3 manage.py runserver
    ```

## О технологиях

Использован API [OpenWeatherMap](https://openweathermap.org/), потому что для него есть библиотека `pyowm`.
