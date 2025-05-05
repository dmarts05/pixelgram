FROM python:3.13.3-slim-bookworm

EXPOSE 8000

# Prevent Python from generating .pyc files and enable unbuffered logging for easier debugging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory and copy your app’s source code.
WORKDIR /app
COPY . /app

# Install uv and export dependencies to a requirements file
RUN pip install uv --no-cache-dir && uv export > requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn --no-cache-dir

# Create a non-root user and assign permissions to the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && \
    chown -R appuser /app
USER appuser

# Start Gunicorn with uvicorn's worker to run your ASGI application.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "pixelgram.__main__:app"]
