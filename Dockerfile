FROM python:3.11.6-alpine3.18

WORKDIR /app

# Copy the entire application
COPY . .

# Install dependencies
RUN pip install -r requirements.txt --no-cache-dir

# CMD to run the Flask application
# CMD ["python", "app.py", "--host=0.0.0.0"]
