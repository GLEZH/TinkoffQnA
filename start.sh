#!/bin/sh

# Установить зависимости
pip install -r requirements.txt

# Запуск Gunicorn с FastAPI приложением
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
