FROM python:3.9

WORKDIR /code

COPY ./api /code/api
COPY ./requirements.txt /code/requirements.txt
COPY ./tests /code/tests
COPY ./static /code/static

ENV PYTHONPATH=/code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--workers", "5"]
