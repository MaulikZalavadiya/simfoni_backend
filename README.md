## create clone
    git clone https://github.com/MaulikZalavadiya/simfoni_backend.git

## create virtualenv
    python3 -m venv <virtualenv name>

## install requirements
    pip3 install -r requirements.txt

## migrate database
    python manage.py makemigrations && python manage.py migrate

## create superuser
    python manage.py createsuperuser

## run server
    python manage.py runserver
