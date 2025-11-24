FROM python:3.11

WORKDIR /app

# Copy requirements first (faster builds)
COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn

# Copy the rest of the project
COPY . /app/

# Expose port
EXPOSE 8000

# No collectstatic here because DB isn’t ready yet.
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn Inventory_Management_System.wsgi:application --bind 0.0.0.0:8000"]
