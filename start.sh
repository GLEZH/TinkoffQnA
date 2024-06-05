#!/bin/sh

# Установить зависимости
pip install -r requirements.txt

# Запуск Gunicorn с FastAPI приложением
if [ `which gunicorn` ]
then
  exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
else
  echo "gunicorn not found"
fi