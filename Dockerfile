# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаём рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Указываем порт, который будет использовать Flask
EXPOSE 5000

# Команда запуска Flask-приложения
CMD ["python", "app.py", "--host=0.0.0.0"]

