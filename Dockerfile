FROM python:3.9-slim

# рабочая директория в контейнере
WORKDIR /app

# зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# копирование приложения в рабочую директорию
COPY . .

# запуск приложения при запуске контейнера
CMD ["python", "app.py"]