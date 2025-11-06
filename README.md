# Lab3 — Контейнеризация проекта с помощью Docker (на основе Lab2)

## Описание проекта

Этот проект — Flask-приложение для управления списком студентов.  
В рамках **лабораторной работы №2** была проведена интеграция инструментов DevSecOps для повышения безопасности и управляемости исходного кода.  
Теперь в **лабораторной работы №3** проект дополнен поддержкой **Docker**, что позволило контейнеризировать приложение и упростить его запуск.

---

## Цели лабораторной работы

- Освоить основы контейнеризации приложений с помощью **Docker**
- Добавить возможность развёртывания проекта в изолированном окружении
- Создать и протестировать файлы `Dockerfile` и `docker-compose.yml`
- Обновить документацию, указав новый способ запуска приложения

---

## Нововведения в рамках лабораторной №3

1. **Создан Dockerfile** - описание сборки проекта
2. **Создан docker-compose.yml** - управление запуском контейнера
3. **Изменён файл app.py** - добавлен запуск на всех интерфейсах контейнера
4. **Обновлён README.md** - с инструкцией по Docker-запуску

### Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

### docker-compose.yml
```yaml
services:
  web:
    build: .
    container_name: flask_app
    ports:
      - "5000:5000"
    env_file:
      - .env
    restart: always
```

### Изменения в app.py
```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```
---

## Структура проекта

```
lab1_Yudina_M/
│
├── app.py                    # Flask-приложение (обновлено)
├── database.py               # Подключение и настройка базы данных
├── models.py                 # Модель данных SQLAlchemy
├── templates/                # HTML-шаблоны
│   ├── index.html
│   └── add_student.html
│
├── .env                      # Переменные окружения
├── Dockerfile                # Сборка Docker-образа
├── docker-compose.yml        # Запуск контейнера
│
├── .gitleaks.toml            # Конфигурация Gitleaks
├── .pre-commit-config.yaml   # Настройка pre-commit
├── requirements.txt          # Зависимости Python
├── sbom.json                 # SBOM отчёт
├── .github/
│   └── dependabot.yml        # Настройка Dependabot
└── README_lab3.txt
```

---

## Запуск приложения через Docker

### Собрать и запустить контейнер:
```bash
docker compose up --build
```

### Открыть приложение:
```
http://127.0.0.1:5000
```

### Остановить и удалить контейнеры:
```bash
docker compose down -v
```
