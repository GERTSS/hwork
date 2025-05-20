FROM python:3.9

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY . /

EXPOSE 8000

WORKDIR /mysite

CMD ["sh", "-c", \
"python manage.py makemigrations && \
python manage.py migrate && \
python manage.py create_orders && \
python manage.py create_products && \
python manage.py runserver 0.0.0.0:8000"]