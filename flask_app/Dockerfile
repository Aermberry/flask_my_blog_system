FROM python:3.11.6-alpine3.18

WORKDIR /app

# Copy the entire application
COPY . .

# Install dependencies
RUN pip install -r requirements.txt --no-cache-dir

# CMD to run the Flask application
# CMD ["python", "app.py", "--host=0.0.0.0"]
# CMD ["uwsgi", "app.ini"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]

# gunicorn -w 4 -b 0.0.0.0:8000 app:app