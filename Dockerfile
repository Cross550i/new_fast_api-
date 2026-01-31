FROM python:3.12.10-slim

WORKDIR /app

# Копируем ТОЛЬКО requirements (для кэша)
COPY requirements.txt .

# Устанавливаем зависимости (ОДИН РАЗ!)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Копируем ВСЁ остальное
COPY . .

EXPOSE 8000

# УБИРАЕМ --reload для Docker!
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
