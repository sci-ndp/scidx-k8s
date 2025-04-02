# Packege the the pop api into a Docker image
# Imitating the volumes section of docker-compose.yml to facilitate k8s deployment

FROM python:3.9

# Set working directory
WORKDIR /code

# Copy the application code and required files
COPY ./api /code/api
COPY ./requirements.txt /code/requirements.txt
COPY ./tests /code/tests
COPY ./static /code/static

# Set environment variable for Python path
ENV PYTHONPATH=/code

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Expose the API port
EXPOSE 8000

# Command to start the server
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--workers", "5"]
