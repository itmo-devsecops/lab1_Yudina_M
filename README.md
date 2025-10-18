# Lab2 — Управление исходным кодом (DevSecOps)

## Описание проекта

Этот проект — Flask-приложение для управления списком студентов.  
В рамках **лабораторной работы №2** была проведена интеграция инструментов DevSecOps для повышения безопасности и управляемости исходного кода.

---

## Цели лабораторной работы

- Освоить практики **управления исходным кодом** в контексте DevSecOps.  
- Научиться выявлять и предотвращать утечки секретов.  
- Очистить историю репозитория от конфиденциальных данных.  
- Настроить **pre-commit hook** для предотвращения коммитов с секретами.  
- Сгенерировать **SBOM** для анализа зависимостей.  
- Настроить **Dependabot** для автоматического обновления зависимостей.

---

## Структура проекта

```
lab1_Yudina_M/
│
├── app.py                    # Основной Flask-файл приложения
├── database.py               # Подключение и настройка базы данных
├── models.py                 # Определение моделей SQLAlchemy
├── templates/                # HTML-шаблоны
│   ├── index.html
│   └── add_student.html
│
├── .gitleaks.toml            # Конфигурация Gitleaks
├── .gitleaksignore           # Исключения для Gitleaks
├── .pre-commit-config.yaml   # Настройка pre-commit hook
├── requirements.txt          # Зависимости проекта
├── sbom.json                 # Сгенерированный SBOM (CycloneDX)
├── .github/
│   └── dependabot.yml        # Конфигурация Dependabot
└── README.md
```

---

## Работа с секретами

### 1️ Добавление тестовых секретов

Был добавлен учебный секрет в файл `.env`:
```
DEMO_SECRET=demo_123e4567-e89b-12d3-a456-426614174000
```

### 2️ Настройка Gitleaks

Создан конфигурационный файл `.gitleaks.toml` с кастомным правилом:
```toml
title = "Lab gitleaks config"

[[rules]]
id = "demo-secret"
description = "Demo secret detection rule"
regex = '''(?i)DEMO_SECRET\s*=\s*demo_[0-9a-f-]{36}'''
keywords = ["DEMO_SECRET"]

[allowlist]
paths = ["README.md"]
```

### 3️ Проверка секретов

Запуск проверки:
```bash
gitleaks detect --source . --no-git --report-format json --report-path gitleaks-before.json
```

В отчёте найден DEMO_SECRET.  

---

## Очистка истории Git

Для удаления секретов из истории:
```bash
git filter-repo --path bad_secret.txt --invert-paths --force
```

Повторная проверка:
```bash
gitleaks detect --source . --log-opts="--all"
```

Результат: “no leaks found”.

---

## Настройка pre-commit hook

Добавлен файл `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/zricethezav/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks
        name: gitleaks (detect secrets)
        entry: gitleaks detect --source . --no-git --config .gitleaks.toml
        language: system
        pass_filenames: false
```

Установка и проверка:
```bash
pre-commit install
pre-commit run --all-files
```

При попытке закоммитить секрет — коммит блокируется.

---

## Генерация SBOM

Установлен инструмент **CycloneDX** и выполнена команда:
```bash
python -m cyclonedx_py requirements -o sbom.json
```

Сгенерирован файл `sbom.json`, содержащий информацию обо всех зависимостях проекта.

---

## Проверка уязвимостей (Grype)

Сканирование зависимостей:
```bash
grype sbom:sbom.json -o json > vulnerabilities.json
```

Найдено 28 уязвимостей:
- 3 критические  
- 7 высоких  
- 14 средних  
- 4 низких

Файл `vulnerabilities.json` содержит полный отчёт об уязвимостях.

---

## Настройка Dependabot

Создан `.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "deps"
    open-pull-requests-limit: 5

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

Dependabot автоматически создаёт Pull Request’ы с обновлениями зависимостей.

---

## Результаты

| Этап | Инструмент | Результат              |
|------|-------------|------------------------|
| Обнаружение секретов | Gitleaks | Найдены учебные секреты |
| Очистка истории | git-filter-repo | История очищена        |
| Pre-commit проверка | pre-commit + gitleaks | Коммиты с секретами блокируются |
| SBOM | CycloneDX | Сгенерирован sbom.json |
| Анализ уязвимостей | Grype | vulnerabilities.json создан |
| Автообновление зависимостей | Dependabot | Настроен               |

---

## Вывод

В ходе лабораторной работы №2 были реализованы основные DevSecOps-практики:

- предотвращение утечек секретов;
- очистка истории репозитория от чувствительных данных;
- внедрение pre-commit-хуков;
- генерация и анализ SBOM;
- автоматизация обновления зависимостей.

Все инструменты успешно интегрированы и протестированы.  
Проект соответствует требованиям безопасной разработки (Secure SDLC).
