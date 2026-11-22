# Medical REST API (with LangGraph)

REST API для медицинского приложения, которое принимает показатели пациента, 
прогоняет их через пайплайн `LangGraph` для оценки уровня риска и сохраняет 
результат в базу данных `SQLite`.

## Требования
- Python 3.11+
- Установленные зависимости (см. `requirements.txt`)

## Установка и запуск

1. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Для Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload