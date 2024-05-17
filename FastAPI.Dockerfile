FROM python:3.9

WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./static ./static
COPY ./app.py .

# CMD ["fastapi", "run", "app.py", "--port", "40001"]
CMD ["python", "app.py"]
