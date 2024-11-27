FROM python:3.12

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# копипаст скрипта в контейнер
COPY entrypoint.sh /entrypoint.sh

# Права выполнения скрипта
RUN chmod +x /entrypoint.sh

# Точка входа контейнера
ENTRYPOINT ["/entrypoint.sh"]