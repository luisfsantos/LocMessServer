# LocMessServer
Server for CMU

```
virtualenv .env
source .env/bin/activate

git clone ...this repo...


cd LocMessServer
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```

Server is run on _8000_ not _8080_

###For tests run:
```
python manage.py test
```
