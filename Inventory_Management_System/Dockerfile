# Use official Python image as base
FROM python:3.11

# Set working directory in the container
WORKDIR /app

# Copy project files
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn  # Install Gunicorn

# Collect static files (for production)
RUN mkdir -p /app/staticfiles && python manage.py collectstatic --noinput

# Expose the port Django runs on
EXPOSE 8000

# Run migrations and start Gunicorn server
CMD ["sh", "-c", "python manage.py migrate && gunicorn Inventory_Management_System.wsgi:application --bind 0.0.0.0:8000"]
