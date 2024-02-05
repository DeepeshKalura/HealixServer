FROM python:3.11.5

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3100

CMD ["./startup.sh"]