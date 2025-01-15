FROM apache/airflow:2.6.0
USER root
#USER root  # Переход на пользователя root для установки

# Установка необходимых пакетов для компиляции
RUN apt-get update && \
    apt-get install -y gcc g++ python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Возвращаемся к пользователю airflow
#USER airflow
USER airflow
# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt



