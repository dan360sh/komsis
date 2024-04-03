 # Используем базовый образ Python
# FROM python:3.9

# # Устанавливаем переменную окружения PYTHONUNBUFFERED, чтобы выводить логи в реальном времени
# ENV PYTHONUNBUFFERED 1
# RUN useradd -rms /bin/bash app && chmod 777 /opt /run
# # Устанавливаем рабочую директорию в /app
# WORKDIR /app



# # Копируем файл requirements.txt в рабочую директорию
# COPY requirements.txt /app/
# USER app

# RUN chown -R app:app /app && chmod 755 /app
# # Копируем текущий каталог в рабочую директорию
# COPY --chown=app:app . .

# # Устанавливаем зависимости приложения
# RUN pip install --no-cache-dir -r requirements.txt
# RUN python manage.py collectstatic

# # Определяем команду для запуска приложения
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "system.wsgi:application"]
FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN useradd -rms /bin/bash app && chmod 777 /opt /run

WORKDIR /app

RUN mkdir /app/static && mkdir /app/media && chown -R app:app /app && chmod 755 /app

COPY --chown=app:app . .

RUN pip install -r requirements.txt

USER app

CMD ["gunicorn","-b","0.0.0.0:8000","system.wsgi:application"]
